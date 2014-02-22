#!/usr/bin/env python3
#Import everything
import subprocess
import urllib.request
import configparser
from datetime import datetime
import xml.etree.ElementTree as etree

## MAJOR CLASSES: input, output, processing, and data
## EACH CLASS DEALS WITH NAME
## THINGS YET TO BE MADE:
##      NATURAL LANGUAGE OUTPUT (We kinda have it, sorta)
## THINGS YET TO BE EXPANDED:
##      ACCURACY (We're better)
##      ETC (We'll expand when we discuss)

## CURRENT THINGS THAT NEED TO BE FIXED
## 1. For some reason wolframalpha will spit out a Keyword: 'title' error even though there is titles in the xml file
## 2. Weather function only works in winter and needs to be more customizable
## 3. We need a system to work with connecting words, like 'in', ex: 'weather in ottawa' =/= 'weather' (normal)




    
class readinput:
    

    def readconfig():
        #global variable for config
        global config
        #load config file and edit it
        configx = configparser.ConfigParser()
        configx.read('config.ini')
        config = configx
        
class output:
    def detout(inputstr): #detout = determine output
        outputx = config['behaviour']['OUTPUT']
        getattr(output, outputx)(processing.replacestrings(inputstr)) # Call child method with name outputx with argument inputstr
                                                                      # EX: if name = espeak, call output.espeak(inputstr)
    
    def espeak(inputstr): #Call espeak
        proc=subprocess.Popen(['espeak',str(hold)])

    def printx(inputstr): #This is a sad method
        print(inputstr)
            
