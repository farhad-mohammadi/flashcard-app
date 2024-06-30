from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QMenu, QDialog, QMessageBox,
    QLabel, QCheckBox, QPushButton, QWidget, QTextEdit, QLineEdit,
    QVBoxLayout, QHBoxLayout, QListWidget
)
from PyQt6.QtGui import QAction
from PyQt6.QtCore import Qt, QUrl
import winsound
from utils.flash_card import FlashCard, FlashCardSet, FlashCardApp

class TopicsWindow(QMainWindow):
    def __init__(self, flashcard_app):
        super().__init__()
        self.flashcard_app = flashcard_app
        # Menu
        menu = self.menuBar()
        file_menu = menu.addMenu("&File")
        terms_menu = menu.addMenu("&Terms")
        # File Menu Submenus
        self.import_menu = QMenu("Import", self)
        self.export_menu = QMenu("Export", self)
        file_menu.addMenu(self.import_menu)
        file_menu.addMenu(self.export_menu)
        # Import Actions
        import_csv_action = QAction("Import CSV", self)
        import_excel_action = QAction("Import Excel", self)
        self.import_menu.addAction(import_csv_action)
        self.import_menu.addAction(import_excel_action)
        # Export Actions
        export_csv_action = QAction("Export CSV", self)
        export_excel_action = QAction("Export Excel", self)
        self.export_menu.addAction(export_csv_action)
        self.export_menu.addAction(export_excel_action)
        self.new_topic_action = QAction('New Topic', self)
        self.new_topic_action.triggered.connect(self.get_new_topic)
        file_menu.addAction(self.new_topic_action)
        # Terms Menu Actions
        self.add_action = QAction("Add", self)
        self.add_action.triggered.connect(self.get_new_data)
        self.delete_action = QAction("Delete", self)
        self.edit_action = QAction("Edit", self)
        terms_menu.addAction(self.add_action)
        terms_menu.addAction(self.delete_action)
        terms_menu.addAction(self.edit_action)
        # Toolbar
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        toolbar.addAction(import_csv_action)
        toolbar.addAction(import_excel_action)
        toolbar.addAction(export_csv_action)
        toolbar.addAction(export_excel_action)
        toolbar.addAction(self.add_action)
        toolbar.addAction(self.delete_action)
        toolbar.addAction(self.edit_action)
        # Lists
        self.topics_list = QListWidget()
        self.topics_list.itemActivated.connect(self.mark_load_cards)
        self.active_topic = None
        self.topics_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.topics_list.customContextMenuRequested.connect(self.topics_list_show_context_menu)
        self.terms_list = QListWidget()
        self.terms_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        # List Layout
        list_layout = QHBoxLayout()
        list_layout.addWidget(self.topics_list)
        list_layout.addWidget(self.terms_list)
        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(list_layout)
        self.setCentralWidget(central_widget)
        # start app
        self.load_topics()
    def load_topics(self):
        self.topics_list.addItems([topic for topic in self.flashcard_app.topics])

    def mark_load_cards(self, current):
        if current is None: return
        if self.active_topic and self.active_topic != current:
            self.active_topic.setText(self.active_topic.text().replace("✓ ", ""))
        topic = current.text()
        if '✓ ' in topic: return
        self.active_topic = current
        current.setText(f"✓ {topic}")
        self.flashcard_app.set_flashcard_set(topic, ask_definitions= False)
        self.flashcard_app.flashcard_set.sort_cards()
        terms = [t.term for t in self.flashcard_app.flashcard_set.flashcards]
        self.terms_list.clear()
        self.terms_list.addItems(terms)
        self.play_effect('sounds\\checked.wav')

    def topics_list_show_context_menu(self, position):
        context_menu = QMenu(self)
        context_menu.addMenu(self.import_menu)
        context_menu.addMenu(self.export_menu)
        context_menu.addAction(self.add_action)
        context_menu.addAction(self.delete_action)
        context_menu.addAction(self.edit_action)
        # show menu
        context_menu.exec(self.topics_list.mapToGlobal(position))

    def get_new_topic(self):
        self.new_topic_dialog = NewTopic(self)
        if self.new_topic_dialog.exec() == QDialog.DialogCode.Accepted:
            new_topic = self.new_topic_dialog.get_data()
            print(new_topic)

    def get_new_data(self):
        self.new_data_dialog = NewData(self)
        if self.new_data_dialog.exec() == QDialog.DialogCode.Accepted:
            new_term, new_definition= self.new_data_dialog.get_data()
            print(new_term, new_definition)

    def play_effect(self, sound):
        winsound.PlaySound(sound, winsound.SND_ASYNC | winsound.SND_ALIAS )

    def closeEvent(self, event):
        if hasattr(self, 'new_topic_dialog'):
            self.new_topic_dialog .reject()
        if hasattr(self, 'new_data_dialog'):
            self.new_data_dialog.reject()
        event.accept()

