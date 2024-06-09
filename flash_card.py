from random import shuffle
from csv_files import write_csv_file, read_csv_file
from excel_files import write_excel_file, read_excel_file
from db_files import write_db_file, read_db_file
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
        return f"{self.term} : {self.definition}"

class FlashCardSet:
    def __init__(self, topic):
        self.topic = topic
        self.flashcards = []

    def load_flashcards(self):
        db_name = os.path.join(DATABASE_PATH, self.topic)
        cards = read_db_file(db_name)
        for term, value in cards.items():
            self.flashcards.append(FlashCard(term, value['definition'], value['learned']))
            
    def shuffle_cards(self):
        shuffle(self.flashcards)

    def sort_cards(self):
        self.flashcards = sorted(self.flashcards, key= lambda x: x.term)

    def details(self):
        self.flashcards[0].learned = True
        count = len(self.flashcards)
        learned = 0
        not_learned = 0
        for card in self.flashcards:
            if card.learned:
                learned+= 1
            else:
                not_learned+= 1
        return count, learned, not_learned
    def __str__(self):
        return self.topic

class FlashCardApp:
    def __init__(self):
        self.topics= []
    def get_topics(self):
        files_list = os.listdir(DATABASE_PATH)
        return files_list
        


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
            csvfile_path = FILES_PATH + db_name + '.csv'
        write_csv_file(csvfile_path, read_db_file(db_name))
    
    def export_excel(self, db_name, excelfile_path= None):
        if excelfile_path is None:
            excelfile_path = FILES_PATH + db_name + '.xlsx'
        write_excel_file(excelfile_path, read_db_file(db_name))

    def __str__(self):
        return "Flash Card application"

if __name__ == '__main__':
    app = FlashCardApp()
    # app.import_csv('files\\words.csv', 'database\\فارسی')
    # app.export_csv('farhad')
    # app.export_excel('database\\farhad', 'text.xlsx')
    # app.import_excel("files\\words.xlsx")
    # app.export_excel('database\\words', 'test.xlsx')
    # print(app.get_topics())
    f = FlashCardSet('english')
    f.load_flashcards()
    f.shuffle_cards()
    f.sort_cards()
    print(f.details())
    for i in f.flashcards[:10]:
        print(i)