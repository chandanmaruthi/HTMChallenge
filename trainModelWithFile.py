from walnutclient import *

#objWalnutClient= walnutclient(5001,'localhost',selProject.ModelMap.RawXML)
strDataFolder = "/home/chandan/chandan/code/brainscience/"
strRootFolder = "/home/chandan/chandan/code/brainscience/"
strAppFolder = "curious/"
strModelFolder = 'curiousWorkbench/test/models/'


strModelFile = 'model1.txt'
strDataFile ='Test_003_1_WordList.csv'

inputModelFile = strRootFolder + strAppFolder + strModelFolder + strModelFile
strInputDataFile = strDataFolder + strDataFile

fo = open(inputModelFile,'r')
strRawModelXML = fo.read()

objwalnutclient = walnutclient(5001, 'localhost',strRawModelXML )
runValue = objwalnutclient.runNetworkWithFile(strInputDataFile, 'CSV',True,False,False,True)
print runValue['returnValue']
