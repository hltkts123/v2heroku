"""
Ung dung tai anh thu tu net chu Han tu strokeorder.info
Phien ban giao dien hien dai voi CustomTkinter
"""

import os
import sys
import json
import subprocess
import platform
import requests
from bs4 import BeautifulSoup
import customtkinter as ctk
from tkinter import messagebox, filedialog
from typing import List, Optional
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
        """Lay URL anh cho mot ky tu"""
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
        """Tai anh ve may"""
        if self._cancelled:
            return False, "Da huy"
        
        try:
            response = self.session.get(image_url, timeout=self.DEFAULT_TIMEOUT)
            
            if response.status_code == 200:
                file_path = folder_path / f"{character}.gif"
                with open(file_path, "wb") as f:
                    f.write(response.content)
                return True, f"? Da tai: {character}"
            else:
                return False, f"? Loi HTTP {response.status_code}: {character}"
                
        except requests.RequestException as e:
            return False, f"? Loi tai {character}: {str(e)}"
    
    def process_character(self, character: str, folder_path: Path) -> tuple[bool, str]:
        """Xu ly mot ky tu: lay URL va tai anh"""
        if self._cancelled:
            return False, "Da huy"
        
        image_url = self.get_image_url(character)
        
        if not image_url:
            return False, f"? Khong tim thay anh cho '{character}'"
        
        return self.download_image(image_url, character, folder_path)


