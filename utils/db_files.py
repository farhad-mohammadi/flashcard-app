import dbm
import pickle
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

if __name__ == '__main__':
    # import csv_files
    # datas = csv_files.read_csv_file('files\\words.csv')
    # write_db_file('test', datas )
    datas = read_db_file('test')
    print(datas)
    print(datas['dance'])