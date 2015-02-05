from socket import *
class CTcpClient:
    "a class connet to with tcp"
    m_host = '10.21.210.250'
    m_port = 10000
    m_clisock = None 
    def Init(self, host, port):
        self.m_host = host
        self.m_port = port
        self.m_clisock = socket(AF_INET, SOCK_STREAM) 
        self.m_clisock.connect((self.m_host, self.m_port)) 
        print ("connect success");
    def SendAndRecv(self,sendbuf):
        BUFSIZE=10240
        self.m_clisock.send(sendbuf) 
        recvbuf = self.m_clisock.recv(BUFSIZE)
        return recvbuf
    def Fini(self):
        self.m_clisock.close()

    def GetSockname(self):
        return self.m_clisock.getsockname()
