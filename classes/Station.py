from utils.Server import Server
from classes.Drone import Drone
from classes.Map import Map
from time import sleep
from threading import Thread
import keyboard

class Station:
  __slots__ = ['__map', '__drones', '__server']
  def __init__(self, host, map: Map, port=None):
    self.__drones = {}
    self.__map = map
    if port is None:
      port = 8000
      
    self.__server = Server(host, port, any_port=True)
    print(f"Server run at {self.__server.getConfig()}")
    sleep(1)
    self.__map.running = True
    
    Thread(target=self.__register).start()
    keyboard.hook(self.__command)
      
  def __register(self):
    while True:
      conn = self.__server.accept()
      drone_no = len(self.__drones) + 1
      if drone_no < 10:
        drone_no = "0" + str(drone_no)
        
      drone_name = f'D{drone_no}'
      self.__drones[drone_name] = conn
      self.__map.updatePosition(drone_name, (0, 0))
      
      Thread(target=self.__updatePosition, args=(drone_name,)).start()

  def __command(self, event):
    if event.event_type == 'down' and event.name == 'c' and keyboard.is_pressed('shift'):
      self.__map.running = False
      command = input('Enter command: e.g. DXX up 2\n').strip()
      # Validation
      splitted = command.split(' ')
      if len(splitted) != 3:
        print("Exactly three csv values must be provided")
        self.__map.running = True
        return 
      
      drone, action, speed = splitted  
      if drone is None or action is None or speed is None:
        print("Drone Name, action, and speed are all required")
      
      elif drone not in self.__drones:
        print("Drone Not Found")
      
      elif action not in ['up', 'right', 'down', 'left', 'stop']:
        print(f"Unknown action {action}: Only 'up', 'right', 'down', and 'left' are allowed")

      else:
        # Applying the command
        try:
          speed = int(speed)
          if speed < Drone.MIN_SPEED or speed > Drone.MAX_SPEED:
            print("OutOfBound speed value")
            return 
          
        except:
          print("Invalid speed value")
          return
        
        self.__drones[drone].send(f"{action} {speed}")

      self.__map.running = True

  def __updatePosition(self, drone: str) -> None:
    conn = self.__drones[drone]
    while True:
      x, y = conn.read().split(',')
      self.__map.updatePosition(drone, (int(x), int(y)))
      sleep(0.1)
