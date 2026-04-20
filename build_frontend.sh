#!/bin/bash

# Build script for Property Management Frontend - Production Deployment

echo "🚀 Building Property Management Frontend for Production..."

# Navigate to frontend directory
cd property_ui

# Install dependencies if node_modules doesn't exist
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    yarn install
fi

# Build the frontend application
echo "🔨 Building frontend application..."
yarn build

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Frontend build completed successfully!"
    echo "📁 Built files are in: property_management/property_management/public/"
    echo "🌐 HTML template is in: property_management/property_management/www/frontend.html"
    echo ""
    echo "🎯 Production Deployment Ready!"
    echo "   - Frontend assets: /assets/property_management/"
    echo "   - Access URL: http://your-site.com/frontend"
    echo ""
    echo "📋 Next Steps:"
    echo "   1. Restart bench: bench restart"
    echo "   2. Clear cache: bench --site [your-site] clear-cache"
    echo "   3. Access frontend at: http://[your-site]:8000/frontend"
    echo "   4. Frontend will be served as static assets from the app"
else
    echo "❌ Frontend build failed!"
    exit 1
fi
