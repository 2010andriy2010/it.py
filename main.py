import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QFileDialog, QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout, QStatusBar, QWidget
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QColor
from PIL import Image, ImageFilter

class ImageEditor(QMainWindow):  # Change to QMainWindow
    def __init__(self):
        super().__init__()
        self.image = None
        self.filename = None
        self.current_dir = ''
        self.save_dir = "Modified/"
        self.extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
        self.init_ui()
        self.setup_connections()
        
    def init_ui(self):
        self.resize(800, 600)
        self.setWindowTitle('Scary Image Editor')

        self.lb_image = QLabel("Cursed Image")
        self.lb_image.setAlignment(Qt.AlignCenter)
        self.lb_image.setStyleSheet("color: red; font-size: 24px; font-weight: bold;")  # Blood red text

        # Spooky Button Texts
        self.btn_dir = QPushButton("Open the Haunted Folder")
        self.lw_files = QListWidget()
        self.btn_left = QPushButton("Turn Left")
        self.btn_right = QPushButton("Turn Right")
        self.btn_flip = QPushButton("Flip Into Madness")
        self.btn_sharp = QPushButton("Sharpen the Horror")
        self.btn_bw = QPushButton("Turn it Into Shadows")

        # Dark Theme
        self.setStyleSheet("background-color: #1a1a1a; color: white; font-size: 14px;")

        row = QHBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()

        col1.addWidget(self.btn_dir)
        col1.addWidget(self.lw_files)

        col2.addWidget(self.lb_image, 95)
        row_tools = QHBoxLayout()
        row_tools.addWidget(self.btn_left)
        row_tools.addWidget(self.btn_right)
        row_tools.addWidget(self.btn_flip)
        row_tools.addWidget(self.btn_sharp)
        row_tools.addWidget(self.btn_bw)
        col2.addLayout(row_tools)

        row.addLayout(col1, 20)
        row.addLayout(col2, 80)

        central_widget = QWidget(self)  # Create a QWidget for the central area
        central_widget.setLayout(row)
        self.setCentralWidget(central_widget)  # Set the central widget

        # Add a status bar for spooky messages
        self.status_bar = QStatusBar(self)  # Set status bar to the window
        self.setStatusBar(self.status_bar)

    def setup_connections(self):
        self.btn_dir.clicked.connect(self.show_filename_list)
        self.lw_files.currentRowChanged.connect(self.show_chosen_image)
        self.btn_left.clicked.connect(self.do_left)
        self.btn_right.clicked.connect(self.do_right)
        self.btn_flip.clicked.connect(self.do_flip)
        self.btn_sharp.clicked.connect(self.do_sharpen)
        self.btn_bw.clicked.connect(self.do_bw)

    def filter_files(self, files):
        result = []
        for filename in files:
            for ext in self.extensions:
                if filename.endswith(ext):
                    result.append(filename)
        return result            

    def show_filename_list(self):
        self.current_dir = QFileDialog.getExistingDirectory()

        if self.current_dir:
            filenames = self.filter_files(os.listdir(self.current_dir))
            self.lw_files.clear()
            for filename in filenames:
                self.lw_files.addItem(filename)

    def show_image(self, path):
        self.lb_image.hide()
        pixmap_image = QPixmap(path)

        w, h = self.lb_image.width(), self.lb_image.height()

        pixmap_image = pixmap_image.scaled(w, h, Qt.KeepAspectRatio)
        self.lb_image.setPixmap(pixmap_image)
        self.lb_image.show()

    def load_image(self, filename):
        self.filename = filename
        image_path = os.path.join(self.current_dir, filename)
        self.image = Image.open(image_path)
        
    def show_chosen_image(self):
        if self.lw_files.currentRow() >= 0:
            filename = self.lw_files.currentItem().text()
            self.load_image(filename)
            self.show_image(os.path.join(self.current_dir, filename))

    def save_image(self):
        path = os.path.join(self.current_dir, self.save_dir)
        
        if not(os.path.exists(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)
        return image_path

    def do_bw(self):
        if self.image:
            self.image = self.image.convert("L")
            saved_path = self.save_image()
            self.show_image(saved_path)
            self.status_bar.showMessage('The image has turned to Shadows...')

    def do_left(self):
        if self.image:
            self.image = self.image.transpose(Image.Transpose.ROTATE_90)
            saved_path = self.save_image()
            self.show_image(saved_path)
            self.status_bar.showMessage('The image turns left into darkness...')

    def do_right(self):
        if self.image:
            self.image = self.image.transpose(Image.Transpose.ROTATE_270)
            saved_path = self.save_image()
            self.show_image(saved_path)
            self.status_bar.showMessage('The image escapes right...')

    def do_sharpen(self):
        if self.image:
            self.image = self.image.filter(ImageFilter.SHARPEN)
            saved_path = self.save_image()
            self.show_image(saved_path)
            self.status_bar.showMessage('The image is now sharper, more cursed!')

    def do_flip(self):
        if self.image:
            self.image = self.image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
            saved_path = self.save_image()
            self.show_image(saved_path)
            self.status_bar.showMessage('The image flips into madness...')

if __name__ == '__main__':
    app = QApplication([])
    editor = ImageEditor()
    editor.show()
    app.exec()