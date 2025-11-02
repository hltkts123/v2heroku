#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerPoint Cleaner Tool
C?ng c? d?n d?p PowerPoint: X?a h?nh ?nh & L?c text
Kh?ng c?n m? PowerPoint, ch?y ??c l?p
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pptx import Presentation
from pptx.util import Inches
import os
import shutil
from datetime import datetime
from pathlib import Path
import re

class PowerPointCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("PowerPoint Cleaner - C?ng c? d?n d?p PowerPoint")
        self.root.geometry("750x700")
        self.root.resizable(False, False)
        
        # Variables
        self.file_path = tk.StringVar()
        self.auto_backup = tk.BooleanVar(value=True)
        
        self.create_widgets()
        
    def create_widgets(self):
        """T?o giao di?n"""
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="PowerPoint Cleaner",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=5)
        
        subtitle_label = tk.Label(
            header_frame,
            text="X?a h?nh ?nh & L?c text - Kh?ng c?n m? PowerPoint",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # Main content
        main_frame = tk.Frame(self.root, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection
        file_frame = tk.LabelFrame(main_frame, text="1. Ch?n file PowerPoint", font=("Arial", 11, "bold"), padx=10, pady=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        file_entry = tk.Entry(file_frame, textvariable=self.file_path, font=("Arial", 10), state="readonly")
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(
            file_frame,
            text="Ch?n file...",
            command=self.browse_file,
            bg="#3498db",
            fg="white",
            font=("Arial", 10),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20
        )
        browse_btn.pack(side=tk.RIGHT)
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Tab 1: X?a h?nh ?nh
        self.create_image_tab()
        
        # Tab 2: L?c text
        self.create_text_tab()
        
        # Options
        options_frame = tk.LabelFrame(main_frame, text="T?y ch?n chung", font=("Arial", 11, "bold"), padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        backup_cb = tk.Checkbutton(
            options_frame,
            text="T? ??ng backup file g?c tr??c khi x? l? (khuy?n ngh?)",
            variable=self.auto_backup,
            font=("Arial", 10)
        )
        backup_cb.pack(anchor="w")
        
        # Action buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        preview_btn = tk.Button(
            button_frame,
            text="Preview - Xem tr??c",
            command=self.preview_changes,
            bg="#f39c12",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10
        )
        preview_btn.pack(side=tk.LEFT, padx=(0, 10), fill=tk.X, expand=True)
        
        process_btn = tk.Button(
            button_frame,
            text="X? l? file",
            command=self.process_file,
            bg="#27ae60",
            fg="white",
            font=("Arial", 11, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=30,
            pady=10
        )
        process_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="S?n s?ng",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#2c3e50",
            anchor="w",
            padx=10,
            pady=5
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_image_tab(self):
        """Tab x?a h?nh ?nh"""
        image_frame = ttk.Frame(self.notebook)
        self.notebook.add(image_frame, text="??? X?a h?nh ?nh")
        
        # Variables
        self.img_width = tk.DoubleVar(value=1.6)
        self.img_height = tk.DoubleVar(value=1.6)
        self.img_tolerance = tk.DoubleVar(value=0.01)
        self.img_mode = tk.StringVar(value="and")
        
        # Instructions
        info_label = tk.Label(
            image_frame,
            text="X?a h?nh ?nh theo k?ch th??c c? th?",
            font=("Arial", 10, "italic"),
            fg="#7f8c8d"
        )
        info_label.pack(pady=10)
        
        # Size settings
        size_frame = tk.LabelFrame(image_frame, text="K?ch th??c (inch)", font=("Arial", 10, "bold"), padx=10, pady=10)
        size_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Width
        width_frame = tk.Frame(size_frame)
        width_frame.pack(fill=tk.X, pady=3)
        tk.Label(width_frame, text="Chi?u r?ng:", font=("Arial", 9), width=15, anchor="w").pack(side=tk.LEFT)
        tk.Spinbox(width_frame, from_=0.1, to=20.0, increment=0.1, textvariable=self.img_width, 
                   font=("Arial", 9), width=8).pack(side=tk.LEFT, padx=5)
        tk.Label(width_frame, text="inch", font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Height
        height_frame = tk.Frame(size_frame)
        height_frame.pack(fill=tk.X, pady=3)
        tk.Label(height_frame, text="Chi?u cao:", font=("Arial", 9), width=15, anchor="w").pack(side=tk.LEFT)
        tk.Spinbox(height_frame, from_=0.1, to=20.0, increment=0.1, textvariable=self.img_height, 
                   font=("Arial", 9), width=8).pack(side=tk.LEFT, padx=5)
        tk.Label(height_frame, text="inch", font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Tolerance
        tol_frame = tk.Frame(size_frame)
        tol_frame.pack(fill=tk.X, pady=3)
        tk.Label(tol_frame, text="Dung sai:", font=("Arial", 9), width=15, anchor="w").pack(side=tk.LEFT)
        tk.Spinbox(tol_frame, from_=0.001, to=0.5, increment=0.01, textvariable=self.img_tolerance, 
                   font=("Arial", 9), width=8).pack(side=tk.LEFT, padx=5)
        tk.Label(tol_frame, text="inch", font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Match mode
        mode_frame = tk.LabelFrame(image_frame, text="Ch? ?? so kh?p", font=("Arial", 10, "bold"), padx=10, pady=5)
        mode_frame.pack(fill=tk.X, padx=20)
        
        modes = [
            ("C? width V? height kh?p (AND)", "and"),
            ("width HO?C height kh?p (OR)", "or"),
            ("Ch? theo width", "width_only"),
            ("Ch? theo height", "height_only")
        ]
        
        for text, value in modes:
            tk.Radiobutton(mode_frame, text=text, variable=self.img_mode, value=value, 
                          font=("Arial", 9)).pack(anchor="w", pady=1)
    
    def create_text_tab(self):
        """Tab l?c text"""
        text_frame = ttk.Frame(self.notebook)
        self.notebook.add(text_frame, text="?? L?c text")
        
        # Variables
        self.text_mode = tk.StringVar(value="keep_vietnamese")
        self.custom_pattern = tk.StringVar()
        
        # Instructions
        info_label = tk.Label(
            text_frame,
            text="L?c v? x?a text trong c?c textbox",
            font=("Arial", 10, "italic"),
            fg="#7f8c8d"
        )
        info_label.pack(pady=10)
        
        # Mode selection
        mode_frame = tk.LabelFrame(text_frame, text="Ch? ?? l?c", font=("Arial", 10, "bold"), padx=10, pady=10)
        mode_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        modes = [
            ("Gi? ti?ng Vi?t - X?a ti?ng Anh (khuy?n ngh?)", "keep_vietnamese"),
            ("Ch? gi? ti?ng Anh - X?a ti?ng Vi?t", "keep_english"),
            ("X?a t?t c? text", "delete_all"),
            ("X?a theo pattern t?y ch?nh (regex)", "custom")
        ]
        
        for text, value in modes:
            tk.Radiobutton(mode_frame, text=text, variable=self.text_mode, value=value,
                          font=("Arial", 9), command=self.on_text_mode_change).pack(anchor="w", pady=2)
        
        # Custom pattern
        self.custom_frame = tk.LabelFrame(text_frame, text="Pattern t?y ch?nh (Regex)", 
                                          font=("Arial", 10, "bold"), padx=10, pady=10)
        self.custom_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        tk.Label(self.custom_frame, text="X?a d?ng kh?p v?i pattern:", 
                font=("Arial", 9)).pack(anchor="w")
        
        pattern_entry = tk.Entry(self.custom_frame, textvariable=self.custom_pattern, 
                                font=("Arial", 9))
        pattern_entry.pack(fill=tk.X, pady=5)
        
        tk.Label(self.custom_frame, text="V? d?: ^[0-9]+$ (x?a d?ng ch? c? s?)", 
                font=("Arial", 8), fg="gray").pack(anchor="w")
        
        self.custom_frame.pack_forget()  # ?n m?c ??nh
        
        # Options
        opt_frame = tk.LabelFrame(text_frame, text="T?y ch?n", font=("Arial", 10, "bold"), padx=10, pady=10)
        opt_frame.pack(fill=tk.X, padx=20)
        
        self.delete_empty_shapes = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_frame, text="X?a textbox r?ng sau khi l?c", 
                      variable=self.delete_empty_shapes, font=("Arial", 9)).pack(anchor="w")
        
        # Examples
        example_frame = tk.LabelFrame(text_frame, text="V? d?", font=("Arial", 10, "bold"), padx=10, pady=10)
        example_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        
        example_text = tk.Text(example_frame, height=6, font=("Courier", 8), wrap=tk.WORD, 
                               bg="#f8f9fa", relief=tk.FLAT)
        example_text.pack(fill=tk.X)
        
        example_content = """Tr??c:
Hello World
Xin ch?o Vi?t Nam
English text
Ti?ng Vi?t c? d?u

Sau (ch? ?? "Gi? ti?ng Vi?t"):
Xin ch?o Vi?t Nam
Ti?ng Vi?t c? d?u"""
        
        example_text.insert("1.0", example_content)
        example_text.config(state=tk.DISABLED)
    
    def on_text_mode_change(self):
        """Hi?n/?n custom pattern frame"""
        if self.text_mode.get() == "custom":
            self.custom_frame.pack(fill=tk.X, padx=20, pady=(0, 10), before=self.custom_frame.master.winfo_children()[-1])
        else:
            self.custom_frame.pack_forget()
    
    def browse_file(self):
        """Ch?n file PowerPoint"""
        filename = filedialog.askopenfilename(
            title="Ch?n file PowerPoint",
            filetypes=[
                ("PowerPoint files", "*.pptx"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.file_path.set(filename)
            self.update_status(f"?? ch?n: {os.path.basename(filename)}")
    
    def update_status(self, message):
        """C?p nh?t status bar"""
        self.status_label.config(text=message)
        self.root.update()
    
    def preview_changes(self):
        """Xem tr??c thay ??i"""
        if not self.file_path.get():
            messagebox.showwarning("C?nh b?o", "Vui l?ng ch?n file PowerPoint!")
            return
        
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        
        if "???" in current_tab:
            self.preview_image_changes()
        else:
            self.preview_text_changes()
    
    def preview_image_changes(self):
        """Preview x?a h?nh ?nh"""
        try:
            self.update_status("?ang ph?n t?ch h?nh ?nh...")
            prs = Presentation(self.file_path.get())
            
            images_to_delete = []
            total_images = 0
            
            for slide_idx, slide in enumerate(prs.slides, 1):
                for shape in slide.shapes:
                    if shape.shape_type == 13:  # Picture
                        total_images += 1
                        width_inches = shape.width / 914400
                        height_inches = shape.height / 914400
                        
                        if self.check_image_match(width_inches, height_inches):
                            images_to_delete.append({
                                'slide': slide_idx,
                                'name': shape.name,
                                'width': width_inches,
                                'height': height_inches
                            })
            
            self.show_preview_window("H?nh ?nh s? x?a", images_to_delete, total_images, "image")
            self.update_status("S?n s?ng")
            
        except Exception as e:
            messagebox.showerror("L?i", f"Kh?ng th? ??c file:\n{str(e)}")
            self.update_status("L?i!")
    
    def preview_text_changes(self):
        """Preview l?c text"""
        try:
            self.update_status("?ang ph?n t?ch text...")
            prs = Presentation(self.file_path.get())
            
            changes = []
            total_textboxes = 0
            
            for slide_idx, slide in enumerate(prs.slides, 1):
                for shape in slide.shapes:
                    if self.has_text(shape):
                        total_textboxes += 1
                        original_text = self.get_shape_text(shape)
                        new_text = self.filter_text(original_text)
                        
                        if new_text != original_text:
                            changes.append({
                                'slide': slide_idx,
                                'name': shape.name,
                                'original': original_text[:100] + "..." if len(original_text) > 100 else original_text,
                                'new': new_text[:100] + "..." if len(new_text) > 100 else new_text,
                                'deleted': len(new_text.strip()) == 0
                            })
            
            self.show_preview_window("Text s? thay ??i", changes, total_textboxes, "text")
            self.update_status("S?n s?ng")
            
        except Exception as e:
            messagebox.showerror("L?i", f"Kh?ng th? ??c file:\n{str(e)}")
            self.update_status("L?i!")
    
    def show_preview_window(self, title, items, total, item_type):
        """Hi?n th? c?a s? preview"""
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"Preview - {title}")
        preview_window.geometry("700x550")
        
        # Header
        if item_type == "image":
            header_text = f"T?m th?y {len(items)} h?nh ?nh s? x?a (T?ng: {total})"
        else:
            header_text = f"T?m th?y {len(items)} textbox s? thay ??i (T?ng: {total})"
        
        header = tk.Label(
            preview_window,
            text=header_text,
            font=("Arial", 12, "bold"),
            bg="#e74c3c",
            fg="white",
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Content
        content_frame = tk.Frame(preview_window, padx=10, pady=10)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        if item_type == "image":
            self.show_image_preview_content(content_frame, items)
        else:
            self.show_text_preview_content(content_frame, items)
        
        # Close button
        close_btn = tk.Button(
            preview_window,
            text="??ng",
            command=preview_window.destroy,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            padx=30,
            pady=5
        )
        close_btn.pack(pady=10)
    
    def show_image_preview_content(self, parent, items):
        """Hi?n th? preview cho h?nh ?nh"""
        scrollbar = tk.Scrollbar(parent)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        listbox = tk.Listbox(parent, font=("Courier", 9), yscrollcommand=scrollbar.set)
        listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=listbox.yview)
        
        if items:
            for img in items:
                item = f"Slide {img['slide']:3d} | {img['name']:35s} | {img['width']:.2f}x{img['height']:.2f} inch"
                listbox.insert(tk.END, item)
        else:
            listbox.insert(tk.END, "Kh?ng t?m th?y h?nh ?nh n?o ph? h?p!")
    
    def show_text_preview_content(self, parent, items):
        """Hi?n th? preview cho text"""
        text_widget = scrolledtext.ScrolledText(parent, font=("Courier", 9), wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        if items:
            for idx, item in enumerate(items, 1):
                status = "[X?A TEXTBOX]" if item['deleted'] else "[C?P NH?T]"
                text_widget.insert(tk.END, f"\n{'='*70}\n")
                text_widget.insert(tk.END, f"{idx}. Slide {item['slide']} - {item['name']} {status}\n")
                text_widget.insert(tk.END, f"{'='*70}\n")
                text_widget.insert(tk.END, f"Tr??c:\n{item['original']}\n\n")
                text_widget.insert(tk.END, f"Sau:\n{item['new'] if item['new'] else '[R?ng - s? x?a]'}\n")
        else:
            text_widget.insert(tk.END, "Kh?ng t?m th?y text n?o c?n thay ??i!")
        
        text_widget.config(state=tk.DISABLED)
    
    def process_file(self):
        """X? l? file"""
        if not self.file_path.get():
            messagebox.showwarning("C?nh b?o", "Vui l?ng ch?n file PowerPoint!")
            return
        
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        
        if "???" in current_tab:
            self.process_images()
        else:
            self.process_text()
    
    def process_images(self):
        """X? l? x?a h?nh ?nh"""
        mode_text = {
            "and": "C? width V? height kh?p",
            "or": "width HO?C height kh?p",
            "width_only": "ch? width kh?p",
            "height_only": "ch? height kh?p"
        }
        
        confirm_msg = f"""X?a h?nh ?nh v?i c?i ??t:

Width: {self.img_width.get()} inch
Height: {self.img_height.get()} inch
Ch? ??: {mode_text[self.img_mode.get()]}

Ti?p t?c?"""
        
        if not messagebox.askyesno("X?c nh?n", confirm_msg):
            return
        
        try:
            file_path = self.file_path.get()
            
            if self.auto_backup.get():
                self.update_status("?ang backup...")
                backup_path = self.create_backup(file_path)
            
            self.update_status("?ang x? l?...")
            prs = Presentation(file_path)
            
            deleted_count = 0
            total_images = 0
            
            for slide in prs.slides:
                shapes_to_delete = []
                
                for shape in slide.shapes:
                    if shape.shape_type == 13:
                        total_images += 1
                        width_inches = shape.width / 914400
                        height_inches = shape.height / 914400
                        
                        if self.check_image_match(width_inches, height_inches):
                            shapes_to_delete.append(shape)
                
                for shape in shapes_to_delete:
                    sp = shape.element
                    sp.getparent().remove(sp)
                    deleted_count += 1
            
            self.update_status("?ang l?u...")
            prs.save(file_path)
            
            messagebox.showinfo(
                "Ho?n t?t!",
                f"?? x?a h?nh ?nh th?nh c?ng!\n\n"
                f"T?ng: {total_images}\n"
                f"?? x?a: {deleted_count}\n"
                f"C?n l?i: {total_images - deleted_count}"
            )
            
            self.update_status("Ho?n t?t!")
            
        except Exception as e:
            messagebox.showerror("L?i", f"Kh?ng th? x? l?:\n{str(e)}")
            self.update_status("L?i!")
    
    def process_text(self):
        """X? l? l?c text"""
        mode_names = {
            "keep_vietnamese": "Gi? ti?ng Vi?t - X?a ti?ng Anh",
            "keep_english": "Gi? ti?ng Anh - X?a ti?ng Vi?t",
            "delete_all": "X?a t?t c? text",
            "custom": "Pattern t?y ch?nh"
        }
        
        mode = self.text_mode.get()
        mode_name = mode_names.get(mode, mode)
        
        confirm_msg = f"""L?c text v?i ch? ??:

{mode_name}

X?a textbox r?ng: {'C?' if self.delete_empty_shapes.get() else 'Kh?ng'}

Ti?p t?c?"""
        
        if not messagebox.askyesno("X?c nh?n", confirm_msg):
            return
        
        try:
            file_path = self.file_path.get()
            
            if self.auto_backup.get():
                self.update_status("?ang backup...")
                backup_path = self.create_backup(file_path)
            
            self.update_status("?ang x? l?...")
            prs = Presentation(file_path)
            
            modified_count = 0
            deleted_count = 0
            total_textboxes = 0
            
            for slide in prs.slides:
                shapes_to_delete = []
                
                for shape in slide.shapes:
                    if self.has_text(shape):
                        total_textboxes += 1
                        original_text = self.get_shape_text(shape)
                        new_text = self.filter_text(original_text)
                        
                        if new_text != original_text:
                            if len(new_text.strip()) == 0 and self.delete_empty_shapes.get():
                                shapes_to_delete.append(shape)
                                deleted_count += 1
                            else:
                                self.set_shape_text(shape, new_text)
                                modified_count += 1
                
                for shape in shapes_to_delete:
                    sp = shape.element
                    sp.getparent().remove(sp)
            
            self.update_status("?ang l?u...")
            prs.save(file_path)
            
            messagebox.showinfo(
                "Ho?n t?t!",
                f"?? l?c text th?nh c?ng!\n\n"
                f"T?ng textbox: {total_textboxes}\n"
                f"?? c?p nh?t: {modified_count}\n"
                f"?? x?a: {deleted_count}"
            )
            
            self.update_status("Ho?n t?t!")
            
        except Exception as e:
            messagebox.showerror("L?i", f"Kh?ng th? x? l?:\n{str(e)}")
            self.update_status("L?i!")
    
    def check_image_match(self, width_inches, height_inches):
        """Ki?m tra h?nh ?nh c? kh?p kh?ng"""
        target_width = self.img_width.get()
        target_height = self.img_height.get()
        tolerance = self.img_tolerance.get()
        mode = self.img_mode.get()
        
        width_match = abs(width_inches - target_width) < tolerance
        height_match = abs(height_inches - target_height) < tolerance
        
        if mode == "and":
            return width_match and height_match
        elif mode == "or":
            return width_match or height_match
        elif mode == "width_only":
            return width_match
        elif mode == "height_only":
            return height_match
        
        return False
    
    def has_text(self, shape):
        """Ki?m tra shape c? text kh?ng"""
        try:
            return shape.has_text_frame and shape.text_frame.text.strip()
        except:
            return False
    
    def get_shape_text(self, shape):
        """L?y text t? shape"""
        try:
            return shape.text_frame.text
        except:
            return ""
    
    def set_shape_text(self, shape, text):
        """Set text cho shape"""
        try:
            shape.text_frame.text = text
        except:
            pass
    
    def filter_text(self, text):
        """L?c text theo ch? ??"""
        mode = self.text_mode.get()
        
        if mode == "keep_vietnamese":
            return self.keep_unicode_lines(text)
        elif mode == "keep_english":
            return self.keep_ascii_lines(text)
        elif mode == "delete_all":
            return ""
        elif mode == "custom":
            return self.filter_by_pattern(text)
        
        return text
    
    def keep_unicode_lines(self, text):
        """Gi? d?ng c? Unicode (ti?ng Vi?t)"""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            if self.has_unicode_char(line):
                result.append(line)
        
        return '\n'.join(result)
    
    def keep_ascii_lines(self, text):
        """Gi? d?ng ch? ASCII (ti?ng Anh)"""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            if not self.has_unicode_char(line) and line.strip():
                result.append(line)
        
        return '\n'.join(result)
    
    def has_unicode_char(self, line):
        """Ki?m tra c? k? t? Unicode kh?ng"""
        if not line.strip():
            return False
        
        for char in line:
            if ord(char) > 127:
                return True
        
        return False
    
    def filter_by_pattern(self, text):
        """L?c theo regex pattern"""
        try:
            pattern = self.custom_pattern.get()
            if not pattern:
                return text
            
            lines = text.split('\n')
            result = []
            
            for line in lines:
                if not re.search(pattern, line):
                    result.append(line)
            
            return '\n'.join(result)
        except Exception as e:
            messagebox.showwarning("L?i pattern", f"Pattern kh?ng h?p l?:\n{str(e)}")
            return text
    
    def create_backup(self, file_path):
        """T?o backup file"""
        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        name_without_ext = os.path.splitext(file_name)[0]
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{name_without_ext}_backup_{timestamp}.pptx"
        backup_path = os.path.join(file_dir, backup_name)
        
        shutil.copy2(file_path, backup_path)
        return backup_path


def main():
    root = tk.Tk()
    app = PowerPointCleaner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
