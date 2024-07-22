from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QToolBar, QMenu, QDialog, QMessageBox,
    QLabel, QCheckBox, QPushButton, QWidget, QTextEdit, QLineEdit,
    QVBoxLayout, QHBoxLayout, QListWidget, QListWidgetItem, QFileDialog
)
from PyQt6.QtGui import QAction, QActionGroup
from PyQt6.QtCore import Qt, QUrl
from os import path
from utils.flash_card import FlashCard, FlashCardSet, FlashCardApp
from utils.config import DATABASE_PATH, DEFAULT_SCHEME_PATH
from utils.sound import sound

class TopicsWindow(QMainWindow):
    def __init__(self, flashcard_app):
        super().__init__()

        self.sound_path = DEFAULT_SCHEME_PATH
        self.flag_list_check = False
        self.flag_terms_list = False
        self.flag_topic_list = False
        self.flashcard_app = flashcard_app
        #actiongroup for sounds
        self.soundgroup = QActionGroup (self)
        self.soundgroup.triggered.connect (self.scheme)
        # Menu
        menu = self.menuBar()
        self.file_menu = menu.addMenu("&File")
        self.terms_menu = menu.addMenu("&Terms")
        # Import Actions
        self.import_file_action = QAction("Import", self.soundgroup)
        self.import_file_action.triggered.connect(self.import_file)
        # Export Actions
        self.export_file_action = QAction("Export", self.soundgroup)
        self.export_file_action.triggered.connect(self.export_file)
        self.new_topic_action = QAction('New Topic', self.soundgroup)
        self.new_topic_action.triggered.connect(self.new_topic)
        self.delete_topic_action = QAction('Delete Topic', self.soundgroup)
        self.delete_topic_action.triggered.connect(self.delete_topic)
        self.edit_topic_action = QAction('Edit Topic', self.soundgroup)
        self.edit_topic_action.triggered.connect(self.edit_topic)
        self.file_menu.addAction(self.import_file_action)
        self.file_menu.addAction(self.export_file_action)
        self.file_menu.addAction(self.new_topic_action)
        self.file_menu.addAction(self.delete_topic_action)
        self.file_menu.addAction(self.edit_topic_action)
        self.file_menu.aboutToShow.connect(self.scheme) # پخش افکت صوتی

        # Terms Menu Actions
        self.add_action = QAction("Add", self.soundgroup)
        self.add_action.triggered.connect(self.new_data)
        self.delete_action = QAction("Delete", self.soundgroup)
        self.delete_action.triggered.connect(self.delete_data)
        self.edit_action = QAction("Edit", self.soundgroup)
        self.edit_action.triggered.connect(self.edit_data)
        self.terms_menu.addAction(self.add_action)
        self.terms_menu.addAction(self.delete_action)
        self.terms_menu.addAction(self.edit_action)
        self.terms_menu.aboutToShow.connect(self.scheme) # پخش افکت صوتی

        # Toolbar
        toolbar = QToolBar("My main toolbar")
        self.addToolBar(toolbar)
        toolbar.addAction(self.import_file_action)
        toolbar.addAction(self.export_file_action)
        toolbar.addAction(self.add_action)
        toolbar.addAction(self.delete_action)
        toolbar.addAction(self.edit_action)

        # Lists
        self.topics_list = QListWidget()
        self.topics_list.itemActivated.connect(self.mark_load_cards)
        self.active_topic = None
        self.topics_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.topics_list.customContextMenuRequested.connect(self.topics_list_show_menu)
        self.topics_list.currentItemChanged.connect(self.scheme)
        self.terms_list = QListWidget()
        self.terms_list.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.terms_list.customContextMenuRequested.connect(self.terms_list_show_menu)
        self.terms_list.currentItemChanged.connect(self.scheme)
        # List Layout
        list_layout = QHBoxLayout()
        list_layout.addWidget(self.topics_list)
        list_layout.addWidget(self.terms_list)
        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(list_layout)
        self.setCentralWidget(central_widget)
        # start app
        sound(self.sound_path +'topic_window.wav')
        self.load_topics()
        if self.flashcard_app.active_topic :
            item = self.topics_list.findItems(self.flashcard_app.active_topic, Qt.MatchFlag.MatchExactly)
            if item:
                self.mark_load_cards(item[0])

    def load_topics(self):
        self.topics_list.clear()
        self.topics_list.addItems([topic for topic in self.flashcard_app.topics])

    def mark_load_cards(self, current):
        if current is None: return
        if self.active_topic and self.active_topic != current:
            self.active_topic.setText(self.active_topic.text().replace("✓ ", ""))
        topic = current.text()
        if '✓ ' in topic: return
        self.active_topic = current
        current.setText(f"✓ {topic}")
        if self.flashcard_app.active_topic :
            self.flashcard_app.save_flashcard_set()
        self.flashcard_app.set_flashcard_set(topic, ask_definitions= False)
        self.flashcard_app.flashcard_set.sort_cards()
        terms = [t.term for t in self.flashcard_app.flashcard_set.flashcards]
        self.terms_list.clear()
        self.terms_list.addItems(terms)
        self.flashcard_app.set_flashcard_set(topic)
        self.flashcard_app.initialize()
        self.topics_list.setCurrentItem(current)
        if self.flag_list_check:
            sound(self.sound_path +'list_checked.wav')
        self.flag_list_check = True

    def topics_list_show_menu(self, position):
        context_menu = QMenu(self)
        context_menu.addAction(self.import_file_action)
        context_menu.addAction(self.export_file_action)
        context_menu.addAction(self.new_topic_action)
        context_menu.addAction(self.delete_topic_action)
        context_menu.addAction(self.edit_topic_action)
        # show menu
        context_menu.exec(self.topics_list.mapToGlobal(position))

    def terms_list_show_menu(self, position):
        context_menu = QMenu(self)
        context_menu.addAction(self.add_action)
        context_menu.addAction(self.delete_action)
        context_menu.addAction(self.edit_action)
        # show menu
        context_menu.exec(self.topics_list.mapToGlobal(position))

    def new_topic(self):
        self.new_topic_dialog = NewTopic(parent= self, title= 'New Topic')
        if self.new_topic_dialog.exec() == QDialog.DialogCode.Accepted:
            new_topic = self.new_topic_dialog.get_data()
            self.flashcard_app.make_new_topic(new_topic)
            new_item = QListWidgetItem(new_topic)
            self.topics_list.addItem(new_item)
            self.mark_load_cards(new_item)

    def edit_topic(self):
        selected_item = self.topics_list.currentItem()
        if selected_item:
            checked = False
            if '✓ ' in selected_item.text():
                checked = True
                selected_item.setText(selected_item.text().replace('✓ ', ''))
            self.new_topic_dialog = NewTopic(parent= self, title= 'Edit Topic', old_topic= selected_item.text())
            if self.new_topic_dialog.exec() == QDialog.DialogCode.Accepted:
                new_topic = self.new_topic_dialog.get_data()
                self.flashcard_app.edit_flashcard_set(selected_item.text(), new_topic)
                selected_item.setText(new_topic)
                if checked:
                    self.mark_load_cards(selected_item)
    def delete_topic(self):
        selected_item = self.topics_list.currentItem()
        if selected_item:
            if '✓ ' in selected_item.text():
                selected_item.setText(selected_item.text().replace('✓ ', ''))
                self.terms_list.clear()
            self.flashcard_app.delete_flashcard_set(selected_item.text())
            self.topics_list.takeItem(self.topics_list.row(selected_item))

    def new_data(self):
        self.new_data_dialog = NewData(parent= self, title= 'New Data')
        if self.new_data_dialog.exec() == QDialog.DialogCode.Accepted:
            new_term, new_definition= self.new_data_dialog.get_data()
            self.flashcard_app.flashcard_set.add_card(
                {'term': new_term,
                'definition': new_definition,
                'learned': False}
            )
            self.flashcard_app.flashcard_set.sort_cards()
            terms = [t.term for t in self.flashcard_app.flashcard_set.flashcards]
            self.terms_list.clear()
            self.terms_list.addItems(terms)



    def edit_data(self):
        selected_item = self.terms_list.currentItem()
        if selected_item:
            card = self.flashcard_app.flashcard_set.find_card(selected_item.text())
            self.edit_term_dialog = NewData(parent= self, title= 'Edit Data', old_term= card.term, old_definition= card.definition)
            if self.edit_term_dialog .exec() == QDialog.DialogCode.Accepted:
                new_term, new_definition = self.edit_term_dialog.get_data()
                self.flashcard_app.flashcard_set.delete_card(card)
                self.flashcard_app.flashcard_set.add_card(
                    {
                        'term': new_term,
                        'definition': new_definition,
                        'learned': False
                    }
                )
                selected_item.setText(new_term)

    def delete_data(self):
        selected_item = self.terms_list.currentItem()
        if selected_item:
            card  = self.flashcard_app.flashcard_set.find_card(selected_item.text())
            self.flashcard_app.flashcard_set.delete_card(card)
            self.terms_list.takeItem(self.terms_list.row(selected_item))

    def play_effect(self, sound):
        winsound.PlaySound(sound, winsound.SND_ASYNC | winsound.SND_ALIAS )

    def import_file(self, filename):
        filter = 'Excel Files (*.xlsx *.csv)'
        file_name, _ = QFileDialog.getOpenFileName(filter=filter)
        if file_name:
            _, ext = path.splitext(file_name)
            if ext == '.xlsx':
                self.flashcard_app.import_excel(file_name)
            else:
                self.flashcard_app.import_csv(file_name)
            self.load_topics()

    def export_file(self):
        selected_item = self.topics_list.currentItem()
        if selected_item:
            topic = selected_item.text()
            if '✓ ' in topic:
                topic = topic.replace('✓ ', '')
            db_name = path.join(DATABASE_PATH, topic)
            sujjestion = topic
            filter = 'CSV Files (*.csv);;Excel Files (*.xlsx)'
            filename, _ = QFileDialog.getSaveFileName(self, "Save File", sujjestion, filter)
            if filename:
                _, ext = path.splitext(filename)
                if ext == '.xlsx':
                    self.flashcard_app.export_excel(db_name= db_name, excelfile_path= filename)
                else:
                    self.flashcard_app.export_csv(db_name= db_name, csvfile_path= filename)

    def closeEvent(self, event):
        if hasattr(self, 'new_topic_dialog'):
            self.new_topic_dialog .reject()
        if hasattr(self, 'new_data_dialog'):
            self.new_data_dialog.reject()
        event.accept()


    def get_path_scheme(self, path):
        self.sound_path = path

    def scheme(self):
        sender = self.sender()
        if sender == self.soundgroup :
            sound_name = 'generic_btn.wav'
        elif sender == self.file_menu :
            sound_name = 'menu.wav'
        elif sender == self.terms_menu :
            sound_name = 'menu.wav'
        elif sender == self.terms_list and self.flag_terms_list is True:
            sound_name = 'list.wav'
        elif sender == self.topics_list and self.flag_topic_list is True:
            sound_name = 'list.wav'
        else:
            self.flag_terms_list = True
            self.flag_topic_list = True
            return

        sound(self.sound_path +sound_name)



