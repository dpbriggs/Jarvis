#!/usr/bin/env python3
#Import everything
import subprocess
import urllib.request 

##Random Functions

#load config file and edit it
tempconfig = open("config.txt").readlines()
config = []
for i in range(0, len(tempconfig)):  #elements in array
    if tempconfig[i].find('#') == -1 and tempconfig[i] != "\n":
        config.append(tempconfig[i])      

#Call espeak
def callespeak(inputstr):
    proc=subprocess.Popen(['espeak',str(inputstr)])


def accuracy(input, output):
    inputterms = input.split(' ')
    outputterms = output.split(' ')
    hold = 0
    for i in inputterms:
        if i in outputterms:
            hold += 1
    return hold
#print(accuracy('this is an cat', 'this is a dog'))
##/    

#Weather information
    
def formatweatherinfo(tempurature, windchill, conditions):
    hold = [tempurature, windchill, conditions]
    print(hold)
    for i in range(0, len(hold)-1):
        if hold[i][0] == "-":
            hold[i] = "negative " + hold[i][1:]

    output = "It is " + hold[0] + " Degrees with a Windchill of " + hold[1] + " and the skys are" + hold[2]
    return output

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

#getweather()
urlInput = "How big is the sun"



class wolfram:

    matchingkey = config[2]
 
    def geninfo(urlInput):
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
       
            

        
wolfram.geninfo(urlInput)









