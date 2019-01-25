#!/usr/bin/python3
# -*- coding: utf-8 -*-
import codecs
import logging
import configparser
import requests
import json

from loader_memrise import loader_memrise


# *********************************************
def show_wait(text, i):
    if (i % 4) == 0:
        print(text + '%s' % ("/"), end='\r')
    elif (i % 4) == 1:
        print(text + '%s' % ("-"), end='\r')
    elif (i % 4) == 2:
        print(text + '%s' % ("\\"), end='\r')
    elif (i % 4) == 3:
        print(text + '%s' % ("|"), end='\r')
    elif i == -1:
        print(text + 'Done!')
        print()


# *********************************************
def get_parms_from_conf_file(conf_file_name, default_parms):
    ret_params = default_parms.copy()
    config = configparser.ConfigParser()

    try:
        logging.debug("Opening %s file" % conf_file_name)
        config.read(conf_file_name)
    except Exception as e:
        print("Error reading {} file".format(conf_file_name))
        logging.error("Error reading %s file" % conf_file_name)
        raise e

    try:
        ret_params['quizlet_username'] = config['SETTINGS']['quizlet_username']
    except Exception as e:
        logging.error("Error reading ['SETTINGS']['quizlet_username'] in %s file" % conf_file_name)
        ret_params['quizlet_username'] = None

    try:
        ret_params['quizlet_password'] = config['SETTINGS']['quizlet_password']
    except Exception as e:
        logging.error("Error reading ['SETTINGS']['quizlet_password'] in %s file" % conf_file_name)
        ret_params['quizlet_password'] = None

    try:
        ret_params['quizlet_folder'] = config['SETTINGS']['quizlet_folder']
    except Exception as e:
        logging.error("Error reading ['SETTINGS']['quizlet_folder'] in %s file" % conf_file_name)
        ret_params['quizlet_folder'] = None

    return ret_params


memrise_url = "https://www.memrise.com/course/192612/estonian-tere-tere-jalle-keel-selgeks-a0-b1/104/"

conf_file_name = "settings.conf"
save_page_to_file = False
page_filename = "page.html"

def_parms = dict(quizlet_username=None,
                 quizlet_password=None,
                 quizlet_folder=None)

logging.basicConfig(filename='memzlet.log',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s \
                    - %(lineno)d - %(message)s')

logging.debug('#' * 50)

version = '0.01'

print('Memrise to quizlet importer. Version %s' % version)
logging.debug('Script version is %s' % version)

logging.debug('----   ---   start working   ----   ---')
print("Opening {} configuration file".format(conf_file_name))

logging.debug("Opening %s configuration file" % conf_file_name)

loaded_parms = get_parms_from_conf_file(conf_file_name, def_parms)

for parm_key, parm_value in loaded_parms.items():
    if parm_value is None:
        logging.debug("Params %s is None. Stop script" % parm_key)
        print("Params %s is None. Stop script" % parm_key)
        exit()

if memrise_url is None:
        logging.debug("memrise url is None. Stop script")
        print("memrise url is None. Stop script")
        exit()

text_to_parse = None
memrise = loader_memrise()

while memrise_url:
    req = requests.get(memrise_url)
    if req.status_code == requests.codes.ok:
        text_to_parse = req.text

        parse_result = memrise.parse(text_to_parse)
        filename = parse_result['filename']

        with codecs.open(filename, mode='w', encoding='UTF-8') as parsed_text_out_file:
            json.dump(parse_result['title'], parsed_text_out_file, indent=4, ensure_ascii=False)
            json.dump(parse_result['terms'], parsed_text_out_file, indent=4, ensure_ascii=False)
            parsed_text_out_file.close()

        memrise_url = parse_result['next_url']

        print(memrise_url)

        if save_page_to_file:
            with codecs.open(page_filename, mode='w', encoding='utf8') as f:
                f.write(text_to_parse)
                f.close()

    else:
        logging.debug("Status code is %s. Stop script" % req.status_code)
        print("Status code is %s. Stop script" % req.status_code)
        exit()
