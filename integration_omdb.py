import requests
import json
import sys
import networkx as nx
import matplotlib.pyplot as plt
import PIL
import PIL.Image
import StringIO
import random
import cPickle as pickle
import os
import sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import *
from matplotlib import pylab
sys.path.append('/home/ubuntu/chandan/brainscience/curious/')

from walnutclient import *

class OMDBServiceIntegration:




    def FindMovie(self, movieTitle='', year ='', plot = '' ,tomatoes = True ):
        print movieTitle

        payload = {'t': movieTitle , 'plot': 'short','r':'json', 'tomatoes':'true'}
        print payload
        if movieTitle !='':
            r = requests.get("http://www.omdbapi.com/", params=payload)

        responseText = r.text
        responseDict = json.loads(responseText)
        retVal = self.getWalnutResponse(movieTitle)
        predictionGraph =retVal['PredictionGraph']
        predictionGraphImagePath = self.drawPredictionGraph(predictionGraph)
        try:
            msg=''
            msg += ':+1: Title : ' + responseDict['Title'] + ' IMDB [:star:' + responseDict['imdbRating'] +  '] Tomatoes [:star:' + responseDict['tomatoRating'] + ']\n'
            msg += ':calendar: Year : ' + responseDict['Year'] + '\n '
            msg += ':clock1: Runtime : ' + responseDict['Runtime'] + '\n '
            msg += ':cinema: Genre : ' + responseDict['Genre'] + '\n '
            msg += ':dancer: Actors : ' + responseDict['Actors'] + '\n '
            msg += ':pencil: Plot  : ' + responseDict['Plot'] +'\n'
            msg += str(retVal)
            #print msg
        except KeyError, Arguement:
            msg='I couldnt find that movie :anguished: , lets try something else '
        return msg

    def getWalnutResponse(self, trainValue):
        strRawModelXML = self.getModelFile()
        objWalnutClient= walnutclient(5001,'localhost',strRawModelXML)
        runValue =  objWalnutClient.runNetworkWithValue(trainValue, False,False,False,True)
        return runValue

    def getModelFile(self):
        strDataFolder = "/home/ubuntu/chandan/Data/"
        strRootFolder = "/home/ubuntu/chandan/brainscience/"
        strAppFolder = "curious/"
        strModelFolder = 'curiousWorkbench/test/models/'


        strModelFile = 'model2.txt'
        #strDataFile ='Test_003_1_WordList.csv'
        strDataFile ='Test_003_WordListNew.csv'

        inputModelFile = strRootFolder + strAppFolder + strModelFolder + strModelFile
        strInputDataFile = strDataFolder + strDataFile

        fo = open(inputModelFile,'r')
        strRawModelXML = fo.read()
        return strRawModelXML

    def drawPredictionGraph(self,predictionGraph):
        graph = predictionGraph
        #a=predictionGraph[0
        # create networkx graph
        G = None
        G=nx.Graph()
        # add nodes
        nodes =[]
        labelsDict ={}
        for connect in graph:
            if connect[0] in nodes == False:
                nodes.append(u(connect[0]))
            if connect[1] in nodes == False:
                nodes.append(u(connect[1]))
        for node in nodes:
            labelsDict[node] = node

        G.add_nodes_from(nodes)
        pos = nx.spring_layout(G)
        #pos = nx.ego_graph(G,a)
        H=nx.relabel_nodes(G,labelsDict)
        # add edges
        for edge in graph:
            H.add_edge(edge[0], edge[1])

        # draw graph
        nx.draw_spring(H, node_size=1000, node_color="#99CCFF", with_labels = True, node_shape='o', alpha=0.8, font_size=8)
        buffer = StringIO.StringIO()
        randomeKey=random.randint(1, 100000000)
        absFileLocation = '/home/ubuntu/chandan/brainscience/curious/curiousWorkbench/static/curiousWorkbench/images' +'/predictionGraph.png'
        # show graph
        #plt.savefig(buffer, format='png')
        plt.savefig(absFileLocation)

        #plt.show()
        #buffer.seek(0)
        #im = Image.open(imgdata)
        pylab.close()

        # draw example
        #return HttpResponse(buffer.getvalue(), content_type = "image/png")
        return absFileLocation + '?dummy=' + str(randomeKey)
