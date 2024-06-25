from random import shuffle
from utils.csv_files import write_csv_file, read_csv_file
from utils.excel_files import write_excel_file, read_excel_file
from utils.db_files import write_db_file, read_db_file
import os

base_dir = os.path.dirname(__file__)
DATABASE_PATH = os.path.join(base_dir, 'database')
FILES_PATH = os.path.join(base_dir, 'files')

class FlashCard:
    def __init__(self, term, definition, learned):
        self.term = term
        self.definition = definition
        self.learned = learned
    def __str__(self):
        return f"{self.term} :: {self.definition}"

class FlashCardSet:
    def __init__(self, topic):
        self.topic = topic
        self.flashcards = self.load_flashcards()
        self.learned_flashcards = []
        self.not_learned_flashcards = []
        
    def load_flashcards(self, ask_definition= False):
        db_name = os.path.join(DATABASE_PATH, self.topic)
        cards = read_db_file(db_name)
        if not ask_definition:
            return [FlashCard(t, v['definition'], v['learned']) for t,v in cards.items()]
        else:
            return [FlashCard(v['definition'], t, v['learned']) for t,v in cards.items()]

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
    def get_topics(self):
        files_list = os.listdir(DATABASE_PATH)
        self.topics =         [topic[:-4] for topic in files_list if topic[-3:] == 'dat']
        
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
