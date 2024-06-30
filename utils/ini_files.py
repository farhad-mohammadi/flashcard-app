import configparser

def read_ini_file(filename):
    config = configparser.ConfigParser()
    config.read(filename)
    data = {
        'dark_mode': config['setting']['dark_mode'],
        'active_topic': config['topics']['active']
    }
    return data

def write_ini_file(dark_mode= False, active_topic= ''):
    config = configparser.ConfigParser()
    config['setting'] = {'dark_mode': int(dark_mode)}
    config['topics'] = {'active': active_topic}
    with open(filename, 'w') as configfile:
        config.write(configfile)

if __name__=='__main__':
    filename = 'data\\setting.ini'
    write_ini_file()
    print(read_ini_file(filename))
