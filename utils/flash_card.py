from random import shuffle
from utils.csv_files import write_csv_file, read_csv_file
from utils.excel_files import write_excel_file, read_excel_file
from utils.db_files import write_db_file, read_db_file, delete_data_from_db_file, delete_db_file, edit_db_file
import os
from utils.config import DATABASE_PATH, FILES_PATH

class FlashCard:
    def __init__(self, term, definition, learned):
        self.term = term
        self.definition = definition
        self.learned = learned
    def __str__(self):
        return f"{self.term} : {self.definition} : {self.learned}"

class FlashCardSet:
    def __init__(self):
        self.learned_flashcards = []
        self.not_learned_flashcards = []
        self.flashcards = []
        self.terms = []
        self.topic = None
        self.db_name = None

    def load_flashcards(self, topic, ask_definition= False):
        self.db_name = os.path.join(DATABASE_PATH, topic)
        cards = read_db_file(self.db_name)
        self.topic = topic
        if not ask_definition:
            self.flashcards = [FlashCard(t, v['definition'], v['learned']) for t,v in cards.items()]
        else:
            self.flashcards = [FlashCard(v['definition'], t, v['learned']) for t,v in cards.items()]
        self.terms = list(cards.keys())
        self.separate_cards()
        return self.flashcards
    
    def to_dict(self):
        return {c.term : {'definition': c.definition, 'learned': c.learned} for c in self.flashcards}
    
    def add_card(self, card):
        card = FlashCard(**card)
        self.flashcards.append(card)
        write_db_file(self.db_name, {card.term: {'definition': card.definition, 'learned': card.learned}})

    def delete_card(self, card):
        if not isinstance(card, FlashCard):
            card = FlashCard(**card)
        self.flashcards.remove(card)
        delete_data_from_db_file(self.db_name, card.term)

    def find_card(self, term):
        for card in self.flashcards:
            if card.term == term :
                return card

    def shuffle_cards(self):
        shuffle(self.flashcards)

    def sort_cards(self, reverse= False):
        self.flashcards = sorted(self.flashcards, key= lambda x: x.term.lower(), reverse= reverse)

    def separate_cards(self):
        self.learned_flashcards = []
        self.not_learned_flashcards = []
        for card in self.flashcards:
            if card.learned:
                self.learned_flashcards.append(card)
            else:
                self.not_learned_flashcards.append(card)
            
    def details(self):
        return len(self.flashcards), len(self.learned_flashcards), len(self.not_learned_flashcards)
    
    def __str__(self):
        return self.topic

class FlashCardApp:
    def __init__(self):
        self.topics= []
        self.get_topics()
        self.flashcard_set = FlashCardSet()
        self.active_topic = None
        self.active_card = None
        self.active_card_pos = 0

    def get_topics(self):
        files_list = os.listdir(DATABASE_PATH)
        self.topics =         [topic[:-4] for topic in files_list if topic[-3:] == 'dat']
        
    def set_flashcard_set(self, topic, ask_definitions= False):
        self.flashcard_set.load_flashcards(topic, ask_definition= False)
        self.active_topic = topic
        self.active_card = None
        self.active_card_pos = 0
        
    def next_card(self):
        self.active_card_pos += 1
        if self.active_card_pos < len(self.flashcard_set.not_learned_flashcards) :
            self.active_card = self.flashcard_set.not_learned_flashcards[self.active_card_pos]
            return self.active_card, len(self.flashcard_set.not_learned_flashcards) - self.active_card_pos -1

    def previous_card(self):
        self.active_card_pos -= 1
        if self.active_card_pos >= 0:
            self.active_card = self.flashcard_set.not_learned_flashcards[self.active_card_pos]
            return self.active_card, self.active_card_pos


    def make_new_topic(self, topic):
        db_name = os.path.join(DATABASE_PATH, topic)
        self.active_topic =  topic
        self.active_card = None
        self.active_card_pos = 0
        write_db_file(db_name, {})

    def delete_flashcard_set(self, topic):
        db_name = os.path.join(DATABASE_PATH, topic)
        self.active_topic = None
        self.active_card = None
        self.active_card_pos = 0
        delete_db_file(db_name)
        
    def edit_flashcard_set(self, old_topic, new_topic):
        old_db_name = os.path.join(DATABASE_PATH, old_topic)
        new_db_name = os.path.join(DATABASE_PATH, new_topic)
        edit_db_file(old_db_name, new_db_name)
        self.set_flashcard_set(new_topic, ask_definitions= False)

    def save_flashcard_set(self):
        db_name = os.path.join(DATABASE_PATH, self.active_topic)
        write_db_file(db_name, self.flashcard_set.to_dict())

    def import_csv(self, csvfile_path, db_name= None):
        if db_name is None:
            db_name = os.path.splitext(os.path.basename(csvfile_path))[0]
            db_name = os.path.join(DATABASE_PATH, db_name)
        write_db_file(db_name, read_csv_file(csvfile_path))

    def import_excel(self, excelfile_path, db_name= None):
        if db_name is None:
            db_name = os.path.splitext(os.path.basename(excelfile_path))[0]
            db_name = os.path.join(DATABASE_PATH, db_name)
        write_db_file(db_name, read_excel_file(excelfile_path))

    def export_csv(self, db_name, csvfile_path= None):
        if csvfile_path is None:
            csvfile_path = os.path.join(FILES_PATH , db_name + '.csv')
        write_csv_file(csvfile_path, read_db_file(db_name))
    
    def export_excel(self, db_name, excelfile_path= None):
        if excelfile_path is None:
            excelfile_path = os.path.join(FILES_PATH , db_name + '.xlsx')
        write_excel_file(excelfile_path, read_db_file(db_name))

    def __str__(self):
        return "Flash Card application"

