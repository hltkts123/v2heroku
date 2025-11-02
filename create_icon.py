#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create icon for PowerPoint Cleaner
"""

try:
    from PIL import Image, ImageDraw, ImageFont
    import os
    
    # Create 256x256 icon
    size = 256
    img = Image.new('RGB', (size, size), color='#2c3e50')
    draw = ImageDraw.Draw(img)
    
    # Draw background gradient effect
    for i in range(size):
        color_value = int(44 + (i / size) * 30)
        draw.line([(0, i), (size, i)], fill=(color_value, color_value + 18, color_value + 30))
    
    # Draw PowerPoint-like icon shape
    margin = 40
    
    # Main document shape (white rectangle with orange accent)
    doc_left = margin
    doc_top = margin + 20
    doc_right = size - margin
    doc_bottom = size - margin
    
    # White document
    draw.rectangle([doc_left, doc_top, doc_right, doc_bottom], 
                   fill='white', outline='#e74c3c', width=4)
    
    # Orange accent bar (like PowerPoint)
    accent_height = 40
    draw.rectangle([doc_left, doc_top, doc_right, doc_top + accent_height], 
                   fill='#e74c3c')
    
    # Draw "PP" text for PowerPoint
    try:
        # Try to use a nice font
        font_large = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 70)
        font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 40)
    except:
        try:
            font_large = ImageFont.truetype("arial.ttf", 70)
            font_small = ImageFont.truetype("arial.ttf", 40)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
    
    # "PP" text in white on orange bar
    text_pp = "PP"
    bbox = draw.textbbox((0, 0), text_pp, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_x = doc_left + (doc_right - doc_left - text_width) // 2
    text_y = doc_top + (accent_height - text_height) // 2 - 5
    draw.text((text_x, text_y), text_pp, fill='white', font=font_large)
    
    # Draw checkmark icon (cleaner symbol)
    check_size = 60
    check_x = doc_left + (doc_right - doc_left) // 2
    check_y = doc_top + accent_height + 50
    
    # Green circle background
    circle_radius = check_size // 2
    draw.ellipse([check_x - circle_radius, check_y - circle_radius,
                  check_x + circle_radius, check_y + circle_radius],
                 fill='#27ae60', outline='#229954', width=3)
    
    # White checkmark
    check_points = [
        (check_x - 15, check_y),
        (check_x - 5, check_y + 15),
        (check_x + 15, check_y - 15)
    ]
    draw.line(check_points, fill='white', width=8, joint='curve')
    
    # Draw "Clean" text below
    text_clean = "Clean"
    bbox = draw.textbbox((0, 0), text_clean, font=font_small)
    text_width = bbox[2] - bbox[0]
    text_x = doc_left + (doc_right - doc_left - text_width) // 2
    text_y = check_y + circle_radius + 20
    draw.text((text_x, text_y), text_clean, fill='#2c3e50', font=font_small)
    
    # Save as ICO
    # ICO format needs multiple sizes
    icon_sizes = [(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)]
    images = []
    for icon_size in icon_sizes:
        resized = img.resize(icon_size, Image.Resampling.LANCZOS)
        images.append(resized)
    
    # Save multi-resolution ICO
    images[0].save('icon.ico', format='ICO', sizes=[img.size for img in images])
    
    print("? Icon created successfully: icon.ico")
    
except ImportError:
    print("! Pillow not installed, using default icon")
except Exception as e:
    print(f"! Error creating icon: {e}")
    print("  Using default icon")
