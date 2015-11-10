# Socket server in python using select function
#import net
import socket, select
from curiousWorkbench.networkBuilder import *
import walnutserver
import struct

class walnutserver:
    VAL=0
    CALL_NUMBER = 0
    #newNetworkObject = None
    MODEL_DESC = ""

    def __init__(self):
        print 'do nothing'

    def resetTraining(self):
        returnV = self.initNetwork({'RAW_XML':self.MODEL_DESC, 'RESET_MEMORY':'TRUE'})
        return returnV

    def dispatchCommand(self, command):
        #self.VAL +=1
        #print 'in dispatcher'
        if self.CALL_NUMBER==0:
            #print 'initiating Network ...'
            self.initNetwork(command)
            self.CALL_NUMBER +=1
        if command['ACTION'] == 'runNetworkWithValue':
            #print 'calling runNetworkWithValue'
            return self.runNetworkWithValue(command)
        elif command['ACTION'] == 'runNetworkWithFile':
            #print 'calling runNetworkWithFile'
            return self.runNetworkWithFile(command)
        elif command['ACTION'] == 'resetTraining':
            return self.resetTraining()

    def initNetwork(self, command):
        self.newNetworkObject = Network()
        strRawXML = ''
        strRawXML = command['RAW_XML']

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
    def runNetworkWithFile(self, command):
        #print('runNetworkWithFile')
        inputFile = str(command['inputFile'])
        filetype = command['filetype']
        learnFlag = command['learnFlag']
        reset = command['reset']
        printStates = command['printStates']
        computeInfOutput = command['computeInfOutput']
        print inputFile,filetype, learnFlag, reset, printStates, computeInfOutput
        ReturnVal = self.newNetworkObject.runNetworkWithFile(inputFile, learnFlag, reset, printStates, computeInfOutput)
        return ReturnVal

    def runNetworkWithValue(self, command):
        #print('runNetworkWithFile')
        inputValue = str(command['inputValue'])
        learnFlag = command['learnFlag']
        reset = command['reset']
        printStates = command['printStates']
        computeInfOutput = command['computeInfOutput']
        ReturnVal = self.newNetworkObject.runNetworkWithValue(inputValue,learnFlag, reset, printStates, computeInfOutput)
        return ReturnVal

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


if __name__ == "__main__":

    #newNetworkObject = None
    CONNECTION_LIST = []    # list of socket clients
    RECV_BUFFER = 4096 # Advisable to keep it as an exponent of 2
    PORT = 5001

    walnutserverobj=walnutserver()
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # this has no effect, why ?
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen(10)

    # Add server socket to the list of readable connections
    CONNECTION_LIST.append(server_socket)

    print "Walntnutserver started on port " + str(PORT)


    while 1:
        # Get the list sockets which are ready to be read through select
        read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])

        for sock in read_sockets:

            #New connection
            if sock == server_socket:
                # Handle the case in which there is a new connection recieved through server_socket
                sockfd, addr = server_socket.accept()
                CONNECTION_LIST.append(sockfd)
                print "Client (%s, %s) connected" % addr
                #sock.send('s')

            #Some incoming message from a client
            else:
                # Data recieved from client, process it
                #try:
                #In Windows, sometimes when a TCP program closes abruptly,
                # a "Connection reset by peer" exception will be thrown
                #print 'receiving data'
                data = walnutserverobj.recv_msg(sock)
                #print 'received data'
                # echo back the client message
                #print str(data)
                if data:
                    #print data
                    ReturnVal = walnutserverobj.dispatchCommand(eval(data))
                    #print 'sending back value'
                    #print 'ReturnVal'
                    walnutserverobj.send_msg(sock,str(ReturnVal))

                # client disconnected, so remove from socket list
                # except:
                #     print "exception"
                #     #broadcast_data(sock, "Client (%s, %s) is offline" % addr)
                #     print "Client (%s, %s) is offline" % addr
                #     sock.close()
                #     CONNECTION_LIST.remove(sock)
                #     continue

    server_socket.close()
