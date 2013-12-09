#!/usr/bin/env python3
#Import everything
import subprocess
import urllib.request 

<<<<<<< HEAD
## MAJOR CLASSES: input, output, format, and data
## EACH CLASS DEALS NAME
## CLASSES YET TO BE MADE:
=======
## MAJOR CLASSES: input, output, processing, and data
## EACH CLASS DEALS WITH NAME
## THINGS YET TO BE MADE:
>>>>>>> refs/remotes/origin/master
##      NATURAL LANGUAGE OUTPUT
##      INPUT OF ANY KIND
## CLASSES YET TO BE EXPANDED:
##      ACCURACY
##      ETC (We'll expand when we discuss)

<<<<<<< HEAD
    
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
    
            
class processing:
    
    def weatherinfo(tempurature, windchill, conditions):
        hold = [tempurature, windchill, conditions]
        print(hold)
        for i in range(0, len(hold)-1):
            if hold[i][0] == "-":
                hold[i] = "negative " + hold[i][1:]
                
        output = "It is " + hold[0] + " Degrees with a Windchill of " + hold[1] + " and the skys are" + hold[2]
        return output
    
    def numkeywords(input, output):
        inputterms = input.split(' ')
        outputterms = output.split(' ')
        hold = 0
        for i in inputterms:
            if i in outputterms:
                hold += 1
        return hold
    #print(accuracy('this is an cat', 'this is a dog'))
    
class data:
    
=======
## INCONSISTENCIES IN THE WOLFRAMALPHA XML FILE MAKE SUBPOD SUPPORT VERY DIFFICULT
## WILL DISCUSS WITH YOU GUYS LATER

    
class readinput:
    def readconfig():
        #load config file and edit it
        tempconfig = open("config.txt").readlines()
        config = []
        for i in range(0, len(tempconfig)):  #elements in array
            if tempconfig[i].find('#') == -1 and tempconfig[i] != "\n":
                config.append(tempconfig[i].rstrip('\n'))
        config[3] = config[3].split(',') #seperate keywords (wolframalpha keywords we like)
        return config
    
    def linkedwords(inputfile):
        tempconfig = open(inputfile).readlines()
        keywords = []
        for i in range(0, len(tempconfig)):           
            if tempconfig[i].find('#') == -1 and tempconfig[i] != "\n":
                textline = tempconfig[i].rstrip('\n')
                keywords.append(textline.split(','))
        return keywords
    
class output:
    #Call espeak
    def callespeak(inputstr):
        hold = str(inputstr)
        replacewords = readinput.linkedwords('language.txt')
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
            inputterms[i] = inputterms[i].rstrip(' ')
        outputterms = output
        hold = []
        for i in inputterms:
            if i in outputterms:
                hold.append(i)
        return hold

    def readwolframinfo(inputx):
        goodwords = config[3]
        valuelist = []
        for i in range(0, len(inputx)):
            valuelist.append(len(processing.numkeywords(inputx[i][0], goodwords)))
        gooddata = inputx[valuelist[valuelist.index(max(valuelist))]][1]
        return gooddata[0].replace('\n', ' ')
        
        
    
class data:
>>>>>>> refs/remotes/origin/master
    
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
        outdata = processing.weatherinfo(str(celsius), str(windchill), conditions)
<<<<<<< HEAD
        output.callespeak(outdata)

 
    def wolframinfo(urlInput):
        url = 'http://api.wolframalpha.com/v2/query?input="' + urlInput.replace(" ", "%20") + '"&appid=' + config[1]
        wolfinfo = urllib.request.urlopen(url).read()
        xmltext = wolfinfo.decode('utf-8') #Decodes from binary
        xmltext = xmltext.split('</pod>') # Splits Pod
        numsubpod = []
        numpods = xmltext[0][xmltext[0].find('numpods=')+9:xmltext[0].find('datatypes=')-1].rstrip('"')
        for i in range(0, len(xmltext)):
            numsubpod.append(xmltext[i][xmltext[i].find('numsubpods='):xmltext[i].find('datatypes=')-1].rstrip('"'))
        return
        print (numsubpod)
        podinfo = []
        info = {}

        for i in range(1, numpods): #Info Proc
            if numsubpod == 1:
                podtitle = xmltext[i][xmltext[i].find('<pod title="')+len('<pod title="')+3:xmltext[i].find('scanner')-7].split('|')
                podinfo = xmltext[i][xmltext[i].find('<plaintext>')+len('<plaintext>'):xmltext[i].find('</plaintext>')].split('|')
                info[i] = (podtitle, podinfo,)
            if numsubpod > 1:
                podtitle = xmltext[i][xmltext[i].find('<pod title="')+len('<pod title="')+3:xmltext[i].find('scanner')-7].split('|')
                podinfo = xmltext[i][xmltext[i].find('<plaintext>')+len('<plaintext>'):xmltext[i].find('</plaintext>')].split('|')
                subpodtitle = xmlsubtext[i][xmlsubtext[i].find('<subpod title="')+len('<subpod title="')+3:xmlsubtext[i].find('scanner')-7].split('|')
                subpodinfo = xmlsubtext[i][xmlsubtext[i].find('<plaintext>')+len('<plaintext>'):xmlsubtext[i].find('</plaintext>')].split('|')
                info[i] = (podtitle,(subpodtitle,subpodinfo))
        return  info
        



config = input.readconfig()
#print(config)
#urlInput = "what is the weather in ajax?"

print(data.wolframinfo("How many m and m's could fit in a bathtub."))

#urlInput = "what is eulors number?"
=======
        return outdata


    def wolframinfo(urlInput):
        url = 'http://api.wolframalpha.com/v2/query?input="' + urlInput.replace(" ", "%20") + '"&appid=' + config[1]
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
        return processing.readwolframinfo(info)

 
config = readinput.readconfig()
hold = readinput.linkedwords('keywords.txt')
keywords = []
functions = []
for i in range(0, len(hold)):
    keywords.append(hold[i][0])
    functions.append(hold[i][1])



urlInput = "how many m and m's can fit into a bathtub"



def parseinput(inputx, keywords, functions):
    matching = processing.numkeywords(inputx, keywords)
    
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
    
#print('search '+urlInput)
#parseinput('weather', keywords, functions)
inputx = str(input('Enter Question: '))
parseinput(inputx, keywords, functions)

    




>>>>>>> refs/remotes/origin/master






