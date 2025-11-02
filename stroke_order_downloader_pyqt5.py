"""
Ung dung tai anh thu tu net chu Han tu strokeorder.info
Phien ban PyQt5 voi giao dien chuyen nghiep va icon dep
"""

import os
import sys
import json
import subprocess
import platform
import requests
from bs4 import BeautifulSoup
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTextEdit, QLabel, QProgressBar,
    QFileDialog, QMessageBox, QGroupBox, QFrame
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QSize
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QPixmap, QPainter
from typing import List, Optional
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
                return True, f"[OK] Da tai: {character}"
            else:
                return False, f"[ERR] HTTP {response.status_code}: {character}"
                
        except requests.RequestException as e:
            return False, f"[ERR] Tai {character}: {str(e)}"
    
    def process_character(self, character: str, folder_path: Path) -> tuple[bool, str]:
        """Xu ly mot ky tu: lay URL va tai anh"""
        if self._cancelled:
            return False, "Da huy"
        
        image_url = self.get_image_url(character)
        
        if not image_url:
            return False, f"[WARN] Khong tim thay anh cho '{character}'"
        
        return self.download_image(image_url, character, folder_path)


class DownloadThread(QThread):
    """Thread de tai anh khong lam dong UI"""
    
    progress_updated = pyqtSignal(int, int, str)  # current, total, message
    log_message = pyqtSignal(str, str)  # message, type
    finished = pyqtSignal(int, int)  # success_count, fail_count
    
    def __init__(self, characters: List[str], folder_path: Path):
        super().__init__()
        self.characters = characters
        self.folder_path = folder_path
        self.downloader = StrokeOrderDownloader()
    
    def run(self):
        """Chay qua trinh tai"""
        success_count = 0
        fail_count = 0
        total = len(self.characters)
        
        with ThreadPoolExecutor(max_workers=StrokeOrderDownloader.MAX_WORKERS) as executor:
            future_to_char = {
                executor.submit(self.downloader.process_character, char, self.folder_path): char
                for char in self.characters
            }
            
            for i, future in enumerate(as_completed(future_to_char), 1):
                char = future_to_char[future]
                
                try:
                    success, message = future.result()
                    
                    if success:
                        self.log_message.emit(message, "success")
                        success_count += 1
                    elif "[ERR]" in message:
                        self.log_message.emit(message, "error")
                        fail_count += 1
                    else:
                        self.log_message.emit(message, "warning")
                        fail_count += 1
                    
                except Exception as e:
                    self.log_message.emit(f"[ERR] Xu ly '{char}': {str(e)}", "error")
                    fail_count += 1
                
                self.progress_updated.emit(i, total, f"Dang xu ly {i}/{total}")
        
        self.finished.emit(success_count, fail_count)
    
    def cancel(self):
        """Huy qua trinh tai"""
        self.downloader.cancel()


class IconFactory:
    """Factory de tao icon don gian bang code"""
    
    @staticmethod
    def create_icon(icon_type: str, size: QSize = QSize(24, 24)) -> QIcon:
        """Tao icon don gian"""
        pixmap = QPixmap(size)
        pixmap.fill(Qt.transparent)
        
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.Antialiasing)
        
        if icon_type == "download":
            # Mui ten xuong (download)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#1976D2"))
            points = [
                (12, 4), (12, 14),
                (8, 10), (12, 14), (16, 10)
            ]
            painter.drawLine(12, 4, 12, 14)
            painter.drawLine(8, 10, 12, 14)
            painter.drawLine(16, 10, 12, 14)
            painter.drawRect(6, 18, 12, 2)
            
        elif icon_type == "folder":
            # Thu muc
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#FFA726"))
            painter.drawRect(4, 8, 16, 12)
            painter.drawRect(4, 6, 8, 2)
            
        elif icon_type == "folder_open":
            # Mo thu muc
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#FFA726"))
            painter.drawRect(3, 10, 18, 10)
            painter.drawRect(3, 8, 8, 2)
            
        elif icon_type == "cancel":
            # Dau X (cancel)
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#D32F2F"))
            painter.drawEllipse(4, 4, 16, 16)
            painter.setPen(QColor("white"))
            painter.drawLine(9, 9, 15, 15)
            painter.drawLine(15, 9, 9, 15)
            
        elif icon_type == "success":
            # Dau check
            painter.setPen(Qt.NoPen)
            painter.setBrush(QColor("#388E3C"))
            painter.drawEllipse(4, 4, 16, 16)
            painter.setPen(QColor("white"))
            painter.drawLine(8, 12, 11, 15)
            painter.drawLine(11, 15, 16, 9)
            
        elif icon_type == "input":
            # O nhap lieu
            painter.setPen(QColor("#1976D2"))
            painter.setBrush(Qt.NoBrush)
            painter.drawRect(4, 8, 16, 8)
            painter.drawLine(6, 12, 10, 12)
        
        painter.end()
        return QIcon(pixmap)


