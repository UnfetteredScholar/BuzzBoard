import json
from logging import getLogger
from typing import Dict, List

from core.authentication.auth_middleware import get_current_active_user
from core.authentication.role import allow_resource_admin
from core.storage import storage
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from schemas.categories import Category, CategoryIn, CategoryUpdate
from schemas.user import User
from services.mongo_storage import change_id_key

router = APIRouter()


@router.get(path="/categories", response_model=List[Category])
def get_categories(
    page_number: int = 1,
    page_size: int = 10,
):
    """Gets all available categories"""
    logger = getLogger(__name__ + ".get_categories")
    try:

        skip = (page_number - 1) * page_size

        categories = (
            storage.db["categories"].find().skip(skip).limit(page_size)
        )
        categories = [
            change_id_key(json.loads(json.dumps(category, default=str)))
            for category in categories
        ]

        return categories
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.get(path="/categories/{category_id}", response_model=Category)
def get_category(
    category_id: str,
):
    """Get category by its id"""
    logger = getLogger(__name__ + ".get_category")
    try:

        category = storage.verify_category_record({"_id": category_id})

        return category
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.post(
    path="/categories",
    response_model=Dict[str, str],
    dependencies=[Depends(allow_resource_admin)],
)
def add_category(
    data: CategoryIn, current_user: User = Depends(get_current_active_user)
):
    """Adds a new category"""
    logger = getLogger(__name__ + ".add_category")
    try:
        id = storage.create_category_record(data)

        response_message = {"message": "Added Category successfully", "id": id}

        return JSONResponse(response_message)
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.patch(
    path="/categories/{category_id}",
    response_model=Dict[str, str],
    dependencies=[Depends(allow_resource_admin)],
)
def update_category(
    category_id: str,
    data: CategoryUpdate,
    replace_topics: bool = False,
    current_user: User = Depends(get_current_active_user),
):
    """Updates a category"""
    logger = getLogger(__name__ + ".update_category")
    try:
        category = storage.verify_category_record({"_id": category_id})
        update = {}
        for k, v in data.model_dump().items():
            if v is not None:
                update[k] = v

        if "topics" in update and replace_topics is False:
            update["topics"] = list(set(update["topics"] + category.topics))

        storage.update_category_record(
            filter={"_id": category_id},
            update=update,
        )

        response_message = {"message": "Updated Category successfully"}

        return JSONResponse(response_message)
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.delete(
    path="/categories/{category_id}",
    response_model=Dict[str, str],
    dependencies=[Depends(allow_resource_admin)],
)
def delete_category(
    category_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """Removes a category"""
    logger = getLogger(__name__ + ".delete_category")
    try:
        storage.delete_category_record({"_id": category_id})
        response_message = {"message": "Removed Category successfully"}

        return JSONResponse(response_message)
    except Exception as ex:
        logger.error(ex)
        raise ex
