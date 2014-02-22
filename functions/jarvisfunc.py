##This file contains useful functions
import xml.etree.ElementTree as etree
import urllib.request


def returnXml(url):
    ##Requires you to have xml.etree.ElementTree imported
    try:
        xmltext = (urllib.request.urlretrieve(url))
    except:
        print('Internet connection is not valid')
    root = (etree.parse(xmltext[0])).getroot()
    return root
    
def addNumberSS(number):
    if number == 1:
        return ' first'
    elif number == 2:
        return ' second'
    elif number == 3:
        return ' third'
    elif number < 20 and number > 3:
        return str(number) + 'th'
    else:
        if number % 10 == 1:
            return str(number) + ' first'
        elif number % 10 == 2:
            return str(number) + ' second'
        elif number % 10 == 3:
            return str(number) + ' third'
        else:
            return str(number) + 'th'
