#!/bin/bash

# DVT Report Generator - GCP Cloud Run Deployment Script
# Project: hardware-firmware-dvt (Target deployment project)
# Note: This is different from the development project (dp-experimental)

set -e  # Exit on any error

echo "🚀 Starting DVT Report Generator deployment to GCP..."

# Set project variables for TEST deployment in dp-experimental
PROJECT_ID="dp-experimental"  # Testing project (your development project)
SERVICE_NAME="dvt-report-generator-test"
REGION="us-central1"
IMAGE_NAME="gcr.io/${PROJECT_ID}/${SERVICE_NAME}"

echo "📋 Deployment Configuration:"
echo "   Test Project: ${PROJECT_ID} (Development/Testing)"
echo "   Service Name: ${SERVICE_NAME}"
echo "   Region: ${REGION}"
echo "   Image: ${IMAGE_NAME}"
echo ""
echo "🧪 NOTE: This is a TEST deployment to dp-experimental project"
echo "   Later we'll deploy the same to hardware-firmware-dvt"
echo ""

# Use the installed Google Cloud SDK from deploy_che_1
GCLOUD_PATH="/Users/jianhuache/Downloads/DVT_v1/deploy_che_1/google-cloud-sdk/bin/gcloud"

# Check if gcloud is available
if [ ! -f "$GCLOUD_PATH" ]; then
    echo "❌ Google Cloud CLI not found at $GCLOUD_PATH"
    echo "Please make sure Google Cloud SDK is installed."
    exit 1
fi

echo "✅ Found Google Cloud CLI at: $GCLOUD_PATH"

# Check authentication status
echo "🔐 Checking authentication..."
if ! $GCLOUD_PATH auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ You are not authenticated with gcloud."
    echo "Please run: $GCLOUD_PATH auth application-default login"
    echo "Or run: $GCLOUD_PATH auth login"
    exit 1
fi

echo "✅ Authentication verified!"

# Switch to the test project (dp-experimental)
echo "🔧 Switching to test project: ${PROJECT_ID}..."
$GCLOUD_PATH config set project ${PROJECT_ID}

# Verify we're in the correct project
CURRENT_PROJECT=$($GCLOUD_PATH config get-value project)
echo "📍 Current active project: ${CURRENT_PROJECT}"

if [ "$CURRENT_PROJECT" != "$PROJECT_ID" ]; then
    echo "❌ Failed to switch to project ${PROJECT_ID}"
    echo "Please check your permissions for the dp-experimental project"
    exit 1
fi

# Enable required APIs
echo "🔌 Enabling required APIs..."
$GCLOUD_PATH services enable cloudbuild.googleapis.com
$GCLOUD_PATH services enable run.googleapis.com
$GCLOUD_PATH services enable containerregistry.googleapis.com

# Build and push Docker image
echo "🐳 Building Docker image..."
$GCLOUD_PATH builds submit --tag ${IMAGE_NAME}

# Deploy to Cloud Run with production settings
echo "🚀 Deploying to Cloud Run..."
$GCLOUD_PATH run deploy ${SERVICE_NAME} \
    --image ${IMAGE_NAME} \
    --platform managed \
    --region ${REGION} \
    --allow-unauthenticated \
    --memory 4Gi \
    --cpu 2 \
    --timeout 300 \
    --max-instances 10 \
    --port 8000 \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=${PROJECT_ID}" \
    --set-env-vars="GOOGLE_CLOUD_LOCATION=${REGION}" \
    --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=true"

# Get the service URL
SERVICE_URL=$($GCLOUD_PATH run services describe ${SERVICE_NAME} --region=${REGION} --format="value(status.url)")

echo ""
echo "✅ TEST Deployment completed successfully!"
echo "🌐 Your DVT Report Generator TEST version is now live at:"
echo "   ${SERVICE_URL}"
echo ""
echo "📝 Environment Configuration:"
echo "   GOOGLE_CLOUD_PROJECT: ${PROJECT_ID}"
echo "   GOOGLE_CLOUD_LOCATION: ${REGION}"
echo "   GOOGLE_GENAI_USE_VERTEXAI: true"
echo ""
echo "🧪 Testing Instructions:"
echo "   1. Test your application by visiting the URL above"
echo "   2. Upload test files and generate a sample report"
echo "   3. Verify all features work correctly"
echo ""
echo "🚀 After testing is successful:"
echo "   1. Get permissions for hardware-firmware-dvt project"
echo "   2. Change PROJECT_ID back to 'hardware-firmware-dvt' in deploy.sh"
echo "   3. Run ./deploy.sh again for production deployment"
echo ""
echo "📊 Monitor logs with:"
echo "   $GCLOUD_PATH logs tail /projects/${PROJECT_ID}/logs/run.googleapis.com%2Frequest"
echo ""
