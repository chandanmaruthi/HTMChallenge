from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext, loader
from django.shortcuts import get_object_or_404, render, render_to_response
from django.core.urlresolvers import reverse
from models import ModelMap, Project, DataFile ,DataFolder
from django.utils import timezone
from django.core.exceptions import ValidationError
from forms import trainingDataForm
from django.contrib.auth.decorators import login_required
from networkBuilder import Network
from django.contrib.auth import authenticate, login, logout
from walnutclient import *
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib.pyplot import *
from matplotlib import pylab
import redis
import PIL
import PIL.Image
import StringIO
import networkx as nx
import matplotlib.pyplot as plt
import operator
import random
import cPickle as pickle
import os
import sys

from networkBuilder import Network
from networkBuilder import Region
from networkBuilder import Node

predictionGraph = None
def user_login(request):
    state = "Please log in below..."
    username = ''
    password = ''
    if request.POST:
        state = "here 1"
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in!"
            else:
                state = "Your account is not active, please contact the site admin."

            template = loader.get_template('curiousWorkbench/index.html')
            context =  RequestContext(request, {
                'state': state,
                })
            return HttpResponse(template.render(context))
        else:
            state = "Your username and/or password were incorrect."
            template = loader.get_template('curiousWorkbench/login.html')
            context =  RequestContext(request, {
                'state': state,
                })
            return HttpResponse(template.render(context))

    #state = "error occured."
    template = loader.get_template('curiousWorkbench/login.html')
    context =  RequestContext(request, {
        'state': state,
        })
    return HttpResponse(template.render(context))




def user_logout(request):
    logout(request)
    template = loader.get_template('curiousWorkbench/login.html')
    context =  RequestContext(request, {
        'state': "You Have been logged out, Please login again if you wish to continue ",
    })
    return HttpResponse(template.render(context))

@login_required
def index(request):
    template = loader.get_template('curiousWorkbench/index.html')
    context =  RequestContext(request, {
        'latest_question_list': 1,
    })
    return HttpResponse(template.render(context))

@login_required
def configModel(request):
    modelMapList = ModelMap.objects.order_by('-Created')
    template = loader.get_template('curiousWorkbench/configModel.html')
    context =  RequestContext(request, {
     'modelMapList': modelMapList,
    })
    return HttpResponse(template.render(context))

@login_required
def deleteModel(request,model_Id):
    selMap = ModelMap.objects.get(pk=model_Id)
    selMap.delete()

    modelMapList = ModelMap.objects.order_by('-Created')
    template = loader.get_template('curiousWorkbench/configModel.html')
    context =  RequestContext(request, {
     'modelMapList': modelMapList,
    })
    return HttpResponse(template.render(context))

@login_required
def trainProject(request, project_id):
    dataFileList = DataFile.objects.order_by('-LastUpdated')
    strMsg = ""
    selProject=get_object_or_404(Project, pk=project_id)
    objWalnutClient= walnutclient(5001,'localhost',selProject.ModelMap.RawXML)

    if 'trainForValue' in request.POST:
        trainValue=request.POST["txtTrain"]
        if trainValue.strip() !='':
            runValueList=None
            modelMap = selProject.ModelMap

            runValue =  objWalnutClient.runNetworkWithValue(trainValue, False,False,False,True)

            predictionGraph = runValue["PredictionGraph"]
            #FormattedReturn=formatPrediction(0, returnValue)
            template = loader.get_template('curiousWorkbench/trainProject.html')
            predictionGraphImagePath = drawPredictionGraph(predictionGraph)
            context =  RequestContext(request, {
            'project' : selProject,
            'modelMap': modelMap,
            'runValue':runValue["returnValue"],
             'strMsg':runValue["strMsg"],
             'predictionGraphImagePath':predictionGraphImagePath,
             'dataFileList': dataFileList,
            })
        else:
            modelMap = selProject.ModelMap
            template = loader.get_template('curiousWorkbench/trainProject.html')
            context =  RequestContext(request, {
            'project' : selProject,
            'modelMap': modelMap,
            'runValue':'',
             'strMsg':'',
             'predictionGraphImagePath':'',
             'dataFileList': dataFileList,
            })
    elif 'trainWithFile' in request.POST:
        if request.POST["rdoDataFile"] != "0":
            trainValueFile=request.POST["rdoDataFile"]
            runValue = objWalnutClient.runNetworkWithFile(trainValueFile,'CSV',True,False,False,True)
        else:
            runValue = {"returnValue":"No File Selected","strMsg":""}
        selProject=get_object_or_404(Project, pk=project_id)
        modelMap = selProject.ModelMap


        template = loader.get_template('curiousWorkbench/trainProject.html')
        context =  RequestContext(request, {
        'project' : selProject,
         'modelMap': modelMap,
         'runValue':runValue['returnValue'],
         'strMsg':runValue['strMsg'],
         'dataFileList': dataFileList
        })
    elif 'resetProject' in request.POST:
        returnV = objWalnutClient.resetTraining()

        #objNetwork = Network()
        #objNetwork.resetTraining(project_id)
        selProject=get_object_or_404(Project, pk=project_id)
        modelMap = selProject.ModelMap


        template = loader.get_template('curiousWorkbench/trainProject.html')
        context =  RequestContext(request, {
        'project' : selProject,
         'modelMap': modelMap,
         'runValue':"--",
         'strMsg':"",
         'dataFileList': dataFileList
        })
    else:
        selProject=get_object_or_404(Project, pk=project_id)
        modelMap = selProject.ModelMap
        template = loader.get_template('curiousWorkbench/trainProject.html')
        context =  RequestContext(request, {
        'project' : selProject,
         'modelMap': modelMap,
         'runValue':"--",
         'strMsg':"",
         'dataFileList': dataFileList,
        })

    return HttpResponse(template.render(context))


