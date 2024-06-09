import csv

def read_csv_file(file_name):
    with open(file_name, 'r', encoding='utf_8') as file:
        data = csv.reader(file)
        datas = {}
        for i in data:
            datas[i[0]] = {'definition': i[1], 'learned': False}
    return datas

def write_csv_file(file_name, datas):
    with open(file_name, 'w', newline='', encoding='utf_8') as file:
        data = csv.writer(file)
        for k, v in datas.items():
            data.writerow([k, v['definition']])

if __name__ == '__main__':
    datas = read_csv_file('files\\words.csv')
    print(datas)
    write_csv_file('test.csv', datas)