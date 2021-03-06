#!/usr/bin/python
from ConfigUtils import getBaseConfig
from LogUtils import getModuleLogger
from StringUtils import isValidUrl, soupParse


import os
import re
import sys


cDir = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.abspath(os.path.join(cDir, os.pardir))
baseConfig = getBaseConfig(rootDir)
logging = getModuleLogger(__name__)


def getMalc0deList():
    try:
        raw_list = []

        logging.info('Fetching latest Malc0de list.')

        xml = soupParse('http://malc0de.com/rss')

        if xml:
            for row in xml('description'):
                raw_list.append(row)
            del raw_list[0]

            malList = []

            for row in raw_list:
                location = re.sub('&amp;','&',str(row).split()[1]).replace(',','')
                if location.strip():
                    url = 'http://{0}'.format(location)
                    if isValidUrl(url):
                        malList.append(url)

            return malList

        else:
            logging.error('Empty Malc0de XML. Potential connection error. Please try again later.')

    except Exception as e:
        logging.warning('Problem connecting to Malc0de. Aborting task.')
        logging.exception(sys.exc_info())
        logging.exception(type(e))
        logging.exception(e.args)
        logging.exception(e)

    return []
