from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QMenu,
    QLabel, QCheckBox, QPushButton, QWidget, QTextEdit,
    QVBoxLayout, QHBoxLayout, QListWidget
)
from PyQt6.QtGui import QAction, QImage, QPixmap
from PyQt6.QtCore import Qt
from utils.flash_card import FlashCard, FlashCardSet, FlashCardApp
from utils.text_in_image import create_text_image
from topics_form import TopicsWindow
from PIL import ImageQt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        # Menu
        self.menu = self.menuBar()
        file_menu = self.menu.addMenu("&File")
        help_menu = self.menu.addMenu("&Help")
        # File Menu Actions
        topics_action = QAction("Topics", self)
        topics_action.setShortcut('Ctrl+T')
        topics_action.setStatusTip("Open Topics")
        topics_action.triggered.connect(self.open_topics_window)
        exit_action = QAction("Exit", self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.close)
        file_menu.addAction(topics_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        # Help Menu Actions
        about_action = QAction("About", self)
        about_action.setShortcut('Ctrl+H')
        about_action.setStatusTip("About the application")
        help_menu.addAction(about_action)
        # Toolbar
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        toolbar.addAction(topics_action)
        toolbar.addAction(about_action)
        # Image 
        self.image_label = QLabel()
        self.image_label.setFixedSize(300, 240)
        self.image_label.setStatusTip("Image display area")
    
        # Read-Only Edit Box
        self.term_edit_box = QTextEdit()
        self.term_edit_box.setTabChangesFocus(True)
        self.term_edit_box.setReadOnly(True)
        self.term_edit_box.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByKeyboard | Qt.TextInteractionFlag.TextSelectableByMouse)
        self.term_edit_box.setStatusTip("Display Term")
        # initialize term
        text = 'Select\na Topics'
        self.update_image_label(text, dark_mode= True)
        self.term_edit_box.setText(text)
        # Checkbox
        self.learned_checkbox = QCheckBox("Learned")
        self.learned_checkbox.setStatusTip("Mark as learned")
        # Buttons
        self.previous_button = QPushButton("Previous")
        self.previous_button.setStatusTip("Go to the previous term")
        self.flip_button = QPushButton('Flip')
        self.flip_button.setStatusTip("Flip the card")
        self.next_button = QPushButton("Next")
        self.next_button.setStatusTip("Go to the next term")
        # Button Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.previous_button)
        button_layout.addWidget(self.next_button)

        # Main Layout
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.addWidget(self.term_edit_box)
        layout.addWidget(self.learned_checkbox)
        layout.addLayout(button_layout)
        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        # FlashCard App
        self.flashcard_app = FlashCardApp()
        self.flashcard_set = None
    
    def update_image_label(self, text, dark_mode):
        image = create_text_image(text, dark_mode=dark_mode)
        qimage = ImageQt.ImageQt(image)
        pixmap = QPixmap.fromImage(qimage)
        self.image_label.setPixmap(pixmap.scaled(
            self.image_label.width(), self.image_label.height(),
            Qt.AspectRatioMode.KeepAspectRatio)
        )

    def open_topics_window(self):        
        self.topics_window = TopicsWindow(self.flashcard_app)
        self.topics_window.show()
        
    def closeEvent(self, event):
        if hasattr(self, 'topics_window'):
            self.topics_window.close()
        event.accept()

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
