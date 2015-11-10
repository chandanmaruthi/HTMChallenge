from networkBuilder import *
class newCode(object):
    strDataFolder = "/home/chandan/chandan/code/Data/"
    strRootFolder = "/home/chandan/chandan/code/brainscience/"
    strAppFolder = "curious/"
    strModelFolder = 'curiousWorkbench/test/models/'


    strModelFile = 'model2.txt'
    #strDataFile ='Test_003_1_WordList.csv'
    strDataFile ='Test_003_WordListNew.csv'

    inputModelFile = strRootFolder + strAppFolder + strModelFolder + strModelFile
    strInputDataFile = strDataFolder + strDataFile

    fo = open(inputModelFile,'r')
    strRawModelXML = fo.read()
    newNetworkObject =None

    def start(self):
        self.newNetworkObject = Network()
        strRawXML = ''
        strRawXML = self.strRawModelXML
        try:
            strResetMemory = command['RESET_MEMORY']
        except:
            strResetMemory = 'FALSE'

        self.MODEL_DESC = strRawXML
        #print 'Entering initNetwork in walnutserver.py'
        #print strRawXML
        # Step 2 :Call network.setConfigPath() to provide the network a path of the config file
        #objNetwork.setConfigPath("/home/chandanmaruthi/chandan/code/brainscience/config.xml")

        self.newNetworkObject.setConfigModel(strRawXML)

        # Step 3 :Call network.initiateNetwork, this step performs the following tasks
        # a.) calls the createNodes functions, to create regions as specified in config
        # B.) calls connect nodes connect to setup connections between nodes are specified in the config
        self.newNetworkObject.initNetwork(strResetMemory)

        # Test Network Setup by printing the values
        self.newNetworkObject.printNetwork("a")

        #def runNetworkWithFile(self, inputFile,  learnFlag=True, reset=False, printStates=False, computeInfOutput=False):

        runValue = self.newNetworkObject.runNetworkWithFile(inputFile=self.strInputDataFile, learnFlag=True,reset=False,printStates=False,computeInfOutput=True)
        if runValue['returnValue'] !=None:
            print runValue['returnValue']

objNewCode = newCode()
print objNewCode.start()
