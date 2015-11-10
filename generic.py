
import math
import numbers

import numpy
from nupic.data import SENTINEL_VALUE_FOR_MISSING_DATA
from nupic.data.fieldmeta import FieldMetaType
from nupic.bindings.math import SM32, GetNTAReal
from nupic.encoders.base import Encoder, EncoderResult
import redis


class GenericEncoder:
    width=0
    numberOfOnBits=0
    TallLetters = ['b','d','f','g','h','j','k','l','p','q','t','y','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','X','Y','Z']
    r_server = redis.Redis('localhost')

    def __init__(self, w=0, n=0, forced = False, name="s"):
        self.width=w
        self.numberOfOnBits=n

    def encode(self, stringToEncode, debug = False):
        stringToEncode=str(stringToEncode)
        Entity = stringToEncode
        #>>> np.lib.pad(a, (2,3), 'constant', constant_values=(4,6))

        EdgeStart = map(int,list(str(bin(ord(stringToEncode[:1]))[2:])))
        EdgeEnd = map(int,list(str(bin(ord(stringToEncode[len(stringToEncode)-1:]))[2:])))
        ShapeW = map(int,list(str(bin(len(stringToEncode))[2:])))
        Contour = self.getCountour(stringToEncode)
        #print Contour
        npArray= numpy.zeros(100)

        EdgeStartReturn = numpy.lib.pad(EdgeStart,(20-len(EdgeStart),0),'constant',constant_values=(0))
        EdgeEndReturn = numpy.lib.pad(EdgeEnd,(20-len(EdgeEnd),0),'constant',constant_values=(0))
        ShapeWReturn = numpy.lib.pad(ShapeW,(20-len(ShapeW),0),'constant',constant_values=(0))
        ContourReturn= numpy.zeros(20)
        BlankPlaceHolder = numpy.zeros(20)
        for index in Contour:
            if index < len(ContourReturn):
                ContourReturn[index] = 1
            #ContourReturn[index] = 1

        returnArray = numpy.append(EdgeStartReturn,EdgeEndReturn)
        returnArray = numpy.append(returnArray,ShapeWReturn )
        returnArray = numpy.append(returnArray,ContourReturn)
        returnArray = numpy.append(returnArray,BlankPlaceHolder)

        #self.r_server.set(returnArray,stringToEncode)
        self.r_server.set(stringToEncode, numpy.flatnonzero(returnArray))

        if debug == True:
            #EdgeStartReturn = numpy.lib.pad(EdgeStart,(0,20-len(EdgeStart)),'constant',constant_values=(0))
            print "Entity : " + str(Entity)
            print "EdgeStart : " + str(EdgeStartReturn)
            print "EdgeEnd : " + str(EdgeEndReturn)
            print "ShapeW : " + str(ShapeWReturn)
            print "Contour : " + str(ContourReturn)
            print "FullEncodedArray : " + str(returnArray)
            print "FullEncodedArray NonZeros: " + str(numpy.nonzero(returnArray))

        return returnArray

    def decode(self, encodedValue):
        retrievedValue=self.r_server.get(encodedValue)
        return retrievedValue

    def getCountour(self, stringToEncode):
        contourList=[]
        chrPlace=0
        for char in stringToEncode:
            if char in self.TallLetters:
                contourList.append(chrPlace)
            chrPlace = chrPlace + 1
        return contourList
# w : width of the SDR
# n : number of active bits
# Entity
# Edge Detection
# Start ASCII Chr
# Edge Detection
# End ASCII Chr
# Shape width / height
# Contour
