#!/bin/bash

# QUICK START GUIDE - Spam Detection System
# Run this file to set up and start the Spam Detection system

echo "=================================="
echo "🛡️  SPAM DETECTION SYSTEM - SETUP"
echo "=================================="
echo ""

# Check Python
echo "✓ Kiểm tra Python..."
if ! command -v python &> /dev/null; then
    echo "❌ Python chưa được cài đặt!"
    echo "Vui lòng cài đặt Python 3.8+ từ https://www.python.org"
    exit 1
fi

python_version=$(python --version 2>&1 | awk '{print $2}')
echo "✅ Phiên bản Python: $python_version"
echo ""

# Install dependencies
echo "📦 Cài đặt dependencies..."
pip install -r requirements.txt -q

if [ $? -eq 0 ]; then
    echo "✅ Dependencies cài đặt thành công"
else
    echo "❌ Lỗi cài đặt dependencies"
    exit 1
fi
echo ""

# Train model
echo "🤖 Huấn luyện mô hình Naive Bayes..."
python train_model.py

if [ $? -eq 0 ]; then
    echo "✅ Mô hình huấn luyện thành công"
else
    echo "❌ Lỗi huấn luyện mô hình"
    exit 1
fi
echo ""

# Start API
echo "🚀 Khởi động API..."
echo "API sẽ chạy tại: http://localhost:5000"
echo "Giao diện web: Mở file frontend/index.html trong trình duyệt"
echo ""
echo "Nhấp Ctrl+C để tắt API"
echo ""

python app.py