class processing:

    def replacestrings(inputx):
        hold = str(inputx)
        replacewords = eval(config['language']['REPLACE'])
        for i in range(0, len(replacewords)):
            hold = hold.replace(replacewords[i][0], ' '+str(replacewords[i][1])+' ')
        return hold
    def weatherinfo(tempurature, windchill, conditions):
        hold = [tempurature, windchill, conditions]  
        for i in range(0, len(hold)-1):
            if hold[i][0] == "-":
                hold[i] = "negative " + hold[i][1:]      
        output = "It is " + hold[0] + " Degrees with a Windchill of " + hold[1] + " and the skys are" + hold[2]
        return output

    
    def numkeywords(inputx, output):
        if inputx == list(inputx): #Double checks if item is a list, and if not makes it a list based on spaces
            inputterms = inputx
        else:
            inputterms = inputx.split(' ')
        
        for i in range(0, len(inputterms)):
            inputterms[i] = inputterms[i].strip(' ') #gets rid of extra space 
                                                     #ex "hello world" --> ['hello', ' world'] --> ['hello', 'world']
        outputterms = output
        hold = []
        for i in inputterms:
            if i in outputterms:
                hold.append(i) #append matching words to a list
        return hold

    def readwolframinfo(inputx):
        goodwords = eval(config['behaviour']['WOLFKEYWORDS'])
        
        valuelist = []
        if inputx == []:
            return "Wolfram Alpha did not return any information"
        else:
            for i in range(0, len(inputx)):
                #Rank result by number of matching keywords per element in list
                #(Generally first result in wolframalpha is more accurate, so we may not need to worry about elements having equal values)
                valuelist.append(len(processing.numkeywords(inputx[i][0].lower(), goodwords)))

            ######## Check if all elements are 0 ########
            if all(x == 0 for x in valuelist) == True:
                return "Wolfram alpha returned no useful information"
            else:
                #Since inputx and valuelist are going to be of equal size, we can index inputx by the greatest value index in valuelist
                gooddata = inputx[valuelist[valuelist.index(max(valuelist))]][1]
                return gooddata.replace('\n', ' ')
        
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
                return str(number -1) + ' first'
            elif number % 10 == 2:
                return str(number -2) + ' second'
            elif number % 10 == 3:
                return str(number -3) + ' third'
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
            output.espeak(date)
        elif i == 2: #Only time
            if AM == 'AM' and now.hour > 12:
                if now.minute < 10: #If we don't add the 'o', it says 8-5 PM not 8:05
                    time = (str(now.hour-12),'o' +str(now.minute), ' PM')#Add o to make 12:03 sound like "12 'o'3" and not "12...3"
                else:
                    time = (str(now.hour-12),str(now.minute), ' PM')
            elif AM == 'AM' and now.hour <= 12:
                if now.minute < 10:
                    time = (str(now.hour), 'o '+str(now.minute), ' AM')#Add o to make 12:03 sound like "12 'o'3" and not "12...3"
                else:
                    time = (str(now.hour),str(now.minute), ' AM')
            else:
                if now.minute < 10:
                    time = (str(now.hour), 'o '+str(now.minute)) #Add o to make 12:03 sound like "12 'o'3" and not "12...3"
                else:
                    time = (str(now.hour), str(now.minute))
            #output.detout(time)
            #print(time)
            outputx = str(time)
        elif i == 3: #Time and date
            date = ((month[now.month-1]),processing.addnumbersuperscript(now.day),now.year)
            if AM == 'AM' and now.hour > 12:
                time = (str(now.hour-12),str(now.minute), ' PM')
            elif AM == 'AM' and now.hour <= 12:
                time = (str(now.hour),str(now.minute), ' AM')
            else:
                time = (str(now.hour), str(now.minute))
             
            outputx = 'It is ' + str(time) + ' and the date is ' + str(date)
        return outputx

    
    def getweather():
        url = 'http://weather.noaa.gov/pub/data/observations/metar/decoded/'+ config['userinfo']['ICAO'] +'.TXT'
        url = urllib.request.urlopen(url).read()
        text = url.decode('utf-8')
        text = text.split("\n") #Formats text file
        nowindchill = 0
        for i in range(0, len(text)):
            if text[i].find('Temperature') != -1: #find returns -1 if the search string is not in the file (bigger string)
                celsius = text[i]
                celsius = celsius[celsius.find('(')+1:celsius.find(')')-1].rstrip('C') #this will return '1 C', .rstrip gets rid of 'C'
                a = 1
            if text[i].find('Windchill') != -1:
                windchill = text[i]
                windchill = windchill[windchill.find('(')+1:windchill.find(')')-1].rstrip('C')
                nowindchill = 1 #This tells us if windchill is even in the file
                                #I know it's naughty
            if text[i].find('Sky conditions') != -1:
                conditions = text[i][len('Sky conditions:'):] #Since we seperated the file by lines, we can just pull the entire line-
                                                              #after the string 'Sky conditions:'
        if nowindchill != 1: #We set nowindchill to 1 earlier to tell us if we even had windchill
            windchill = 0
        outdata = processing.weatherinfo(str(celsius), str(windchill), conditions)
        return outdata


    def wolframinfo(urlInput):
        url = 'http://api.wolframalpha.com/v2/query?input="' + urlInput.replace(" ", "%20") + '"&appid=' + config['userinfo']['WOLFAPI']
        xmltext = (urllib.request.urlretrieve(url))
        root = (etree.parse(xmltext[0])).getroot() #Using ElementTree to read wolframalpha xml file
        print(root.attrib)
        info = []
        for i in range(0, len(root)):
            podtitle = (root[i].attrib)['title'] #Pulls title off pod
            podinfo = root[i][0][0].text #Pulls info off <plaintext> pod
            info.append((podtitle, podinfo))
            
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
    
    matching = processing.numkeywords(inputx, keywords) #Finds all matching keywords in INPUT_STRING with establish KEYWORDS (in .ini file)
    matchingkeys = []
    matchingfunc = []
    for i in matching: #It uses this information to check against the keyword file to get position of the function itself
        if i in keywords: #Keywords and functions are associated in the .ini file and thus will have equal index
            matchingfunc.append(functions[keywords.index(i)])
       
    if len(matchingfunc) == 1: #If there's only one matching keyword
        if matchingfunc[0] == 'weather':
            output.detout(data.getweather())
        elif matchingfunc[0] == 'wolfram':
            output.detout(data.wolframinfo(inputx.rstrip(matching[0])))
        elif matchingfunc[0] == 'date':
            output.detout(data.timeanddate(1, config['behaviour']['TIME']))
        elif matchingfunc[0] == 'time':
            output.detout(data.timeanddate(2, config['behaviour']['TIME']))
            
    elif len(matchingfunc) == 2: #If there's only 2 matching keywords
        if 'date' in matchingfunc and 'time' in matchingfunc:
            output.detout(data.timeanddate(3, config['behaviour']['TIME']))
            
    
#print('search '+urlInput)
#parseinput('weather', keywords, functions)

while(3<6):
    inputx = str(input('Enter Question: '))
    parseinput(inputx, keywords, functions)





