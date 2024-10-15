from socket import socket, AF_INET, SOCK_STREAM

class Socket:
  """
  A wrapper class for handling socket connections with basic send, receive, and management functionalities. Wrappers are often created to achieve centralization and encapsulating low-level functionalities
  
  What to learn:
  1. The restricted access to attributes
  2. __slots__ magic variable
  3. method decorators
  4. Exception Handling
  """
        
  __slots__ = ['_host', '_port', '_socket']
  def __init__(self, host: any = 'localhost', port: int = 8000):
    self._socket = socket(AF_INET, SOCK_STREAM)
    self._host = host if host is not None else 'localhost'
    self._port = int(port)
    
  def getConfig(self):
    return (self._host, self._port)
  
  @staticmethod
  def getLocalIP():
    """
    identify the device local ip
    """
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    return host
      
  def send(self, msg: str) -> bool:
    """
    Send msg through socket pipe
    """
    try:
      self._socket.sendall(msg.encode())
      return True
    except Exception as e:
      print(f"Failed to send message: {e}")
      return False

  def read(self, sanitizer: callable = None) -> str:
    try:
      data = self._socket.recv(1024).decode()
      if sanitizer is not None:
        data = sanitizer(data)
      return data
    except Exception as e:
      print(f"Failed to receive data: {e}")
      return None
    
  def kill(self):
    self._socket.close()
    
  def connect(self):
    self._socket.connect((self._host, self._port))
    
  @staticmethod
  def fromSocket(socket: socket):
    """
    Factory method
    """
    temp = Socket()
    temp._socket = socket
    return temp