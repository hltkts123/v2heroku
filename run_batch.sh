#!/bin/bash
# PowerPoint Cleaner Batch - Run Script (Mac/Linux)

echo "Dang khoi dong PowerPoint Cleaner (Batch Mode)..."
python3 ppt_cleaner_batch.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Khong the chay ung dung!"
    read -p "Nhan Enter de thoat..."
fi
