# Task Objective
This task is designed to help you learn how to implement cooperative systems using Object-Oriented Programming (OOP). You'll gain hands-on experience in structuring systems that rely on `multiple objects interacting with each other`, such as simulating a network of drones controlled by a station. This example will also teach you important concepts like defensive programming, thread management, and software design principles that contribute to building reliable, and scalable systems.

# System High-level Overflow
1. The user runs the station on a some ip and port. 
2. The station starts listening for new drones joining the system and prints real-time map showing drones' positions.
3. The user then launches drones one by one and must pass the station ip and port as parameter to the python file to which the drone will connect to join the system. Drones start publishing there position in real-time to the station and listens for any commands to be received by the station
4. Clicking the hotkey `Shift + C` activates the command prompt so that you can send a command to a certain drone. Command is formatted like `<drone_name> <action> <speed>`
5. Drone movement is simulated by an action (up, right, down, or left), and speed (speed levels range from 1 to 3). Drone class dedicates a thread for applying the motion intuitively to appear as if it is moving in the real-life by calculating the time needed to traverse a cell given the movement start time and speed. Also some assumptions are set to be able to complete the simulation and stated in the class documentation 

# Architectural Style and Design Characteristics
1. **Client-Server Communication Model**
2. **Domain-Driven Development(DDD)** means decomposing the system into context-related classes instead of tech-related classes (e.g. Drone, Map, Station, instead of Client, Server, Output)
3. **Modular System** means decomposing the system into reusable and decoupled components that can be easily separated from each other. Drone class does not need a Station class to work. Any other class with the same interface would make for it and this leverages the `SoC` and system `flexibility`
4. **Defensive Techniques**: applied defensive techniques to help eliminate the most critical issues like handling connection failures using exceptions, validating inputs, etc...

# System Design Walkthrough
The system mainly consists of three entities which are `Station`, `Drone`, and `Map`. They use some low-level utilities which are `Server` and `Socket` to handle low-level computations that provide them with pretty and straightforward interface to the features. The same applies for `Args`.

