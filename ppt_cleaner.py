#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerPoint Cleaner Tool
Cong cu don dep PowerPoint: Xoa hinh anh & Loc text
Khong can mo PowerPoint, chay doc lap
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
        self.root.title("PowerPoint Cleaner - Cong cu don dep PowerPoint")
        self.root.geometry("750x700")
        self.root.resizable(False, False)
        
        # Variables
        self.file_path = tk.StringVar()
        self.auto_backup = tk.BooleanVar(value=True)
        
        self.create_widgets()
        
    def create_widgets(self):
        """Tao giao dien"""
        
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
            text="Xoa hinh anh & Loc text - Khong can mo PowerPoint",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # Main content
        main_frame = tk.Frame(self.root, padx=20, pady=15)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection
        file_frame = tk.LabelFrame(main_frame, text="1. Chon file PowerPoint", font=("Arial", 11, "bold"), padx=10, pady=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        file_entry = tk.Entry(file_frame, textvariable=self.file_path, font=("Arial", 10), state="readonly")
        file_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(
            file_frame,
            text="Chon file...",
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
        
        # Tab 1: Xoa hinh anh
        self.create_image_tab()
        
        # Tab 2: Loc text
        self.create_text_tab()
        
        # Options
        options_frame = tk.LabelFrame(main_frame, text="Tuy chon chung", font=("Arial", 11, "bold"), padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=(0, 10))
        
        backup_cb = tk.Checkbutton(
            options_frame,
            text="Tu dong backup file goc truoc khi xu ly (khuyen nghi)",
            variable=self.auto_backup,
            font=("Arial", 10)
        )
        backup_cb.pack(anchor="w")
        
        # Action buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(5, 0))
        
        preview_btn = tk.Button(
            button_frame,
            text="Preview - Xem truoc",
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
            text="Xu ly file",
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
            text="San sang",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#2c3e50",
            anchor="w",
            padx=10,
            pady=5
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_image_tab(self):
        """Tab xoa hinh anh"""
        image_frame = ttk.Frame(self.notebook)
        self.notebook.add(image_frame, text=" Xoa hinh anh")
        
        # Variables
        self.img_width = tk.DoubleVar(value=1.6)
        self.img_height = tk.DoubleVar(value=1.6)
        self.img_tolerance = tk.DoubleVar(value=0.01)
        self.img_mode = tk.StringVar(value="and")
        
        # Instructions
        info_label = tk.Label(
            image_frame,
            text="Xoa hinh anh theo kich thuoc cu the",
            font=("Arial", 10, "italic"),
            fg="#7f8c8d"
        )
        info_label.pack(pady=10)
        
        # Size settings
        size_frame = tk.LabelFrame(image_frame, text="Kich thuoc (inch)", font=("Arial", 10, "bold"), padx=10, pady=10)
        size_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        # Width
        width_frame = tk.Frame(size_frame)
        width_frame.pack(fill=tk.X, pady=3)
        tk.Label(width_frame, text="Chieu rong:", font=("Arial", 9), width=15, anchor="w").pack(side=tk.LEFT)
        tk.Spinbox(width_frame, from_=0.1, to=20.0, increment=0.1, textvariable=self.img_width, 
                   font=("Arial", 9), width=8).pack(side=tk.LEFT, padx=5)
        tk.Label(width_frame, text="inch", font=("Arial", 9)).pack(side=tk.LEFT)
        
        # Height
        height_frame = tk.Frame(size_frame)
        height_frame.pack(fill=tk.X, pady=3)
        tk.Label(height_frame, text="Chieu cao:", font=("Arial", 9), width=15, anchor="w").pack(side=tk.LEFT)
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
        mode_frame = tk.LabelFrame(image_frame, text="Che do so khop", font=("Arial", 10, "bold"), padx=10, pady=5)
        mode_frame.pack(fill=tk.X, padx=20)
        
        modes = [
            ("CA width VA height khop (AND)", "and"),
            ("width HOAC height khop (OR)", "or"),
            ("Chi theo width", "width_only"),
            ("Chi theo height", "height_only")
        ]
        
        for text, value in modes:
            tk.Radiobutton(mode_frame, text=text, variable=self.img_mode, value=value, 
                          font=("Arial", 9)).pack(anchor="w", pady=1)
    
    def create_text_tab(self):
        """Tab loc text"""
        text_frame = ttk.Frame(self.notebook)
        self.notebook.add(text_frame, text=" Loc text")
        
        # Variables
        self.text_mode = tk.StringVar(value="keep_vietnamese")
        self.custom_pattern = tk.StringVar()
        
        # Instructions
        info_label = tk.Label(
            text_frame,
            text="Loc va xoa text trong cac textbox",
            font=("Arial", 10, "italic"),
            fg="#7f8c8d"
        )
        info_label.pack(pady=10)
        
        # Mode selection
        mode_frame = tk.LabelFrame(text_frame, text="Che do loc", font=("Arial", 10, "bold"), padx=10, pady=10)
        mode_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        modes = [
            ("Giu tieng Viet - Xoa tieng Anh (khuyen nghi)", "keep_vietnamese"),
            ("Chi giu tieng Anh - Xoa tieng Viet", "keep_english"),
            ("Xoa tat ca text", "delete_all"),
            ("Xoa theo pattern tuy chinh (regex)", "custom")
        ]
        
        for text, value in modes:
            tk.Radiobutton(mode_frame, text=text, variable=self.text_mode, value=value,
                          font=("Arial", 9), command=self.on_text_mode_change).pack(anchor="w", pady=2)
        
        # Custom pattern
        self.custom_frame = tk.LabelFrame(text_frame, text="Pattern tuy chinh (Regex)", 
                                          font=("Arial", 10, "bold"), padx=10, pady=10)
        self.custom_frame.pack(fill=tk.X, padx=20, pady=(0, 10))
        
        tk.Label(self.custom_frame, text="Xoa dong khop voi pattern:", 
                font=("Arial", 9)).pack(anchor="w")
        
        pattern_entry = tk.Entry(self.custom_frame, textvariable=self.custom_pattern, 
                                font=("Arial", 9))
        pattern_entry.pack(fill=tk.X, pady=5)
        
        tk.Label(self.custom_frame, text="Vi du: ^[0-9]+$ (xoa dong chi co so)", 
                font=("Arial", 8), fg="gray").pack(anchor="w")
        
        self.custom_frame.pack_forget()  # An mac dinh
        
        # Options
        opt_frame = tk.LabelFrame(text_frame, text="Tuy chon", font=("Arial", 10, "bold"), padx=10, pady=10)
        opt_frame.pack(fill=tk.X, padx=20)
        
        self.delete_empty_shapes = tk.BooleanVar(value=True)
        tk.Checkbutton(opt_frame, text="Xoa textbox rong sau khi loc", 
                      variable=self.delete_empty_shapes, font=("Arial", 9)).pack(anchor="w")
        
        # Examples
        example_frame = tk.LabelFrame(text_frame, text="Vi du", font=("Arial", 10, "bold"), padx=10, pady=10)
        example_frame.pack(fill=tk.X, padx=20, pady=(10, 0))
        
        example_text = tk.Text(example_frame, height=6, font=("Courier", 8), wrap=tk.WORD, 
                               bg="#f8f9fa", relief=tk.FLAT)
        example_text.pack(fill=tk.X)
        
        example_content = """Truoc:
Hello World
Xin chao Viet Nam
English text
Tieng Viet co dau

Sau (che do "Giu tieng Viet"):
Xin chao Viet Nam
Tieng Viet co dau"""
        
        example_text.insert("1.0", example_content)
        example_text.config(state=tk.DISABLED)
    
    def on_text_mode_change(self):
        """Hien/an custom pattern frame"""
        if self.text_mode.get() == "custom":
            self.custom_frame.pack(fill=tk.X, padx=20, pady=(0, 10), before=self.custom_frame.master.winfo_children()[-1])
        else:
            self.custom_frame.pack_forget()
    
    def browse_file(self):
        """Chon file PowerPoint"""
        filename = filedialog.askopenfilename(
            title="Chon file PowerPoint",
            filetypes=[
                ("PowerPoint files", "*.pptx"),
                ("All files", "*.*")
            ]
        )
        if filename:
            self.file_path.set(filename)
            self.update_status(f"Da chon: {os.path.basename(filename)}")
    
    def update_status(self, message):
        """Cap nhat status bar"""
        self.status_label.config(text=message)
        self.root.update()
    
    def preview_changes(self):
        """Xem truoc thay doi"""
        if not self.file_path.get():
            messagebox.showwarning("Canh bao", "Vui long chon file PowerPoint!")
            return
        
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        
        if "hinh anh" in current_tab.lower():
            self.preview_image_changes()
        else:
            self.preview_text_changes()
    
    def preview_image_changes(self):
        """Preview xoa hinh anh"""
        try:
            self.update_status("Dang phan tich hinh anh...")
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
            
            self.show_preview_window("Hinh anh se xoa", images_to_delete, total_images, "image")
            self.update_status("San sang")
            
        except Exception as e:
            messagebox.showerror("Loi", f"Khong the doc file:\n{str(e)}")
            self.update_status("Loi!")
    
    def preview_text_changes(self):
        """Preview loc text"""
        try:
            self.update_status("Dang phan tich text...")
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
            
            self.show_preview_window("Text se thay doi", changes, total_textboxes, "text")
            self.update_status("San sang")
            
        except Exception as e:
            messagebox.showerror("Loi", f"Khong the doc file:\n{str(e)}")
            self.update_status("Loi!")
    
    def show_preview_window(self, title, items, total, item_type):
        """Hien thi cua so preview"""
        preview_window = tk.Toplevel(self.root)
        preview_window.title(f"Preview - {title}")
        preview_window.geometry("700x550")
        
        # Header
        if item_type == "image":
            header_text = f"Tim thay {len(items)} hinh anh se xoa (Tong: {total})"
        else:
            header_text = f"Tim thay {len(items)} textbox se thay doi (Tong: {total})"
        
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
            text="Dong",
            command=preview_window.destroy,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            padx=30,
            pady=5
        )
        close_btn.pack(pady=10)
    
    def show_image_preview_content(self, parent, items):
        """Hien thi preview cho hinh anh"""
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
            listbox.insert(tk.END, "Khong tim thay hinh anh nao phu hop!")
    
    def show_text_preview_content(self, parent, items):
        """Hien thi preview cho text"""
        text_widget = scrolledtext.ScrolledText(parent, font=("Courier", 9), wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        if items:
            for idx, item in enumerate(items, 1):
                status = "[XOA TEXTBOX]" if item['deleted'] else "[CAP NHAT]"
                text_widget.insert(tk.END, f"\n{'='*70}\n")
                text_widget.insert(tk.END, f"{idx}. Slide {item['slide']} - {item['name']} {status}\n")
                text_widget.insert(tk.END, f"{'='*70}\n")
                text_widget.insert(tk.END, f"Truoc:\n{item['original']}\n\n")
                text_widget.insert(tk.END, f"Sau:\n{item['new'] if item['new'] else '[Rong - se xoa]'}\n")
        else:
            text_widget.insert(tk.END, "Khong tim thay text nao can thay doi!")
        
        text_widget.config(state=tk.DISABLED)
    
    def process_file(self):
        """Xu ly file"""
        if not self.file_path.get():
            messagebox.showwarning("Canh bao", "Vui long chon file PowerPoint!")
            return
        
        current_tab = self.notebook.tab(self.notebook.select(), "text")
        
        if "hinh anh" in current_tab.lower():
            self.process_images()
        else:
            self.process_text()
    
    def process_images(self):
        """Xu ly xoa hinh anh"""
        mode_text = {
            "and": "CA width VA height khop",
            "or": "width HOAC height khop",
            "width_only": "chi width khop",
            "height_only": "chi height khop"
        }
        
        confirm_msg = f"""Xoa hinh anh voi cai dat:

Width: {self.img_width.get()} inch
Height: {self.img_height.get()} inch
Che do: {mode_text[self.img_mode.get()]}

Tiep tuc?"""
        
        if not messagebox.askyesno("Xac nhan", confirm_msg):
            return
        
        try:
            file_path = self.file_path.get()
            
            if self.auto_backup.get():
                self.update_status("Dang backup...")
                backup_path = self.create_backup(file_path)
            
            self.update_status("Dang xu ly...")
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
            
            self.update_status("Dang luu...")
            prs.save(file_path)
            
            messagebox.showinfo(
                "Hoan tat!",
                f"Da xoa hinh anh thanh cong!\n\n"
                f"Tong: {total_images}\n"
                f"Da xoa: {deleted_count}\n"
                f"Con lai: {total_images - deleted_count}"
            )
            
            self.update_status("Hoan tat!")
            
        except Exception as e:
            messagebox.showerror("Loi", f"Khong the xu ly:\n{str(e)}")
            self.update_status("Loi!")
    
    def process_text(self):
        """Xu ly loc text"""
        mode_names = {
            "keep_vietnamese": "Giu tieng Viet - Xoa tieng Anh",
            "keep_english": "Giu tieng Anh - Xoa tieng Viet",
            "delete_all": "Xoa tat ca text",
            "custom": "Pattern tuy chinh"
        }
        
        mode = self.text_mode.get()
        mode_name = mode_names.get(mode, mode)
        
        confirm_msg = f"""Loc text voi che do:

{mode_name}

Xoa textbox rong: {'Co' if self.delete_empty_shapes.get() else 'Khong'}

Tiep tuc?"""
        
        if not messagebox.askyesno("Xac nhan", confirm_msg):
            return
        
        try:
            file_path = self.file_path.get()
            
            if self.auto_backup.get():
                self.update_status("Dang backup...")
                backup_path = self.create_backup(file_path)
            
            self.update_status("Dang xu ly...")
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
            
            self.update_status("Dang luu...")
            prs.save(file_path)
            
            messagebox.showinfo(
                "Hoan tat!",
                f"Da loc text thanh cong!\n\n"
                f"Tong textbox: {total_textboxes}\n"
                f"Da cap nhat: {modified_count}\n"
                f"Da xoa: {deleted_count}"
            )
            
            self.update_status("Hoan tat!")
            
        except Exception as e:
            messagebox.showerror("Loi", f"Khong the xu ly:\n{str(e)}")
            self.update_status("Loi!")
    
    def check_image_match(self, width_inches, height_inches):
        """Kiem tra hinh anh co khop khong"""
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
        """Kiem tra shape co text khong"""
        try:
            return shape.has_text_frame and shape.text_frame.text.strip()
        except:
            return False
    
    def get_shape_text(self, shape):
        """Lay text tu shape"""
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
        """Loc text theo che do"""
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
        """Giu dong co Unicode (tieng Viet)"""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            if self.has_unicode_char(line):
                result.append(line)
        
        return '\n'.join(result)
    
    def keep_ascii_lines(self, text):
        """Giu dong chi ASCII (tieng Anh)"""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            if not self.has_unicode_char(line) and line.strip():
                result.append(line)
        
        return '\n'.join(result)
    
    def has_unicode_char(self, line):
        """Kiem tra co ky tu Unicode khong"""
        if not line.strip():
            return False
        
        for char in line:
            if ord(char) > 127:
                return True
        
        return False
    
    def filter_by_pattern(self, text):
        """Loc theo regex pattern"""
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
            messagebox.showwarning("Loi pattern", f"Pattern khong hop le:\n{str(e)}")
            return text
    
    def create_backup(self, file_path):
        """Tao backup file"""
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
