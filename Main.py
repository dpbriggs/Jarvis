#!/usr/bin/env python3
#Import everything
import subprocess
import urllib.request 



#load config file and edit it
tempconfig = open("config.txt").readlines()
config = []
for i in range(0, len(tempconfig)):  #elements in array
    if tempconfig[i].find('#') == -1 and tempconfig[i] != "\n":
        config.append(tempconfig[i])
        
        

#Call espeak
def callespeak(inputstr):
    proc=subprocess.Popen(['espeak',str(inputstr)])


def formatweatherinfo(tempurature, windchill, conditions):
    hold = [tempurature, windchill, conditions]
    print(hold)
    for i in range(0, len(hold)-1):
        if hold[i][0] == "-":
            hold[i] = "negative " + hold[i][1:]

    output = "It is " + hold[0] + " Degrees with a Windchill of " + hold[1] + " and the sky is" + hold[2]
    return output
    

#Pull weather information

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
    output = formatweatherinfo(str(celsius), str(windchill), conditions)
    callespeak(output)    

getweather()
urlInput = "How many m and m's could fit in a bathtub?"

def accuracy(input, output):
    inputterms = input.split(' ')
    outputterms = output.split(' ')
    hold = 0
    for i in inputterms:
        if i in outputterms:
            hold += 1
    return hold
#print(accuracy('this is an cat', 'this is a dog'))

class wolfram:

    matchingkey = config[2]
 
    def geninfo(urlInput):
        url = 'http://api.wolframalpha.com/v2/query?input="' + urlInput.replace(" ", "%20") + '"&appid=' + config[1]
        wolfinfo = urllib.request.urlopen(url).read()
        xmltext = wolfinfo.decode('utf-8')
        xmltext = xmltext.split('</pod>')
        numpods = xmltext[0][xmltext[0].find('numpods=')+9:xmltext[0].find('datatypes=')-1].rstrip('"')
        podinfo = []
       # for i in xmltext:
          #  podinfo.append([
            

        
#wolfram.geninfo(urlInput)









