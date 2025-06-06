# Vertex AI Embedding Provider for Dify

This Dify plugin provides text embeddings using Google's `text-multilingual-embedding-002` model through Vertex AI. It integrates seamlessly with Dify's embedding system for semantic search, similarity comparison, and other vector operations.

## Installation

### Option 1: Install from GitHub Release (Recommended)

1. In your Dify application, go to **Settings** → **Model Providers**
2. Click **Install Plugin**
3. Enter the GitHub release URL:
   ```
   https://github.com/kdpisda/dify-vertex-embedding-provider/releases/latest/download/vertex-embedding-provider-[VERSION].difypkg
   ```
   Replace `[VERSION]` with the specific version tag (e.g., `v0.0.1`)

### Option 2: Manual Installation

1. Download the latest `.difypkg` file from the [Releases page](https://github.com/kdpisda/dify-vertex-embedding-provider/releases)
2. In Dify, go to **Settings** → **Model Providers** → **Install Plugin** → **Install via Local File**
3. Upload the downloaded `.difypkg` file

## Creating Releases (For Developers)

This repository uses GitHub Actions to automatically create releases with proper Dify plugin packaging. To create a new release:

1. Update the version in `manifest.yaml` if needed
2. Create and push a new tag:
   ```bash
   git tag v0.0.2
   git push origin v0.0.2
   ```
3. GitHub Actions will automatically:
   - Update the manifest version
   - Download the official Dify plugin CLI tool
   - Package the plugin using the official Dify packaging format (`.difypkg`)
   - Create a new release with proper installation instructions
   - Upload the `.difypkg` file as a release asset

### Using the Helper Script

Alternatively, use the included helper script:
```bash
./scripts/create-release.sh v0.0.2
```

This script will handle version updates, git operations, and trigger the automated packaging process.

## Features

- Uses Google's state-of-the-art `text-multilingual-embedding-002` model
- Supports multiple languages
- Provides high-quality embeddings with 768 dimensions
- Easy integration with Dify's knowledge base and RAG systems
- Secure credential management

## Prerequisites

1. A Google Cloud Platform (GCP) account
2. A GCP project with Vertex AI API enabled
3. A service account with the following roles:
   - `roles/aiplatform.user`
   - `roles/serviceusage.serviceUsageConsumer`

## Setup Instructions

### 1. Enable Vertex AI API

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Select your project or create a new one
3. Navigate to "APIs & Services" > "Library"
4. Search for "Vertex AI API" and enable it

### 2. Create a Service Account

1. Go to "IAM & Admin" > "Service Accounts"
2. Click "Create Service Account"
3. Provide a name and description
4. Assign the required roles:
   - `Vertex AI User`
   - `Service Usage Consumer`
5. Create and download the JSON key file

### 3. Install the Plugin

1. Install the plugin in your Dify application
2. Configure the following credentials:
   - **Google Cloud Project ID**: Your GCP project ID
   - **Google Cloud Location**: The region where you want to use Vertex AI (e.g., `us-central1`)
   - **Google Cloud Service Account Key**: The entire JSON content of your service account key file

## Usage

Once configured, the plugin will be available as an embedding provider in Dify. You can:

1. Use it in Knowledge Base configurations for document indexing
2. Select it as the embedding model in RAG applications
3. Use it for semantic search and similarity comparisons

### Model Specifications

- **Model**: `text-multilingual-embedding-002`
- **Dimensions**: 768
- **Context Size**: 2048 tokens
- **Languages**: Supports 100+ languages
- **Use Cases**: Text similarity, semantic search, clustering, classification

## Pricing

The plugin uses Google Cloud Vertex AI pricing:
- **Input**: $0.00002 per 1K tokens
- **Currency**: USD

For the most up-to-date pricing, please refer to the [Google Cloud Vertex AI pricing page](https://cloud.google.com/vertex-ai/pricing).

## Security and Privacy

- All credentials are encrypted and stored securely within Dify
- Text input is processed in real-time and not stored permanently
- Communication with Google Cloud uses secure HTTPS connections
- See [PRIVACY.md](PRIVACY.md) for detailed privacy information

## Troubleshooting

### Common Issues

1. **Authentication Error**: Ensure your service account has the correct permissions and the JSON key is valid
2. **Location Error**: Make sure the specified location supports Vertex AI and the embedding model
3. **Quota Exceeded**: Check your Google Cloud quotas and billing settings

### Support

For issues related to:
- **Plugin functionality**: Create an issue in this repository
- **Google Cloud setup**: Refer to [Google Cloud documentation](https://cloud.google.com/vertex-ai/docs)
- **Dify integration**: Check [Dify documentation](https://docs.dify.ai/)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details. 