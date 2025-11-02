"""
Ung dung tai anh thu tu net chu Han tu strokeorder.info
Phien ban cai tien voi da luong va UI hien dai
"""

import os
import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from typing import List, Optional
import threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed


class StrokeOrderDownloader:
    """Class quan ly viec tai anh thu tu net chu Han"""
    
    BASE_URL = "http://www.strokeorder.info/mandarin.php"
    DEFAULT_TIMEOUT = 10
    MAX_WORKERS = 5
    
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
                return True, f"? Da tai: {character}"
            else:
                return False, f"? Loi HTTP {response.status_code}: {character}"
                
        except requests.RequestException as e:
            return False, f"? Loi tai {character}: {str(e)}"
    
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
            return False, f"?? Khong tim thay anh cho '{character}'"
        
        return self.download_image(image_url, character, folder_path)


class StrokeOrderApp:
    """Ung dung GUI cho viec tai anh thu tu net"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("Tai Anh Thu Tu Net Chu Han")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        # Thiet lap thu muc mac dinh (cross-platform)
        home_dir = Path.home()
        self.default_folder = home_dir / "Stroke_images"
        self.default_folder.mkdir(parents=True, exist_ok=True)
        
        self.folder_path_var = tk.StringVar(value=str(self.default_folder))
        self.downloader: Optional[StrokeOrderDownloader] = None
        self.is_downloading = False
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Thiet lap giao dien nguoi dung"""
        
        # Frame chinh
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Tieu de
        title_label = ttk.Label(
            main_frame, 
            text="Tai Anh Thu Tu Net Chu Han",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Frame nhap lieu
        input_frame = ttk.LabelFrame(main_frame, text="Nhap du lieu", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        instruction_label = ttk.Label(
            input_frame, 
            text="Nhap cac ky tu tieng Trung (co the cach nhau bang dau phay hoac khoang trang):"
        )
        instruction_label.pack(anchor=tk.W)
        
        self.entry = ttk.Entry(input_frame, font=("Arial", 14), width=50)
        self.entry.pack(fill=tk.X, pady=5)
        self.entry.bind("<Return>", lambda e: self.start_download())
        
        # Frame thu muc
        folder_frame = ttk.LabelFrame(main_frame, text="Thu muc luu anh", padding="10")
        folder_frame.pack(fill=tk.X, pady=5)
        
        folder_display_frame = ttk.Frame(folder_frame)
        folder_display_frame.pack(fill=tk.X)
        
        self.folder_label = ttk.Label(
            folder_display_frame, 
            textvariable=self.folder_path_var,
            foreground="blue",
            wraplength=500
        )
        self.folder_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        folder_button = ttk.Button(
            folder_display_frame, 
            text="Chon thu muc", 
            command=self.select_folder
        )
        folder_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Frame nut dieu khien
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        self.download_button = ttk.Button(
            button_frame, 
            text="?? Bat dau tai", 
            command=self.start_download,
            width=20
        )
        self.download_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = ttk.Button(
            button_frame, 
            text="?? Huy", 
            command=self.cancel_download,
            state=tk.DISABLED,
            width=20
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Thanh tien trinh
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="San sang")
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            mode='determinate',
            length=600
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Khu vuc hien thi ket qua
        result_frame = ttk.LabelFrame(main_frame, text="Ket qua", padding="5")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Scrollbar cho text widget
        scrollbar = ttk.Scrollbar(result_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.result_text = tk.Text(
            result_frame, 
            height=12, 
            font=("Arial", 10),
            yscrollcommand=scrollbar.set
        )
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.result_text.yview)
        
        # Them tags cho text mau sac
        self.result_text.tag_config("success", foreground="green")
        self.result_text.tag_config("error", foreground="red")
        self.result_text.tag_config("warning", foreground="orange")
        self.result_text.tag_config("info", foreground="blue")
    
    def select_folder(self):
        """Chon thu muc luu anh"""
        folder_selected = filedialog.askdirectory(initialdir=self.folder_path_var.get())
        if folder_selected:
            self.folder_path_var.set(folder_selected)
    
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
        
        # Chuan bi UI
        self.is_downloading = True
        self.download_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.entry.config(state=tk.DISABLED)
        self.result_text.delete(1.0, tk.END)
        
        # Parse input
        characters = self.parse_input(words_input)
        self.log_message(f"?? Tim thay {len(characters)} ky tu duy nhat", "info")
        self.log_message(f"?? Thu muc luu: {folder_path}", "info")
        self.log_message("?" * 60, "info")
        
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
                    else:
                        self.log_message(message, "error" if "?" in message else "warning")
                        fail_count += 1
                    
                except Exception as e:
                    self.log_message(f"? Loi xu ly '{char}': {str(e)}", "error")
                    fail_count += 1
                
                # Update progress
                self.progress_bar["value"] = i
                self.progress_label.config(text=f"Dang xu ly: {i}/{len(characters)}")
                self.root.update_idletasks()
        
        # Hoan thanh
        self.log_message("?" * 60, "info")
        if self.downloader._cancelled:
            self.log_message("?? Da huy qua trinh tai!", "warning")
        else:
            self.log_message("?? Qua trinh tai hoan tat!", "success")
        
        self.log_message(f"?? Thong ke: {success_count} thanh cong, {fail_count} that bai", "info")
        
        # Reset UI
        self._reset_ui()
    
    def cancel_download(self):
        """Huy qua trinh tai"""
        if self.downloader:
            self.downloader.cancel()
            self.cancel_button.config(state=tk.DISABLED)
            self.log_message("? Dang huy...", "warning")
    
    def _reset_ui(self):
        """Reset UI ve trang thai ban dau"""
        self.is_downloading = False
        self.download_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.entry.config(state=tk.NORMAL)
        self.progress_label.config(text="Hoan thanh")
        self.downloader = None


def main():
    """Ham main de chay ung dung"""
    root = tk.Tk()
    app = StrokeOrderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