@login_required
def addModel(request):
    template = loader.get_template('curiousWorkbench/addModel.html')
    context =  RequestContext(request, {'timeStamp':timezone.now()})
    return HttpResponse(template.render(context))

@login_required
def editModel(request, model_Id):
    modelMapSpecfic = get_object_or_404(ModelMap, pk=model_Id)
    template = loader.get_template('curiousWorkbench/editModel.html')
    context =  RequestContext(request, {
     'modelMap': modelMapSpecfic,
    })
    return HttpResponse(template.render(context))

@login_required
def saveModel(request, model_Id):

    if 'saveModel' in request.POST:
        selectedmodelMap = get_object_or_404(ModelMap, pk=model_Id)
        updatedXML = request.POST['RawXML']
        modelDescription = request.POST['modelDescription']
        selMap = ModelMap.objects.get(pk=model_Id)
        selMap.Description = modelDescription
        selMap.RawXML = updatedXML
        selMap.Created = timezone.now()
        selMap.save()
        return HttpResponseRedirect(reverse('curiousWorkbench:editModel', args=(selMap.id,)))
    elif 'deleteModel' in request.POST:
        selMap = ModelMap.objects.get(pk=model_Id)
        selMap.delete()
        return HttpResponseRedirect(reverse('curiousWorkbench:configModel', ))

@login_required
def saveNewModel(request):
    try:
        selMap = ModelMap()
        rawXMLValue = request.POST['RawXML']
        modelMapNameValue = request.POST['modelMapName']
        modelDescription = request.POST['modelDescription']
        if modelMapNameValue == '' or rawXMLValue == '':
            raise ValidationError(u'Model Name and Configuration are Mandatory' )
        selMap.Name = modelMapNameValue
        selMap.Description = modelDescription
        selMap.RawXML = rawXMLValue
        selMap.Created = timezone.now()
        selMap.CreatedBy = 'Chandan'
    except KeyError:
        # Redisplay the question voting form.
        return render(request, 'curiousWorkbench/configModel.html', {})
    else:
        selMap.save()
    return HttpResponseRedirect(reverse('curiousWorkbench:editModel', args=(selMap.id,)))

@login_required
def configDataFile(request):
    if request.method == 'POST':
        form = trainingDataForm(request.POST, request.FILES)
        if form.is_valid():
            fileNameValue=request.POST['FileName']
            #dataFolderInstance=get_object_or_404(DataFolder, pk=1)
            newdoc = DataFile(dataFile = request.FILES['docfile'],
                              FileName = fileNameValue,
                              CreatedBy = 'chandan',
                              LastUpdated = timezone.now(),
                              Description ='')
            newdoc.save()
            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('curiousWorkbench:configDataFile'))
        else:
            form = trainingDataForm()
    #A empty, unbound form
    #Load documents for the list page
    #documents = DataFile.objects.all()
    dataFileList = DataFile.objects.order_by('-LastUpdated')
    template = loader.get_template('curiousWorkbench/configDataFile.html')
    #Render list page with the documents and the form
    return render_to_response(
        'curiousWorkbench/configDataFile.html',
        {'dataFileList': dataFileList, 'form': trainingDataForm},
        context_instance=RequestContext(request))

