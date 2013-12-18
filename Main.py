#!/usr/bin/env python3
#Import everything
import subprocess
import urllib.request
import configparser
from datetime import datetime

## MAJOR CLASSES: input, output, processing, and data
## EACH CLASS DEALS WITH NAME
## THINGS YET TO BE MADE:
##      NATURAL LANGUAGE OUTPUT (We kinda have it, sorta)
##      INPUT OF ANY KIND
## CLASSES YET TO BE EXPANDED:
##      ACCURACY
##      ETC (We'll expand when we discuss)

## INCONSISTENCIES IN THE WOLFRAMALPHA XML FILE MAKE SUBPOD SUPPORT VERY DIFFICULT
## WILL DISCUSS WITH YOU GUYS LATER

    
class readinput:
    

    def readconfig():
        #global variable for config
        global config
        #load config file and edit it
        configx = configparser.ConfigParser()
        configx.read('config.ini')
        config = configx
    
class output:
    #Call espeak
    def callespeak(inputstr):
        hold = str(inputstr)
        replacewords = eval(config['language']['REPLACE'])
        for i in range(0, len(replacewords)):
            hold = hold.replace(replacewords[i][0], ' '+str(replacewords[i][1])+' ')  
        
        proc=subprocess.Popen(['espeak',str(hold)])
    
            
class processing:
    
    def weatherinfo(tempurature, windchill, conditions):
        hold = [tempurature, windchill, conditions]  
        for i in range(0, len(hold)-1):
            if hold[i][0] == "-":
                hold[i] = "negative " + hold[i][1:]      
        output = "It is " + hold[0] + " Degrees with a Windchill of " + hold[1] + " and the skys are" + hold[2]
        return output

    
    def numkeywords(inputx, output):
        if inputx == list(inputx):
            inputterms = inputx
        else:
            inputterms = inputx.split(' ')
            for i in range(0, len(inputterms)):
                inputterms[i] = inputterms[i].strip(' ') 
        for i in range(0, len(inputterms)):
            inputterms[i] = inputterms[i].rstrip(' ')
        outputterms = output
        hold = []
        for i in inputterms:
            if i in outputterms:
                hold.append(i)
        return hold

    def readwolframinfo(inputx):
        goodwords = eval(config['behaviour']['WOLFKEYWORDS'])
        valuelist = []
        for i in range(0, len(inputx)):
            valuelist.append(len(processing.numkeywords(inputx[i][0], goodwords)))
        gooddata = inputx[valuelist[valuelist.index(max(valuelist))]][1]
        return gooddata[0].replace('\n', ' ')
        
    def addnumbersuperscript(number):
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
    
