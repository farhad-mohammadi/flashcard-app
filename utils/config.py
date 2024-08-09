import os
from utils.ini_files import  read_ini_file, write_ini_file

base_dir = os.path.dirname(__file__)
DATABASE_PATH = os.path.join(base_dir, 'database')
FILES_PATH = os.path.join(base_dir, 'files')
FONT_PATH = os.path.join(base_dir, 'fonts\\tahoma.ttf')
BASE_INI_PATH = os.path.join(base_dir, 'data')
INI_PATH = os.path.join(base_dir, 'data\\sett.ini')
DEFAULT_SCHEME_PATH = '.\\utils\\sounds\\default\\'
ALTERNATIVE_SCHEME_PATH = '.\\utils\\sounds\\alternative\\'
CUSTOM_SCHEME_PATH = '.\\utils\\sounds\\custom\\'

if not os.path.exists(DATABASE_PATH):
    os.mkdir(DATABASE_PATH)

if not os.path.exists(FILES_PATH):
    os.mkdir(FILES_PATH)
if not os.path.exists(BASE_INI_PATH):
    os.mkdir(BASE_INI_PATH)
def read_config():

    if not os.path.exists(INI_PATH):
        write_ini_file(INI_PATH)
    return read_ini_file(INI_PATH)

data = read_config()
dark_mode = data['dark_mode']
ask_definition = data['ask_definition']
active_topic = data['active_topic']
