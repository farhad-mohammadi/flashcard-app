from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QMenu,
    QLabel, QCheckBox, QPushButton, QWidget, QTextEdit,
    QVBoxLayout, QHBoxLayout, QListWidget
)
from PyQt6.QtGui import QAction
from utils.flash_card import FlashCard, FlashCardSet, FlashCardApp

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
        topics_button = QAction("Topics", self)
        topics_button.setStatusTip("Open Topics")
        about_button = QAction("About", self)
        about_button.setStatusTip("About the application")
        toolbar.addAction(topics_button)
        toolbar.addAction(about_button)
        # Image 
        self.image_label = QLabel()
        self.image_label.setFixedSize(300, 240)
        self.image_label.setStyleSheet("background-color: white")
        self.image_label.setStatusTip("Image display area")
        # Read-Only Edit Box
        self.term_edit_box = QTextEdit()
        self.term_edit_box.setReadOnly(True)
        self.term_edit_box.setStatusTip("Display Term")
        # Checkbox
        self.learned_checkbox = QCheckBox("Learned")
        self.learned_checkbox.setStatusTip("Mark as learned")
        # Buttons
        self.previous_button = QPushButton("Previous")
        self.previous_button.setStatusTip("Go to the previous term")
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

    def open_topics_window(self):        
        self.topics_window = TopicsWindow()
        self.topics_window.show()
        """
    def close(self):
        self.topics_window.close()
        self.close()
        """
    def closeEvent(self, event):
        if hasattr(self, 'topics_window'):
            self.topics_window.close()
        event.accept()
    
class TopicsWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # Menu
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        terms_menu = menu.addMenu("&Terms")
        # File Menu Submenus
        import_menu = QMenu("Import", self)
        export_menu = QMenu("Export", self)
        file_menu.addMenu(import_menu)
        file_menu.addMenu(export_menu)
        # Import Actions
        import_csv_action = QAction("Import CSV", self)
        import_excel_action = QAction("Import Excel", self)
        import_menu.addAction(import_csv_action)
        import_menu.addAction(import_excel_action)
        # Export Actions
        export_csv_action = QAction("Export CSV", self)
        export_excel_action = QAction("Export Excel", self)
        export_menu.addAction(export_csv_action)
        export_menu.addAction(export_excel_action)
        # Terms Menu Actions
        add_action = QAction("Add", self)
        delete_action = QAction("Delete", self)
        edit_action = QAction("Edit", self)
        terms_menu.addAction(add_action)
        terms_menu.addAction(delete_action)
        terms_menu.addAction(edit_action)
        # Toolbar
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        toolbar.addAction(import_csv_action)
        toolbar.addAction(import_excel_action)
        toolbar.addAction(export_csv_action)
        toolbar.addAction(export_excel_action)
        toolbar.addAction(add_action)
        toolbar.addAction(delete_action)
        toolbar.addAction(edit_action)
        # Lists
        self.topics_list = QListWidget()
        self.terms_list = QListWidget()
        # List Layout
        list_layout = QHBoxLayout()
        list_layout.addWidget(self.topics_list)
        list_layout.addWidget(self.terms_list)
        # Buttons
        self.add_button = QPushButton("Add")
        self.delete_button = QPushButton("Delete")
        self.import_button = QPushButton("Import")
        self.export_button = QPushButton("Export")
        # Button Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.import_button)
        button_layout.addWidget(self.export_button)
        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(list_layout)
        main_layout.addLayout(button_layout)
        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
