#!/bin/bash

# Configuration
PROJECT_ROOT=$(pwd)
BUILD_DIR="$PROJECT_ROOT/build"
ZIP_FILE="$PROJECT_ROOT/lambda_function.zip"
SRC_DIR="$PROJECT_ROOT/src"

echo "🚀 Starting Lambda Deployment Packaging..."

# 1. Clean up previous builds
rm -rf "$BUILD_DIR"
rm -f "$ZIP_FILE"
mkdir -p "$BUILD_DIR"

# 2. Export dependencies using uv
echo "📦 Exporting dependencies..."
uv export --format requirements-txt --no-hashes --output-file "$BUILD_DIR/requirements.txt"

# 3. Install dependencies into build directory
echo "🛠 Installing dependencies..."
if [ -f "$BUILD_DIR/requirements.txt" ]; then
    pip install -r "$BUILD_DIR/requirements.txt" --target "$BUILD_DIR"
else
    echo "⚠️  Warning: requirements.txt not found. Packaging without dependencies."
fi

# 4. Copy source code
echo "📂 Copying source code..."
cp -r "$SRC_DIR/"* "$BUILD_DIR/"

# 5. Create ZIP package
echo "🗜 Creating deployment package..."
cd "$BUILD_DIR"
zip -r "$ZIP_FILE" . -x "requirements.txt"
cd "$PROJECT_ROOT"

echo "✅ Deployment package created: $ZIP_FILE"
echo "ℹ️  Next steps: 
1. Upload this ZIP to your AWS Lambda functions.
2. Set the Handler to 'handlers.training.handler' or 'handlers.inference.handler' as needed.
3. Configure the environment variables in the AWS Console matching your .env file."
