import json
from typing import List

from google.cloud import aiplatform
from google.oauth2 import service_account

from dify_plugin import TextEmbeddingModel
from dify_plugin.entities.model import EmbeddingUsage, TextEmbeddingResult


class VertexTextEmbeddingModel(TextEmbeddingModel):
    """
    Model class for Vertex AI text embedding model.
    """

    def _invoke(self, model: str, credentials: dict, texts: List[str], user: str = None) -> TextEmbeddingResult:
        """
        Invoke text embedding model

        :param model: model name
        :param credentials: model credentials
        :param texts: texts to embed
        :param user: unique user id
        :return: embeddings result
        """
        try:
            # Get credentials
            project_id = credentials["project_id"]
            location = credentials["location"]
            credentials_json = json.loads(credentials["credentials"])

            # Initialize Vertex AI client
            credentials_obj = service_account.Credentials.from_service_account_info(credentials_json)
            aiplatform.init(
                project=project_id,
                location=location,
                credentials=credentials_obj
            )

            # Get the model
            embedding_model = aiplatform.TextEmbeddingModel.from_pretrained(model)

            # Generate embeddings
            embeddings_response = embedding_model.get_embeddings(texts)

            # Extract embedding vectors
            embeddings = []
            total_tokens = 0
            
            for embedding in embeddings_response:
                embeddings.append(embedding.values)
                # Estimate tokens (rough approximation: 1 token ≈ 4 characters)
                total_tokens += len(texts[embeddings_response.index(embedding)]) // 4

            # Create usage object
            usage = EmbeddingUsage(
                tokens=total_tokens,
                total_tokens=total_tokens
            )

            # Return result
            return TextEmbeddingResult(
                embeddings=embeddings,
                usage=usage,
                model=model
            )

        except Exception as e:
            raise RuntimeError(f"Error generating embeddings: {str(e)}")

    def get_num_tokens(self, model: str, credentials: dict, texts: List[str]) -> int:
        """
        Get number of tokens for given texts

        :param model: model name
        :param credentials: model credentials
        :param texts: texts to embed
        :return: number of tokens
        """
        # Rough estimation: 1 token ≈ 4 characters
        return sum(len(text) // 4 for text in texts) 