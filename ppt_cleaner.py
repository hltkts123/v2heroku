#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PowerPoint Cleaner Tool - Single File Processing
Cong cu don dep PowerPoint: Xu ly 1 file
Ho tro xu ly textbox long nhau (nested/group shapes)
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE
import os
import shutil
from datetime import datetime

class PowerPointCleaner:
    def __init__(self, root):
        self.root = root
        self.root.title("PowerPoint Cleaner")
        self.root.geometry("1050x980")
        self.root.resizable(True, True)
        self.root.minsize(950, 880)
        
        # Variables
        self.file_path = None
        self.auto_backup = tk.BooleanVar(value=True)
        
        self.create_widgets()
        
    def create_widgets(self):
        """Tao giao dien"""
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=70)
        header_frame.pack(fill=tk.X)
        
        title_label = tk.Label(
            header_frame,
            text="PowerPoint Cleaner",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=5)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Xu ly 1 file - Ho tro textbox long nhau",
            font=("Arial", 9),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # Main content with scrollbar
        main_container = tk.Frame(self.root)
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Canvas for scrolling
        canvas = tk.Canvas(main_container)
        scrollbar = tk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        
        main_frame = tk.Frame(canvas, padx=15, pady=10)
        
        # Configure scroll region
        main_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        canvas.create_window((0, 0), window=main_frame, anchor="nw", width=canvas.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Mouse wheel scrolling
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        
        # Update canvas width on window resize
        def _on_canvas_configure(event):
            canvas.itemconfig(canvas.find_withtag("all")[0], width=event.width)
        canvas.bind("<Configure>", _on_canvas_configure)
        
        # File selection
        file_frame = tk.LabelFrame(main_frame, text="1. Chon file PowerPoint", font=("Arial", 11, "bold"), padx=10, pady=10)
        file_frame.pack(fill=tk.X, pady=(0, 15))
        
        btn_frame = tk.Frame(file_frame)
        btn_frame.pack(fill=tk.X)
        
        self.file_label = tk.Label(
            btn_frame,
            text="Chua chon file",
            font=("Arial", 10),
            fg="gray",
            anchor="w",
            width=50
        )
        self.file_label.pack(side=tk.LEFT, padx=5)
        
        browse_btn = tk.Button(
            btn_frame,
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
        
        # Processing mode
        mode_frame = tk.LabelFrame(main_frame, text="2. Chon chuc nang xu ly", font=("Arial", 11, "bold"), padx=10, pady=10)
        mode_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.process_mode = tk.StringVar(value="both")
        
        modes = [
            ("Xu ly CA HAI: Xoa hinh anh VA loc text", "both"),
            ("CHI xoa hinh anh", "image_only"),
            ("CHI loc text", "text_only")
        ]
        
        for text, value in modes:
            tk.Radiobutton(mode_frame, text=text, variable=self.process_mode, value=value,
                          font=("Arial", 10), command=self.update_tabs_visibility).pack(anchor="w", pady=2)
        
        # Notebook (Tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Tab 1: Xoa hinh anh
        self.create_image_tab()
        
        # Tab 2: Loc text
        self.create_text_tab()
        
        # Options
        options_frame = tk.LabelFrame(main_frame, text="Tuy chon", font=("Arial", 11, "bold"), padx=10, pady=10)
        options_frame.pack(fill=tk.X, pady=(0, 15))
        
        backup_cb = tk.Checkbutton(
            options_frame,
            text="Tu dong backup truoc khi xu ly",
            variable=self.auto_backup,
            font=("Arial", 10)
        )
        backup_cb.pack(anchor="w")
        
        # Action buttons
        button_frame = tk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.process_btn = tk.Button(
            button_frame,
            text="? XU LY FILE",
            command=self.process_file,
            bg="#27ae60",
            fg="white",
            font=("Arial", 13, "bold"),
            cursor="hand2",
            relief=tk.RAISED,
            padx=40,
            pady=12,
            borderwidth=3
        )
        self.process_btn.pack(fill=tk.X, ipady=5)
        
        # Status bar
        self.status_label = tk.Label(
            self.root,
            text="San sang - Chon file de bat dau",
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
        self.image_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.image_frame, text=" Xoa hinh anh")
        
        # Variables
        self.img_width = tk.DoubleVar(value=1.6)
        self.img_height = tk.DoubleVar(value=1.6)
        self.img_tolerance = tk.DoubleVar(value=0.01)
        self.img_mode = tk.StringVar(value="and")
        
        # Size settings
        size_frame = tk.LabelFrame(self.image_frame, text="Kich thuoc (inch)", font=("Arial", 10, "bold"), padx=10, pady=10)
        size_frame.pack(fill=tk.X, padx=20, pady=10)
        
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
        mode_frame = tk.LabelFrame(self.image_frame, text="Che do so khop", font=("Arial", 10, "bold"), padx=10, pady=5)
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
        self.text_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.text_frame, text=" Loc text")
        
        # Variables
        self.text_mode = tk.StringVar(value="keep_vietnamese")
        self.delete_empty_shapes = tk.BooleanVar(value=True)
        
        # Info
        info_label = tk.Label(
            self.text_frame,
            text="XU LY DE QUY: Tu dong xu ly textbox trong groups va nested shapes",
            font=("Arial", 9, "italic"),
            fg="#16a085"
        )
        info_label.pack(pady=5)
        
        # Mode selection
        mode_frame = tk.LabelFrame(self.text_frame, text="Che do loc", font=("Arial", 10, "bold"), padx=10, pady=10)
        mode_frame.pack(fill=tk.X, padx=20, pady=10)
        
        modes = [
            ("Giu tieng Viet - Xoa tieng Anh", "keep_vietnamese"),
            ("Chi giu tieng Anh - Xoa tieng Viet", "keep_english"),
            ("Xoa tat ca text", "delete_all")
        ]
        
        for text, value in modes:
            tk.Radiobutton(mode_frame, text=text, variable=self.text_mode, value=value,
                          font=("Arial", 9)).pack(anchor="w", pady=2)
        
        # Options
        opt_frame = tk.LabelFrame(self.text_frame, text="Tuy chon", font=("Arial", 10, "bold"), padx=10, pady=10)
        opt_frame.pack(fill=tk.X, padx=20)
        
        tk.Checkbutton(opt_frame, text="Xoa textbox rong sau khi loc", 
                      variable=self.delete_empty_shapes, font=("Arial", 9)).pack(anchor="w")
    
    def update_tabs_visibility(self):
        """Cap nhat hien thi tabs theo mode"""
        pass
    
    def browse_file(self):
        """Chon file"""
        filename = filedialog.askopenfilename(
            title="Chon file PowerPoint",
            filetypes=[("PowerPoint files", "*.pptx"), ("All files", "*.*")]
        )
        if filename:
            self.file_path = filename
            self.file_label.config(text=os.path.basename(filename), fg="green")
            self.status_label.config(text=f"Da chon: {os.path.basename(filename)}")
    
    def process_file(self):
        """Xu ly file"""
        if not self.file_path:
            messagebox.showwarning("Canh bao", "Vui long chon file truoc!")
            return
        
        if not os.path.exists(self.file_path):
            messagebox.showerror("Loi", "File khong ton tai!")
            return
        
        mode = self.process_mode.get()
        mode_text = {
            "both": "XOA HINH ANH VA LOC TEXT",
            "image_only": "CHI XOA HINH ANH",
            "text_only": "CHI LOC TEXT"
        }
        
        if not messagebox.askyesno("Xac nhan", 
            f"Xu ly file voi che do:\n\n{mode_text[mode]}\n\nThao tac nay khong the hoan tac!"):
            return
        
        try:
            # Backup
            if self.auto_backup.get():
                backup_path = self.create_backup(self.file_path)
                self.status_label.config(text=f"Da backup: {os.path.basename(backup_path)}")
            
            # Process
            self.status_label.config(text="Dang xu ly...")
            self.root.update()
            
            prs = Presentation(self.file_path)
            result = {}
            
            if mode in ["both", "image_only"]:
                img_result = self.process_images(prs)
                result.update(img_result)
            
            if mode in ["both", "text_only"]:
                txt_result = self.process_texts(prs)
                result.update(txt_result)
            
            prs.save(self.file_path)
            
            self.show_result(result, mode)
            self.status_label.config(text="Hoan tat!")
            
        except Exception as e:
            messagebox.showerror("Loi", f"Loi khi xu ly file:\n{str(e)}")
            self.status_label.config(text="Loi!")
    
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
        """Xu ly loc text - HO TRO DE QUY"""
        modified_count = 0
        deleted_count = 0
        total_textboxes = 0
        
        for slide in prs.slides:
            # Collect all changes first
            changes = []
            self.collect_text_changes(slide.shapes, changes)
            
            # Count total textboxes
            total_textboxes += len(changes)
            
            # Apply text updates first
            for change in changes:
                if not change['delete']:
                    self.set_shape_text(change['shape'], change['new_text'])
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
        elif mode == "width_only":
            return width_match
        elif mode == "height_only":
            return height_match
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
        mode = self.text_mode.get()
        
        if mode == "keep_vietnamese":
            return self.keep_unicode_lines(text)
        elif mode == "keep_english":
            return self.keep_ascii_lines(text)
        elif mode == "delete_all":
            return ""
        return text
    
    def keep_unicode_lines(self, text):
        """Giu dong co Unicode (tieng Viet)"""
        lines = text.split('\n')
        result = [line for line in lines if self.has_unicode_char(line)]
        return '\n'.join(result)
    
    def keep_ascii_lines(self, text):
        """Giu dong chi ASCII (tieng Anh)"""
        lines = text.split('\n')
        result = [line for line in lines if not self.has_unicode_char(line) and line.strip()]
        return '\n'.join(result)
    
    def has_unicode_char(self, line):
        """Kiem tra co ky tu Unicode khong"""
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
    
    def show_result(self, result, mode):
        """Hien thi ket qua"""
        result_window = tk.Toplevel(self.root)
        result_window.title("Ket qua xu ly")
        result_window.geometry("600x400")
        
        # Header
        header = tk.Label(
            result_window,
            text="Hoan tat!",
            font=("Arial", 14, "bold"),
            bg="#27ae60",
            fg="white",
            pady=10
        )
        header.pack(fill=tk.X)
        
        # Content
        content_frame = tk.Frame(result_window, padx=20, pady=20)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        text_widget = scrolledtext.ScrolledText(content_frame, font=("Courier", 10), wrap=tk.WORD)
        text_widget.pack(fill=tk.BOTH, expand=True)
        
        text_widget.insert(tk.END, f"File: {os.path.basename(self.file_path)}\n")
        text_widget.insert(tk.END, f"{'='*50}\n\n")
        
        if mode in ["both", "image_only"]:
            text_widget.insert(tk.END, "[HINH ANH]\n")
            text_widget.insert(tk.END, f"  Tong hinh: {result.get('total_images', 0)}\n")
            text_widget.insert(tk.END, f"  Da xoa: {result.get('deleted_images', 0)}\n\n")
        
        if mode in ["both", "text_only"]:
            text_widget.insert(tk.END, "[TEXT]\n")
            text_widget.insert(tk.END, f"  Tong textbox: {result.get('total_textboxes', 0)}\n")
            text_widget.insert(tk.END, f"  Da cap nhat: {result.get('modified_text', 0)}\n")
            text_widget.insert(tk.END, f"  Da xoa: {result.get('deleted_text', 0)}\n")
        
        text_widget.config(state=tk.DISABLED)
        
        # Close button
        close_btn = tk.Button(
            result_window,
            text="Dong",
            command=result_window.destroy,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10),
            padx=30,
            pady=5
        )
        close_btn.pack(pady=10)


def main():
    root = tk.Tk()
    app = PowerPointCleaner(root)
    root.mainloop()


if __name__ == "__main__":
    main()
