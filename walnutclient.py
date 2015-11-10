#!/usr/bin/python           # This is client.py file
import socket               # Import socket module
import struct

class walnutclient:
    PORT_NUMBER = 0
    HOST_NAME = ''
    MODEL_DESC = ''
    #CALL_NUMBER = 0

    def __init__(self, portnumber, hostname, strRawXML):

        self.PORT_NUMBER = portnumber
        self.HOST_NAME = hostname
        self.MODEL_DESC = strRawXML
        # if self.CALL_NUMBER == 0:
        #     self.initNetwork()
        # s = socket.socket()         # Create a socket object
        # host = self.HOST_NAME # Get local machine name
        # #socket.gethostname()
        # port = self.PORT_NUMBER                # Reserve a port for your service.
        # s.connect((host, port))
        # s.send('connected')
        # b=''
        # print s.recv(1024)
        # #print b
        # s.close                     # Close the socket when done

    def initNetwork(self):
        transmitInstruction ={}
        transmitInstruction['ACTION'] = 'initNetwork'
        transmitInstruction['RAW_XML'] = self.MODEL_DESC
        s = socket.socket()         # Create a socket object

        port = self.PORT_NUMBER                # Reserve a port for your service.
        s.connect((self.HOST_NAME, self.PORT_NUMBER))
        self.send_msg(s, str(transmitInstruction))
        socketReturn = self.recv_msg(s)
        #print socketReturn
        return socketReturn

    def runNetworkWithFile(self, inputFile,filetype = 'CSV', learnFlag=True, reset=False, printStates=False, computeInfOutput=False):
        transmitInstruction ={}
        transmitInstruction['ACTION'] = 'runNetworkWithFile'
        transmitInstruction['inputFile'] = inputFile
        transmitInstruction['learnFlag'] = learnFlag
        transmitInstruction['reset'] = reset
        transmitInstruction['printStates'] = printStates
        transmitInstruction['computeInfOutput'] = computeInfOutput
        transmitInstruction['RAW_XML'] = self.MODEL_DESC
        transmitInstruction['filetype'] = filetype

        s = socket.socket()         # Create a socket object
        host = self.HOST_NAME # Get local machine name
        #socket.gethostname()
        port = self.PORT_NUMBER                # Reserve a port for your service.
        s.connect((host, port))
        self.send_msg(s, str(transmitInstruction))
        socketReturn = self.recv_msg(s)
        #print 'ok running somehting 344----'
        #print socketReturn
        return eval(str(socketReturn))

    def runNetworkWithValue(self, inputValue,learnFlag=False, reset=False, printStates=False, computeInfOutput=True):
        transmitInstruction ={}
        transmitInstruction['ACTION'] = 'runNetworkWithValue'
        transmitInstruction['inputValue'] = inputValue
        transmitInstruction['learnFlag'] = learnFlag
        transmitInstruction['reset'] = reset
        transmitInstruction['printStates'] = printStates
        transmitInstruction['computeInfOutput'] = computeInfOutput
        transmitInstruction['RAW_XML'] = self.MODEL_DESC


        s = socket.socket()         # Create a socket object
        host = self.HOST_NAME # Get local machine name
        #socket.gethostname()
        port = self.PORT_NUMBER                # Reserve a port for your service.
        s.connect((host, port))
        self.send_msg(s, str(transmitInstruction))
        socketReturn = self.recv_msg(s)
        #print 'ok running somehting 344----'
        #print socketReturn
        return eval(str(socketReturn))

    def resetTraining(self):
        transmitInstruction={}
        transmitInstruction['ACTION'] = 'resetTraining'
        transmitInstruction['RAW_XML'] = self.MODEL_DESC
        transmitInstruction['RESET_MEMORY'] = 'TRUE'
        s = socket.socket()         # Create a socket object
        host = self.HOST_NAME # Get local machine name
        #socket.gethostname()
        port = self.PORT_NUMBER                # Reserve a port for your service.
        s.connect((host, port))
        self.send_msg(s, str(transmitInstruction))
        socketReturn = self.recv_msg(s)
        #print 'ok running somehting 344----'
        #print socketReturn
        return eval(str(socketReturn))
    def close(self):
        print 'closing'
    def send_msg(self, sock, msg):
        # Prefix each message with a 4-byte length (network byte order)
        msg = struct.pack('>I', len(msg)) + msg
        sock.sendall(msg)

    def recv_msg(self, sock):
        # Read message length and unpack it into an integer
        raw_msglen = self.recvall(sock, 4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        # Read the message data
        return self.recvall(sock, msglen)

    def recvall(self, sock, n):
        # Helper function to recv n bytes or return None if EOF is hit
        data = ''
        while len(data) < n:
            packet = sock.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data

#walnutclient = walnutclient(5001,'localhost','g')
#walnutclient.initNetwork()
#walnutclient.runNetworkWithValue('c',False,False,False, True)
#walnutclient.runNetworkWithFile('c',False,False,False, True)
