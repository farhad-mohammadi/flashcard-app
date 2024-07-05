import configparser

def read_ini_file(filename):
    config = configparser.ConfigParser()
    config.read(filename, encoding= 'utf-8')
    data = {
        'dark_mode': bool(int(config['setting']['dark_mode'])),
        'ask_definition':bool(int(config['setting']['ask_definition'])),
        'active_topic': config['topics']['active']
    }
    return data

def write_ini_file(filename, dark_mode= True, ask_definition= False, active_topic= ''):
    config = configparser.ConfigParser()
    config['setting'] = {'dark_mode': int(dark_mode), 'ask_definition': int(ask_definition)}
    config['topics'] = {'active': active_topic}
    with open(filename, 'w', encoding= 'utf-8') as configfile:
        config.write(configfile)

if __name__=='__main__':
    filename = 'data\\setting.ini'
    write_ini_file()
    print(read_ini_file(filename))