class NewTopic(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('New Topic')
        self.flashcard_app = parent.flashcard_app
        self.topic_lable = QLabel('Topic name :')
        self.topic_edit = QLineEdit()
        self.topic_edit.setAccessibleName(self.topic_lable.text())
        self.topic_edit.textChanged.connect(self.enable_ok_btn)
        topic_layout = QHBoxLayout()
        topic_layout.addWidget(self.topic_lable)
        topic_layout.addWidget(self.topic_edit)

        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.clicked.connect(self.reject)
        self.ok_btn = QPushButton('Ok')
        self.ok_btn.setDisabled(True)
        self.ok_btn.clicked.connect(self.accepted_data)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.ok_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(topic_layout)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)
        self.show()

    def enable_ok_btn(self):
        self.ok_btn.setEnabled(bool(self.topic_edit.text()))

    def accepted_data(self):
        if self.topic_edit.text() in self.flashcard_app.topics:
            msg = QMessageBox(self)
            msg.setWindowTitle('Duplicate topic')
            msg.setText('The entered topic is duplicate!')
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return
        self.accept()

    def get_data(self):
        return self.topic_edit.text()

class NewData(QDialog):
    def __init__(self, parent=None):
        super().__init__()
        self.setWindowTitle('New Data')
        self.flashcard_app = parent.flashcard_app
        self.term_lable = QLabel('Term :')
        self.term_edit = QTextEdit()
        self.term_edit.setAccessibleName(self.term_lable.text())
        self.term_edit.setTabChangesFocus(True)
        self.term_edit.textChanged.connect(self.enable_ok_btn)
        term_layout = QHBoxLayout()
        term_layout.addWidget(self.term_lable)
        term_layout.addWidget(self.term_edit)

        self.definition_lable = QLabel('Definition :')
        self.definition_edit = QTextEdit()
        self.definition_edit.setAccessibleName(self.definition_lable.text())
        self.definition_edit.setTabChangesFocus(True)
        definition_layout = QHBoxLayout()
        definition_layout.addWidget(self.definition_lable)
        definition_layout.addWidget(self.definition_edit)

        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.clicked.connect(self.reject)
        self.ok_btn = QPushButton('Ok')
        self.ok_btn.setDisabled(True)
        self.ok_btn.clicked.connect(self.accepted_data)
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.ok_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(term_layout)
        main_layout.addLayout(definition_layout)
        main_layout.addLayout(btn_layout)
        self.setLayout(main_layout)
        self.show()

    def enable_ok_btn(self):
        self.ok_btn.setEnabled(bool(self.term_edit.toPlainText()))

    def accepted_data(self):
        if self.term_edit.toPlainText() in self.flashcard_app.flashcard_set.terms:
            msg = QMessageBox(self)
            msg.setWindowTitle('Duplicate term')
            msg.setText('The entered term is duplicate!')
            msg.setIcon(QMessageBox.Icon.Critical)
            msg.exec()
            return
        self.accept()

    def get_data(self):
        return self.term_edit.toPlainText(), self.definition_edit.toPlainText()

if __name__ == '__main__':
    
    app = QApplication([])
    window = TopicsWindow(FlashCardApp())
    window.show()
    app.exec()
