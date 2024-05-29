import json
from logging import getLogger
from typing import Dict, List, Optional

from core.authentication.auth_middleware import get_current_active_user
from core.storage import storage
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from schemas.comments import Comment, CommentIn
from schemas.user import User
from services.mongo_storage import change_id_key

router = APIRouter()


@router.get(path="/posts/{post_id}/comments", response_model=List[Comment])
def get_comments(
    post_id: str,
    reply_to_id: Optional[str] = None,
    page_number: int = 1,
    page_size: int = 10,
):
    """Gets all comments to a post"""
    logger = getLogger(__name__ + ".get_comments")
    try:
        storage.verify_post_record({"_id": post_id})

        skip = (page_number - 1) * page_size

        comments = (
            storage.db["comments"]
            .find({"post_id": post_id, "reply_to_id": reply_to_id})
            .sort({"date_created": -1})
            .skip(skip)
            .limit(page_size)
        )
        comments = [
            change_id_key(json.loads(json.dumps(comment, default=str)))
            for comment in comments
        ]

        return comments
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.get(
    path="/posts/{post_id}/comments/{comment_id}",
    response_model=Comment,
)
def get_comment(
    post_id: str,
    comment_id: str,
):
    """Get comment by its id"""
    logger = getLogger(__name__ + ".get_comment")
    try:

        comment = storage.verify_comment_record(
            {"_id": comment_id, "post_id": post_id}
        )

        return comment
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.post(
    path="/posts/{post_id}/comments",
    response_model=Dict[str, str],
)
def add_comment(
    post_id: str,
    data: CommentIn,
    current_user: User = Depends(get_current_active_user),
):
    """
    Adds a new comment to a post.
    """
    logger = getLogger(__name__ + ".add_comment")
    try:
        id = storage.create_comment_record(
            data=data, post_id=post_id, user_id=current_user.id
        )

        response_message = {"message": "Added Comment successfully", "id": id}

        return JSONResponse(response_message)
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.delete(
    path="/posts/{post_id}/comments/{comment_id}",
    response_model=Dict[str, str],
)
def delete_comment(
    post_id: str,
    comment_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """Removes a user's comment to a post"""
    logger = getLogger(__name__ + ".delete_comment")
    try:
        storage.delete_comment_record(
            {"_id": comment_id, "post_id": post_id, "user_id": current_user.id}
        )
        response_message = {"message": "Removed Comment successfully"}

        return JSONResponse(response_message)
    except Exception as ex:
        logger.error(ex)
        raise ex