class ModernStrokeOrderApp(QMainWindow):
    """Ung dung PyQt5 voi giao dien chuyen nghiep"""
    
    CONFIG_FILE = Path.home() / ".stroke_order_config.json"
    
    def __init__(self):
        super().__init__()
        
        # Thiet lap thu muc mac dinh
        home_dir = Path.home()
        self.default_folder = home_dir / "Stroke_images"
        self.default_folder.mkdir(parents=True, exist_ok=True)
        
        # Load config
        config = self._load_config()
        self.folder_path = config.get('last_folder') or str(self.default_folder)
        
        # Tao icon factory
        self.icon_factory = IconFactory()
        
        self.download_thread = None
        
        self._init_ui()
        self._apply_stylesheet()
    
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
    
    def _init_ui(self):
        """Khoi tao giao dien"""
        self.setWindowTitle("Tai Anh Thu Tu Net Chu Han - PyQt5")
        self.setGeometry(100, 100, 900, 700)
        
        # Tao icon cho window (dung Qt standard icon)
        self.setWindowIcon(self.style().standardIcon(self.style().SP_ComputerIcon))
        
        # Widget chinh
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout chinh
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(15)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title
        title = QLabel("Tai Anh Thu Tu Net Chu Han")
        title.setFont(QFont("Arial", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)
        
        # Input group
        input_group = QGroupBox("Nhap Du Lieu")
        input_group.setFont(QFont("Arial", 10, QFont.Bold))
        input_layout = QVBoxLayout()
        
        label = QLabel("Nhap cac ky tu tieng Trung (cach nhau bang dau phay hoac khoang trang):")
        input_layout.addWidget(label)
        
        self.input_entry = QLineEdit()
        self.input_entry.setPlaceholderText("Vi du: ????")
        self.input_entry.setFont(QFont("Arial", 14))
        self.input_entry.setMinimumHeight(40)
        self.input_entry.returnPressed.connect(self.start_download)
        input_layout.addWidget(self.input_entry)
        
        input_group.setLayout(input_layout)
        main_layout.addWidget(input_group)
        
        # Folder group
        folder_group = QGroupBox("Thu Muc Luu Anh")
        folder_group.setFont(QFont("Arial", 10, QFont.Bold))
        folder_layout = QVBoxLayout()
        
        self.folder_label = QLabel(self.folder_path)
        self.folder_label.setWordWrap(True)
        self.folder_label.setStyleSheet("color: #1976D2; padding: 5px;")
        folder_layout.addWidget(self.folder_label)
        
        folder_btn_layout = QHBoxLayout()
        
        self.select_folder_btn = QPushButton("Chon Thu Muc")
        self.select_folder_btn.setIcon(self.style().standardIcon(self.style().SP_DirIcon))
        self.select_folder_btn.setMinimumHeight(40)
        self.select_folder_btn.clicked.connect(self.select_folder)
        folder_btn_layout.addWidget(self.select_folder_btn)
        
        self.open_folder_btn = QPushButton("Mo Thu Muc")
        self.open_folder_btn.setIcon(self.style().standardIcon(self.style().SP_DirOpenIcon))
        self.open_folder_btn.setMinimumHeight(40)
        self.open_folder_btn.clicked.connect(self.open_folder)
        folder_btn_layout.addWidget(self.open_folder_btn)
        
        folder_layout.addLayout(folder_btn_layout)
        folder_group.setLayout(folder_layout)
        main_layout.addWidget(folder_group)
        
        # Control buttons
        control_layout = QHBoxLayout()
        
        self.download_btn = QPushButton("BAT DAU TAI")
        self.download_btn.setIcon(self.style().standardIcon(self.style().SP_ArrowDown))
        self.download_btn.setMinimumHeight(50)
        self.download_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.download_btn.clicked.connect(self.start_download)
        control_layout.addWidget(self.download_btn)
        
        self.cancel_btn = QPushButton("HUY BO")
        self.cancel_btn.setIcon(self.style().standardIcon(self.style().SP_DialogCancelButton))
        self.cancel_btn.setMinimumHeight(50)
        self.cancel_btn.setFont(QFont("Arial", 12, QFont.Bold))
        self.cancel_btn.setEnabled(False)
        self.cancel_btn.clicked.connect(self.cancel_download)
        control_layout.addWidget(self.cancel_btn)
        
        main_layout.addLayout(control_layout)
        
        # Progress group
        progress_group = QGroupBox("Tien Trinh")
        progress_group.setFont(QFont("Arial", 10, QFont.Bold))
        progress_layout = QVBoxLayout()
        
        self.progress_label = QLabel("San sang")
        self.progress_label.setAlignment(Qt.AlignCenter)
        progress_layout.addWidget(self.progress_label)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setMinimumHeight(25)
        self.progress_bar.setTextVisible(True)
        progress_layout.addWidget(self.progress_bar)
        
        progress_group.setLayout(progress_layout)
        main_layout.addWidget(progress_group)
        
        # Result group
        result_group = QGroupBox("Ket Qua")
        result_group.setFont(QFont("Arial", 10, QFont.Bold))
        result_layout = QVBoxLayout()
        
        self.result_text = QTextEdit()
        self.result_text.setReadOnly(True)
        self.result_text.setFont(QFont("Consolas", 10))
        result_layout.addWidget(self.result_text)
        
        result_group.setLayout(result_layout)
        main_layout.addWidget(result_group)
    
    def _apply_stylesheet(self):
        """Ap dung stylesheet"""
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QGroupBox {
                border: 2px solid #1976D2;
                border-radius: 8px;
                margin-top: 10px;
                padding-top: 15px;
                font-weight: bold;
            }
            QGroupBox::title {
                subcontrol-origin: margin;
                left: 10px;
                padding: 0 5px 0 5px;
                color: #1976D2;
            }
            QPushButton {
                background-color: #1976D2;
                color: white;
                border: none;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #1565C0;
            }
            QPushButton:pressed {
                background-color: #0D47A1;
            }
            QPushButton:disabled {
                background-color: #BDBDBD;
            }
            QPushButton#cancel_btn {
                background-color: #D32F2F;
            }
            QPushButton#cancel_btn:hover {
                background-color: #C62828;
            }
            QLineEdit {
                border: 2px solid #BDBDBD;
                border-radius: 5px;
                padding: 8px;
                background-color: white;
            }
            QLineEdit:focus {
                border: 2px solid #1976D2;
            }
            QTextEdit {
                border: 2px solid #BDBDBD;
                border-radius: 5px;
                background-color: white;
            }
            QProgressBar {
                border: 2px solid #BDBDBD;
                border-radius: 5px;
                text-align: center;
                background-color: white;
            }
            QProgressBar::chunk {
                background-color: #1976D2;
                border-radius: 3px;
            }
        """)
        
        # Set style cho cancel button rieng
        self.cancel_btn.setObjectName("cancel_btn")
        self.cancel_btn.setStyleSheet("""
            QPushButton#cancel_btn {
                background-color: #D32F2F;
            }
            QPushButton#cancel_btn:hover {
                background-color: #C62828;
            }
            QPushButton#cancel_btn:disabled {
                background-color: #BDBDBD;
            }
        """)
    
    def select_folder(self):
        """Chon thu muc luu anh"""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Chon Thu Muc Luu Anh",
            self.folder_path
        )
        
        if folder:
            self.folder_path = folder
            self.folder_label.setText(folder)
            self._save_config()
            self.log_message(f"[INFO] Da chon thu muc: {folder}", "info")
    
    def open_folder(self):
        """Mo thu muc trong file explorer"""
        folder_path = Path(self.folder_path)
        
        if not folder_path.exists():
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(self, "Loi", f"Khong the tao thu muc: {e}")
                return
        
        try:
            system = platform.system()
            if system == "Windows":
                os.startfile(str(folder_path))
            elif system == "Darwin":
                subprocess.run(["open", str(folder_path)])
            else:
                subprocess.run(["xdg-open", str(folder_path)])
            self.log_message(f"[INFO] Da mo thu muc: {folder_path}", "info")
        except Exception as e:
            QMessageBox.critical(self, "Loi", f"Khong the mo thu muc: {e}")
    
    def log_message(self, message: str, msg_type: str = "info"):
        """Them message vao result text"""
        # Xac dinh mau sac
        color = "black"
        if msg_type == "success" or "[OK]" in message:
            color = "#388E3C"
        elif msg_type == "error" or "[ERR]" in message:
            color = "#D32F2F"
        elif msg_type == "warning" or "[WARN]" in message:
            color = "#F57C00"
        elif msg_type == "info" or "[INFO]" in message:
            color = "#1976D2"
        
        self.result_text.append(f'<span style="color: {color};">{message}</span>')
    
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
        if self.download_thread and self.download_thread.isRunning():
            return
        
        words_input = self.input_entry.text().strip()
        if not words_input:
            QMessageBox.warning(self, "Canh bao", "Ban chua nhap tu nao!")
            return
        
        folder_path = Path(self.folder_path)
        if not folder_path.exists():
            try:
                folder_path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                QMessageBox.critical(self, "Loi", f"Khong the tao thu muc: {e}")
                return
        
        self._save_config()
        
        # UI state
        self.download_btn.setEnabled(False)
        self.cancel_btn.setEnabled(True)
        self.input_entry.setEnabled(False)
        self.result_text.clear()
        
        # Parse input
        characters = self.parse_input(words_input)
        self.log_message("=" * 60, "info")
        self.log_message("     BAT DAU TAI ANH STROKE     ", "info")
        self.log_message("=" * 60, "info")
        self.log_message(f"[INFO] Tim thay {len(characters)} ky tu: {' '.join(characters)}", "info")
        self.log_message(f"[INFO] Thu muc: {folder_path}", "info")
        self.log_message("-" * 60, "info")
        
        # Start download thread
        self.download_thread = DownloadThread(characters, folder_path)
        self.download_thread.progress_updated.connect(self.update_progress)
        self.download_thread.log_message.connect(self.log_message)
        self.download_thread.finished.connect(self.download_finished)
        self.download_thread.start()
    
    def update_progress(self, current: int, total: int, message: str):
        """Cap nhat progress bar"""
        percent = int((current / total) * 100)
        self.progress_bar.setValue(percent)
        self.progress_label.setText(f"{message} ({percent}%)")
    
    def download_finished(self, success_count: int, fail_count: int):
        """Xu ly khi tai xong"""
        self.log_message("-" * 60, "info")
        if self.download_thread.downloader._cancelled:
            self.log_message("[NOTIFY] Da huy qua trinh tai!", "warning")
            self.progress_label.setText("Da huy")
        else:
            self.log_message("[SUCCESS] Hoan tat!", "success")
            self.progress_label.setText("Hoan thanh")
        
        self.log_message(f"[STATS] Thanh cong: {success_count} | That bai: {fail_count}", "info")
        self.log_message("=" * 60, "info")
        
        self._reset_ui()
    
    def cancel_download(self):
        """Huy qua trinh tai"""
        if self.download_thread and self.download_thread.isRunning():
            self.download_thread.cancel()
            self.cancel_btn.setEnabled(False)
            self.log_message("[NOTIFY] Dang huy...", "warning")
    
    def _reset_ui(self):
        """Reset UI ve trang thai ban dau"""
        self.download_btn.setEnabled(True)
        self.cancel_btn.setEnabled(False)
        self.input_entry.setEnabled(True)


def main():
    """Ham main"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Set application icon
    app.setApplicationName("Stroke Order Downloader")
    
    window = ModernStrokeOrderApp()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
