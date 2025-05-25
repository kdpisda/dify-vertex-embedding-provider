from dify_plugin import Plugin

# Create plugin instance
plugin = Plugin()

# Register the provider
from provider.vertex_embedding import VertexEmbeddingProvider
plugin.register_model_provider(VertexEmbeddingProvider)

# Register the embedding model
from text_embedding.text_embedding import VertexTextEmbeddingModel
plugin.register_text_embedding_model(VertexTextEmbeddingModel)

if __name__ == "__main__":
    plugin.run() 