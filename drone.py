from utils.Args import Args
from classes.Drone import Drone

if __name__ == '__main__':
  args = Args(
      host={'type': str, 'required': True},
      port={'type': int, 'required': True}
    )
  
  host, port = args.get('host', 'port')
  
  # Registering the drone
  drone = Drone(host, port)
  drone.run()