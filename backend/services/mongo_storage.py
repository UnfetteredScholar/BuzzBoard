import json
from datetime import UTC, datetime
from os import getenv
from typing import Any, Dict, Union

from bson.objectid import ObjectId
from dotenv import load_dotenv
from fastapi import HTTPException, status
from pymongo import ASCENDING, DESCENDING, MongoClient

import schemas
import schemas.user as s_user
from core.authentication.hashing import get_hash
from core.config import settings

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

        self.db["users"].update_one(filter, {"$set": update})

    def delete_user_record(self, filter: Dict):
        """Deletes a user record by the filter"""
        self.verify_user_record(filter)

        if "_id" in filter and type(filter["_id"]) is str:
            filter["_id"] = ObjectId(filter["_id"])

        self.db["users"].delete_one(filter)
