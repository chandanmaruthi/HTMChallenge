#!/usr/bin/python
__author__ = 'chandanmaruthi'


#----------------------Import ----------------------
import sys
sys.path.append('/home/chandan/chandan/code/nupic/src')

from generic import GenericEncoder
from nupic.encoders.category import  CategoryEncoder
from nupic.encoders import  ScalarEncoder
from nupic.encoders.date import  DateEncoder
import datetime
from nupic.research.spatial_pooler import SpatialPooler
from nupic.research.TP10X2 import TP
#from nupic.research.temporal_memory_new import TemporalMemory as TP
from copy import deepcopy
from io import StringIO
import numpy as np
import redis
import os
import StringIO
from xml.etree import cElementTree  # C implementation of xml.etree.ElementTree
from xml.parsers.expat import ExpatError  # XML formatting errors
import cPickle as pickle
import logging
from datetime import datetime

#------------------------Variables and File Paths -------------------------
#Current file name and directory for Config File:
#curpath = os.path.dirname(os.path.realpath("config.xml"))
#filename = os.path.join(curpath, "config.xml")
r_server = redis.Redis('localhost')
strRootFolder = "/home/chandan/chandan/code/brainscience/"
strAppFolder = "curious/"
#logging.basicConfig(filename = strRootFolder + strAppFolder + 'log/' + str(datetime.now()) +'.txt',level=logging.DEBUG)
#logging.debug(' Logging Start ' + str(datetime.now()))
#------------------------Region Class------------------------

class Region:

    def getRegion(self, regionName):
        return regionName
    def setRegion(self, regionName):
        return regionName


#------------------------Node Class--------------------------
#The node is the building block of a network. A node has a region, a child and a parent

class Node:
    def __init__(self,
                 nodeName,
                 nodeObj,
                 childNode=None,
                 parentNode=None,
                 nodeType=None,
                 inputWidth=0):
        self.nodeObj=nodeObj
        self.nodeType=nodeType
        self.nodeName=nodeName
        self.childNode=childNode
        self.parentNode=parentNode
        self.inputWidth=inputWidth



    def getNode(self):
        return self
    def setNode(self,nodeName,nodeObj,type,childName,parentName,inputWidth):
        self.nodeName=nodeName
        self.nodeType=type
        self.nodeObj=nodeObj
        self.childName=childName
        self.parentName=parentName
        self.inputWidth=inputWidth
    def setChild(self, childNode):
        self.childNode=childNode
    def setParent(self,parentNode):
        self.parentNode=parentNode
#------------------------Network Class-----------------------