@login_required
def configProject(request):
    if request.method == 'POST':
        projectNameValue=request.POST['projectName']
        projectDescriptionValue=request.POST['projectDescription']
        selModelMapIDValue=request.POST['selModelMap']
        selModelMap=get_object_or_404(ModelMap, pk=selModelMapIDValue)
        newProject = Project(Name = projectNameValue,
                         Description =projectDescriptionValue,
                         ModelMap = selModelMap,
                         CreatedBy = 'chandan',
                         LastUpdated = timezone.now())
        newProject.save()
        # Redirect to the document list after POST
        return HttpResponseRedirect(reverse('curiousWorkbench:configProject'))

    projectList = Project.objects.order_by('-LastUpdated')
    template = loader.get_template('curiousWorkbench/configProject.html')
    context =  RequestContext(request, {
      'projectList': projectList,
      'ModelMap': ModelMap.objects.all(),
      'timeStamp':timezone.now(),
    })
    return HttpResponse(template.render(context))




@login_required
def selectTrainProject(request):
    if request.method == 'POST':
        projectNameValue=request.POST['projectName']
        projectDescriptionValue=request.POST['projectDescription']
        selModelMapIDValue=request.POST['selModelMap']
        selModelMap=get_object_or_404(ModelMap, pk=selModelMapIDValue)
        newProject = Project(Name = projectNameValue,
                         Description =projectDescriptionValue,
                         ModelMap = selModelMap,
                         CreatedBy = 'chandan',
                         LastUpdated = timezone.now())
        newProject.save()
        # Redirect to the document list after POST
        return HttpResponseRedirect(reverse('curiousWorkbench:selectTrainProject'))

    projectList = Project.objects.order_by('-LastUpdated')
    template = loader.get_template('curiousWorkbench/selectTrainProject.html')
    context =  RequestContext(request, {
      'projectList': projectList,
      'ModelMap': ModelMap.objects.all(),
      'timeStamp':timezone.now(),
    })
    return HttpResponse(template.render(context))

@login_required
def deleteDataFile(request, dataFile_Id):
    selectedDataFile = get_object_or_404(DataFile, pk=dataFile_Id)
    selectedDataFile.delete()
    template = loader.get_template('curiousWorkbench/configDataFile.html')
    context =  RequestContext(request, {'timeStamp':timezone.now()})
    return HttpResponseRedirect(reverse('curiousWorkbench:configDataFile', ))

# ------------------------Import\Export Network--------------------------------------
@login_required
def exportNeuralNetwork(request):
    template = loader.get_template('curiousWorkbench/importNeuralNetwork.html')
    context =  RequestContext(request, {'latest_question_list': 1,})
    return HttpResponse(template.render(context))

@login_required
def importNeuralNetwork(request):
    template = loader.get_template('curiousWorkbench/exportNeuralNetwork.html')
    context =  RequestContext(request, {'latest_question_list': 1,})
    return HttpResponse(template.render(context))


#  ------------------------Data Folder--------------------------------------
@login_required
def configDataFolder(request):
    dataFolderList = DataFolder.objects.order_by('-LastUpdated')
    template = loader.get_template('curiousWorkbench/configDataFolder.html')
    context =  RequestContext(request, {'dataFolderList': dataFolderList,})
    return HttpResponse(template.render(context))

@login_required
def addDataFolder(request):
    template = loader.get_template('curiousWorkbench/addDataFolder.html')
    context =  RequestContext(request, {'timeStamp':timezone.now()})
    return HttpResponse(template.render(context))

@login_required
def editDataFolder(request, dataFolder_Id):
    dataFolderSpecfic = get_object_or_404(ModelMap, pk=dataFolder_Id)
    template = loader.get_template('curiousWorkbench/editDataFolder.html')
    context =  RequestContext(request, {
     'dataFolderSpecfic': dataFolderSpecfic,
    })
    return HttpResponse(template.render(context))


@login_required
def addDataFile(request):
    template = loader.get_template('curiousWorkbench/addDataFile.html')
    context =  RequestContext(request, {'timeStamp':timezone.now()})
    return HttpResponse(template.render(context))

@login_required
def editDataFile(request, dataFile_Id):
    dataFileSpecfic = get_object_or_404(ModelMap, pk=dataFile_Id)
    template = loader.get_template('curiousWorkbench/editDataFile.html')
    context =  RequestContext(request, {
     'dataFileSpecfic': dataFileSpecfic,
    })
    return HttpResponse(template.render(context))


