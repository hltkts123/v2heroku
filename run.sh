#!/bin/bash
# PowerPoint Cleaner - Run Script (Mac/Linux)
# Script chay ung dung tren Mac/Linux

echo "Dang khoi dong PowerPoint Cleaner..."
python3 ppt_cleaner.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Khong the chay ung dung!"
    echo "Vui long chay ./install.sh truoc."
    read -p "Nhan Enter de thoat..."
fi
