from utils.Socket import Socket
    
class Server(Socket):
  MAX_TRIALS = 20
  
  __slots__ = ['_host', '_port', '_socket', '__connected']
  
  def __init__(self, host: any = 'localhost', port: int = 8000, any_port: bool = False):
    super().__init__(host, port)
    self.__connected = False
    
    trials = 0
    while not self.__connected and any_port and trials <= self.MAX_TRIALS:
      try:
        self._socket.bind((self._host, self._port))
        self.__connected = True
      except Exception as e:
        print(str(e))
        self._port += 1
        trials+=1
    
    self._socket.listen(self.QUEUE_SIZE)
          
  def accept(self):    
    conn, addr = self._socket.accept()
    return Socket.fromSocket(conn)