from django.conf.urls import patterns, url
from django.conf import settings
from curiousWorkbench import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/', views.user_login, name="user_login"),
    url(r'^logout/', views.user_logout, name="user_logout"),
    url(r'^configProject/', views.configProject, name='configProject'),
    url(r'^selectTrainProject/', views.selectTrainProject, name='selectTrainProject'),
    url(r'^configModel/', views.configModel, name='configModel'),
    url(r'^trainProject/(?P<project_id>\d+)/$', views.trainProject, name='trainProject'),
    url(r'^addModel/', views.addModel, name='addModel'),
    url(r'^editModel/(?P<model_Id>\d+)/$', views.editModel, name='editModel'),
    url(r'^deleteModel/(?P<model_Id>\d+)/$', views.deleteModel, name='deleteModel'),
    url(r'^exportNeuralNetwork/', views.exportNeuralNetwork, name='exportNeuralNetwork'),
    url(r'^importNeuralNetwork/', views.importNeuralNetwork, name='importNeuralNetwork'),
    url(r'^saveModel/(?P<model_Id>\d+)/$', views.saveModel, name='saveModel'),
    url(r'^saveNewModel/', views.saveNewModel, name='saveNewModel'),
    url(r'^configDataFolder/', views.configDataFolder, name='configDataFolder'),
    url(r'^addDataFolder/', views.addDataFolder, name='addDataFolder'),
    url(r'^editDataFolder/(?P<dataFolder_Id>\d+)/$', views.editDataFolder, name='editDataFolder'),
    url(r'^configDataFile/', views.configDataFile, name='configDataFile'),
    url(r'^addDataFile/', views.addDataFile, name='addDataFile'),
    url(r'^editDataFile/(?P<dataFile_Id>\d+)/$', views.editDataFile, name='editDataFile'),
    url(r'^deleteDataFile/(?P<dataFile_Id>\d+)/$', views.deleteDataFile, name='deleteDataFile'),
    url(r'^trainingData/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT,})
)
