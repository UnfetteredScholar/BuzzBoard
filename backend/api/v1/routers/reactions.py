import json
from logging import getLogger
from typing import Dict, List, Optional

from core.authentication.auth_middleware import get_current_active_user
from core.storage import storage
from fastapi import APIRouter, Body, Depends
from fastapi.responses import JSONResponse
from schemas.reactions import Reaction, ReactionIn
from schemas.user import User
from services.mongo_storage import change_id_key

router = APIRouter()


@router.get(
    path="/posts_comments/{target_id}/reactions", response_model=List[Reaction]
)
def get_reactions(
    target_id: str,
    is_like: Optional[bool] = None,
    page_number: int = 1,
    page_size: int = 10,
):
    """Gets all reactions to a post or comment"""
    logger = getLogger(__name__ + ".get_reactions")
    try:

        skip = (page_number - 1) * page_size
        filter = {"target_id": target_id}
        if is_like is not None:
            filter["is_like"] = is_like
        reactions = (
            storage.db["reactions"].find(filter).skip(skip).limit(page_size)
        )
        reactions = [
            change_id_key(json.loads(json.dumps(reaction, default=str)))
            for reaction in reactions
        ]

        return reactions
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.get(
    path="/posts_comments/{target_id}/reactions/{reaction_id}",
    response_model=Reaction,
)
def get_reaction(
    target_id: str,
    reaction_id: str,
):
    """Get reaction by its id"""
    logger = getLogger(__name__ + ".get_reaction")
    try:

        reaction = storage.verify_reaction_record(
            {"_id": reaction_id, "target_id": target_id}
        )

        return reaction
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.post(
    path="/posts_comments/{target_id}/reactions",
    response_model=Dict[str, str],
)
def add_reaction(
    target_id: str,
    is_like: bool = Body(embed=True, default=True),
    current_user: User = Depends(get_current_active_user),
):
    """
    Adds a new reaction to a post or comment.
    If a reaction from the user exists it is replaced.
    """
    logger = getLogger(__name__ + ".add_reaction")
    try:
        existing_reaction = storage.get_reaction_record(
            {"target_id": target_id, "user_id": current_user.id}
        )
        if existing_reaction:
            storage.update_reaction_record(
                filter={"_id": existing_reaction.id},
                update={"is_like": is_like},
            )
            id = existing_reaction.id
        else:
            id = storage.create_reaction_record(
                ReactionIn(target_id=target_id, is_like=is_like),
                current_user.id,
            )

        response_message = {"message": "Added Reaction successfully", "id": id}

        return JSONResponse(response_message)
    except Exception as ex:
        logger.error(ex)
        raise ex


@router.delete(
    path="/posts_comments/{target_id}/reactions/me",
    response_model=Dict[str, str],
)
def delete_reaction(
    target_id: str,
    current_user: User = Depends(get_current_active_user),
):
    """Removes a user's reaction to a post or comment"""
    logger = getLogger(__name__ + ".delete_reaction")
    try:
        storage.delete_reaction_record(
            {"target_id": target_id, "user_id": current_user.id}
        )
        response_message = {"message": "Removed Reaction successfully"}

        return JSONResponse(response_message)
    except Exception as ex:
        logger.error(ex)
        raise ex
