#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to list files with encoding issues
"""
import os

files_to_check = [
    'ppt_cleaner.py',
    'ppt_image_remover.py', 
    'HUONG_DAN_TAI_VE.md',
    'README_CLEANER.md'
]

print("Files that need Vietnamese text fixed:")
for f in files_to_check:
    if os.path.exists(f):
        print(f"  ✓ {f}")
    else:
        print(f"  ✗ {f} (not found)")

print("\nThese files will be recreated with proper Vietnamese text.")
