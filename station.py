from classes.Station import Station
from classes.Drone import Drone
from classes.Map import Map
from utils.Args import Args
from utils.Socket import Socket

if __name__ == '__main__':
  args = Args(
    host={'type': str, 'required': False},
    port={'type': int, 'required': True}
    )
  
  host = args.get('host')
  if host is None:
    host = Socket.getLocalIP()
  
  map = Map((Drone.MAX_ALLOWED_X + 1, Drone.MAX_ALLOWED_Y + 1))
  station = Station(host, port=args.get('port'), map=map)
