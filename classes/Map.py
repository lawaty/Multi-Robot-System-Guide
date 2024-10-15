from threading import Thread
from time import sleep
from datetime import datetime


class Map:
  """
  Map plot service holds all drones' positions and provides interface for the station to update drones' positions on the map
  """
  __slots__ = ['__size', '__drones', '__cells', 'running']
  def __init__(self, size: tuple):
    self.__size = size
    self.__drones = {}
    self.__cells = [['---' for _ in range(size[1])] for _ in range(size[0])]
    self.running = False
    Thread(target=self.__plot).start()
  
  def __plot(self):
    while True:
      if self.running:
        print("\nAt", datetime.now().strftime("%Y-%m-%d %I:%M:%S %p"))
        for x in range(self.__size[0]):
          for y in range(self.__size[1]):
            print(self.__cells[x][y], end=" ")
                  
          print("\n")
      sleep(1)
      
  def get(self, pt: tuple) -> str:
    """
      Get cell content at pt(x, y)
    """
    return self.__cells[pt[1]][pt[0]]
  
  def __set(self, pt: tuple, drones: str) -> None:
    """Hard set the drone content at a certain cell
    """
    
    self.__cells[pt[1]][pt[0]] = f'{drones}'  

  def add(self, pt: tuple, drone: str) -> None:
    """Adds a drone to that positions with csv format
    """
    
    cell_content = self.get(pt)
    if cell_content != '---':
      cell_content += f',{drone}'
    else:
      cell_content = drone
    
    self.__set(pt, cell_content)
      
  def remove(self, pt: tuple, drone: str) -> None:
    """Removes a drone from that position
    """
      
    drones_here = self.get(pt).split(',')
    drones_here.remove(drone)
    if len(drones_here) == 0:
      drones_here = ['---']
    self.__set(pt, ','.join(drones_here))
    
  def updatePosition(self, drone: str, new_pt: tuple) -> None:
    if new_pt[0] > self.__size[0] or new_pt[1] > self.__size[1]:
      print(f"Drone out of the map zone: {new_pt}")
      return None
    
    if drone in self.__drones:
      drone_prev_position = self.__drones[drone]
      if drone_prev_position == new_pt:
        return
      
      self.remove(drone_prev_position, drone)

    self.__drones[drone] = new_pt
    self.add(new_pt, drone)
    