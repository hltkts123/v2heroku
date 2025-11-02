#!/bin/bash
# PowerPoint Image Remover - Installation Script (Mac/Linux)
# Script cai dat tu dong cho Mac/Linux

echo "========================================"
echo "PowerPoint Image Remover - Cai dat"
echo "========================================"
echo ""

# Check Python
echo "[1/3] Kiem tra Python..."
if ! command -v python3 &> /dev/null; then
    echo "[ERROR] Khong tim thay Python 3!"
    echo "Vui long cai dat Python 3:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip python3-tk"
    echo "  macOS:         brew install python3"
    exit 1
fi

python3 --version
echo "Python da duoc cai dat!"
echo ""

# Check pip
echo "[2/3] Kiem tra pip..."
if ! command -v pip3 &> /dev/null; then
    echo "[ERROR] Khong tim thay pip3!"
    exit 1
fi

echo "pip da san sang!"
echo ""

# Install dependencies
echo "[3/3] Cai dat thu vien python-pptx..."
pip3 install python-pptx

if [ $? -ne 0 ]; then
    echo "[ERROR] Khong the cai dat python-pptx!"
    exit 1
fi

echo ""
echo "========================================"
echo "Cai dat thanh cong!"
echo "========================================"
echo ""
echo "De chay ung dung, su dung file run.sh"
echo "Hoac chay lenh: python3 ppt_image_remover.py"
echo ""

# Make run.sh executable
chmod +x run.sh
echo "Da cap quyen thuc thi cho run.sh"