class ModernStrokeOrderApp:
    """Ung dung GUI hien dai voi CustomTkinter"""
    
    CONFIG_FILE = Path.home() / ".stroke_order_config.json"
    
    def __init__(self):
        # Cau hinh CustomTkinter
        ctk.set_appearance_mode("dark")  # "dark" hoac "light"
        ctk.set_default_color_theme("blue")  # "blue", "green", "dark-blue"
        
        self.root = ctk.CTk()
        self.root.title("Tai Anh Thu Tu Net Chu Han - Modern UI")
        self.root.geometry("900x700")
        
        # Thiet lap thu muc mac dinh
        home_dir = Path.home()
        self.default_folder = home_dir / "Stroke_images"
        self.default_folder.mkdir(parents=True, exist_ok=True)
        
        # Load config
        config = self._load_config()
        initial_folder = config.get('last_folder') or str(self.default_folder)
        
        self.folder_path = initial_folder
        self.downloader: Optional[StrokeOrderDownloader] = None
        self.is_downloading = False
        
        self._setup_ui()
    
    def _load_config(self) -> dict:
        """Load cau hinh tu file"""
        try:
            if self.CONFIG_FILE.exists():
                with open(self.CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    folder = config.get('last_folder')
                    if folder and not Path(folder).exists():
                        config['last_folder'] = None
                    return config
        except Exception:
            pass
        return {}
    
    def _save_config(self):
        """Luu cau hinh vao file"""
        try:
            config = {'last_folder': self.folder_path}
            with open(self.CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def _setup_ui(self):
        """Thiet lap giao dien"""
        
        # Main container
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title = ctk.CTkLabel(
            main_frame,
            text="?? TAI ANH THU TU NET CHU HAN",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title.pack(pady=(0, 20))
        
        # Input section
        input_frame = ctk.CTkFrame(main_frame)
        input_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            input_frame,
            text="Nhap cac ky tu tieng Trung:",
            font=ctk.CTkFont(size=14)
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.entry = ctk.CTkEntry(
            input_frame,
            placeholder_text="Vi du: ????",
            height=45,
            font=ctk.CTkFont(size=16)
        )
        self.entry.pack(fill="x", padx=20, pady=(0, 15))
        self.entry.bind("<Return>", lambda e: self.start_download())
        
        # Folder section
        folder_frame = ctk.CTkFrame(main_frame)
        folder_frame.pack(fill="x", pady=10)
        
        ctk.CTkLabel(
            folder_frame,
            text="?? Thu muc luu anh:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.folder_label = ctk.CTkLabel(
            folder_frame,
            text=self.folder_path,
            font=ctk.CTkFont(size=12),
            text_color=("gray60", "gray40")
        )
        self.folder_label.pack(anchor="w", padx=20, pady=(0, 10))
        
        # Folder buttons
        folder_btn_frame = ctk.CTkFrame(folder_frame, fg_color="transparent")
        folder_btn_frame.pack(fill="x", padx=20, pady=(0, 15))
        
        ctk.CTkButton(
            folder_btn_frame,
            text="?? Chon Thu Muc",
            command=self.select_folder,
            width=200,
            height=40
        ).pack(side="left", padx=(0, 10))
        
        ctk.CTkButton(
            folder_btn_frame,
            text="??? Mo Thu Muc",
            command=self.open_folder,
            width=200,
            height=40,
            fg_color="transparent",
            border_width=2
        ).pack(side="left")
        
        # Control buttons
        button_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        self.download_button = ctk.CTkButton(
            button_frame,
            text="?? BAT DAU TAI",
            command=self.start_download,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#1f6aa5",
            hover_color="#144870"
        )
        self.download_button.pack(side="left", padx=10)
        
        self.cancel_button = ctk.CTkButton(
            button_frame,
            text="? HUY BO",
            command=self.cancel_download,
            width=250,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#d32f2f",
            hover_color="#b71c1c",
            state="disabled"
        )
        self.cancel_button.pack(side="left", padx=10)
        
        # Progress section
        progress_frame = ctk.CTkFrame(main_frame)
        progress_frame.pack(fill="x", pady=10)
        
        self.progress_label = ctk.CTkLabel(
            progress_frame,
            text="? San sang",
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.progress_label.pack(pady=(15, 5))
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame, height=20)
        self.progress_bar.pack(fill="x", padx=20, pady=(0, 15))
        self.progress_bar.set(0)
        
        # Result section
        result_frame = ctk.CTkFrame(main_frame)
        result_frame.pack(fill="both", expand=True, pady=10)
        
        ctk.CTkLabel(
            result_frame,
            text="?? Ket qua",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))
        
        self.result_text = ctk.CTkTextbox(
            result_frame,
            font=ctk.CTkFont(family="Consolas", size=12),
            wrap="word"
        )
        self.result_text.pack(fill="both", expand=True, padx=20, pady=(0, 15))
        
        # Theme switcher
        theme_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        theme_frame.pack(pady=10)
        
        ctk.CTkLabel(
            theme_frame,
            text="Giao dien:",
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(0, 10))
        
        self.theme_switch = ctk.CTkSwitch(
            theme_frame,
            text="Che do toi",
            command=self.toggle_theme,
            onvalue="dark",
            offvalue="light"
        )
        self.theme_switch.pack(side="left")
        self.theme_switch.select()  # Mac dinh dark mode
    
    def toggle_theme(self):
        """Chuyen doi giua dark/light mode"""
        mode = self.theme_switch.get()
        ctk.set_appearance_mode(mode)
    
    def select_folder(self):
        """Chon thu muc luu anh"""
        folder = filedialog.askdirectory(initialdir=self.folder_path)
        if folder:
            self.folder_path = folder
            self.folder_label.configure(text=folder)
            self._save_config()
            self.log_message(f"? Da chon thu muc: {folder}")
    
    def open_folder(self):
        """Mo thu muc trong file explorer"""
        folder_path = Path(self.folder_path)
        
        if not folder_path.exists():
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Loi", f"Khong the tao thu muc: {e}")
                return
        
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(str(folder_path))
            elif system == "Darwin":
                subprocess.run(["open", str(folder_path)])
            else:
                subprocess.run(["xdg-open", str(folder_path)])
            self.log_message(f"? Da mo thu muc: {folder_path}")
        except Exception as e:
            messagebox.showerror("Loi", f"Khong the mo thu muc: {e}")
    
    def log_message(self, message: str):
        """Them message vao result text"""
        self.result_text.insert("end", message + "\n")
        self.result_text.see("end")
    
    def parse_input(self, text: str) -> List[str]:
        """Phan tich input va trich xuat cac ky tu"""
        characters = [char for char in text if char not in [",", " ", "\n", "\t"]]
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
        
        folder_path = Path(self.folder_path)
        if not folder_path.exists():
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                messagebox.showerror("Loi", f"Khong the tao thu muc: {e}")
                return
        
        self._save_config()
        
        # UI state
        self.is_downloading = True
        self.download_button.configure(state="disabled")
        self.cancel_button.configure(state="normal")
        self.entry.configure(state="disabled")
        self.result_text.delete("0.0", "end")
        
        # Parse input
        characters = self.parse_input(words_input)
        self.log_message("=" * 60)
        self.log_message("     BAT DAU TAI ANH STROKE     ")
        self.log_message("=" * 60)
        self.log_message(f"?? Tim thay {len(characters)} ky tu: {' '.join(characters)}")
        self.log_message(f"?? Thu muc: {folder_path}")
        self.log_message("-" * 60)
        
        # Start download thread
        thread = threading.Thread(
            target=self._download_worker,
            args=(characters, folder_path),
            daemon=True
        )
        thread.start()
    
    def _download_worker(self, characters: List[str], folder_path: Path):
        """Worker function de tai anh"""
        self.downloader = StrokeOrderDownloader()
        
        # Reset progress
        self.progress_bar.set(0)
        total = len(characters)
        
        success_count = 0
        fail_count = 0
        
        with ThreadPoolExecutor(max_workers=StrokeOrderDownloader.MAX_WORKERS) as executor:
            future_to_char = {
                executor.submit(self.downloader.process_character, char, folder_path): char
                for char in characters
            }
            
            for i, future in enumerate(as_completed(future_to_char), 1):
                char = future_to_char[future]
                
                try:
                    success, message = future.result()
                    self.log_message(message)
                    
                    if success:
                        success_count += 1
                    else:
                        fail_count += 1
                    
                except Exception as e:
                    self.log_message(f"? Loi xu ly '{char}': {str(e)}")
                    fail_count += 1
                
                # Update progress
                progress = i / total
                self.progress_bar.set(progress)
                percent = int(progress * 100)
                self.progress_label.configure(text=f"? Dang xu ly: {i}/{total} ({percent}%)")
        
        # Complete
        self.log_message("-" * 60)
        if self.downloader._cancelled:
            self.log_message("? Da huy qua trinh tai!")
            self.progress_label.configure(text="? Da huy")
        else:
            self.log_message("?? Hoan tat!")
            self.progress_label.configure(text="? Hoan thanh")
        
        self.log_message(f"?? Thong ke: {success_count} thanh cong | {fail_count} that bai")
        self.log_message("=" * 60)
        
        self._reset_ui()
    
    def cancel_download(self):
        """Huy qua trinh tai"""
        if self.downloader:
            self.downloader.cancel()
            self.cancel_button.configure(state="disabled")
            self.log_message("? Dang huy...")
    
    def _reset_ui(self):
        """Reset UI ve trang thai ban dau"""
        self.is_downloading = False
        self.download_button.configure(state="normal")
        self.cancel_button.configure(state="disabled")
        self.entry.configure(state="normal")
        self.downloader = None
    
    def run(self):
        """Chay ung dung"""
        self.root.mainloop()


def main():
    """Ham main"""
    app = ModernStrokeOrderApp()
    app.run()


if __name__ == "__main__":
    main()
