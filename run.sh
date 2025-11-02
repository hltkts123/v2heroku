#!/bin/bash
# PowerPoint Image Remover - Run Script (Mac/Linux)
# Script chay ung dung tren Mac/Linux

echo "Dang khoi dong PowerPoint Image Remover..."
python3 ppt_image_remover.py

if [ $? -ne 0 ]; then
    echo ""
    echo "[ERROR] Khong the chay ung dung!"
    echo "Vui long chay ./install.sh truoc."
    read -p "Nhan Enter de thoat..."
fi