# def runNetworkWithValue(trainValue, strRawXML=""):
#     # Logic
#     # Step 1 :Create an object of the class Network
#     #objNetwork=Network()
#     objWalnutClient= walnutclient(5001,'localhost',strRawXML)
#
#     # Input a value to the encoder and follow it up the nextwork, observe the outputs at each stage
#     returnValue =  objWalnutClient.runNetworkWithValue(trainValue, False,False,False,True)
#
#     objWalnutClient.close()
#
#     #FormattedReturn=formatPrediction(0, returnValue)
#
#     strMsg="wow"
#     return returnValue
#
# def runNetworkWithFile( trainValueFile,strRawXML=""):
#
#     #print strRawXML
#     # Logic
#     # Step 1 :Create an object of the class Network
#     objNetwork=Network()
#
#     # Step 2 :Call network.setConfigPath() to provide the network a path of the config file
#     #objNetwork.setConfigPath("/home/chandanmaruthi/chandan/code/brainscience/config.xml")
#
#     objNetwork.setConfigModel(strRawXML)
#
#     # Step 3 :Call network.initiateNetwork, this step performs the following tasks
#     # a.) calls the createNodes functions, to create regions as specified in config
#     # B.) calls connect nodes connect to setup connections between nodes are specified in the config
#     objNetwork.initNetwork()
#
#     # Test Network Setup by printing the values
#     #objNetwork.printNetwork("a")
#
#     # Input a value to the encoder and follow it up the nextwork, observe the outputs at each stage
#
#     returnValue =  objNetwork.runNetworkWithFile(trainValueFile,True,False,False,False)
#
#     returnValue =  objNetwork.runNetworkWithFile(trainValueFile ,False,False,False,True)
#     objNetwork.exitNetwork()
#
#     #FormattedReturn=formatPrediction(1, returnValueDict)
#
#     #FormattedReturn= returnValue
#
#     return returnValue

def formatPrediction(PredictionType=0, returnValue=""):

    # Prediction Type 0 is single value, prediction type 1 is file\multivalue
    strFormatReturn=  str.replace(returnValue, '\r\n', '<br/>')

    return strFormatReturn

def simple1(request):
    #return HttpResponse(None, content_type = "image/png")

    r_server = redis.Redis('localhost')
    strFromRedis=r_server.get('lastSDR')
    try:
        strFromRedisPredicted=r_server.get('lastPredictedSDR')
        #print 'ok maaaan'
        #print strFromRedisPredicted
        #print strFromRedis
        #print strFromRedis
        npSDRArray = np.fromstring(strFromRedis, sep=',')
        #print 'ok maaaan1'
        npSDRArrayPredicted = np.fromstring(strFromRedisPredicted, sep=',')
        #print 'ok maaaan2', len(npSDRArrayPredicted), len(npSDRArray), strFromRedis
        #print npSDRArray
        for a in npSDRArrayPredicted:
            npSDRArray[a] = 2
        #print 'ok maaaan2.5'
        #npSDRArrayPredicted = np.fromstring(strFromRedisPredicted, sep=',')
        #print npSDRArray
        #print npSDRArray.shape
        npSDRArray=np.reshape(npSDRArray,(32,32))
        #print 'ok maaaan3'
        #print npSDRArray
    except someError:
        print 'error'
        raise someError
    #print strFromRedisPredicted
    #print npSDRArrayPredicted.
    #npSDRArrayPredicted=np.reshape(npSDRArrayPredicted,(128,128))
    #npSDRArrayPredicted[npSDRArrayPredicted ==1 ] = 5
    #npSDRArray = np.hstack[npSDRArray,npSDRArrayPredicted]
    #print npSDRArray.shape
    #print npSDRArray
    #print npSDRArray
    #a = numpy.random.randint(0,2,(10,10))


    x= [1,2,3,4,5]
    y= [1,2,3,4,5]
    #plot(a)
    cdict = {'red': ((0.0, 0.0, 0.0), (0.5, 1.0, 0.7),(1.0, 1.0, 1.0)),
        'green': ((0.0, 0.0, 0.0),(0.5, 1.0, 0.0),(1.0, 1.0, 1.0)),
        'blue': ((0.0, 0.0, 0.0),(0.5, 1.0, 0.0),(1.0, 0.5, 1.0))}
    my_cmap = matplotlib.colors.LinearSegmentedColormap('my_colormap',cdict,256)

    #xlabel('x axix')
    #ylabel('y axis')

    title('SDR')
    grid(True)

    figure(1)
    imshow(npSDRArray, interpolation='nearest', cmap=my_cmap)
    grid(True)

    buffer = StringIO.StringIO()
    canvas = pylab.get_current_fig_manager().canvas
    canvas.draw()
    graphIMG=PIL.Image.fromstring("RGB",canvas.get_width_height(),canvas.tostring_rgb())
    graphIMG.save(buffer, "PNG")
    buffer.seek(0)
    #im = Image.open(imgdata)
    pylab.close()
    return HttpResponse(buffer.getvalue(), content_type = "image/png")

def drawPredictionGraph(predictionGraph):
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
    absFileLocation = '/home/chandan/chandan/code/brainscience/curious/curiousWorkbench/static/curiousWorkbench/images' +'/predictionGraph.png'
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
# Create your views here.