class Network:
    def __init__(self):
        self.networkTree={}
        self.configPath=""
        self.networkNodes=None
        self.configXML=""
        self.INPUT_TYPE = "FILE_CSV"

    def getConfigPath(self):
        self.configPath
    def setConfigPath(self, configFilePath):
        self.configPath=configFilePath

    def setConfigModel(self):
        self.configXML
    def setConfigModel(self, configFileXML):
        self.configXML=configFileXML

    def getNetWork(self, networkName):
        return networkName
    def setNetwork(self, networkName):
        return networkName

    def addNode(self,nodeName,type, nodeObj,connectedFrom,connectedTo):
        nodeObject= Node(nodeName,type,connectedFrom,connectedTo)
        self.networkTree[nodeName]=nodeObject
        #print "adding", self.networkTree[nodeName].getNode()
    def deleteNode(self,nodeName):
        del self.networkTree[nodeName]
    def connectNodes(self):
        links={}
        try:
            #Parse the given XML file:
            #print filename


            configRoot = cElementTree.fromstring(self.configXML)

        except ExpatError as e:

            raise e
        except IOError as e:

            raise e
        else:


            i=0
            for link in configRoot.iter('link'):
                #print link.get('nodeName'),link.get('in')

                if link.get('out') != None:
                    self.networkNodes[link.get('nodeName')].setParent(self.networkNodes[link.get('out')])
                if link.get('in') != None:
                    self.networkNodes[link.get('nodeName')].setChild(self.networkNodes[link.get('in')])


    def printNetwork(self, name):

        for networkNode in self.networkNodes:
            #print "------------------------------------------------------"
            #print 'Node Name :', self.networkNodes[networkNode].nodeName
            if self.networkNodes[networkNode].childNode !=None:
                #print 'Child Node : ', self.networkNodes[networkNode].childNode.nodeName
               return
            else:
                #print 'Child Node : '
                return
            if self.networkNodes[networkNode].parentNode != None:
                #print 'Parent Node : ', self.networkNodes[networkNode].parentNode.nodeName
                return
            else:
                #print 'Parent Node : '
                return


    #------------------------Read Config ------------------------

    def createNodes(self, name):
        nodesInNetwork={}
        #regionsInNetwork = {}
        try:
            #Parse the given XML file:
            #print filename

            #tree = cElementTree.parse(self.configPath)
            configRoot=cElementTree.fromstring(self.configXML)


        except ExpatError as e:
            #print "[XML] Error (line %d): %d" % (e.lineno, e.code)
            #print "[XML] Offset: %d" % (e.offset)
            raise e
        except IOError as e:
            #print "[XML] I/O Error %d: %s" % (e.errno, e.strerror)
            raise e
        else:
            #configRoot = tree.getroot()
            regions =configRoot.iter("regions")
            i=0
            for region in configRoot.iter('region'):
                if region.get("type")=="Sensor":
                    objRegion=self.createSensor(region.find("type").text,region)
                    objNode=Node(region.find("type").text,objRegion,None,None,"EN")
                    nodesInNetwork[region.find("type").text]=objNode

                if region.get("type")=="SpatialPooler":
                    objRegion = self.createSpatialPooler(region.find("type").text,region)
                    objNode=Node(region.get("name"),objRegion,None,None,"SP",int(region.find("inputWidth").text))
                    nodesInNetwork[region.get("name")]=objNode

                if region.get("type")=="TemporalPooler":
                    #print "creating TP"
                    objRegion= self.createTemporalPooler(region.find("type").text,region)
                    objNode=Node(region.get("name"),objRegion,None,None,"TP",int(region.find("inputWidth").text))
                    nodesInNetwork[region.get("name")]=objNode
                    #print "added TP"
            self.networkNodes = nodesInNetwork
            #r_server.set('objNetworkObject', pickle.dumps(self.networkNodes) )




    def initNetwork(self, resetMemory='FALSE'):

        if resetMemory == 'TRUE':
            r_server.flushall()

        #if r_server.get('objNetworkObject') != None:
        #    self.networkNodes = pickle.loads(r_server.get('objNetworkObject'))
        #    #print('read from redis')
        #else:
            #print "initializing network ----------------------"
            #--- call createNodes() this method create a dictionary of nodeObjects.
            # This represents all the regions defined in the network config file
        configRoot = cElementTree.fromstring(self.configXML)
        for link in configRoot.iter('link'):
            if link.get('nodeType') == 'BaseNode':
                self.startNode=link.get('nodeName')

        self.createNodes("a")

        # -- call connectNodes() this methods sets up the connections between nodes
        # Important, nodes in this network are hierarchical , strictly in a child and parent relationship
        self.connectNodes()

        return self

    def exitNetwork(self):

        return self

    def formatRow(self,x):
      s = ''
      for c in range(len(x)):
        if c > 0 and c % 10 == 0:
          s += ','
        s += str(x[c]) + " , "
      s += ','
      return s


    def runNetworkWithValue(self, inputValue,learnFlag=False, reset=False, printStates=False, computeInfOutput=True):
        # configRoot = cElementTree.fromstring(self.configXML)
        # for link in configRoot.iter('link'):
        #     if link.get('nodeType') == 'BaseNode':
        #         start=link.get('nodeName')
        L1Predictions = []
        L2Predictions = []
        rawInputValue = inputValue.strip()
        rawInputValue = rawInputValue.lower()
        PredictionsArray=[]

        if inputValue.strip() == '':
            return {"returnValue": '' ,"strMsg":'', "PredictionGraph": ''}

        #L1 -------------
        retnValue = self.runNetwork(rawInputValue,'CHR', 0, reset, False, True, True)
        L1Predictions = retnValue['predictedValueForResult']
        for L1Prediction in L1Predictions:
             PredictionsArray.append((rawInputValue,L1Prediction))
        #     retnValue2 = self.runNetwork(L1Prediction,'CHR', 0, reset, learnFlag, True, True)
        #     L2Predictions = retnValue2['predictedValueForResult']
        #     #L2 -------------
        #     for L2Prediction in L2Predictions:
        #         PredictionsArray.append((L1Prediction,L2Prediction))
        # print PredictionsArray, '-----'
        #L3 ------------------

        printOutput = True
        strPrintLine = ""
        PredictionStream = ""
        #if retnValue['predictedValueForResult'] != None:
        #    if len(retnValue['predictedValueForResult']) >=1:
        #        print retnValue['predictedValueForResult'][0]
        self.getPredictionInsights(rawInputValue, PredictionsArray)
        if printOutput == True:
            strPrintLine += "<tr><td>" + str(rawInputValue)
            strPrintLine += " </td><td> " + self.formatRow(np.nonzero(retnValue['encodedOP']))
            strPrintLine += " </td><td> " + self.formatRow(np.nonzero(retnValue['SDROutput']))
            strPrintLine += " </td><td> " + self.formatRow(retnValue['predictedCells'])
            strPrintLine += "</td><td>" + self.formatRow(retnValue['predictedValueForResult'])
            strPrintLine += "</td></tr>"
            #PredictionStream += "<tr><td>" + str(rawInputValue) + " </td><td> " + str(self.formatRow(retnValue['predictedValueForResult'])) + "</td></tr>"

        if printOutput == True:
            strPrintLine = "<table class='Console'><tr><td>Input</td><td>Encoder O/p</td><td>SP o/p</td><td>TP Predicted</td><td>Predicted o/p</td></tr>" + strPrintLine
            strPrintLine +="</table>"
            #PredictionStream = "<table class='Console'><tr><td>Input Value</td><td>Predicted Value</td></tr>" + PredictionStream + "</table>"

        return {"returnValue": PredictionStream ,"strMsg":strPrintLine, "PredictionGraph": PredictionsArray}

    def getPredictionInsights(self, strValue, predictionsArray):
        strInsight_1='genre'
        strInsight_2='release year'
        arr1 =set()
        arr2 = set()
        #------------------------------------------------------------------------
        retnValue = self.runNetwork(strValue,'CHR', 0, False, False, True, True)
        v1Predictions = retnValue['predictedValueForResult']
        for v1Prediction in v1Predictions:
            arr1.add(v1Prediction)
            #retnValue2 = self.runNetwork(L1Prediction,'CHR', 0, reset, learnFlag, True, True)
            #L2Predictions = retnValue2['predictedValueForResult']
            #L2 -------------
            #for L2Prediction in L2Predictions:
            #    PredictionsArray.append((L1Prediction,L2Prediction))
        #------------------------------------------------------------------------
        retnValue = self.runNetwork(strInsight_1,'CHR', 0, False, False, True, True)
        v2Predictions = retnValue['predictedValueForResult']
        for v2Prediction in v2Predictions:
            arr2.add(v2Prediction)
            #retnValue2 = self.runNetwork(L1Prediction,'CHR', 0, reset, learnFlag, True, True)
            #L2Predictions = retnValue2['predictedValueForResult']
            #L2 -------------
            #for L2Prediction in L2Predictions:
            #    PredictionsArray.append((L1Prediction,L2Prediction))
        #------------------------------------------------------------------------------

        # for a in predictionsArray:
        #     print a[0], a[1]
        #     if a[0] == strValue:
        #         arr1.add(a[1])
        #     if a[0] == strInsight_2:
        #         print a[0]
        #         arr2.add(a[1])
        print predictionsArray
        print '@@@@@@@@@@@@@@@@@@@@@@', arr1 , '@@@@',arr2, '@@@@', set.intersection(arr1,arr2)

    def formatRow(self, x):
        s = ''
        for c in range(len(x)):
            if c > 0 and c % 10 == 0:
                s += ' '
            s += str(x[c]) + " , "
        s += ' '
        return s


    def runNetworkWithFile(self, inputFile,  learnFlag=True, reset=False, printStates=False, computeInfOutput=False):

        inputFile=inputFile
        self.INPUT_TYPE = "NATURAL_LANGUAGE"
        PrintInput =""
        PrintEncodedOp=None
        PrintSDROutput=None
        PrintPredictedCells=None
        PredictedValueForResult =None
        printOutput = True
        start=""
        reinforcementCount=5

        configRoot = cElementTree.fromstring(self.configXML)
        for link in configRoot.iter('link'):
            if link.get('nodeType') == 'BaseNode':
                start=link.get('nodeName')

        intNodes=0
        objNode = None
        inputVal=None
        outputVal=None
        outputVal1=np.zeros(1)
        strPrintLine = ""
        strPrintLineData = ""
        s = StringIO.StringIO()
        predictedValueForResult=""
        PredictionStream = ""
        strStopVal=""
        DataType = []

        #if self.INPUT_TYPE == 'CSV_CONTINUOUS' or self.INPUT_TYPE == 'CSV_DISCRETE':
        with open(inputFile,'r') as fo:
            fileObject = fo
            cursorCounter=0
            lineCounter = 0
            for fileLine in fileObject:
                fileLine = fileLine.strip()
                if lineCounter == 0:
                    self.INPUT_TYPE = fileLine.split(',')[0]
                    print 'First Line of File', self.INPUT_TYPE
                elif lineCounter == 1 :
                    if self.INPUT_TYPE =='CSVD' or self.INPUT_TYPE=='CSVC':
                        strStopVal=','
                        print 'breeeeeeeeeeeeeeeeeeeeee'
                    else:
                        strStopVal =' '
                    DataType = fileLine.split(strStopVal)
                   # print 'DataTypes', DataType
                elif lineCounter == 2:
                    break
                lineCounter +=1
            fo.close()

        #print self.INPUT_TYPE
        with open(inputFile,'r') as fo:
            fileObject = fo
            cursorCounter=0
            for counter in range(0,1):
                fileObject.seek(0,0)
                print '-------------------------------------------iter  ',counter
                for fileLine in fileObject:
                    fileLine = fileLine.strip()
                    words = fileLine.split(strStopVal)
                    lengthOfWords = len(words)
                    cursorCounter = 0
                    word0 = words[0]
                    word0 = word0.strip().lower()
                    for word in words:
                        word = word.strip()
                        rawInputValue = word
                        rawInputValue = rawInputValue.lower()
                        inputVal = rawInputValue
                        if self.INPUT_TYPE == 'CSVD':
                            if cursorCounter == lengthOfWords-1 or lengthOfWords == 0:
                                resetFl = True
                            else:
                                resetFl = False
                        else:
                            resetFl = False
                        if rawInputValue != '' :
                            #def runNetwork(self, rawInputValue,DataType, counter, resetL, enablelearnFlag , computeInfOutput, predict):
                            for counter in range(0,reinforcementCount):
                                self.runNetwork(word0, DataType[cursorCounter], 0, False, True, True,False)
                                self.runNetwork(rawInputValue, DataType[cursorCounter], 0, True, True, True,False)

                        cursorCounter +=1
                counter+=1
                #print '-------------------------------------------iter  ',counter
            fo.close()
        # with open(inputFile,'r') as fo1:
        #     fileObject1 = fo1
        #     for fileLine in fileObject1:
        #         fileLine = fileLine.strip()
        #         words=fileLine.split(strStopVal)
        #         lengthOfWords = len(words)
        #         cursorCounter = 0
        #         for word in words:
        #             word = word.strip()
        #             rawInputValue = word.strip()
        #             inputVal = word.strip()
        #
        #             if cursorCounter == 0:
        #                 retnValue = self.runNetwork(rawInputValue,DataType[cursorCounter], 0, False, False, True, True)
        #
        #                 if printOutput == True:
        #                     strPrintLineData += "<tr><td>" + str(rawInputValue)
        #                     strPrintLineData += " </td><td> " + self.formatRow(np.nonzero(retnValue['encodedOP']))
        #                     strPrintLineData += " </td><td> " + self.formatRow(np.nonzero(retnValue['SDROutput']))
        #                     strPrintLineData += " </td><td> " + self.formatRow(retnValue['predictedCells'])
        #                     strPrintLineData += "</td><td>" + self.formatRow(retnValue['predictedValueForResult'])
        #                     strPrintLineData += "</td></tr>"
        #                     PredictionStream += "<tr><td>" + str(rawInputValue) + " </td><td> " + str(self.formatRow(retnValue['predictedValueForResult'])) + "</td></tr>"
        #
        #             if cursorCounter == lengthOfWords-1:
        #                 if rawInputValue != '':
        #                     retnValue = self.runNetwork(rawInputValue,DataType[cursorCounter], 0, True, False, True, True)
        #             cursorCounter+=1
        #
        # if printOutput == True:
        #     strPrintLine = "<table class='Console'><tr><td>Input</td><td>Encoder O/p</td><td>SP o/p</td><td>TP Predicted</td><td>Predicted o/p</td></tr>" + strPrintLine
        #     strPrintLine += strPrintLineData
        #     strPrintLine +="</table>"
        #     PredictionStream = "<table class='Console'><tr><td>Input Value</td><td>Predicted Value</td></tr>" + PredictionStream + "</table>"
        #
        # fo1.close()
        # if self.INPUT_TYPE == 'NAT':
        #     with open(inputFile,'r') as fo:
        #         fileObject = fo
        #         cursorCounter=0
        #         for counter in range(0,reinforcementCount):
        #             resetFl = False
        #             for fileLine in fileObject:
        #                 fileLine = fileLine.strip()
        #                 words = fileLine.split(strStopVal)
        #                 lengthOfWords = len(words)
        #                 cursorCounter = 0
        #                 resetFl = True
        #                 for word in words:
        #                     rawInputValue = word
        #                     inputVal = word
        #                     self.runNetwork(rawInputValue, DataType[cursorCounter], 0, resetFl, True, True, False)
        #                     resetFl = False
        #                     cursorCounter +=1
        #             fo.close()
        with open(inputFile,'r') as fo1:
            fileObject1 = fo1
            intLineCounter = 0
            for fileLine in fileObject1:

                fileLine = fileLine.strip()
                words=fileLine.split(",")
                lengthOfWords = len(words)
                cursorCounter = 0
                for word in words:
                    rawInputValue = word.strip()
                    rawInputValue = rawInputValue.lower()
                    inputVal = rawInputValue

                    if intLineCounter >=2:
                        #if cursorCounter == 0:
                        if self.INPUT_TYPE == 'CSVD':
                            if cursorCounter == lengthOfWords-1 or lengthOfWords == 0:
                                resetFl = True
                            else:
                                resetFl = False
                        else:
                            resetFl = False

                        if rawInputValue !='':
                            retnValue = self.runNetwork(rawInputValue,DataType[cursorCounter], 0, resetFl, False, True, True)

                            if printOutput == True:

                                strPrintLine += "<tr><td>" + str(rawInputValue)
                                strPrintLine += " </td><td> " + self.formatRow(np.nonzero(retnValue['encodedOP']))
                                strPrintLine += " </td><td> " + self.formatRow(np.nonzero(retnValue['SDROutput']))
                                strPrintLine += " </td><td> " + self.formatRow(retnValue['predictedCells'])
                                strPrintLine += "</td><td>" + self.formatRow(retnValue['predictedValueForResult'])
                                strPrintLine += "</td></tr>"
                                PredictionStream += "<tr><td>" + str(rawInputValue) + " </td><td> " + str(self.formatRow(retnValue['predictedValueForResult'])) + "</td></tr>"

                            #if cursorCounter == lengthOfWords-1:
                            #    retnValue = self.runNetwork(rawInputValue,DataType[cursorCounter], 0, True, False, True, True)
                        cursorCounter+=1

                    intLineCounter += 1

            if printOutput == True:
                strPrintLine = "<table class='Console'><tr><td>Input</td><td>Encoder O/p</td><td>SP o/p</td><td>TP Predicted</td><td>Predicted o/p</td></tr>" + strPrintLine
                strPrintLine +="</table>"
                #PredictionStream = "<table class='Console'><tr><td>Input Value</td><td>Predicted Value</td></tr>" + PredictionStream + "</table>"


            fo1.close()
            print PredictionStream, '------------'
        return {"returnValue":PredictionStream, "strMsg":strPrintLine}



    def clearModel():
        r_server.set('objNetworkObject',None)
    def loadModel():
        if r_server.get('objNetworkObject') != None:
            self.networkNodes = pickle.loads(r_server.get('objNetworkObject'))
            #print('read from redis')
        #else:
           # print "initializing network ----------------------"
            #--- call createNodes() this method create a dictionary of nodeObjects.
            # This represents all the regions defined in the network config file

    def saveModel():
        try:
            r_server.set('objNetworkObject', pickle.dumps(self.networkNodes))
        except:
            pass


    def runNetwork(self, rawInputValue,DataType, counter, resetL, enablelearnFlag , computeInfOutput, predict):
        #print 'reset flag--------------', resetL
        #print rawInputValue
        intNodes = 0
        objNode = self.networkNodes[self.startNode]
        inputVal=rawInputValue
        counter2 = 0
        s = StringIO.StringIO()
        connectedSynapses=np.zeros(100)
        retPrediction = None
        predictedCells = None
        predictedValueForResult= None
        p =None
        s =None

        #print self.networkNodes
        if DataType == 'NUM':
            objEncNode = self.networkNodes['ScalarEncoder']
            inputVal=float(inputVal)
        elif DataType == 'CHR':
            objEncNode = self.networkNodes['GenericEncoder']
            inputVal = str(inputVal)
        elif DataType == 'DAT':
            objEncNode = self.networkNodes['DateEncoder']
            inputVal =  datetime.datetime.strptime(str(inputVal), '%Y-%m-%d %H:%M:%S')

        # Encode the input value based on the type of encoder
        #print rawInputValue,
        outputVal= objEncNode.nodeObj.encode(inputVal)
        encodedOP = outputVal
        inputVal=outputVal


        for intNodes in range(0, len(self.networkNodes)):
            if objNode != None :
                if objNode.nodeType=="EN" :
                    #inputVal = int(inputVal)
                    #if objNode.nodeType == 'GenericEncoder':
                    #    inputVal= str(inputVal)
                    #elif objNode.nodeType == 'ScalarEncoder':
                    #    inputVal = int(inputVal)
                    #elif objNode.nodeType == 'DataEncoder':
                    #    inputVal =  datetime.datetime.strptime(str(inputVal), '%Y-%m-%d %H:%M:%S')

                    #outputVal= objNode.nodeObj.encode(inputVal)
                    #encodedOP = outputVal
                    print '---'
                if objNode.nodeType=="SP":

                    outputVal1=np.zeros(objNode.inputWidth)
                    objNode.nodeObj.compute(inputVal, learn=True, activeArray=outputVal1)
                    SDROutput = outputVal1
                    print '33333333333333333333333', inputVal.nonzero(), SDROutput.nonzero()

                    #for SDRValSingle in np.nonzero(SDROutput)[0]:
                    #    connectedSynapses = np.zeros(100)
                    #    objNode.nodeObj.getConnectedSynapses(SDRValSingle,connectedSynapses)
                        #print '--0--0--0', SDRValSingle , np.nonzero(connectedSynapses)

                    if counter == 0:
                        r_server.set(np.nonzero(outputVal1) ,np.nonzero(inputVal))
                        #print rawInputValue ,np.nonzero(outputVal1)
                        for counter2 in range(0,len(np.nonzero(outputVal1)[0])):
                            #print 'adding to redis...'
                            r_server.sadd(str("DataKey") + rawInputValue , str(np.nonzero(outputVal1)[0][counter2]))
                            r_server.sadd(str("DataValue") + str(np.nonzero(outputVal1)[0][counter2]), str(rawInputValue))
                    outputVal=outputVal1

                if objNode.nodeType=="TP":
                    #objNode.nodeObj.compute(inputVal, enableLearn = enablelearnFlag, computeInfOutput = computeInfOutput)
                    predictedCells1=None
                    #print enablelearnFlag, '------------000000000----'
                    print 'SDR input ++ :' , inputVal.nonzero()
                    print 'rawInputValue :', rawInputValue
                    print 'encodedOP :' , encodedOP.nonzero()
                    print 'SDROutput :' , SDROutput.nonzero()
                    print 'SDRInput :' , inputVal.nonzero()
                    printPredictedCells=''

                    retnValue = objNode.nodeObj.compute(inputVal, enableLearn = enablelearnFlag, computeInfOutput = computeInfOutput)
                    #inputVal,'CHR',0, enablelearnFlag,True,True)
                    #print predictedCells1, '233---------------------'
                    if predict==True:

                        predictedCells = objNode.nodeObj.getPredictedState()

                        predictedValueForResult= self.getPredictedOutPut(predictedCells)
                        if predictedCells !=None:
                            printPredictedCells=map(int,predictedCells.max(axis=1).nonzero()[0])
                        #predictedValueForResult= self.getPredictedOutPut(map(int,predictedCells.max(axis=1).nonzero()[0]))

                        print '>>>>>>>>>>>>>>>>>>>>>', inputVal.nonzero(),map(int,predictedCells.max(axis=1).nonzero()[0]), predictedValueForResult

                        retPrediction =predictedValueForResult

                        #p = StringIO.StringIO()
                        #print predictedCells , 'predictedCells are here'
                        # z=np.array(map(int,predictedCells.max(axis=1).nonzero()[0]))
                        # z= predictedCells
                        #
                        # if predictedCells !=None:
                        #     np.savetxt(p, z , fmt='%.0f', newline=",")
                        # else:
                        #     np.savetxt(p, '' , fmt='%.0f', newline=",")
                        # r_server.set("lastPredictedSDR", p.getvalue())


                    #Reset the learning
                    if resetL == True:
                        objNode.nodeObj.reset()

                objNode=objNode.parentNode
                inputVal=outputVal

        s = StringIO.StringIO()
        np.savetxt(s, SDROutput, fmt='%.5f', newline=",")
        r_server.set('lastSDR', s.getvalue() )

        if p != None:
            lastPredictedSDRSerialized = p.getvalue()
        else:
            lastPredictedSDRSerialized =None
        return {'encodedOP':encodedOP, 'SDROutput':SDROutput, 'predictedCells':printPredictedCells, 'predictedValueForResult':predictedValueForResult,'lastSDR':s.getvalue(), 'lastPredictedSDR':lastPredictedSDRSerialized}


    def getPredictedOutPut(self, predictedCells):
        opVal=0
        #print predictedCells, 'more here'
        inputVal= np.array(map(str,predictedCells.max(axis=1).nonzero()[0]))
        #inputVal= predictedCells
        #print inputVal,predictedCells, '==================='
        #print inputVal
        d = set()
        possibleValues=[]
        setOfAllPotentialValues=set()
        setOfPotentialValuesForKey=set()
        if inputVal != None:
            for inputCell in inputVal:
                setOfPotentialValuesForKey = r_server.smembers("DataValue" + str(inputCell))

                setOfAllPotentialValues= set.union(setOfAllPotentialValues,setOfPotentialValuesForKey)
        for key in setOfAllPotentialValues:
            SDRforKey=r_server.smembers("DataKey" + str(key))
            #print key,  "SDRforKey" , SDRforKey
            #print "inputVal" , inputVal
            #print "intersection",  set.intersection(set(inputVal.flatten()),set(SDRforKey))

            if(len(set.intersection(set(inputVal),set(SDRforKey))) >= len(SDRforKey)):
               d.add(key)

        returnList=list(d)
        return returnList



    def getParams(self, inputObject):
        returnDict={}
        for k in inputObject:
            try:
                returnDict[k.tag]=int(k.text)
            except:
                try:
                    returnDict[k.tag]=float(k.text)
                except:
                    returnDict[k.tag]=k.text

        return returnDict

    def createSensor(self, sensorType, fieldParams):
        returnParams= self.getParams(fieldParams)
        type=returnParams['type']
        del returnParams['type']
        encoder = eval(sensorType)(**returnParams)
        return encoder

    def createSpatialPooler(self,spType, fieldParams):
        returnParams = self.getParams(fieldParams)
        type=returnParams['type']
        del returnParams['type']
        del returnParams['name']
        del returnParams['spatialImp']
        del returnParams['inputWidth']
        sp = eval(spType)(**returnParams)
        return sp
    def createTemporalPooler(self, tptype, fieldParams):
        returnParams=self.getParams(fieldParams)
        type=returnParams['type']
        del returnParams['name']
        del returnParams['type']
        del returnParams['inputWidth']

        tp = eval(tptype)(**returnParams)
        return tp


    def getModelConfig(project_id):
        strRawXml=""
        return strRawXml

    def resetTraining(self,project_id = None):
        #r_server.delete('objNetworkObject')
        r_server.flushall()
        return True

#------------------------------NetworkBuilder------------------------------------------




#---------------------------------Test--------------------------------------------------




#---------------------- Create Regions ----------------------



#---------------------- Link Regions ----------------------


#---------------------- Link Regions ----------------------
