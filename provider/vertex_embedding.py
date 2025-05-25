import json
from typing import Dict, Any

from google.cloud import aiplatform
from google.oauth2 import service_account

from dify_plugin import ModelProvider
from dify_plugin.entities.model import ProviderCredentialValidationError

class VertexEmbeddingProvider(ModelProvider):
    def validate_provider_credentials(self, credentials: Dict[str, Any]) -> None:
        """Validate the provided Google Cloud credentials."""
        try:
            # Validate project_id
            project_id = credentials.get("project_id")
            if not project_id:
                raise ProviderCredentialValidationError("Project ID is required")

            # Validate location
            location = credentials.get("location")
            if not location:
                raise ProviderCredentialValidationError("Location is required")

            # Validate and parse credentials JSON
            try:
                credentials_json = json.loads(credentials.get("credentials", "{}"))
                if not credentials_json:
                    raise ProviderCredentialValidationError("Service account credentials are required")
            except json.JSONDecodeError:
                raise ProviderCredentialValidationError("Invalid service account credentials JSON format")

            # Initialize Vertex AI client to validate credentials
            credentials_obj = service_account.Credentials.from_service_account_info(credentials_json)
            aiplatform.init(
                project=project_id,
                location=location,
                credentials=credentials_obj
            )

        except Exception as e:
            raise ProviderCredentialValidationError(f"Failed to validate credentials: {str(e)}") 