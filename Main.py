#!/usr/bin/env python3
#Import everything
import subprocess
import urllib.request 

## MAJOR CLASSES: input, output, format, and data
## EACH CLASS DEALS NAME
## CLASSES YET TO BE MADE:
##      NATURAL LANGUAGE OUTPUT
##      INPUT OF ANY KIND
## CLASSES YET TO BE EXPANDED:
##      ACCURACY
##      ETC (We'll expand when we discuss)

    
class input:
    def readconfig():
        #load config file and edit it
        tempconfig = open("config.txt").readlines()
        config = []
        for i in range(0, len(tempconfig)):  #elements in array
            if tempconfig[i].find('#') == -1 and tempconfig[i] != "\n":
                config.append(tempconfig[i].rstrip('\n'))
        config[3] = config[3].split(',') #seperate keywords
        return config

    
class output:
    #Call espeak
    def callespeak(inputstr):
        proc=subprocess.Popen(['espeak',str(inputstr)])


class accuracy:
    
    def numkeywords(input, output):
        inputterms = input.split(' ')
        outputterms = output.split(' ')
        hold = 0
        for i in inputterms:
            if i in outputterms:
                hold += 1
        return hold
    #print(accuracy('this is an cat', 'this is a dog'))

class format:
    def weatherinfo(tempurature, windchill, conditions):
        hold = [tempurature, windchill, conditions]
        print(hold)
        for i in range(0, len(hold)-1):
            if hold[i][0] == "-":
                hold[i] = "negative " + hold[i][1:]

        output = "It is " + hold[0] + " Degrees with a Windchill of " + hold[1] + " and the skys are" + hold[2]
        return output
    
class data:
    
    def getweather():
        url = urllib.request.urlopen(config[0]).read()
        text = url.decode('utf-8')
        text = text.split("\n") #Formats text file
        nowindchill = 0
        for i in range(0, len(text)):
            if text[i].find('Temperature') != -1:
                celsius = text[i]
                celsius = celsius[celsius.find('(')+1:celsius.find(')')-1].rstrip('C')
                a = 1
            if text[i].find('Windchill') != -1:
                windchill = text[i]
                windchill = windchill[windchill.find('(')+1:windchill.find(')')-1].rstrip('C')
                nowindchill = 1
            if text[i].find('Sky conditions') != -1:
                conditions = text[i][len('Sky conditions:'):]
        if nowindchill != 1:
            windchill = 0
        outdata = format.weatherinfo(str(celsius), str(windchill), conditions)
        output.callespeak(outdata)

    matchingkey = config[2]
 
    def wolframinfo(urlInput):
        url = 'http://api.wolframalpha.com/v2/query?input="' + urlInput.replace(" ", "%20") + '"&appid=' + config[1]
        wolfinfo = urllib.request.urlopen(url).read()
        xmltext = wolfinfo.decode('utf-8')
        xmltext = xmltext.split('</pod>')
        numpods = int(xmltext[0][xmltext[0].find('numpods=')+9:xmltext[0].find('datatypes=')-6])
        info = {}
        for i in range(1, numpods):
            podtitle = xmltext[i][xmltext[i].find('<pod title="')+len('<pod title="')+3:xmltext[i].find('scanner')-7].split('|')
            podinfo = xmltext[i][xmltext[i].find('<plaintext>')+len('<plaintext>'):xmltext[i].find('</plaintext>')].split('|')
            info[i] = (podtitle, podinfo)
        return info

config = input.readconfig()
#print(config)
urlInput = "what is eulors number?"

            

        










