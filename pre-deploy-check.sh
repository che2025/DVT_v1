#!/bin/bash

# Pre-deployment check script for hardware-firmware-dvt project

echo "🔍 Pre-deployment checks for hardware-firmware-dvt..."

GCLOUD_PATH="/Users/jianhuache/Downloads/DVT_v1/deploy_che_1/google-cloud-sdk/bin/gcloud"
TARGET_PROJECT="hardware-firmware-dvt"

# Check authentication
echo "1. Checking authentication..."
if ! $GCLOUD_PATH auth list --filter=status:ACTIVE --format="value(account)" | grep -q .; then
    echo "❌ Not authenticated. Please run:"
    echo "   $GCLOUD_PATH auth application-default login"
    exit 1
fi

ACTIVE_ACCOUNT=$($GCLOUD_PATH auth list --filter=status:ACTIVE --format="value(account)" | head -1)
echo "✅ Authenticated as: $ACTIVE_ACCOUNT"

# Check project access
echo "2. Checking access to target project..."
if ! $GCLOUD_PATH projects describe $TARGET_PROJECT &>/dev/null; then
    echo "❌ Cannot access project $TARGET_PROJECT"
    echo "   Please ask your manager to grant you access to the hardware-firmware-dvt project"
    echo "   Required roles: Cloud Run Admin, Cloud Build Editor, Storage Admin"
    exit 1
fi

echo "✅ Can access project: $TARGET_PROJECT"

# Save current project to restore later
CURRENT_PROJECT=$($GCLOUD_PATH config get-value project 2>/dev/null)
echo "📝 Current project: $CURRENT_PROJECT (will be restored after deployment)"

# Test switching to target project
echo "3. Testing project switch..."
$GCLOUD_PATH config set project $TARGET_PROJECT
SWITCHED_PROJECT=$($GCLOUD_PATH config get-value project)

if [ "$SWITCHED_PROJECT" != "$TARGET_PROJECT" ]; then
    echo "❌ Failed to switch to $TARGET_PROJECT"
    exit 1
fi

echo "✅ Successfully switched to: $SWITCHED_PROJECT"

# Check required APIs
echo "4. Checking required APIs..."
REQUIRED_APIS=("cloudbuild.googleapis.com" "run.googleapis.com" "containerregistry.googleapis.com" "aiplatform.googleapis.com")

for API in "${REQUIRED_APIS[@]}"; do
    if $GCLOUD_PATH services list --enabled --filter="name:$API" --format="value(name)" | grep -q "$API"; then
        echo "✅ $API is enabled"
    else
        echo "⚠️  $API is not enabled (will be enabled during deployment)"
    fi
done

# Restore original project
if [ ! -z "$CURRENT_PROJECT" ]; then
    $GCLOUD_PATH config set project $CURRENT_PROJECT
    echo "🔄 Restored original project: $CURRENT_PROJECT"
fi

echo ""
echo "🎉 Pre-deployment checks completed!"
echo "✅ Ready to deploy to hardware-firmware-dvt"
echo ""
echo "Next steps:"
echo "1. Run: ./deploy.sh"
echo "2. The deployment will automatically switch to hardware-firmware-dvt"
echo "3. After deployment, you can switch back with:"
echo "   $GCLOUD_PATH config set project dp-experimental"
