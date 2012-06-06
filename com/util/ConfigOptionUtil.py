import ConfigParser
CONFIG_FILE='/home/fred/workspace/EnglishHyperlink/com/config/hyperlink.conf'

def getConfigOption(section,option=''):
    "get single config option from config file hyperlink.conf"
    cf=ConfigParser.ConfigParser()
    cf.read(CONFIG_FILE) 
    try:                         
        if section:
            if option:    
                return cf.get(section,option)
            else:
                return cf.items(section)
        else:
            raise Exception("No option you wanted")
    except Exception,e:
        #log
        print "No option you wanted",e

def getConfigSection(section):
    '''
        get config section from config file hyperlink.conf
    '''
    cf=ConfigParser.ConfigParser()
    cf.read(CONFIG_FILE)
    configMap={}
    try:
        optionList=cf.items(section)
        for item in optionList:
            configMap[item[0]]=item[1]
    except Exception,e:
        #log
        print e
        pass
    return configMap

def setConfigOption(section,option,value):
    cf=ConfigParser.ConfigParser()
    cf.read(CONFIG_FILE)

if __name__=='__main__':
    print getConfigOption('db','host')
    print getConfigSection('db')
    print getConfigSection('log')
