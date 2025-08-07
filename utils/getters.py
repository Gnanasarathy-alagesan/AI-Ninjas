import os

from dotenv import load_dotenv
from loguru import logger


def get_watsonx_info():
    success = load_dotenv(dotenv_path="secrets/.env.watsonx", override=True)

    if success:
        logger.info(".env.watsonx file loaded successfully.")
    else:
        logger.warning("Failed to load .env.watsonx file.")

    api_key = os.getenv("WATSONX_APIKEY")
    url = os.getenv("WATSONX_URL")
    project_id = os.getenv("PROJECT_ID")

    if not all([api_key, url, project_id]):
        logger.error("One or more required environment variables are missing.")

    return api_key, url, project_id
