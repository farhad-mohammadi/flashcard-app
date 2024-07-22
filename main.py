from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QMenu,
    QLabel, QCheckBox, QPushButton, QWidget, QTextEdit,
    QVBoxLayout, QHBoxLayout, QListWidget
)
from PyQt6.QtGui import QAction, QImage, QPixmap, QActionGroup
from PyQt6.QtCore import Qt
from utils.flash_card import FlashCard, FlashCardSet, FlashCardApp
from utils.text_into_image import create_text_image
from utils import config 
from utils.ini_files import write_ini_file
from topics_form import TopicsWindow
from PIL import ImageQt
from utils.sound import sound


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle ("flashcard app")

        #action group for sfx
        self.soundgroup = QActionGroup (self)
        self.soundgroup.triggered.connect (self.scheme)
        self.sound_path = config.DEFAULT_SCHEME_PATH


        # Menu
        self.menu = self.menuBar()
        self.file_menu = self.menu.addMenu("&File")
        self.tools_menu = self.menu.addMenu("&Tools")
        self.help_menu = self.menu.addMenu("&Help")
        # File Menu Actions
        topics_action = QAction("Topics", self.soundgroup)
        topics_action.setShortcut('Ctrl+T')
        topics_action.setStatusTip("Open Topics")
        topics_action.triggered.connect(self.open_topics_window)
        exit_action = QAction("Exit", self.soundgroup)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.setStatusTip("Exit application")
        exit_action.triggered.connect(self.close)
        self.file_menu.addAction(topics_action)
        self.file_menu.addSeparator()
        self.file_menu.addAction(exit_action)
        self.file_menu.aboutToShow.connect(self.scheme) # پخش افکت صوتی


        # Tools Menu Actions
        self.scheme_menu = QMenu("sound scheme", self)
        self.tools_menu.addMenu(self.scheme_menu)
        default_scheme = QAction("default", self)
        default_scheme.triggered.connect(self.on_default_scheme)

        alternative_scheme = QAction("alternative", self)
        alternative_scheme.triggered.connect(self.on_alternative_scheme)

        custom_scheme = QAction("custom", self)
        custom_scheme.triggered.connect(self.on_custom_scheme)
        self.scheme_menu.addAction(default_scheme)
        self.scheme_menu.addAction(alternative_scheme)
        self.scheme_menu.addAction(custom_scheme)
        self.tools_menu.aboutToShow.connect(self.scheme)
        self.scheme_menu.aboutToShow.connect(self.scheme) # پخش افکت صوتی


        # Help Menu Actions
        about_action = QAction("About", self.soundgroup)
        about_action.setShortcut('Ctrl+H')
        about_action.setStatusTip("About the application")
        self.help_menu.addAction(about_action)
        self.help_menu.aboutToShow.connect(self.scheme) # پخش افکت صوتی

        # Toolbar
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        toolbar.addAction(topics_action)
        toolbar.addAction(about_action)
        # Image 
        self.image_label = QLabel()
        width = 700
        height = width * 9 // 16
        self.image_label.setFixedSize(width, height)
        self.image_label.setStatusTip("Image display area")

        # Read-Only Edit Box
        self.term_edit_box = QTextEdit()
        self.term_edit_box.setTabChangesFocus(True)
        self.term_edit_box.setReadOnly(True)
        self.term_edit_box.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByKeyboard | Qt.TextInteractionFlag.TextSelectableByMouse)
        self.term_edit_box.setStatusTip("Display Term")
        # Checkbox
        self.learned_checkbox = QCheckBox("Learned")
        self.learned_checkbox.setStatusTip("Mark as learned")
        self.learned_checkbox.setDisabled(True)
        self.learned_checkbox.stateChanged.connect(self.change_learned_status)
        self.learned_checkbox.checkStateChanged.connect (self.scheme)
        self.learned_checkbox.setShortcut ('ctrl+l')
        self.learned_checkbox.setAccessibleDescription ('ctrl+l')
        
        # Buttons
        self.previous_button = QPushButton("Previous")
        self.previous_button.setStatusTip("Go to the previous term")
        self.previous_button.setDisabled(True)
        self.previous_button.clicked.connect(self.previous_card)
        self.previous_button.clicked.connect (self.scheme)
        self.previous_button.setShortcut ('ctrl+p')
        self.previous_button.setAccessibleDescription ('ctrl+p')
        self.flip_button = QPushButton('Flip')
        self.flip_button.setStatusTip("Flip the card")
        self.flip_button.setDisabled(True)
        self.flip_button.clicked.connect(self.flip_card)
        self.flip_button.clicked.connect (self.scheme)
        self.flip_button.setShortcut ('ctrl+f')
        self.flip_button.setAccessibleDescription ('ctrl+f')
        self.next_button = QPushButton("Next")
        self.next_button.setStatusTip("Go to the next term")
        self.next_button.setDisabled(True)
        self.next_button.clicked.connect(self.next_card)
        self.next_button.clicked.connect (self.scheme)
        self.next_button.setShortcut ('ctrl+n')
        self.next_button.setAccessibleDescription ('ctrl+n')
        # Button Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.previous_button)
        button_layout.addWidget(self.flip_button)
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
        sound(self.sound_path +'welcome.wav')
        # FlashCard  App
        self.flashcard_app = FlashCardApp()
        
        self.active_flashcard = config.active_topic
        self.dark_mode = config.dark_mode
        self.ask_definition = config.ask_definition
        if self.active_flashcard : self.flashcard_app.set_flashcard_set(self.active_flashcard)
        self.initialize()
        
        self.flashcard_app.initialize = self.initialize

    def initialize(self):
        if not self.flashcard_app.active_topic:
            text = 'Select\na Topic'
            self.update_image_label(text, dark_mode= self.dark_mode)
            self.term_edit_box.setText(text)
            return
        self.flashcard_app.flashcard_set.shuffle_cards()
        if len(self.flashcard_app.flashcard_set.not_learned_flashcards) > 0:
            self.flashcard_app.active_card_pos -= 1
            self.next_card()
            self.previous_button.setDisabled(True)

    def next_card(self):
        card, length = self.flashcard_app.next_card()
        self.learned_checkbox.setChecked(card.learned)
        text = card.term
        self.update_image_label(text, dark_mode= self.dark_mode)
        self.term_edit_box.setText(text)
        self.previous_button.setEnabled(True)
        self.flip_button.setEnabled(True)
        if length > 0 :
            self.next_button.setEnabled(True)
        else:
            self.next_button.setDisabled(True)
        self.term_edit_box.setFocus()
        self.learned_checkbox.setDisabled(True)


    def previous_card(self):
        card, length = self.flashcard_app.previous_card()
        self.learned_checkbox.setChecked(card.learned)
        text = card.term
        self.update_image_label(text, dark_mode= self.dark_mode)
        self.term_edit_box.setText(text)
        self.next_button.setEnabled(True)
        self.flip_button.setEnabled(True)
        if length > 0 :
            self.previous_button.setEnabled(True)
        else:
            self.previous_button.setDisabled(True)
        self.term_edit_box.setFocus()
        

    def flip_card(self):
        if self.ask_definition :
            text = self.flashcard_app.active_card.term
        else:
            text = self.flashcard_app.active_card.definition
        self.update_image_label(text, dark_mode= self.dark_mode)
        self.term_edit_box.setText(text)
        self.term_edit_box.setFocus()
        self.learned_checkbox.setEnabled(True)

    def change_learned_status(self):
        self.flashcard_app.active_card.learned = self.learned_checkbox.isChecked()
        
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
        self.topics_window.get_path_scheme(self.sound_path       )
        self.topics_window.show()
        
    def closeEvent(self, event):
        write_ini_file(config.INI_PATH,dark_mode= self.dark_mode, ask_definition= self.ask_definition, active_topic= self.flashcard_app.active_topic)
        self.flashcard_app.save_flashcard_set()
        if hasattr(self, 'topics_window'):
            self.topics_window.close()
        event.accept()


    #setting source and playing sounds
    def on_default_scheme(self):
        sound_path = config.DEFAULT_SCHEME_PATH
        if hasattr(self, 'topics_window'):
            self.topics_window.get_path_scheme(self.sound_path       )

    def on_alternative_scheme(self):
        self.sound_path = config.ALTERNATIVE_SCHEME_PATH
        if hasattr(self, 'topics_window'):
            self.topics_window.get_path_scheme(self.sound_path       )


    def on_custom_scheme(self):
        self.sound_path        = config.CUSTOM_SCHEME_PATH
        if hasattr(self, 'topics_window'):
            self.topics_window.get_path_scheme(self.sound_path       )

    def scheme (self):
        sender = self.sender()
        if sender == self.soundgroup :
            sound_name = "generic_btn.wav"
        elif sender == self.file_menu :
            sound_name = 'menu.wav'
        elif sender == self.tools_menu :
            sound_name = 'menu.wav'
        elif sender == self.scheme_menu :
            sound_name = 'menu.wav'
        elif sender == self.help_menu :
            sound_name = 'menu.wav'
        elif sender == self.previous_button :
            sound_name = "previous.wav"
        elif sender == self.next_button :
            sound_name = "next.wav"
        elif sender == self.flip_button :
            sound_name = "flip.wav"
        elif sender == self.learned_checkbox:
            if self.learned_checkbox.isChecked () == True :
                sound_name ="checked.wav"
            else:
                sound_name = "unchecked.wav"
        sound(self.sound_path +sound_name)




if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
