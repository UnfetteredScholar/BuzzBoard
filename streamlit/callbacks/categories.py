import os

import requests

BACKEND = os.environ.get("BACKEND", "http://localhost:8000")


def get_categories(
    page: int = 1,
    page_size: int = 100,
) -> list:
    """Gets the post categories"""

    params = {"page": page, "page_size": page_size}

    response = requests.get(
        url=f"{BACKEND}/api/v1/categories",
        params=params,
    )

    return response.json()
