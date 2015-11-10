from django.db import models

class ModelMap(models.Model):
	Name = models.CharField(max_length=200)
	CreatedBy = models.CharField(max_length=200)
	Created = models.DateTimeField('date created')
	Description =models.TextField()
	RawXML = models.TextField()



class DataFolder(models.Model):
	FolderName = models.CharField(max_length=200)
	CreatedBy = models.CharField(max_length=200)
	LastUpdated = models.DateTimeField('date created')
	Description =models.TextField()

class DataFile(models.Model):
	FileName = models.CharField(max_length=200)
	dataFile = models.FileField(upload_to='%Y/%m/%d')
	CreatedBy = models.CharField(max_length=200)
	LastUpdated = models.DateTimeField('date created')
	Description =models.TextField()


class Project(models.Model):
	Name = models.CharField(max_length=200)
	ModelMap = models.ForeignKey(ModelMap)
	CreatedBy = models.CharField(max_length=200)
	LastUpdated = models.DateTimeField('date created')
	Description =models.TextField()

# Create your models here.
