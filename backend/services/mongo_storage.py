import json
from datetime import UTC, datetime
from typing import Any, Dict

import schemas.categories as s_categories
import schemas.posts as s_posts
import schemas.reactions as s_reactions
import schemas.user as s_user
from bson.objectid import ObjectId
from core.authentication.hashing import get_hash
from core.config import settings
from dotenv import load_dotenv
from fastapi import HTTPException, status
from pymongo import ASCENDING, DESCENDING, MongoClient

load_dotenv()


def change_id_key(obj: Dict[str, Any]) -> Dict[str, Any]:
    """Changes the _id key to id"""

    if "_id" in obj:
        obj["id"] = obj["_id"]
        del obj["_id"]

    return obj


class MongoStorage:
    """
    Defines functions for interacting
    with the BuzzBoard db storage
    """

    def __init__(self):
        """Initializes the storage class"""
        self.client = MongoClient(settings.MONGO_DB_URI)
        self.db = self.client[settings.DB_NAME]
        self.db["users"].create_index([("email", ASCENDING)], unique=True)
        self.db["users"].create_index(
            [("date_created", DESCENDING)], unique=False
        )

    # Users
    def create_user_record(self, form_data: s_user.UserIn) -> str:
        """Creates a user record"""

        users_table = self.db["users"]

        if users_table.find_one({"email": form_data.email}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already taken",
            )

        if len(form_data.password) < 8:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid password length. Password"
                + " length must be at least 8 characters",
            )

        date = datetime.now(UTC)
        user = form_data.model_dump()
        user["password"] = get_hash(form_data.password)
        user["status"] = s_user.UserStatus.UNVERIFIED
        user["date_created"] = date
        user["date_modified"] = date

        id = str(users_table.insert_one(user).inserted_id)

        return id

    def get_user_record(self, filter: Dict) -> s_user.User:
        """Gets a user record from the db using the supplied keys"""
        users = self.db["users"]

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        user = users.find_one(filter)

        if user:
            user = change_id_key(json.loads(json.dumps(user, default=str)))
            user = s_user.User(**user)

        return user

    def verify_user_record(self, filter: Dict) -> s_user.User:
        """Checks if a user record exists in the db using the supplied keys"""
        user = self.get_user_record(filter)

        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
            )

        return user

    def update_user_record(self, filter: Dict, update: Dict):
        """Updates a user record"""
        self.verify_user_record(filter)

        for key in ["_id", "email"]:
            if key in update:
                raise KeyError(f"Invalid Key. KEY {key} cannot be changed")

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])
        update["date_modified"] = datetime.now(UTC)

        self.db["users"].update_one(filter, {"$set": update})

    def delete_user_record(self, filter: Dict):
        """Deletes a user record by the filter"""
        self.verify_user_record(filter)

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        self.db["users"].delete_one(filter)

    # Categories
    def create_category_record(self, data: s_categories.CategoryIn) -> str:
        """Creates a category record"""

        categories = self.db["categories"]

        if categories.find_one({"name": data.name}):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Category already exists",
            )

        date = datetime.now(UTC)
        category = data.model_dump()
        category["date_created"] = date
        category["date_modified"] = date

        id = str(categories.insert_one(category).inserted_id)

        return id

    def get_category_record(self, filter: Dict) -> s_categories.Category:
        """Gets a category record using the filter"""

        categories = self.db["categories"]

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        category = categories.find_one(filter)

        if category:
            category = change_id_key(
                json.loads(json.dumps(category, default=str))
            )
            category = s_categories.Category(**category)

        return category

    def verify_category_record(self, filter: Dict) -> s_categories.Category:
        """
        Checks if a category record exists
        in the db using the supplied keys
        """
        category = self.get_category_record(filter)

        if category is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Category not found",
            )

        return category

    def update_category_record(self, filter: Dict, update: Dict):
        """Updates a category record"""
        self.verify_category_record(filter)

        for key in ["_id"]:
            if key in update:
                raise KeyError(f"Invalid Key. KEY {key} cannot be changed")

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])
        update["date_modified"] = datetime.now(UTC)

        self.db["categories"].update_one(filter, {"$set": update})

    def delete_category_record(self, filter: Dict):
        """Deletes a category record by the filter"""
        self.verify_category_record(filter)

        self.db["categories"].delete_one(filter)

    # Reactions
    def create_reaction_record(
        self, data: s_reactions.ReactionIn, user_id: str
    ) -> str:
        """Creates a reaction record"""

        reactions = self.db["reactions"]

        if reactions.find_one(
            {"target_id": data.target_id, "user_id": user_id}
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Reaction already exists",
            )

        date = datetime.now(UTC)
        reaction = data.model_dump()
        reaction["user_id"] = user_id
        reaction["date_created"] = date
        reaction["date_modified"] = date

        id = str(reactions.insert_one(reaction).inserted_id)

        return id

    def get_reaction_record(self, filter: Dict) -> s_reactions.Reaction:
        """Gets a reaction record using the filter"""

        reactions = self.db["reactions"]

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        reaction = reactions.find_one(filter)

        if reaction:
            reaction = change_id_key(
                json.loads(json.dumps(reaction, default=str))
            )
            reaction = s_reactions.Reaction(**reaction)

        return reaction

    def verify_reaction_record(self, filter: Dict) -> s_reactions.Reaction:
        """
        Checks if a reaction record exists
        in the db using the supplied keys
        """
        reaction = self.get_reaction_record(filter)

        if reaction is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Reaction not found",
            )

        return reaction

    def update_reaction_record(self, filter: Dict, update: Dict):
        """Updates a reaction record"""
        self.verify_reaction_record(filter)

        for key in ["_id", "user_id", "target_id"]:
            if key in update:
                raise KeyError(f"Invalid Key. KEY {key} cannot be changed")

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])
        update["date_modified"] = datetime.now(UTC)

        self.db["reactions"].update_one(filter, {"$set": update})

    def delete_reaction_record(self, filter: Dict):
        """Deletes a reaction record by the filter"""
        self.verify_reaction_record(filter)

        self.db["reactions"].delete_one(filter)

    # Posts
    def create_post_record(self, data: s_posts.PostIn, user_id: str) -> str:
        """Creates a post record"""

        posts = self.db["posts"]

        self.verify_category_record(
            {"_id": data.category_id, "topics": data.category_topic}
        )

        date = datetime.now(UTC)
        post = data.model_dump()
        post["user_id"] = user_id
        post["post_image_url"] = None
        post["likes"] = 0
        post["dislikes"] = 0
        post["comments"] = 0
        post["date_created"] = date
        post["date_modified"] = date

        id = str(posts.insert_one(post).inserted_id)

        return id

    def get_post_record(self, filter: Dict) -> s_posts.Post:
        """Gets a post record using the filter"""

        posts = self.db["posts"]

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        post = posts.find_one(filter)

        if post:
            post = change_id_key(json.loads(json.dumps(post, default=str)))
            post = s_posts.Post(**post)

        return post

    def verify_post_record(self, filter: Dict) -> s_posts.Post:
        """
        Checks if a post record exists
        in the db using the supplied keys
        """
        post = self.get_post_record(filter)

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found",
            )

        return post

    def update_post_record(self, filter: Dict, update: Dict):
        """Updates a post record"""
        self.verify_post_record(filter)

        for key in [
            "_id",
            "user_id",
            "category_id",
            "likes",
            "dislikes",
            "comments",
        ]:
            if key in update:
                raise KeyError(f"Invalid Key. KEY {key} cannot be changed")

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])
        update["date_modified"] = datetime.now(UTC)

        self.db["posts"].update_one(filter, {"$set": update})

    def delete_post_record(self, filter: Dict):
        """Deletes a post record by the filter"""
        self.verify_post_record(filter)

        self.db["posts"].delete_one(filter)
