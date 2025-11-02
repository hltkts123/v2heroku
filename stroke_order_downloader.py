"""
?ng d?ng t?i ?nh th? t? n?t ch? H?n t? strokeorder.info
Phi?n b?n c?i ti?n v?i ?a lu?ng v? UI hi?n ??i
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
    """Class qu?n l? vi?c t?i ?nh th? t? n?t ch? H?n"""
    
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
        """H?y qu? tr?nh t?i"""
        self._cancelled = True
    
    def get_image_url(self, character: str) -> Optional[str]:
        """
        L?y URL ?nh cho m?t k? t?
        
        Args:
            character: K? t? c?n t?m ?nh
            
        Returns:
            URL c?a ?nh ho?c None n?u kh?ng t?m th?y
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
        T?i ?nh v? m?y
        
        Args:
            image_url: URL c?a ?nh
            character: T?n k? t? (d?ng l?m t?n file)
            folder_path: Th? m?c l?u ?nh
            
        Returns:
            Tuple (success, message)
        """
        if self._cancelled:
            return False, "?? h?y"
        
        try:
            response = self.session.get(image_url, timeout=self.DEFAULT_TIMEOUT)
            
            if response.status_code == 200:
                file_path = folder_path / f"{character}.gif"
                with open(file_path, "wb") as f:
                    f.write(response.content)
                return True, f"? ?? t?i: {character}"
            else:
                return False, f"? L?i HTTP {response.status_code}: {character}"
                
        except requests.RequestException as e:
            return False, f"? L?i t?i {character}: {str(e)}"
    
    def process_character(self, character: str, folder_path: Path) -> tuple[bool, str]:
        """
        X? l? m?t k? t?: l?y URL v? t?i ?nh
        
        Args:
            character: K? t? c?n x? l?
            folder_path: Th? m?c l?u ?nh
            
        Returns:
            Tuple (success, message)
        """
        if self._cancelled:
            return False, "?? h?y"
        
        image_url = self.get_image_url(character)
        
        if not image_url:
            return False, f"?? Kh?ng t?m th?y ?nh cho '{character}'"
        
        return self.download_image(image_url, character, folder_path)


class StrokeOrderApp:
    """?ng d?ng GUI cho vi?c t?i ?nh th? t? n?t"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("T?i ?nh Th? T? N?t Ch? H?n")
        self.root.geometry("700x550")
        self.root.resizable(False, False)
        
        # Thi?t l?p th? m?c m?c ??nh (cross-platform)
        home_dir = Path.home()
        self.default_folder = home_dir / "Stroke_images"
        self.default_folder.mkdir(parents=True, exist_ok=True)
        
        self.folder_path_var = tk.StringVar(value=str(self.default_folder))
        self.downloader: Optional[StrokeOrderDownloader] = None
        self.is_downloading = False
        
        self._setup_ui()
    
    def _setup_ui(self):
        """Thi?t l?p giao di?n ng??i d?ng"""
        
        # Frame ch?nh
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Ti?u ??
        title_label = ttk.Label(
            main_frame, 
            text="T?i ?nh Th? T? N?t Ch? H?n",
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # Frame nh?p li?u
        input_frame = ttk.LabelFrame(main_frame, text="Nh?p d? li?u", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        instruction_label = ttk.Label(
            input_frame, 
            text="Nh?p c?c k? t? ti?ng Trung (c? th? c?ch nhau b?ng d?u ph?y ho?c kho?ng tr?ng):"
        )
        instruction_label.pack(anchor=tk.W)
        
        self.entry = ttk.Entry(input_frame, font=("Arial", 14), width=50)
        self.entry.pack(fill=tk.X, pady=5)
        self.entry.bind("<Return>", lambda e: self.start_download())
        
        # Frame th? m?c
        folder_frame = ttk.LabelFrame(main_frame, text="Th? m?c l?u ?nh", padding="10")
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
            text="Ch?n th? m?c", 
            command=self.select_folder
        )
        folder_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Frame n?t ?i?u khi?n
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        self.download_button = ttk.Button(
            button_frame, 
            text="?? B?t ??u t?i", 
            command=self.start_download,
            width=20
        )
        self.download_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = ttk.Button(
            button_frame, 
            text="?? H?y", 
            command=self.cancel_download,
            state=tk.DISABLED,
            width=20
        )
        self.cancel_button.pack(side=tk.LEFT, padx=5)
        
        # Thanh ti?n tr?nh
        progress_frame = ttk.Frame(main_frame)
        progress_frame.pack(fill=tk.X, pady=5)
        
        self.progress_label = ttk.Label(progress_frame, text="S?n s?ng")
        self.progress_label.pack()
        
        self.progress_bar = ttk.Progressbar(
            progress_frame, 
            mode='determinate',
            length=600
        )
        self.progress_bar.pack(fill=tk.X, pady=5)
        
        # Khu v?c hi?n th? k?t qu?
        result_frame = ttk.LabelFrame(main_frame, text="K?t qu?", padding="5")
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
        
        # Th?m tags cho text m?u s?c
        self.result_text.tag_config("success", foreground="green")
        self.result_text.tag_config("error", foreground="red")
        self.result_text.tag_config("warning", foreground="orange")
        self.result_text.tag_config("info", foreground="blue")
    
    def select_folder(self):
        """Ch?n th? m?c l?u ?nh"""
        folder_selected = filedialog.askdirectory(initialdir=self.folder_path_var.get())
        if folder_selected:
            self.folder_path_var.set(folder_selected)
    
    def log_message(self, message: str, tag: str = "info"):
        """
        Th?m message v?o khu v?c k?t qu?
        
        Args:
            message: N?i dung message
            tag: Tag ?? ??nh d?ng (success, error, warning, info)
        """
        self.result_text.insert(tk.END, message + "\n", tag)
        self.result_text.see(tk.END)
        self.root.update_idletasks()
    
    def parse_input(self, text: str) -> List[str]:
        """
        Ph?n t?ch input v? tr?ch xu?t c?c k? t?
        
        Args:
            text: Chu?i input t? ng??i d?ng
            
        Returns:
            List c?c k? t? duy nh?t
        """
        # Lo?i b? d?u ph?y v? kho?ng tr?ng
        characters = [char for char in text if char not in [",", " ", "\n", "\t"]]
        # Lo?i b? tr?ng l?p nh?ng gi? th? t?
        seen = set()
        unique_chars = []
        for char in characters:
            if char not in seen:
                seen.add(char)
                unique_chars.append(char)
        return unique_chars
    
    def start_download(self):
        """B?t ??u qu? tr?nh t?i ?nh"""
        if self.is_downloading:
            return
        
        words_input = self.entry.get().strip()
        if not words_input:
            messagebox.showwarning("C?nh b?o", "B?n ch?a nh?p t? n?o!")
            return
        
        folder_path = Path(self.folder_path_var.get())
        if not folder_path.exists():
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                messagebox.showerror("L?i", f"Kh?ng th? t?o th? m?c: {e}")
                return
        
        # Chu?n b? UI
        self.is_downloading = True
        self.download_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        self.entry.config(state=tk.DISABLED)
        self.result_text.delete(1.0, tk.END)
        
        # Parse input
        characters = self.parse_input(words_input)
        self.log_message(f"?? T?m th?y {len(characters)} k? t? duy nh?t", "info")
        self.log_message(f"?? Th? m?c l?u: {folder_path}", "info")
        self.log_message("?" * 60, "info")
        
        # Ch?y download trong thread ri?ng
        thread = threading.Thread(
            target=self._download_worker,
            args=(characters, folder_path),
            daemon=True
        )
        thread.start()
    
    def _download_worker(self, characters: List[str], folder_path: Path):
        """
        Worker function ch?y trong thread ri?ng ?? t?i ?nh
        
        Args:
            characters: List k? t? c?n t?i
            folder_path: Th? m?c l?u ?nh
        """
        self.downloader = StrokeOrderDownloader()
        
        # Reset progress bar
        self.progress_bar["maximum"] = len(characters)
        self.progress_bar["value"] = 0
        
        success_count = 0
        fail_count = 0
        
        # S? d?ng ThreadPoolExecutor ?? t?i song song
        with ThreadPoolExecutor(max_workers=StrokeOrderDownloader.MAX_WORKERS) as executor:
            # Submit t?t c? c?c task
            future_to_char = {
                executor.submit(self.downloader.process_character, char, folder_path): char
                for char in characters
            }
            
            # X? l? k?t qu? khi ho?n th?nh
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
                    self.log_message(f"? L?i x? l? '{char}': {str(e)}", "error")
                    fail_count += 1
                
                # Update progress
                self.progress_bar["value"] = i
                self.progress_label.config(text=f"?ang x? l?: {i}/{len(characters)}")
                self.root.update_idletasks()
        
        # Ho?n th?nh
        self.log_message("?" * 60, "info")
        if self.downloader._cancelled:
            self.log_message("?? ?? h?y qu? tr?nh t?i!", "warning")
        else:
            self.log_message("?? Qu? tr?nh t?i ho?n t?t!", "success")
        
        self.log_message(f"?? Th?ng k?: {success_count} th?nh c?ng, {fail_count} th?t b?i", "info")
        
        # Reset UI
        self._reset_ui()
    
    def cancel_download(self):
        """H?y qu? tr?nh t?i"""
        if self.downloader:
            self.downloader.cancel()
            self.cancel_button.config(state=tk.DISABLED)
            self.log_message("? ?ang h?y...", "warning")
    
    def _reset_ui(self):
        """Reset UI v? tr?ng th?i ban ??u"""
        self.is_downloading = False
        self.download_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
        self.entry.config(state=tk.NORMAL)
        self.progress_label.config(text="Ho?n th?nh")
        self.downloader = None


def main():
    """H?m main ?? ch?y ?ng d?ng"""
    root = tk.Tk()
    app = StrokeOrderApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