class NewTopic(QDialog):
    def __init__(self, title, old_topic= '', parent=None):
        super().__init__()
        self.setWindowTitle(title)
        self.flashcard_app = parent.flashcard_app
        self.topic_lable = QLabel('Topic name :')
        self.topic_edit = QLineEdit()
        self.topic_edit.setAccessibleName(self.topic_lable.text())
        self.topic_edit.setText(old_topic)
        self.topic_edit.textChanged.connect(self.enable_ok_btn)
        topic_layout = QHBoxLayout()
        topic_layout.addWidget(self.topic_lable)
        topic_layout.addWidget(self.topic_edit)

        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.clicked.connect(self.reject)
        self.ok_btn = QPushButton('Ok')
        if not old_topic:
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
    def __init__(self, title, old_term= '', old_definition='', old_learned= '', parent=None):
        super().__init__()
        self.editing = False if not old_term else True
        self.setWindowTitle(title)
        self.flashcard_app = parent.flashcard_app
        self.term_lable = QLabel('Term :')
        self.term_edit = QTextEdit()
        self.term_edit.setAccessibleName(self.term_lable.text())
        self.term_edit.setTabChangesFocus(True)
        self.term_edit.setPlainText(old_term)
        self.term_edit.textChanged.connect(self.enable_ok_btn)
        term_layout = QHBoxLayout()
        term_layout.addWidget(self.term_lable)
        term_layout.addWidget(self.term_edit)

        self.definition_lable = QLabel('Definition :')
        self.definition_edit = QTextEdit()
        self.definition_edit.setAccessibleName(self.definition_lable.text())
        self.definition_edit.setPlainText(old_definition)
        self.definition_edit.setTabChangesFocus(True)
        definition_layout = QHBoxLayout()
        definition_layout.addWidget(self.definition_lable)
        definition_layout.addWidget(self.definition_edit)

        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.clicked.connect(self.reject)
        self.ok_btn = QPushButton('Ok')
        if not old_term:
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
        if not self.editing and self.term_edit.toPlainText() in self.flashcard_app.flashcard_set.terms:
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
