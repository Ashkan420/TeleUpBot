import os
import requests


def upload_image_to_imgbb(file_path: str, api_key: str) -> str:
    """
    Uploads an image to ImgBB and returns the URL.
    Raises Exception if upload fails.
    """
    if not api_key:
        raise Exception("IMGBB_API_KEY is not set.")

    with open(file_path, "rb") as f:
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            params={"key": api_key},
            files={"image": f},
            timeout=20
        ).json()

    if "data" not in response or "url" not in response["data"]:
        raise Exception(f"ImgBB upload failed: {response}")

    return response["data"]["url"]
