from socket import socket, AF_INET, SOCK_STREAM
import requests
    
class Socket:
  QUEUE_SIZE = 5
  SAME_THREAD = 1
  NEW_THREAD = 2
  
  __slots__ = ['_host', '_port', '_socket']
  
  def __init__(self, host: any = 'localhost', port: int = 8000):
    self._socket = socket(AF_INET, SOCK_STREAM)
    self._host = host if host is not None else 'localhost'
    self._port = int(port)
    
  def getConfig(self):
    return (self._host, self._port)
  
  @staticmethod
  def getLocalIP():
    s = socket(AF_INET, SOCK_STREAM)
    s.connect(("8.8.8.8", 80))
    host = s.getsockname()[0]
    s.close()
    return host
      
  def send(self, msg: str) -> bool:
    try:
      self._socket.sendall(msg.encode())
      return True
    except Exception as e:
      print(f"Failed to send message: {e}")
      return False

  def read(self, sanitizer = None) -> str:
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
    temp = Socket()
    temp._socket = socket
    return temp