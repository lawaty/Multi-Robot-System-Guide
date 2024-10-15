from utils.Socket import Socket
from threading import Thread
from time import sleep, time_ns

def time_s():
  return round(time_ns() / 1_000_000_000)

class Drone:
  """A class simulating a single drone in the system

  Responsibilities:
  1- Holding robot state including position, action, and speed
  2- Uses threads to provide real-time robot motion along with real-time communication with the station to receive commands and publish its state as well
  3- Simulates abstract movement of the robot with speed and direction
  """
  # Abstraction Assumptions
  MIN_SPEED = 1 # unit/sec
  MAX_SPEED = 3 # unit/sec
  MAX_ALLOWED_Y = 4 # not allowed to move past the row #5
  MAX_ALLOWED_X = 4 # not allowed to move past the column #5
  ROBOT_CLOCK = 0.1 # robot processing clock
  
  __slots__ = ['__conn', '__action', '__position', '__speed', '__moving', '__listener', '__publisher']
  def __init__(self, host: str, port: int):
    self.__position = [0, 0] # Assuming that every drone is manually launched at (0, 0)
    self.__action = None
    self.__speed = -1
    self.__moving = Thread(target=self.__move)
    self.__listener = Thread(target=self.__listen)
    self.__publisher = Thread(target=self.__publish)
    self.__conn = Socket(host, port)
    
  def run(self):
    self.__conn.connect()
    self.__listener.start()
    self.__moving.start()
    self.__publisher.start()
    print("Drone launched")
    
  def kill(self):
    self.__action = 'stop'
    self.__conn.kill()
    self.__moving.stop()
    self.__moving.join()
  
  def __listen(self):
    while True:
      try:
        data = self.__conn.read(self.__sanitize)
        if data is None:
          print("Connection Closed.")
          exit()
        self.__action, self.__speed = data.split(' ')
        self.__speed = int(self.__speed)
        print(f"Received Command: {data}")
      except Exception as e:
        print(str(e))
  
  def __sanitize(self, data: str) -> str:
    action, speed = data.split(' ')
    if action is None or speed is None:
      raise Exception("Drone Name, action, and speed are all required")
  
    if action not in ['up', 'right', 'down', 'left', 'stop']:
      raise Exception(f"Unknown action {action}: Only 'up', 'right', 'down', and 'left' are allowed")
    
    try:
      speed = int(speed)
      if speed < Drone.MIN_SPEED or speed > Drone.MAX_SPEED:
        raise Exception("OutOfBound speed value")
         
    except:
      raise Exception("Invalid speed value")
    
    return data
    
  def __publish(self):
    while True:
      print(f"publishing {self.__position[0]},{self.__position[1]}")
      if not self.__conn.send(f"{self.__position[0]},{self.__position[1]}"):
        print("Publish Failed")
      sleep(1)
      
  def __up(self):
    start = time_s()
    while self.__action == 'up':
      # Boundary Check
      if self.__position[1] == 0:
        pass
      
      elif time_s() - start > 1 / self.__speed: # should have moved one cell
        self.__position[1] -= 1
        start = time_s()
      
      sleep(self.ROBOT_CLOCK) # Position update clock 
      
  def __down(self):
    start = time_s()
    while self.__action == 'down':
      # Boundary Check
      if self.__position[1] == self.MAX_ALLOWED_Y:
        pass
      
      elif time_s() - start > 1 / self.__speed: # should have moved one cell
        self.__position[1] += 1
        start = time_s()
        
      sleep(self.ROBOT_CLOCK) # Position update clock 
    
  def __left(self):
    start = time_s()
    while self.__action == 'left':
      # Boundary Check
      if self.__position[0] == 0:
        pass
      
      elif time_s() - start > 1 / self.__speed: # should have moved one cell
        self.__position[0] -= 1
        start = time_s()
      
      sleep(self.ROBOT_CLOCK) # Position update clock 
    
  def __right(self):
    start = time_s()
    while self.__action == 'right':
      # Boundary Check
      if self.__position[0] == self.MAX_ALLOWED_X:
        pass
      
      elif time_s() - start > 1 / self.__speed: # should have moved one cell
        self.__position[0] += 1
        start = time_s()
      
      sleep(self.ROBOT_CLOCK) # Position update clock 
         
  def __move(self):
    # Assuming that drones can only be positioned at the center of each unit. They cannot be shifted to any direction around the center. they translate from the center of a cell to the center of the other after some time ignoring what happens across every cell and also ignoring acceleration and inertia
    
    self.__action = 'stop'
    self.__speed = self.MIN_SPEED
    
    while True: # infinite movement loop   
      if self.__action == 'stop':
        pass
      elif self.__action == 'up':
        self.__up()
      elif self.__action == 'down':
        self.__down()
      elif self.__action == 'right':
        self.__right()
      elif self.__action == 'left':
        self.__left()
        
      sleep(self.ROBOT_CLOCK) # Position update clock