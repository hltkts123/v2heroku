#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerPoint Cleaner Tool - Batch Processing
Cong cu don dep PowerPoint: Xu ly NHIEU file cung luc
Ho tro xu ly textbox long nhau (nested/group shapes)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
import os
import shutil
from datetime import datetime
from threading import Thread
import queue

class PowerPointCleanerBatch:
    def __init__(self, root):
        self.root = root
        self.root.title("PowerPoint Cleaner - Xu ly nhieu file")
        self.root.geometry("950x730")
        self.root.resizable(True, True)
        self.root.minsize(900, 700)
        
        # Variables
        self.file_paths = []
        self.auto_backup = tk.BooleanVar(value=True)
        self.processing = False
        self.result_queue = queue.Queue()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Tao giao dien"""
        
        # Header - compact
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=50)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="PowerPoint Cleaner - Batch",
            font=("Arial", 16, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=3)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Giu nguyen dinh dang text",
            font=("Arial", 8),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # Main content - NO SCROLLBAR
        main_frame = tk.Frame(self.root, padx=15, pady=10)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # File selection - compact
        file_frame = tk.LabelFrame(main_frame, text="1. Chon files", font=("Arial", 10, "bold"), padx=8, pady=5)
        file_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Buttons
        btn_frame = tk.Frame(file_frame)
        btn_frame.pack(fill=tk.X, pady=(0, 5))
        
        add_files_btn = tk.Button(
            btn_frame,
            text="+ Them files",
            command=self.add_files,
            bg="#3498db",
            fg="white",
            font=("Arial", 8),
            cursor="hand2",
            relief=tk.FLAT,
            padx=10,
            pady=2
        )
        add_files_btn.pack(side=tk.LEFT, padx=(0, 3))
        
        add_folder_btn = tk.Button(
            btn_frame,
            text="+ Them folder",
            command=self.add_folder,
            bg="#3498db",
            fg="white",
            font=("Arial", 8),
            cursor="hand2",
            relief=tk.FLAT,
            padx=10,
            pady=2
        )
        add_folder_btn.pack(side=tk.LEFT, padx=3)
        
        clear_btn = tk.Button(
            btn_frame,
            text="Xoa tat ca",
            command=self.clear_files,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 8),
            cursor="hand2",
            relief=tk.FLAT,
            padx=10,
            pady=2
        )
        clear_btn.pack(side=tk.RIGHT)
        
        # File list - compact
        list_frame = tk.Frame(file_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox = tk.Listbox(
            list_frame,
            font=("Courier", 8),
            yscrollcommand=scrollbar.set,
            selectmode=tk.EXTENDED,
            height=6
        )
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.file_listbox.yview)
        
        # Right-click menu
        self.context_menu = tk.Menu(self.file_listbox, tearoff=0)
        self.context_menu.add_command(label="Xoa file da chon", command=self.remove_selected)
        self.file_listbox.bind("<Button-3>", self.show_context_menu)
        
        self.file_count_label = tk.Label(file_frame, text="Chua chon file nao", font=("Arial", 8), fg="gray")
        self.file_count_label.pack(pady=(3, 0))
        
        # Processing mode - compact
        mode_frame = tk.LabelFrame(main_frame, text="2. Chuc nang", font=("Arial", 10, "bold"), padx=8, pady=5)
        mode_frame.pack(fill=tk.X, pady=(0, 5))
        
        self.process_mode = tk.StringVar(value="both")
        
        modes = [
            ("CA HAI: Xoa anh + Loc text", "both"),
            ("CHI xoa hinh anh", "image_only"),
            ("CHI loc text", "text_only")
        ]
        
        for text, value in modes:
            tk.Radiobutton(mode_frame, text=text, variable=self.process_mode, value=value,
                          font=("Arial", 9)).pack(anchor="w", pady=1)
        
        # Notebook (Tabs) - compact
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 5))
        
        # Tab 1: Xoa hinh anh
        self.create_image_tab()
        
        # Tab 2: Loc text
        self.create_text_tab()
        
        # Options - compact in 1 row with progress
        bottom_frame = tk.Frame(main_frame)
        bottom_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Left: Options
        options_frame = tk.LabelFrame(bottom_frame, text="Tuy chon", font=("Arial", 10, "bold"), padx=8, pady=5)
        options_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        backup_cb = tk.Checkbutton(
            options_frame,
            text="Tu dong backup",
            variable=self.auto_backup,
            font=("Arial", 8)
        )
        backup_cb.pack(anchor="w")
        
        # Right: Progress
        self.progress_frame = tk.LabelFrame(bottom_frame, text="Tien trinh", font=("Arial", 10, "bold"), padx=8, pady=5)
        self.progress_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, mode='determinate')
        self.progress_bar.pack(fill=tk.X, pady=(0, 3))
        
        self.progress_label = tk.Label(self.progress_frame, text="Chua bat dau", font=("Arial", 8))
        self.progress_label.pack()
        
        # Action button - prominent
        self.process_btn = tk.Button(
            main_frame,
            text="? XU LY TAT CA FILES",
            command=self.process_all_files,
            bg="#27ae60",
            fg="white",
            font=("Arial", 13, "bold"),
            cursor="hand2",
            relief=tk.RAISED,
            pady=12,
            borderwidth=2
        )
        self.process_btn.pack(fill=tk.X, pady=(5, 0))
        
        # Status bar - compact
        self.status_label = tk.Label(
            self.root,
            text="San sang - Them files de bat dau",
            font=("Arial", 8),
            bg="#ecf0f1",
            fg="#2c3e50",
            anchor="w",
            padx=10,
            pady=3
        )
        self.status_label.pack(side=tk.BOTTOM, fill=tk.X)
    
    def create_image_tab(self):
        """Tab xoa hinh anh - Kich thuoc va Che do cung 1 hang"""
        self.image_frame = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(self.image_frame, text="Xoa anh")
        
        # Variables
        self.img_width = tk.DoubleVar(value=1.6)
        self.img_height = tk.DoubleVar(value=1.6)
        self.img_tolerance = tk.DoubleVar(value=0.01)
        self.img_mode = tk.StringVar(value="and")
        
        # Container for 2 columns
        container = tk.Frame(self.image_frame)
        container.pack(fill=tk.BOTH, expand=True)
        
        # LEFT: Kich thuoc
        left_frame = tk.LabelFrame(container, text="Kich thuoc (inch)", font=("Arial", 10, "bold"), padx=6, pady=4)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 4))
        
        # Width
        width_frame = tk.Frame(left_frame)
        width_frame.pack(fill=tk.X, pady=2)
        tk.Label(width_frame, text="Rong:", font=("Arial", 9), width=8, anchor="w").pack(side=tk.LEFT)
        tk.Spinbox(width_frame, from_=0.1, to=20.0, increment=0.1, textvariable=self.img_width, 
                   font=("Arial", 9), width=6).pack(side=tk.LEFT, padx=2)
        
        # Height
        height_frame = tk.Frame(left_frame)
        height_frame.pack(fill=tk.X, pady=2)
        tk.Label(height_frame, text="Cao:", font=("Arial", 9), width=8, anchor="w").pack(side=tk.LEFT)
        tk.Spinbox(height_frame, from_=0.1, to=20.0, increment=0.1, textvariable=self.img_height, 
                   font=("Arial", 9), width=6).pack(side=tk.LEFT, padx=2)
        
        # Tolerance
        tol_frame = tk.Frame(left_frame)
        tol_frame.pack(fill=tk.X, pady=2)
        tk.Label(tol_frame, text="Dung sai:", font=("Arial", 9), width=8, anchor="w").pack(side=tk.LEFT)
        tk.Spinbox(tol_frame, from_=0.001, to=0.5, increment=0.01, textvariable=self.img_tolerance, 
                   font=("Arial", 9), width=6).pack(side=tk.LEFT, padx=2)
        
        # RIGHT: Che do
        right_frame = tk.LabelFrame(container, text="Che do", font=("Arial", 10, "bold"), padx=6, pady=4)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        modes = [
            ("CA width VA height", "and"),
            ("Width HOAC height", "or"),
            ("Chi width", "width_only"),
            ("Chi height", "height_only")
        ]
        
        for text, value in modes:
            tk.Radiobutton(right_frame, text=text, variable=self.img_mode, value=value, 
                          font=("Arial", 9)).pack(anchor="w", pady=1)
    
    def create_text_tab(self):
        """Tab loc text - compact"""
        self.text_frame = ttk.Frame(self.notebook, padding=8)
        self.notebook.add(self.text_frame, text="Loc text")
        
        # Variables
        self.text_mode = tk.StringVar(value="delete_english")
        self.delete_empty_shapes = tk.BooleanVar(value=True)
        
        # Info
        info_label = tk.Label(
            self.text_frame,
            text="? GIU NGUYEN dinh dang: font, size, color, bold, italic...\n? XOA CHI tieng Anh - GIU tat ca ngon ngu khac",
            font=("Arial", 9, "bold"),
            fg="#16a085",
            justify="left",
            bg="#e8f8f5",
            padx=8,
            pady=6
        )
        info_label.pack(fill=tk.X, pady=(0, 6))
        
        # Mode selection - compact
        mode_frame = tk.LabelFrame(self.text_frame, text="Che do", font=("Arial", 9, "bold"), padx=8, pady=5)
        mode_frame.pack(fill=tk.X, pady=(0, 5))
        
        modes = [
            ("Xoa tieng Anh - Giu Viet/Trung/Nhat/Han", "delete_english"),
            ("Chi giu tieng Anh", "keep_english"),
            ("Xoa tat ca", "delete_all")
        ]
        
        for text, value in modes:
            tk.Radiobutton(mode_frame, text=text, variable=self.text_mode, value=value,
                          font=("Arial", 8)).pack(anchor="w", pady=1)
        
        # Options
        tk.Checkbutton(self.text_frame, text="Xoa textbox rong", 
                      variable=self.delete_empty_shapes, font=("Arial", 8)).pack(anchor="w", pady=3)
    
    def add_files(self):
        """Them files"""
        filenames = filedialog.askopenfilenames(
            title="Chon cac file PowerPoint",
            filetypes=[("PowerPoint files", "*.pptx"), ("All files", "*.*")]
        )
        if filenames:
            for filename in filenames:
                if filename not in self.file_paths:
                    self.file_paths.append(filename)
                    self.file_listbox.insert(tk.END, os.path.basename(filename))
            self.update_file_count()
    
    def add_folder(self):
        """Them tat ca file .pptx trong folder"""
        folder = filedialog.askdirectory(title="Chon folder chua cac file PowerPoint")
        if folder:
            added = 0
            for file in os.listdir(folder):
                if file.endswith('.pptx') and not file.startswith('~'):
                    full_path = os.path.join(folder, file)
                    if full_path not in self.file_paths:
                        self.file_paths.append(full_path)
                        self.file_listbox.insert(tk.END, file)
                        added += 1
            
            if added > 0:
                self.update_file_count()
                messagebox.showinfo("Thanh cong", f"Da them {added} file tu folder!")
            else:
                messagebox.showinfo("Thong bao", "Khong tim thay file .pptx nao trong folder!")
    
    def clear_files(self):
        """Xoa tat ca files"""
        if self.file_paths and messagebox.askyesno("Xac nhan", "Xoa tat ca files da chon?"):
            self.file_paths.clear()
            self.file_listbox.delete(0, tk.END)
            self.update_file_count()
    
    def remove_selected(self):
        """Xoa files da chon"""
        selected = self.file_listbox.curselection()
        if selected:
            for index in reversed(selected):
                self.file_listbox.delete(index)
                del self.file_paths[index]
            self.update_file_count()
    
    def show_context_menu(self, event):
        """Hien context menu"""
        if self.file_listbox.curselection():
            self.context_menu.post(event.x_root, event.y_root)
    
    def update_file_count(self):
        """Cap nhat so luong files"""
        count = len(self.file_paths)
        if count == 0:
            self.file_count_label.config(text="Chua chon file nao", fg="gray")
            self.status_label.config(text="San sang - Them files de bat dau")
        else:
            self.file_count_label.config(text=f"Da chon: {count} file", fg="green")
            self.status_label.config(text=f"San sang xu ly {count} file")
    
    def process_all_files(self):
        """Xu ly tat ca files"""
        if not self.file_paths:
            messagebox.showwarning("Canh bao", "Vui long chon it nhat 1 file!")
            return
        
        if self.processing:
            messagebox.showwarning("Canh bao", "Dang xu ly, vui long doi!")
            return
        
        # Confirm
        mode = self.process_mode.get()
        mode_text = {
            "both": "XOA HINH ANH VA LOC TEXT",
            "image_only": "CHI XOA HINH ANH",
            "text_only": "CHI LOC TEXT"
        }
        
        if not messagebox.askyesno("Xac nhan", 
            f"Xu ly {len(self.file_paths)} file voi che do:\n\n"
            f"{mode_text[mode]}\n\n"
            "Thao tac nay khong the hoan tac!"):
            return
        
        # Start processing
        self.processing = True
        self.process_btn.config(state=tk.DISABLED, text="Dang xu ly...")
        
        thread = Thread(target=self.process_files_thread, daemon=True)
        thread.start()
        
        self.root.after(100, self.check_progress)
    
    def process_files_thread(self):
        """Xu ly files trong thread rieng"""
        total = len(self.file_paths)
        results = []
        mode = self.process_mode.get()
        
        for idx, file_path in enumerate(self.file_paths, 1):
            try:
                progress = (idx / total) * 100
                filename = os.path.basename(file_path)
                self.result_queue.put(('progress', progress, f"Dang xu ly ({idx}/{total}): {filename}"))
                
                # Backup
                if self.auto_backup.get():
                    self.create_backup(file_path)
                
                # Process
                result = self.process_single_file(file_path, mode)
                results.append({'file': filename, 'status': 'success', 'data': result})
                
            except Exception as e:
                results.append({'file': os.path.basename(file_path), 'status': 'error', 'data': str(e)})
        
        self.result_queue.put(('done', results))
    
    def process_single_file(self, file_path, mode):
        """Xu ly 1 file theo mode"""
        prs = Presentation(file_path)
        result = {}
        
        if mode in ["both", "image_only"]:
            img_result = self.process_images(prs)
            result.update(img_result)
        
        if mode in ["both", "text_only"]:
            txt_result = self.process_texts(prs)
            result.update(txt_result)
        
        prs.save(file_path)
        return result
    
    def process_images(self, prs):
        """Xu ly xoa hinh anh"""
        deleted_count = 0
        total_images = 0
        
        for slide in prs.slides:
            shapes_to_delete = []
            
            for shape in slide.shapes:
                if shape.shape_type == MSO_SHAPE_TYPE.PICTURE:
                    total_images += 1
                    width_inches = shape.width / 914400
                    height_inches = shape.height / 914400
                    
                    if self.check_image_match(width_inches, height_inches):
                        shapes_to_delete.append(shape)
            
            for shape in shapes_to_delete:
                sp = shape.element
                sp.getparent().remove(sp)
                deleted_count += 1
        
        return {'total_images': total_images, 'deleted_images': deleted_count}
    
    def process_texts(self, prs):
        """Xu ly loc text - HO TRO DE QUY - XOA CHI TIENG ANH"""
        modified_count = 0
        deleted_count = 0
        total_textboxes = 0
        
        for slide in prs.slides:
            # Collect all changes first
            changes = []
            self.collect_text_changes(slide.shapes, changes)
            
            # Count total textboxes
            total_textboxes += len(changes)
            
            # Apply text updates - PRESERVE FORMATTING
            for change in changes:
                if not change['delete']:
                    self.filter_text_preserve_format(change['shape'])
                    modified_count += 1
            
            # Delete empty shapes
            shapes_to_delete = [c['shape'] for c in changes if c['delete']]
            for shape in shapes_to_delete:
                try:
                    sp = shape.element
                    sp.getparent().remove(sp)
                    deleted_count += 1
                except:
                    pass
        
        return {'total_textboxes': total_textboxes, 'modified_text': modified_count, 'deleted_text': deleted_count}
    
    def collect_text_changes(self, shapes, changes):
        """Thu thap thay doi text - DE QUY xu ly group"""
        for shape in shapes:
            try:
                # Xu ly group de quy
                if shape.shape_type == MSO_SHAPE_TYPE.GROUP:
                    self.collect_text_changes(shape.shapes, changes)
                    continue
                
                # Chi xu ly shapes co text
                if self.has_text(shape):
                    original_text = self.get_shape_text(shape)
                    new_text = self.filter_text(original_text)
                    
                    if new_text != original_text:
                        delete_it = len(new_text.strip()) == 0 and self.delete_empty_shapes.get()
                        changes.append({
                            'shape': shape,
                            'original': original_text,
                            'new_text': new_text,
                            'delete': delete_it
                        })
            except Exception as e:
                # Skip shapes that cause errors
                continue
    
    def check_progress(self):
        """Kiem tra tien trinh"""
        try:
            while True:
                msg = self.result_queue.get_nowait()
                
                if msg[0] == 'progress':
                    _, progress, text = msg
                    self.progress_bar['value'] = progress
                    self.progress_label.config(text=text)
                    self.status_label.config(text=text)
                    
                elif msg[0] == 'done':
                    _, results = msg
                    self.processing = False
                    self.process_btn.config(state=tk.NORMAL, text="? XU LY TAT CA FILES")
                    self.progress_bar['value'] = 100
                    self.progress_label.config(text="Hoan tat!")
                    self.show_results(results)
                    return
        except queue.Empty:
            pass
        
        if self.processing:
            self.root.after(100, self.check_progress)
    
    def show_results(self, results):
        """Hien thi ket qua"""
        result_window = tk.Toplevel(self.root)
        result_window.title("Ket qua xu ly")
        result_window.geometry("700x500")
        
        # Header
        success_count = sum(1 for r in results if r['status'] == 'success')
        error_count = len(results) - success_count
        
        header = tk.Label(
            result_window,
            text=f"Hoan tat! Thanh cong: {success_count} | Loi: {error_count}",
            font=("Arial", 11, "bold"),
            bg="#27ae60" if error_count == 0 else "#f39c12",
            fg="white",
            pady=8
        )
        header.pack(fill=tk.X)
        
        # Content
        content_frame = tk.Frame(result_window, padx=10, pady=10)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = scrolledtext.ScrolledText(content_frame, font=("Courier", 8), wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        mode = self.process_mode.get()
        
        for idx, result in enumerate(results, 1):
            text_widget.insert(tk.END, f"\n{'='*60}\n")
            text_widget.insert(tk.END, f"{idx}. {result['file']}\n")
            text_widget.insert(tk.END, f"{'='*60}\n")
            
            if result['status'] == 'success':
                text_widget.insert(tk.END, "Trang thai: THANH CONG\n\n")
                data = result['data']
                
                if mode in ["both", "image_only"]:
                    text_widget.insert(tk.END, "[HINH ANH]\n")
                    text_widget.insert(tk.END, f"  Tong: {data.get('total_images', 0)}\n")
                    text_widget.insert(tk.END, f"  Da xoa: {data.get('deleted_images', 0)}\n\n")
                
                if mode in ["both", "text_only"]:
                    text_widget.insert(tk.END, "[TEXT]\n")
                    text_widget.insert(tk.END, f"  Tong textbox: {data.get('total_textboxes', 0)}\n")
                    text_widget.insert(tk.END, f"  Da cap nhat: {data.get('modified_text', 0)}\n")
                    text_widget.insert(tk.END, f"  Da xoa: {data.get('deleted_text', 0)}\n")
            else:
                text_widget.insert(tk.END, f"Trang thai: LOI\n")
                text_widget.insert(tk.END, f"Chi tiet: {result['data']}\n")
        
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(
            result_window,
            text="Dong",
            command=result_window.destroy,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 9),
            padx=25,
            pady=4
        )
        close_btn.pack(pady=8)
    
    # Helper methods
    def check_image_match(self, width_inches, height_inches):
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
        return False
    
    def has_text(self, shape):
        try:
            return shape.has_text_frame and shape.text_frame.text.strip()
        except:
            return False
    
    def get_shape_text(self, shape):
        try:
            return shape.text_frame.text
        except:
            return ""
    
    def set_shape_text(self, shape, text):
        try:
            shape.text_frame.text = text
        except:
            pass
    
    def filter_text(self, text):
        """Loc text theo mode - CHINH XAC chi xoa tieng Anh"""
        mode = self.text_mode.get()
        
        if mode == "delete_english":
            return self.delete_english_lines(text)
        elif mode == "keep_english":
            return self.keep_ascii_lines(text)
        elif mode == "delete_all":
            return ""
        return text
    
    def delete_english_lines(self, text):
        """XOA dong CHI co tieng Anh (pure ASCII) - GIU dong co Unicode (Viet/Trung/Nhat/Han)"""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            # Dong rong -> giu
            if not line.strip():
                result.append(line)
                continue
            
            # Dong co it nhat 1 ky tu Unicode -> GIU (Viet, Trung, Nhat, Han, etc.)
            if self.has_unicode_char(line):
                result.append(line)
            # Dong PURE ASCII -> XOA (tieng Anh)
            # Khong append vao result
        
        return '\n'.join(result)
    
    def keep_ascii_lines(self, text):
        """Chi giu dong ASCII (tieng Anh) - Xoa dong co Unicode"""
        lines = text.split('\n')
        result = []
        
        for line in lines:
            if not line.strip():
                continue
            # Chi giu dong khong co ky tu Unicode
            if not self.has_unicode_char(line):
                result.append(line)
        
        return '\n'.join(result)
    
    def has_unicode_char(self, line):
        """Kiem tra co ky tu Unicode khong (>127: Viet, Trung, Nhat, Han, etc.)"""
        if not line.strip():
            return False
        return any(ord(char) > 127 for char in line)
    
    def create_backup(self, file_path):
        file_dir = os.path.dirname(file_path)
        file_name = os.path.basename(file_path)
        name_without_ext = os.path.splitext(file_name)[0]
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"{name_without_ext}_backup_{timestamp}.pptx"
        backup_path = os.path.join(file_dir, backup_name)
        
        shutil.copy2(file_path, backup_path)
        return backup_path


    
    def filter_text_preserve_format(self, shape):
        """LOC text NHUNG GIU NGUYEN dinh dang (font, size, color, bold, italic...)"""
        mode = self.text_mode.get()
        
        try:
            if not shape.has_text_frame:
                return
            
            text_frame = shape.text_frame
            
            # Neu delete_all -> xoa tat ca bang cach an toan
            if mode == "delete_all":
                text_frame.clear()
                return
            
            # Duyet qua tung paragraph
            for paragraph in text_frame.paragraphs:
                # Thu thap text moi cho paragraph nay
                new_runs = []
                
                for run in paragraph.runs:
                    run_text = run.text
                    
                    # Kiem tra xem run co nen giu lai khong
                    should_keep = False
                    
                    if mode == "delete_english":
                        # Giu run neu co Unicode (khong phai pure ASCII)
                        should_keep = not self.is_pure_ascii_text(run_text)
                    
                    elif mode == "keep_english":
                        # Giu run neu la pure ASCII
                        should_keep = not self.has_unicode_char(run_text)
                    
                    if should_keep:
                        new_runs.append({
                            'text': run_text,
                            'font': run.font
                        })
                
                # Xoa tat ca runs cu
                for _ in range(len(paragraph.runs)):
                    paragraph.runs[0]._element.getparent().remove(paragraph.runs[0]._element)
                
                # Them lai runs moi voi format goc
                for run_data in new_runs:
                    new_run = paragraph.add_run()
                    new_run.text = run_data['text']
                    # Copy font properties
                    try:
                        new_run.font.name = run_data['font'].name
                        new_run.font.size = run_data['font'].size
                        new_run.font.bold = run_data['font'].bold
                        new_run.font.italic = run_data['font'].italic
                        new_run.font.underline = run_data['font'].underline
                        if run_data['font'].color.type:
                            new_run.font.color.rgb = run_data['font'].color.rgb
                    except:
                        pass
        
        except Exception as e:
            # Fallback: dung phuong phap don gian hon
            try:
                original_text = self.get_shape_text(shape)
                new_text = self.filter_text(original_text)
                shape.text_frame.text = new_text
            except:
                pass
    
    def is_pure_ascii_text(self, text):
        """Kiem tra text co phai pure ASCII khong (chi 0-127)"""
        if not text.strip():
            return False
        return all(ord(char) <= 127 for char in text)

def main():
    root = tk.Tk()
    app = PowerPointCleanerBatch(root)
    root.mainloop()


if __name__ == "__main__":
    main()