class data:

    def timeanddate(i, AM):
        now = datetime.now()
        current_year = str(now.year)
        current_month = str(now.month)
        current_day = str(now.day)
        current_hour = str(now.hour)
        current_minute = str(now.minute)
        month = ['january' , 'february', 'march' , 'april', 'may', 'june', 'july', 'augest', 'september', 'october', 'november', 'december']

        if i == 1: # Only date
            date = ((month[now.month-1]),processing.addnumbersuperscript(now.day),now.year)
            output.callespeak(date)
        elif i == 2: #Only time
            if AM == 'AM' and now.hour > 12:
                if now.minute < 10: #If we don't add the 'o', it says 8-5 PM not 8:05
                    time = (str(now.hour-12),'o' +str(now.minute), ' PM')
                else:
                    time = (str(now.hour-12),str(now.minute), ' PM')
            elif AM == 'AM' and now.hour <= 12:
                if now.minute < 10:
                    time = (str(now.hour), 'o '+str(now.minute), ' AM')
                else:
                    time = (str(now.hour),str(now.minute), ' AM')
            else:
                if now.minute < 10:
                    time = (str(now.hour), 'o '+str(now.minute))
                else:
                    time = (str(now.hour), str(now.minute))
            output.callespeak(time)
            print(time)
        elif i == 3: #Time and date
            date = ((month[now.month-1]),processing.addnumbersuperscript(now.day),now.year)
            if AM == 'AM' and now.hour > 12:
                time = (str(now.hour-12),str(now.minute), ' PM')
            elif AM == 'AM' and now.hour <= 12:
                time = (str(now.hour),str(now.minute), ' AM')
            else:
                time = (str(now.hour), str(now.minute))
             
            outputx = 'It is ' + str(time) + ' and the date is ' + str(date)
            output.callespeak(outputx)

    
    def getweather():
        url = 'http://weather.noaa.gov/pub/data/observations/metar/decoded/'+ config['userinfo']['ICAO'] +'.TXT'
        url = urllib.request.urlopen(url).read()
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
        outdata = processing.weatherinfo(str(celsius), str(windchill), conditions)
        return outdata


    def wolframinfo(urlInput):
        url = 'http://api.wolframalpha.com/v2/query?input="' + urlInput.replace(" ", "%20") + '"&appid=' + config['userinfo']['WOLFAPI']
        wolfinfo = urllib.request.urlopen(url).read()
        xmltext = wolfinfo.decode('utf-8')
        xmltext = xmltext.split('</pod>')
        #numpods = xmltext[0][xmltext[0].find('numpods=')+9:xmltext[0].find('datatypes=')-1].rstrip('"')
        podinfo = []
        numpods = int(xmltext[0][xmltext[0].find('numpods=')+9:xmltext[0].find('datatypes=')-6])
        numsubpods = []
        ## Second line (numsubpod[1]) has primary='true' tag, so it must be included seperated (talking about numsubpods)
        #numsubpods.append(int(xmltext[0][xmltext[0].find('numsubpods=')+len('numsubpods=')+1:xmltext[0].find('<subpod')-5]))
        ##Line Two \/\/\/
        #numsubpods.append(int(xmltext[1][xmltext[1].find('numsubpods=')+len('numsubpods=')+1:xmltext[1].find('primary')-7]))
        #for i in range(2, len(xmltext)):
          #  numsubpods.append(int(xmltext[i][xmltext[i].find('numsubpods=')+len('numsubpods=')+1:xmltext[i].find('<subpod')-5]))
                
        info = []
        for i in range(1, numpods): #It starts at one because (for some reason) xmltext[0] is messy (interpretation info?)
            podtitle = xmltext[i][xmltext[i].find('<pod title="')+len('<pod title="')+3:xmltext[i].find('scanner')-7].split('|')
            podinfo = xmltext[i][xmltext[i].find('<plaintext>')+len('<plaintext>'):xmltext[i].find('</plaintext>')].split('|')
            info.append((podtitle, podinfo))
        print(info)
        return processing.readwolframinfo(info)

readinput.readconfig()
hold = eval(config['behaviour']['KEYWORDS'])
keywords = []
functions = []
for i in range(0, len(hold)):
    keywords.append(hold[i][0])
    functions.append(hold[i][1])



urlInput = "how many m and m's can fit into a bathtub"



def parseinput(inputx, keywords, functions):
    matching = processing.numkeywords(inputx, keywords)
    print(matching)
    matchingkeys = []
    matchingfunc = []
    for i in matching:
        if i in keywords:
            matchingfunc.append(functions[keywords.index(i)])
       
    if len(matchingfunc) == 1:
        if matchingfunc[0] == 'weather':
            output.callespeak(data.getweather())
        elif matchingfunc[0] == 'wolfram':
            output.callespeak(data.wolframinfo(inputx.rstrip(matching[0])))
        elif matchingfunc[0] == 'date':
            data.timeanddate(1, config['behaviour']['TIME'])
        elif matchingfunc[0] == 'time':
            data.timeanddate(2, config['behaviour']['TIME'])
            
    elif len(matchingfunc) == 2:
        if 'date' in matchingfunc and 'time' in matchingfunc:
            data.timeanddate(3, config['behaviour']['TIME'])
            
    
#print('search '+urlInput)
#parseinput('weather', keywords, functions)

inputx = str(input('Enter Question: '))
parseinput(inputx, keywords, functions)






