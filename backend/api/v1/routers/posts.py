import json
from datetime import UTC, datetime
from logging import getLogger
from typing import Dict, List, Optional

from core.authentication.auth_middleware import get_current_active_user
from core.storage import storage
from fastapi import APIRouter, Depends, File, Form, UploadFile
from fastapi.responses import JSONResponse
from schemas.posts import Post, PostIn, PostSortTypes
from schemas.user import User
from services.mongo_storage import change_id_key

router = APIRouter()


@router.get(path="/posts/general_feed", response_model=List[Post])
def get_posts_general_feed(
    category_id: Optional[str] = None,
    category_topic: Optional[str] = None,
    page_number: int = 1,
    page_size: int = 10,
    sort_by: PostSortTypes = PostSortTypes.HOT,
):
    """Gets the general post feed posts"""
    logger = getLogger(__name__ + ".get_posts_general_feed")
    try:

        skip = (page_number - 1) * page_size
        filter = {}

        if category_id is not None:
            filter["category_id"] = category_id
        if category_topic is not None:
            filter["category_topic"] = category_topic

        if sort_by == PostSortTypes.NEW:
            pipeline = [
                {"$match": filter},
                {"$sort": {"date_created": -1}},
                {"$skip": skip},
                {"$limit": page_size},
            ]
        elif sort_by == PostSortTypes.TOP:
            pipeline = [
                {"$match": filter},
                {
                    "$addFields": {
                        "difference": {"$subtract": ["$likes", "$dislikes"]}
                    }
                },
                {"$sort": {"difference": -1}},
                {"$skip": skip},
                {"$limit": page_size},
            ]
        else:
            pipeline = [
                {"$match": filter},
                {
                    "$addFields": {
                        "currentDate": datetime.now(UTC),
                        "score": {
                            "$divide": [
                                {"$subtract": ["$likes", "$dislikes"]},
                                {
                                    "$subtract": [
                                        datetime.now(UTC),
                                        "$date_created",
                                    ]
                                },
                            ]
                        },
                    }
                },
                {"$sort": {"score": -1}},
                {"$skip": skip},
                {"$limit": page_size},
            ]

        posts = storage.db["posts"].aggregate(pipeline)
        # posts = storage.db["posts"].find(filter).skip(skip).limit(page_size)
        posts = [
            change_id_key(json.loads(json.dumps(post, default=str)))
            for post in posts
        ]

        return posts
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.get(path="/posts/user_feed", response_model=List[Post])
def get_posts_user_feed(
    page_number: int = 1,
    page_size: int = 10,
    sort_by: PostSortTypes = PostSortTypes.HOT,
    current_user: User = Depends(get_current_active_user),
):
    """
    Gets all posts matching the user's subscribed categories
    If user has no subscriptions, feed is populated with every category
    """
    logger = getLogger(__name__ + ".get_posts_user_feed")
    try:

        skip = (page_number - 1) * page_size
        filter = {}
        if len(current_user.subscribed) > 0:
            filter = {"category_id": {"$in": current_user.subscribed}}

        if sort_by == PostSortTypes.NEW:
            pipeline = [
                {"$match": filter},
                {"$sort": {"date_created": -1}},
                {"$skip": skip},
                {"$limit": page_size},
            ]
        elif sort_by == PostSortTypes.TOP:
            pipeline = [
                {"$match": filter},
                {
                    "$addFields": {
                        "difference": {"$subtract": ["$likes", "$dislikes"]}
                    }
                },
                {"$sort": {"difference": -1}},
                {"$skip": skip},
                {"$limit": page_size},
            ]
        else:
            pipeline = [
                {"$match": filter},
                {
                    "$addFields": {
                        "currentDate": datetime.now(UTC),
                        "score": {
                            "$divide": [
                                {"$subtract": ["$likes", "$dislikes"]},
                                {
                                    "$subtract": [
                                        datetime.now(UTC),
                                        "$date_created",
                                    ]
                                },
                            ]
                        },
                    }
                },
                {"$sort": {"score": -1}},
                {"$skip": skip},
                {"$limit": page_size},
            ]

        posts = storage.db["posts"].aggregate(pipeline)
        # posts = storage.db["posts"].find(filter).skip(skip).limit(page_size)
        posts = [
            change_id_key(json.loads(json.dumps(post, default=str)))
            for post in posts
        ]

        return posts
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.get(path="/posts", response_model=List[Post])
def get_posts(
    category_id: Optional[str] = None,
    category_topic: Optional[str] = None,
    page_number: int = 1,
    page_size: int = 10,
    current_user: User = Depends(get_current_active_user),
):
    """Gets posts created by the user"""
    logger = getLogger(__name__ + ".get_posts")
    try:

        skip = (page_number - 1) * page_size
        filter = {"user_id": current_user.id}

        if category_id is not None:
            filter["category_id"] = category_id
        if category_topic is not None:
            filter["category_topic"] = category_topic

        posts = (
            storage.db["posts"]
            .find(filter)
            .sort({"date_created": -1})
            .skip(skip)
            .limit(page_size)
        )
        posts = [
            change_id_key(json.loads(json.dumps(post, default=str)))
            for post in posts
        ]

        return posts
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.get(
    path="/posts/{post_id}",
    response_model=Post,
)
def get_post(
    post_id: str,
):
    """Get post by its id"""
    logger = getLogger(__name__ + ".get_post")
    try:

        post = storage.verify_post_record({"_id": post_id})

        return post
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.post(
    path="/posts",
    response_model=Dict[str, str],
)
async def add_post(
    # data: PostIn,
    post_image: UploadFile = File(None),
    category_id: str = Form(...),
    category_topic: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    current_user: User = Depends(get_current_active_user),
):
    """
    Adds a new post to a post to a category
    """
    logger = getLogger(__name__ + ".add_post")
    try:

        has_image = post_image is not None
        data = PostIn(
            category_id=category_id,
            category_topic=category_topic,
            title=title,
            content=content,
        )

        id = storage.create_post_record(data, current_user.id)

        if has_image:
            filename = f"{id}.{post_image.filename.split('.')[-1]}"
            with open(f"./media/{filename}", "wb") as f:
                f.write(await post_image.read())

            storage.update_post_record(
                filter={"_id": id},
                update={"post_image_url": f"/api/v1/media/{filename}"},
            )

        response_message = {"message": "Added Post successfully", "id": id}

        return JSONResponse(response_message)
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.delete(
    path="/posts/{post_id}",
    response_model=Dict[str, str],
)
def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """Removes a user's post"""
    logger = getLogger(__name__ + ".delete_post")
    try:
        storage.delete_post_record(
            {"_id": post_id, "user_id": current_user.id}
        )
        response_message = {"message": "Removed Post successfully"}

        return JSONResponse(response_message)
    except Exception as ex:
        logger.error(ex)
        raise ex
