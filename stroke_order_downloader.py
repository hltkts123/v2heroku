#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ung dung tai anh thu tu net chu Han tu strokeorder.info
Phien ban cai tien voi da luong va UI hien dai
"""

import os
import sys
import json
import subprocess
import platform
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from typing import List, Optional, Dict
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


class StrokeOrderDownloader:
    """Class quan ly viec tai anh thu tu net chu Han"""
    
    BASE_URL = "http://www.strokeorder.info/mandarin.php"
    DEFAULT_TIMEOUT = 10
    MAX_WORKERS = 10
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self._cancelled = False
    
    def cancel(self):
        """Huy qua trinh tai"""
        self._cancelled = True
    
    def get_image_url(self, character: str) -> Optional[str]:
        """
        Lay URL anh cho mot ky tu
        
        Args:
            character: Ky tu can tim anh
            
        Returns:
            URL cua anh hoac None neu khong tim thay
        """
        try:
            url = f"{self.BASE_URL}?q={character}"
            response = self.session.get(url, timeout=self.DEFAULT_TIMEOUT)
            
            if response.status_code != 200:
                return None
            
            soup = BeautifulSoup(response.text, 'html.parser')
            image_tag = soup.find("img", {"src": lambda x: x and "/characters/" in x})
            
            if image_tag and "src" in image_tag.attrs:
                return image_tag["src"]
            
            return None
            
        except requests.RequestException:
            return None
    
    def download_image(self, image_url: str, character: str, folder_path: Path) -> tuple[bool, str]:
        """
        Tai anh ve may
        
        Args:
            image_url: URL cua anh
            character: Ten ky tu (dung lam ten file)
            folder_path: Thu muc luu anh
            
        Returns:
            Tuple (success, message)
        """
        if self._cancelled:
            return False, "Da huy"
        
        try:
            response = self.session.get(image_url, timeout=self.DEFAULT_TIMEOUT)
            
            if response.status_code == 200:
                file_path = folder_path / f"{character}.gif"
                with open(file_path, "wb") as f:
                    f.write(response.content)
                return True, f"[OK] Da tai: {character}"
            else:
                return False, f"[ERR] HTTP {response.status_code}: {character}"
                
        except requests.RequestException as e:
            return False, f"[ERR] Tai {character}: {str(e)}"
    
    def process_character(self, character: str, folder_path: Path) -> tuple[bool, str]:
        """
        Xu ly mot ky tu: lay URL va tai anh
        
        Args:
            character: Ky tu can xu ly
            folder_path: Thu muc luu anh
            
        Returns:
            Tuple (success, message)
        """
        if self._cancelled:
            return False, "Da huy"
        
        image_url = self.get_image_url(character)
        
        if not image_url:
            return False, f"[!] Khong tim thay anh cho '{character}'"
        
        return self.download_image(image_url, character, folder_path)


class StrokeOrderApp:
    """Ung dung GUI cho viec tai anh thu tu net"""
    
    CONFIG_FILE = Path.home() / ".stroke_order_config.json"
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tai Anh Thu Tu Net Chu Han")
        self.root.geometry("750x600")
        self.root.resizable(True, True)
        
        # Thiet lap thu muc mac dinh (cross-platform)
        home_dir = Path.home()
        self.default_folder = home_dir / "Stroke_images"
        self.default_folder.mkdir(parents=True, exist_ok=True)
        
        # Load config tu lan su dung truoc
        saved_folder = self._load_config()
        initial_folder = saved_folder if saved_folder else str(self.default_folder)
        
        self.folder_path_var = tk.StringVar(value=initial_folder)
        self.downloader: Optional[StrokeOrderDownloader] = None
        self.is_downloading = False
        
        self._setup_ui()
    
    def _load_config(self) -> Optional[str]:
        """
        Load cau hinh tu file
        
        Returns:
            Thu muc da luu hoac None
        """
        try:
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    folder = config.get('last_folder')
                    # Kiem tra thu muc co ton tai khong
                    if folder and Path(folder).exists():
                        return folder
        except Exception:
            pass
        return None
    
    def _save_config(self):
        """Luu cau hinh vao file"""
        try:
            config = {
                'last_folder': self.folder_path_var.get()
            }
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def _setup_ui(self):
        """Thiet lap giao dien nguoi dung"""
        
        # Frame chinh
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tieu de
        title_label = ttk.Label(
            main_frame, 
            text="TAI ANH THU TU NET CHU HAN",
            font=("Arial", 16, "bold"),
            foreground="#2C3E50"
        )
        title_label.pack(pady=(0, 15))
        
        # Frame nhap lieu
        input_frame = ttk.LabelFrame(main_frame, text=" NHAP DU LIEU ", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        instruction_label = ttk.Label(
            input_frame, 
            text="Nhap cac ky tu tieng Trung (co the cach nhau bang dau phay hoac khoang trang):",
            font=("Arial", 9)
        )
        instruction_label.pack(anchor=tk.W, pady=(0, 5))
        
        self.entry = ttk.Entry(input_frame, font=("Arial", 14), width=50)
        self.entry.pack(fill=tk.X, pady=5)
        self.entry.bind("<Return>", lambda e: self.start_download())
        
        # Frame thu muc
        folder_frame = ttk.LabelFrame(main_frame, text=" THU MUC LUU ANH ", padding="10")
        folder_frame.pack(fill=tk.X, pady=5)
        
        # Hien thi duong dan
        path_display_frame = ttk.Frame(folder_frame)
        path_display_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(path_display_frame, text="Duong dan:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        
        self.folder_label = ttk.Label(
            path_display_frame, 
            textvariable=self.folder_path_var,
            foreground="#2980B9",
            wraplength=650,
            font=("Arial", 9)
        )
        self.folder_label.pack(anchor=tk.W, pady=(2, 0))
        
        # Buttons frame
        folder_buttons_frame = ttk.Frame(folder_frame)
        folder_buttons_frame.pack(fill=tk.X)
        
        folder_button = ttk.Button(
            folder_buttons_frame, 
            text="[+] Chon Thu Muc", 
            command=self.select_folder,
            width=22
        )
        folder_button.pack(side=tk.LEFT, padx=(0, 5))
        
        open_folder_button = ttk.Button(
            folder_buttons_frame, 
            text="[>] Mo Thu Muc", 
            command=self.open_folder,
            width=22
        )
        open_folder_button.pack(side=tk.LEFT, padx=(0, 5))
        
        # Frame nut dieu khien
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=15)
        
        self.download_button = ttk.Button(
            button_frame, 
            text=">> BAT DAU TAI <<", 
            command=self.start_download,
            width=25
        )
        self.download_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = ttk.Button(
            button_frame, 
            text="[X] HUY BO", 
            command=self.cancel_download,
            state=tk.DISABLED,
            width=25
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Thanh tien trinh
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(
            progress_frame, 
            text="Trang thai: San sang",
            font=("Arial", 9, "bold"),
            foreground="#27AE60"
        )
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            mode='determinate',
            length=680
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Khu vuc hien thi ket qua
        result_frame = ttk.LabelFrame(main_frame, text=" KET QUA ", padding="5")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar cho text widget
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = tk.Text(
            result_frame, 
            height=13, 
            font=("Consolas", 9),
            yscrollcommand=scrollbar.set,
            bg="#F8F9FA",
            relief=tk.FLAT,
            padx=5,
            pady=5
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_text.yview)
        
        # Them tags cho text mau sac
        self.result_text.tag_config("success", foreground="#27AE60", font=("Consolas", 9, "bold"))
        self.result_text.tag_config("error", foreground="#E74C3C", font=("Consolas", 9, "bold"))
        self.result_text.tag_config("warning", foreground="#F39C12", font=("Consolas", 9, "bold"))
        self.result_text.tag_config("info", foreground="#2980B9", font=("Consolas", 9))
        self.result_text.tag_config("header", foreground="#2C3E50", font=("Consolas", 9, "bold"))
    
    def select_folder(self):
        """Chon thu muc luu anh"""
        folder_selected = filedialog.askdirectory(initialdir=self.folder_path_var.get())
        if folder_selected:
            self.folder_path_var.set(folder_selected)
            self._save_config()  # Luu config khi chon thu muc moi
            self.log_message(f"[INFO] Da chon thu muc: {folder_selected}", "info")
    
    def open_folder(self):
        """Mo thu muc trong file explorer"""
        folder_path = self.folder_path_var.get()
        
        # Tao thu muc neu chua ton tai
        if not Path(folder_path).exists():
            try:
                Path(folder_path).mkdir(parents=True, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Loi", f"Khong the tao thu muc: {e}")
                return
        
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(folder_path)
            elif system == "Darwin":  # macOS
                subprocess.run(["open", folder_path])
            else:  # Linux and other Unix-like
                subprocess.run(["xdg-open", folder_path])
            self.log_message(f"[INFO] Da mo thu muc: {folder_path}", "info")
        except Exception as e:
            messagebox.showerror("Loi", f"Khong the mo thu muc: {e}")
    
    def log_message(self, message: str, tag: str = "info"):
        """
        Them message vao khu vuc ket qua
        
        Args:
            message: Noi dung message
            tag: Tag de dinh dang (success, error, warning, info)
        """
        self.result_text.insert(tk.END, message + "\n", tag)
        self.result_text.see(tk.END)
        self.root.update_idletasks()
    
    def parse_input(self, text: str) -> List[str]:
        """
        Phan tich input va trich xuat cac ky tu
        
        Args:
            text: Chuoi input tu nguoi dung
            
        Returns:
            List cac ky tu duy nhat
        """
        # Loai bo dau phay va khoang trang
        characters = [char for char in text if char not in [",", " ", "\n", "\t"]]
        # Loai bo trung lap nhung giu thu tu
        seen = set()
        unique_chars = []
        for char in characters:
            if char not in seen:
                seen.add(char)
                unique_chars.append(char)
        return unique_chars
    
    def start_download(self):
        """Bat dau qua trinh tai anh"""
        if self.is_downloading:
            return
        
        words_input = self.entry.get().strip()
        if not words_input:
            messagebox.showwarning("Canh bao", "Ban chua nhap tu nao!")
            return
        
        folder_path = Path(self.folder_path_var.get())
        if not folder_path.exists():
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Loi", f"Khong the tao thu muc: {e}")
                return
        
        # Luu config khi bat dau tai
        self._save_config()
        
        # Chuan bi UI
        self.is_downloading = True
        self.download_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.entry.config(state=tk.DISABLED)
        self.result_text.delete(1.0, tk.END)
        
        # Parse input
        characters = self.parse_input(words_input)
        self.log_message("=" * 70, "header")
        self.log_message("          BAT DAU QUA TRINH TAI ANH          ", "header")
        self.log_message("=" * 70, "header")
        self.log_message(f"[INFO] Tim thay {len(characters)} ky tu duy nhat: {' '.join(characters)}", "info")
        self.log_message(f"[INFO] Thu muc luu: {folder_path}", "info")
        self.log_message("-" * 70, "info")
        
        # Chay download trong thread rieng
        thread = threading.Thread(
            target=self._download_worker,
            args=(characters, folder_path),
            daemon=True
        )
        thread.start()
    
    def _download_worker(self, characters: List[str], folder_path: Path):
        """
        Worker function chay trong thread rieng de tai anh
        
        Args:
            characters: List ky tu can tai
            folder_path: Thu muc luu anh
        """
        self.downloader = StrokeOrderDownloader()
        
        # Reset progress bar
        self.progress_bar["maximum"] = len(characters)
        self.progress_bar["value"] = 0
        
        success_count = 0
        fail_count = 0
        
        # Su dung ThreadPoolExecutor de tai song song
        with ThreadPoolExecutor(max_workers=StrokeOrderDownloader.MAX_WORKERS) as executor:
            # Submit tat ca cac task
            future_to_char = {
                executor.submit(self.downloader.process_character, char, folder_path): char
                for char in characters
            }
            
            # Xu ly ket qua khi hoan thanh
            for i, future in enumerate(as_completed(future_to_char), 1):
                char = future_to_char[future]
                
                try:
                    success, message = future.result()
                    
                    # Update UI
                    if success:
                        self.log_message(message, "success")
                        success_count += 1
                    elif "[ERR]" in message:
                        self.log_message(message, "error")
                        fail_count += 1
                    else:
                        self.log_message(message, "warning")
                        fail_count += 1
                    
                except Exception as e:
                    self.log_message(f"[ERR] Xu ly '{char}': {str(e)}", "error")
                    fail_count += 1
                
                # Update progress
                self.progress_bar["value"] = i
                percent = int((i / len(characters)) * 100)
                self.progress_label.config(
                    text=f"Trang thai: Dang xu ly {i}/{len(characters)} ({percent}%)",
                    foreground="#F39C12"
                )
                self.root.update_idletasks()
        
        # Hoan thanh
        self.log_message("-" * 70, "info")
        if self.downloader._cancelled:
            self.log_message("[NOTIFY] Da huy qua trinh tai!", "warning")
            self.progress_label.config(text="Trang thai: Da huy", foreground="#E74C3C")
        else:
            self.log_message("[SUCCESS] Qua trinh tai hoan tat!", "success")
            self.progress_label.config(text="Trang thai: Hoan thanh", foreground="#27AE60")
        
        self.log_message(f"[STATS] Thanh cong: {success_count} | That bai: {fail_count} | Tong: {len(characters)}", "header")
        self.log_message("=" * 70, "header")
        
        # Reset UI
        self._reset_ui()
    
    def cancel_download(self):
        """Huy qua trinh tai"""
        if self.downloader:
            self.downloader.cancel()
            self.cancel_button.config(state=tk.DISABLED)
            self.log_message("[NOTIFY] Dang huy qua trinh...", "warning")
    
    def _reset_ui(self):
        """Reset UI ve trang thai ban dau"""
        self.is_downloading = False
        self.download_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.entry.config(state=tk.NORMAL)
        self.downloader = None


def main():
    """Ham main de chay ung dung"""
    root = tk.Tk()
    
    # Set style cho Windows
    style = ttk.Style()
    if platform.system() == "Windows":
        try:
            style.theme_use('vista')
        except:
            style.theme_use('default')
    
    app = StrokeOrderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
