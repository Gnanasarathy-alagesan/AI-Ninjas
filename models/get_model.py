from ibm_watsonx_ai.credentials import Credentials
from ibm_watsonx_ai.foundation_models import ModelInference

from utils.getters import get_watsonx_info


def get_model_instance(model_id: str) -> ModelInference:
    """
    Creates and returns a ModelInference instance for the given model ID.

    This function automatically loads WatsonX credentials and project information
    using `get_watsonx_info()` and instantiates the ModelInference object.

    Args:
        model_id (str): The WatsonX model ID (e.g., "ibm/granite-13b-instruct-v2").

    Returns:
        ModelInference: An instance of the ModelInference class configured with the
                        specified model ID and loaded credentials.
    """
    api_key, url, project_id = get_watsonx_info()
    creds = Credentials(url=url, api_key=api_key)

    return ModelInference(model_id=model_id, credentials=creds, project_id=project_id)
