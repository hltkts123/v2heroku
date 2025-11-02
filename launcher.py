#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Launcher cho cac cong cu PowerPoint va Chu Han
"""

import tkinter as tk
from tkinter import ttk
import subprocess
import sys
from pathlib import Path


class ToolLauncher:
    """Launcher chinh cho tat ca cac cong cu"""
    
    def __init__(self, root):
        self.root = root
        self.root.title("Cong Cu Tien Ich")
        self.root.geometry("600x500")
        self.root.resizable(False, False)
        
        # Center window
        self.center_window()
        
        self.setup_ui()
    
    def center_window(self):
        """Dat cua so o giua man hinh"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_ui(self):
        """Thiet lap giao dien"""
        
        # Header
        header_frame = tk.Frame(self.root, bg="#2c3e50", height=80)
        header_frame.pack(fill=tk.X)
        header_frame.pack_propagate(False)
        
        title_label = tk.Label(
            header_frame,
            text="CONG CU TIEN ICH",
            font=("Arial", 20, "bold"),
            bg="#2c3e50",
            fg="white"
        )
        title_label.pack(pady=10)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Chon cong cu ban muon su dung",
            font=("Arial", 10),
            bg="#2c3e50",
            fg="#ecf0f1"
        )
        subtitle_label.pack()
        
        # Main content
        main_frame = tk.Frame(self.root, padx=30, pady=30)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tool 1: PowerPoint Cleaner (Single)
        tool1_frame = tk.LabelFrame(
            main_frame,
            text="PowerPoint Cleaner - Xu ly 1 file",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )
        tool1_frame.pack(fill=tk.X, pady=(0, 15))
        
        desc1 = tk.Label(
            tool1_frame,
            text="? Xoa hinh anh theo kich thuoc\n? Loc text (giu tieng Viet/Trung, xoa tieng Anh)\n? Giu nguyen dinh dang text (font, size, color)",
            font=("Arial", 9),
            justify="left",
            fg="#555"
        )
        desc1.pack(anchor="w", pady=(0, 10))
        
        btn1 = tk.Button(
            tool1_frame,
            text="? Mo PowerPoint Cleaner",
            command=self.launch_ppt_cleaner,
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        btn1.pack(fill=tk.X)
        
        # Tool 2: PowerPoint Cleaner Batch
        tool2_frame = tk.LabelFrame(
            main_frame,
            text="PowerPoint Cleaner Batch - Xu ly nhieu file",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )
        tool2_frame.pack(fill=tk.X, pady=(0, 15))
        
        desc2 = tk.Label(
            tool2_frame,
            text="? Xu ly nhieu file PowerPoint cung luc\n? Toan bo tinh nang cua phien ban Single\n? Batch processing voi progress tracking",
            font=("Arial", 9),
            justify="left",
            fg="#555"
        )
        desc2.pack(anchor="w", pady=(0, 10))
        
        btn2 = tk.Button(
            tool2_frame,
            text="? Mo PowerPoint Cleaner Batch",
            command=self.launch_ppt_cleaner_batch,
            bg="#27ae60",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        btn2.pack(fill=tk.X)
        
        # Tool 3: Stroke Order Downloader
        tool3_frame = tk.LabelFrame(
            main_frame,
            text="Tai anh thu tu net chu Han",
            font=("Arial", 11, "bold"),
            padx=15,
            pady=15
        )
        tool3_frame.pack(fill=tk.X, pady=(0, 15))
        
        desc3 = tk.Label(
            tool3_frame,
            text="? Tai anh thu tu net chu Han tu strokeorder.info\n? Tai song song nhieu ky tu\n? Luu anh dinh dang GIF",
            font=("Arial", 9),
            justify="left",
            fg="#555"
        )
        desc3.pack(anchor="w", pady=(0, 10))
        
        btn3 = tk.Button(
            tool3_frame,
            text="? Mo Stroke Order Downloader",
            command=self.launch_stroke_order,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            cursor="hand2",
            relief=tk.FLAT,
            padx=20,
            pady=8
        )
        btn3.pack(fill=tk.X)
        
        # Footer
        footer_frame = tk.Frame(self.root, bg="#ecf0f1", height=40)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        footer_frame.pack_propagate(False)
        
        footer_label = tk.Label(
            footer_frame,
            text="Version 3.3.1 | Chon cong cu phia tren de bat dau",
            font=("Arial", 9),
            bg="#ecf0f1",
            fg="#7f8c8d"
        )
        footer_label.pack(pady=10)
    
    def launch_ppt_cleaner(self):
        """Khoi dong PowerPoint Cleaner (single file)"""
        try:
            script_path = Path(__file__).parent / "ppt_cleaner.py"
            subprocess.Popen([sys.executable, str(script_path)])
        except Exception as e:
            tk.messagebox.showerror("Loi", f"Khong the mo cong cu:\n{str(e)}")
    
    def launch_ppt_cleaner_batch(self):
        """Khoi dong PowerPoint Cleaner Batch"""
        try:
            script_path = Path(__file__).parent / "ppt_cleaner_batch.py"
            subprocess.Popen([sys.executable, str(script_path)])
        except Exception as e:
            tk.messagebox.showerror("Loi", f"Khong the mo cong cu:\n{str(e)}")
    
    def launch_stroke_order(self):
        """Khoi dong Stroke Order Downloader"""
        try:
            script_path = Path(__file__).parent / "stroke_order_downloader.py"
            subprocess.Popen([sys.executable, str(script_path)])
        except Exception as e:
            tk.messagebox.showerror("Loi", f"Khong the mo cong cu:\n{str(e)}")


def main():
    root = tk.Tk()
    app = ToolLauncher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
