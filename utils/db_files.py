import dbm
import pickle
import os

def write_db_file(file_name, datas):
    with dbm.open(file_name, 'c') as db:
        for k, v in datas.items():
            db[k] = pickle.dumps(v)

def read_db_file(file_name):
    datas = {}
    with dbm.open(file_name, 'r') as db:
        for k, v in db.items():
            datas[k.decode('utf-8')] = pickle.loads(v)
    return datas

def delete_data_from_db_file(file_name, key):
    with dbm.open(file_name, 'c') as db:
        if key in list(map(lambda x: x.decode('utf-8'), db.keys())):
            del db[key]

def delete_db_file(filename):
    for ext in ['.dir', '.dat', '.bak']:
        if os.path.exists(filename +ext):
            os.remove(filename + ext)
def edit_db_file(old_filename, new_filename):
    for ext in ['.dir', '.dat', '.bak']:
        if os.path.exists(old_filename +ext):
            os.rename(old_filename + ext, new_filename + ext)

if __name__ == '__main__':
    # import csv_files
    # datas = csv_files.read_csv_file('files\\words.csv')
    # write_db_file('test', datas )
    # write_db_file('database\\farhad', {'iran': {'definition': 'tehran', 'learned': True}})
    # delete_data_from_db_file('database\\farhad', 'movie')
    # datas = read_db_file('database\\farhad')
    # print(datas)
    delete_db_file('database\\jafar')