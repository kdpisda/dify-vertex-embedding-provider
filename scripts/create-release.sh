#!/bin/bash

# Vertex AI Embedding Provider Release Script
# This script helps create a new release for the Dify plugin

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if version argument is provided
if [ $# -eq 0 ]; then
    print_error "Please provide a version number (e.g., v0.0.2)"
    echo "Usage: $0 <version>"
    echo "Example: $0 v0.0.2"
    exit 1
fi

VERSION=$1

# Validate version format
if [[ ! $VERSION =~ ^v[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
    print_error "Version must be in format vX.Y.Z (e.g., v0.0.2)"
    exit 1
fi

# Extract numeric version (without 'v' prefix)
NUMERIC_VERSION=${VERSION#v}

print_status "Creating release for version: $VERSION"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    print_error "This script must be run from the root of the git repository"
    exit 1
fi

# Check if working directory is clean
if [ -n "$(git status --porcelain)" ]; then
    print_warning "Working directory is not clean. The following files have changes:"
    git status --short
    echo
    read -p "Do you want to continue? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        print_error "Aborted by user"
        exit 1
    fi
fi

# Check if tag already exists
if git tag -l | grep -q "^$VERSION$"; then
    print_error "Tag $VERSION already exists"
    exit 1
fi

# Update version in manifest.yaml
print_status "Updating version in manifest.yaml to $NUMERIC_VERSION"
sed -i.bak "s/^version: .*/version: $NUMERIC_VERSION/" manifest.yaml
sed -i.bak "s/^    version: .*/    version: $NUMERIC_VERSION/" manifest.yaml

# Remove backup file
rm -f manifest.yaml.bak

# Show the changes
print_status "Updated manifest.yaml:"
grep -n "version:" manifest.yaml

# Ask for confirmation
echo
print_warning "This will:"
echo "1. Commit the version update"
echo "2. Create and push tag: $VERSION"
echo "3. Trigger GitHub Actions to create the release"
echo
read -p "Do you want to continue? (y/N): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    print_error "Aborted by user"
    # Restore original manifest.yaml
    git checkout manifest.yaml
    exit 1
fi

# Commit the version update
print_status "Committing version update..."
git add manifest.yaml
git commit -m "Bump version to $VERSION"

# Create and push the tag
print_status "Creating and pushing tag: $VERSION"
git tag -a "$VERSION" -m "Release $VERSION"
git push origin main
git push origin "$VERSION"

print_status "Release process initiated!"
print_status "GitHub Actions will now create the release automatically."
print_status "You can monitor the progress at: https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^.]*\).*/\1/')/actions"

echo
print_status "Once the release is created, users can install the plugin using:"
echo "https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\([^.]*\).*/\1/')/releases/download/$VERSION/vertex-embedding-provider-$VERSION.tar.gz" 