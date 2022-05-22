"""grocery controller."""

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, Motor, DistanceSensor
from controller import Robot
import matplotlib.pyplot as plt
from scipy.signal import convolve2d
import math
import numpy as np
import cv2
import copy
from ikpy.chain import Chain
from ikpy.link import OriginLink, URDFLink

#Initialization
print("=== Initializing Grocery Shopper...")
#Consts
MAX_SPEED = 7.0  # [rad/s]
MAX_SPEED_MS = 0.633 # [m/s]
AXLE_LENGTH = 0.4044 # m
MOTOR_LEFT = 10
MOTOR_RIGHT = 11
N_PARTS = 12
LIDAR_ANGLE_BINS = 667
LIDAR_SENSOR_MAX_RANGE = 2.75 # Meters was 2.75 in lab 5
LIDAR_ANGLE_RANGE = math.radians(240)

#MANIPULATION
Manipulation = False			#setting manipulation state to false to start
placingInBasket = False		#setting placing state to false
Grasping = False					#setting grasping state to false
ikSkip = 7								#initialize ik skip variable to set off at the start

# create the Robot instance.dw
robot = Robot()

# get the time step of the current world.
timestep = int(robot.getBasicTimeStep())

#RUN ONCE THEN COMMENT OUT - used to setup .urdf file in directory
# with open("tiago_urdf.urdf", "w") as file:  
    # file.write(robot.getUrdf())
  
#ikPy wiki setup procedure setting up the links, joints and the end effector chain to be used in ikPy
base_elements=["base_link", "base_link_Torso_joint", "Torso", "torso_lift_joint", "torso_lift_link", "torso_lift_link_TIAGo front arm_joint", "TIAGo front arm"]
my_chain = Chain.from_urdf_file("tiago_urdf.urdf", last_link_vector=[0.004, 0,-0.1741], base_elements=["base_link", "base_link_Torso_joint", "Torso", "torso_lift_joint", "torso_lift_link", "torso_lift_link_TIAGo front arm_joint", "TIAGo front arm"])


# The Tiago robot has multiple motors, each identified by their names below
part_names = ("head_2_joint", "head_1_joint", "torso_lift_joint", "arm_1_joint",
              "arm_2_joint",  "arm_3_joint",  "arm_4_joint",      "arm_5_joint",
              "arm_6_joint",  "arm_7_joint",  "wheel_left_joint", "wheel_right_joint")

for link_id in range(len(my_chain.links)):		#from ikPy wiki. setting up the active link mask for the joints

    # #This is the actual link object
    link = my_chain.links[link_id]
    
    #if link.name == "torso_lift_link_TIAGo front arm_joint":
        #my_chain.active_links_mask[link_id] = True
    if link.name not in part_names or  link.name =="torso_lift_joint":
        #print("Disabling {}".format(link.name))
        my_chain.active_links_mask[link_id] = False

#Initialize the arm motors and encoders from ikPy wiki
motors = []
for link in my_chain.links:
    if link.name in part_names and link.name != "torso_lift_joint":
        motor = robot.getDevice(link.name)

        if link.name == "torso_lift_joint":
            motor.setVelocity(0.07)
        else:
            motor.setVelocity(1)
            
        position_sensor = motor.getPositionSensor()
        position_sensor.enable(timestep)
        motors.append(motor)  

# All motors except the wheels are controlled by position control. The wheels
# are controlled by a velocity controller. We therefore set their position to infinite.
target_pos = (0, 0, 0, 0.3, -0.5, -2.3, 2.15, 1.5, -1.39, -0.25, 'inf', 'inf')
robot_parts=[]

for i in range(N_PARTS):
    robot_parts.append(robot.getDevice(part_names[i]))
    robot_parts[i].setPosition(float(target_pos[i]))
    robot_parts[i].setVelocity(robot_parts[i].getMaxVelocity() / 2.0)
    

# Enable Camera
camera = robot.getDevice('camera')
camera.enable(timestep)
camera.recognitionEnable(timestep)

# Enable GPS and compass localization
gps = robot.getDevice("gps")
gps.enable(timestep)
compass = robot.getDevice("compass")
compass.enable(timestep)

# Enable LiDAR
lidar = robot.getDevice('Hokuyo URG-04LX-UG01')
lidar.enable(timestep)
lidar.enablePointCloud()

# Enable display
display = robot.getDevice("display")

# Odometry
pose_x     = 0
pose_y     = 0
pose_theta = 0

vL = 0
vR = 0

lidar_sensor_readings = [] # List to hold sensor readings
lidar_offsets = np.linspace(-LIDAR_ANGLE_RANGE/4., +LIDAR_ANGLE_RANGE/4., LIDAR_ANGLE_BINS)
lidar_offsets = lidar_offsets[83:len(lidar_offsets)-83] # Only keep lidar readings not blocked by robot chassis

map = None

##### Our Code #####
keyboard = robot.getKeyboard()
keyboard.enable(timestep)

mode = 'manual'
#mode = 'planner'
# mode = 'autonomous'

color_ranges = []

# ------------------------------------------------------------------
# Helper Functions

#### IMAGE RECOGNITION ####

# Function to add range of colors to global variable for recogntion
def add_color_range(lower, upper):
    global color_ranges
    color_ranges.append([lower, upper])
    return

# Function checks color against 
def check_color(bgr_tuple):
    global color_ranges
    for entry in color_ranges:
        low, high = entry[0], entry[1]
        in_range = True
        for i in range(len(bgr_tuple)):
            if (bgr_tuple[i] < low[i]) or (bgr_tuple[i] > high[i]):
                in_range = False
                break
        if in_range:
            return True
        return False

def color_filtering(img):
    height = img.shape[0]
    width = img.shape[1]
    
    mask = np.zeros([height, width])
    
    for y in range(height):
        for x in range(width):
            if check_color(img[y, x]):
                mask[y,x] = 1
    
    return mask

def expand_nr(img_mask, cur_coord, coordinates_in_blob):
    coordinates_in_blob = []
    coordinates_list = [cur_coord]
    while (len(coordinates_list) > 0):
        current = coordinates_list.pop()
        if (current[0] < 0) or (current[1] < 0) or (current[0] >= img_mask.shape[0]) or (current[1] >= img_mask.shape[1]):
            continue
        if img_mask[current[0], current[1]] == 0.0:
            continue
        
        img_mask[current[0], current[1]] = 0
        coordinates_in_blob.append(current)
        
        above = [current[0]-1, current[1]]
        below = [current[0]+1, current[1]]
        left = [current[0], current[1]-1]
        right = [current[0], current[1]+1]
        coordinates_list.extend([above, below, left, right])
        
    return coordinates_in_blob

def get_blobs(img_mask):
    height = img_mask.shape[0]
    width = img_mask.shape[1]
    
    img = copy.copy(img_mask)
    blobs_list = []
    
    for y in range(height):
        for x in range(width):
            if img[y,x] == 1:
                blob_coords = expand_nr(img, [y,x], [])
                blobs_list.append(blob_coords)
    
    return blobs_list      
    
def get_blob_centroids(blobs_list, blob_min=20):
    obj_positions = []
    for blob in blobs_list:
        if len(blob) < blob_min:
            continue
        centroid = np.mean(blob, axis=0)
        obj_positions.append(centroid)
        
    return obj_positions
    
def run_camera_recognition():
    # Uses camera to obtain image and writes BGRA data to 135x240 array
    cam_data = camera.getImage()
    img = np.frombuffer(cam_data, np.uint8).reshape((camera.getHeight(), camera.getWidth(), 4))
    camera.saveImage("robot_cam.png", 100)
    # Have OpenCV read image
    image = cv2.imread("robot_cam.png")
    add_color_range([32, 105, 65], [64, 194, 127])
    image_mask = color_filtering(image)
    blobs = get_blobs(image_mask)
    obj_positions = get_blob_centroids(blobs)
    if (len(obj_positions) >= 1):
        size_cutoff = 20
        while (len(obj_positions) > 1):
            size_cutoff += 5
            obj_positions = get_blob_centroids(blobs, size_cutoff)
        if (len(obj_positions) == 0):
          size_cutoff -= 5
          obj_positions = get_blob_centroids(blobs, size_cutoff)
        recognized_objects = camera.getRecognitionObjects()
        #print(obj_positions[0])
        for item in recognized_objects:
            pos = item.get_position_on_image()
            #print(pos)
            if (pos[0] >= (obj_positions[0][1] - 5)) and (pos[0] <= (obj_positions[0][1] + 5)) and (pos[1] >= (obj_positions[0][0] - 5)) and (pos[1] <= (obj_positions[0][0] + 5)):
                return item.get_position(), item.get_orientation()
    else:
        return []    
    return []
  
#### MANIPULATION HELPER ####

def placeInBasket():		#helper function used to place the cubes in the basket once grasped 
      target_pos = (0, 0, 0, 0.3, -0.5, -2.3, 2.15, 1.5, -1.39, -0.25, 'inf', 'inf')		#hard coded joint positions to place cube. much less lag than IK

      for i in range(N_PARTS):
          robot_parts[i].setPosition(float(target_pos[i]))										#setting the position of each joint
          robot_parts[i].setVelocity(robot_parts[i].getMaxVelocity() / 4.0)		#setting the speed each joint rotates, slowed it down to prevent jerk

      initial_position = [0,0,0,0] + [m.getPositionSensor().getValue() for m in motors] + [0,0,0,0]			#get current position of the joints
      offset_target = [0.29974, -0.03804, 0.75525]																											#final position of the end effector for error calculation
      fkResults = my_chain.forward_kinematics(initial_position)																					#get the current end effector position

      error = 0
      for item in range(3):
          error += (offset_target[item] - fkResults[item][3])**2 #calculates the error between current and desired
      error = math.sqrt(error)

      if(error < 0.05):			#if the error is within tolerance the block is dropped in the basket
          return True
      else:
          return False

#### PLANNER ####

def retrace_path(node, previous):
    s = node
    path = []
    while(previous[s] != None):
        path = [previous[s]] + path
        s = previous[s]
    
    return path

if mode == 'planner':
    # start and end in world coordinate 
    if robot.step(timestep) != -1:
        pose_y = gps.getValues()[2]
        pose_x = gps.getValues()[0]
        
    start_w = (pose_x, pose_y) # (Pose_X, Pose_Z) in meters
    end_w = (10.0, 7.0) # (Pose_X, Pose_Z) in meters

    # Convert the start_w and end_w from the webots coordinate frame into the map frame
    start = (int(12*start_w[0]), int(12*start_w[1])) # (x, y) in 360x192 map
    end = (int(12*end_w[0]), int(12*end_w[1])) # (x, y) in 360x192 map

    # Implement A* or Dijkstra's Algorithm to find a path
    def path_planner(map, start, goal):
        '''
        :param map: A 2D numpy array of size 360x194 representing the world's cspace with 0 as free space and 1 as obstacle
        :param start: A tuple of indices representing the start cell in the map
        :param end: A tuple of indices representing the end cell in the map
        :return: A list of tuples as a path from the given start to the given end in the given maze
        '''
        frontier = []
        frontier.append((start[0], start[1]))
        previous = {start: None}
        costs = {start: 0}
        heuristic = {start: 0}
        if start == goal:
            path_out = [start]
            return path_out
        heuristic[start] = ((goal[1] - start[1])**2 + (goal[0] - start[0])**2)**(1/2)
        #for point in heuristic:
            #print(point, heuristic[point])
        while frontier:
            s = frontier[0]
            min_value = costs[s] + heuristic[s]
            minval_index = 0
            for i in range(len(frontier)):
                s = frontier[i]
                #print(costs[s])
                #print(heuristic[s])
                if (costs[s] + heuristic[s] < min_value):
                    min_value = costs[s] + heuristic[s]
                    minval_index = i
            s = frontier.pop(minval_index)
            not_left = False
            not_right = False
            not_up = False
            not_down = False
            if (s[0] == 0):
                not_left = True
            if (s[0] == 360):
                not_right = True
            if (s[1] == 0):
                not_up = True
            if (s[1] == 192):
                not_down = True
            
            if not not_left:
                if ((s[0] - 1, s[1]) not in previous) and ((s[0] - 1, s[1]) not in frontier) and (map[s[0]-1][s[1]] != 1):
                    frontier.append((s[0] - 1, s[1]))
                    previous[(s[0]-1,s[1])] = s
                    costs[(s[0]-1, s[1])] = costs[s] + 1
                    heuristic[(s[0]-1, s[1])] = ((goal[1] - s[1])**2 + (goal[0] - (s[0]-1))**2)**(1/2)
                    if (s[0]-1, s[1]) == goal:
                        path_out = retrace_path(goal, previous)
                        return path_out
                if not not_up:
                    if ((s[0] - 1, s[1] - 1) not in previous) and ((s[0] - 1, s[1] - 1) not in frontier) and (map[s[0]-1][s[1]-1] != 1):
                        frontier.append((s[0] - 1, s[1] - 1))
                        previous[(s[0]-1,s[1]-1)] = s
                        costs[(s[0]-1, s[1]-1)] = costs[s] + np.sqrt(2)
                        heuristic[(s[0]-1, s[1]-1)] = ((goal[1] - (s[1]-1))**2 + (goal[0] - (s[0]-1))**2)**(1/2)
                        if (s[0]-1, s[1]-1) == goal:
                            path_out = retrace_path(goal, previous)
                            return path_out
                if not not_down:
                    if ((s[0] - 1, s[1] + 1) not in previous) and ((s[0] - 1, s[1] + 1) not in frontier) and (map[s[0]-1][s[1]+1] != 1):
                        frontier.append((s[0] - 1, s[1] + 1))
                        previous[(s[0]-1,s[1]+1)] = s
                        costs[(s[0]-1, s[1]+1)] = costs[s] + np.sqrt(2)
                        heuristic[(s[0]-1, s[1]+1)] = ((goal[1] - (s[1]+1))**2 + (goal[0] - (s[0]-1))**2)**(1/2)
                        if (s[0]-1, s[1]+1) == goal:
                            path_out = retrace_path(goal, previous)
                            return path_out
            if not not_right:
                if ((s[0] + 1, s[1]) not in previous) and ((s[0] + 1, s[1]) not in frontier) and (map[s[0]+1][s[1]] != 1):
                    frontier.append((s[0] + 1, s[1]))
                    previous[(s[0]+1,s[1])] = s
                    costs[(s[0]+1, s[1])] = costs[s] + 1
                    heuristic[(s[0]+1, s[1])] = ((goal[1] - s[1])**2 + (goal[0] - (s[0]+1))**2)**(1/2)
                    if (s[0]+1, s[1]) == goal:
                        path_out = retrace_path(goal, previous)
                        return path_out
                if not not_up:
                    if ((s[0] + 1, s[1] - 1) not in previous) and ((s[0] + 1, s[1] - 1) not in frontier) and (map[s[0]+1][s[1]-1] != 1):
                        frontier.append((s[0] + 1, s[1] - 1))
                        previous[(s[0]+1,s[1]-1)] = s
                        costs[(s[0]+1, s[1]-1)] = costs[s] + np.sqrt(2)
                        heuristic[(s[0]+1, s[1]-1)] = ((goal[1] - (s[1]-1))**2 + (goal[0] - (s[0]+1))**2)**(1/2)
                        if (s[0]+1, s[1]-1) == goal:
                            path_out = retrace_path(goal, previous)
                            return path_out
                if not not_down:
                    if ((s[0] + 1, s[1] + 1) not in previous) and ((s[0] + 1, s[1] + 1) not in frontier) and (map[s[0]+1][s[1]+1] != 1):
                        frontier.append((s[0] + 1, s[1] + 1))
                        previous[(s[0]+1,s[1]+1)] = s
                        costs[(s[0]+1, s[1]+1)] = costs[s] + np.sqrt(2)
                        heuristic[(s[0]+1, s[1]+1)] = ((goal[1] - (s[1]+1))**2 + (goal[0] - (s[0]+1))**2)**(1/2)
                        if (s[0]+1, s[1]+1) == goal:
                            path_out = retrace_path(goal, previous)
                            return path_out
            if not not_up:
                if ((s[0], s[1] - 1) not in previous) and ((s[0], s[1] - 1) not in frontier) and (map[s[0]][s[1]-1] != 1):
                    frontier.append((s[0], s[1] - 1))
                    previous[(s[0],s[1]-1)] = s
                    costs[(s[0], s[1]-1)] = costs[s] + 1
                    heuristic[(s[0], s[1]-1)] = ((goal[1] - (s[1]-1))**2 + (goal[0] - (s[0]))**2)**(1/2)
                    if (s[0], s[1]-1) == goal:
                        path_out = retrace_path(goal, previous)
                        return path_out
            if not not_down:
                if ((s[0], s[1] + 1) not in previous) and ((s[0], s[1] + 1) not in frontier) and (map[s[0]][s[1]+1] != 1):
                    frontier.append((s[0], s[1] + 1))
                    previous[(s[0],s[1]+1)] = s
                    costs[(s[0], s[1]+1)] = costs[s] + 1
                    heuristic[(s[0], s[1]+1)] = ((goal[1] - (s[1]+1))**2 + (goal[0] - (s[0]))**2)**(1/2)
                    if (s[0], s[1]+1) == goal:
                        path_out = retrace_path(goal, previous)
                        return path_out
            
        
        return []
      
    

    # Load map (map.npy) from disk and visualize it
    map = np.load("map.npy")
    
    plt.imshow(map)
    plt.show()

    # Compute an approximation of the “configuration space”
    kernel = np.ones((30, 16))
    convolved_map = convolve2d(map, kernel, mode='same')
    for i in range(convolved_map.shape[0]):
        for j in range(convolved_map.shape[1]):
            if (convolved_map[i][j] != 0):
                convolved_map[i][j] = 1
    plt.imshow(convolved_map)
    plt.show()

    # continuation: Call path_planner
    
    path = path_planner(convolved_map, start, end)

    # Turn paths into waypoints and save on disk as path.npy and visualize it
    waypoints = []
    for i in range(len(path)):
        waypoints.append((path[i][0]/12, path[i][1]/12))
    for k in range(len(path)):
        convolved_map[path[k][0]][path[k][1]] = 0.5
    plt.imshow(convolved_map)
    plt.show()
    np.save("path.npy", waypoints)


#### MAPPING ####

map = np.ndarray(shape=(360,192), dtype=float)

if mode == 'autonomous':
     waypoints = np.load("path.npy")
state = 0

while robot.step(timestep) != -1 and mode != 'planner':
    robot.getDevice("gripper_right_finger_joint").setPosition(0.045)		#set the grip joints to the max size
    robot.getDevice("gripper_left_finger_joint").setPosition(0.045)
    pose_y = gps.getValues()[2]
    pose_x = gps.getValues()[0]
    
    n = compass.getValues()
    rad = -((math.atan2(n[0], n[2])) - 1.5708)
    pose_theta = rad
    
    lidar_sensor_readings = lidar.getRangeImage()
    lidar_sensor_readings = lidar_sensor_readings[83:len(lidar_sensor_readings)-83]

    for i, rho in enumerate(lidar_sensor_readings):
        alpha = lidar_offsets[i]

        if rho > LIDAR_SENSOR_MAX_RANGE:
            continue

        rx = math.cos(alpha)*rho
        ry = -math.sin(alpha)*rho
 
        # Convert robot to world coordinates
        wx =  math.cos(pose_theta)*rx - math.sin(pose_theta)*ry + pose_x
        wy =  -(math.sin(pose_theta)*rx + math.cos(pose_theta)*ry) + pose_y
    
        if rho < LIDAR_SENSOR_MAX_RANGE:
        # Using a multiplier of 12 in order to conver map from 30x16m to 360x192px
            if(int(wx*12)<= 359) and (int(wy*12) <= 192):
                if map[int((wx*12)), int(wy*12)] < 1:
                    map[int((wx*12)), int(wy*12)] += 0.005
                
                if map[int((wx*12)), int(wy*12)] > 1:
                    map[int((wx*12)), int(wy*12)] = 1
                    
                g = int(map[int((wx*12)), int(wy*12)]*255)
                color = (g*256**2) + (g*256) + g
                
                
                display.setColor(color)
                display.drawPixel(125+int(wy*12), 185+int(wx*12))
                
    
    display.setColor(int(0xFF0000))
    display.drawPixel(125+int(pose_y*12), 185+int(pose_x*12))

    #### Arrow Key Controller ####
    if mode == 'manual':
        key = keyboard.getKey()
        while(keyboard.getKey() != -1): pass
        if key == keyboard.LEFT :
            vL = -MAX_SPEED
            vR = MAX_SPEED
        elif key == keyboard.RIGHT:
            vL = MAX_SPEED
            vR = -MAX_SPEED
        elif key == keyboard.UP:
            vL = MAX_SPEED
            vR = MAX_SPEED
        elif key == keyboard.DOWN:
            vL = -MAX_SPEED
            vR = -MAX_SPEED
        elif key == ord(' '):
            vL = 0
            vR = 0
        elif key == ord('S'):
            filtered_map = np.ndarray(shape=(360,192), dtype=int)
            for i in range(filtered_map.shape[0]):
                for j in range(filtered_map.shape[1]):
                    if map[i, j] > 0.7:
                        filtered_map[i, j] = 1
                    else:
                        filtered_map[i, j] = 0
            np.save("map.npy", filtered_map)
            print("Map file saved")
        elif key == ord('L'):
            mapnew = np.load("map.npy")
            print("Map loaded")
        elif key == ord('B'):
            print("Running recognition")
            obj = run_camera_recognition()							#detect the object in the camera
            print(f"Recognized object position: {obj}")	
            if(len(obj) > 0):														#if we have coordinates
                Manipulation = True											#set manipulation flag high
                prevError = 4														#initialize error to be large
                staticError = 0													#initialize static error counter, if robot doesnt move over certain amount of time, it will reset
                positionList = [[-obj[2]+0.14, -obj[0]+0.05, 0.56], [-obj[2]+0.25, -obj[0]+0.05, 0.56]]			#list of waypoints for the arm. the first is a little in front of the cube to line it up, the second in the cube position
            #if (err > 1.1):
            #    print("Move closer to block")
           
        else:
            vL *= 0.75
            vR *= 0.75
         # INSERT MANIPULATION CODE HERE (Move to X:obj[0], Y:obj[1], Z:obj[2] + offsets)    
        if(placingInBasket):					#if we have a block grasped and are placing it in the basket
            placed = placeInBasket()		#call function to set position and determine error
            robot.getDevice("gripper_right_finger_joint").setPosition(0)	#grasp
            robot.getDevice("gripper_left_finger_joint").setPosition(0)   #grasp
            
            if(placed):		#if we are within the position error, we drop the cube
                robot.getDevice("gripper_right_finger_joint").setPosition(0.045)		#open grasp, drop cube
                robot.getDevice("gripper_left_finger_joint").setPosition(0.045)
                placingInBasket = False																							#state is set to false
        elif(Grasping):				#if we are in the process of grasping, we need to give it time to close
            delayStep += 1		#increment delay step
            robot.getDevice("gripper_right_finger_joint").setPosition(0)	#keep grasp closed
            robot.getDevice("gripper_left_finger_joint").setPosition(0) #
            
            if(delayStep > 35):				#once time has passed, move arm to basket
                Grasping = False			#set grasping flag to false
                placingInBasket = True	#set placing flag to true
                robot.getDevice("gripper_right_finger_joint").setPosition(0)	#keep arm closed
                robot.getDevice("gripper_left_finger_joint").setPosition(0) #grab item
        elif(Manipulation):		#once we locate the cube, we go and grabit
            ikSkip += 1				#used to prevent calling inverse kinematics every time step
            initial_position = [0,0,0,0] + [m.getPositionSensor().getValue() for m in motors] + [0,0,0,0]		#get initial position of the joints
            if(len(obj) > 0):    #if obj is coordinates
                blockPos = positionList[0]	#take first coordinate in the list
            else:
                blockPos = [0.8, 0, 0.54]		#arbitrary coordinates if empty
                
            fkResults = my_chain.forward_kinematics(initial_position)		#get current position of end effector
            
            blockError = 0		#initialize error between end effector and waypoint
            for item in range(3):
                blockError += (blockPos[item] - fkResults[item][3])**2		#calculate error between ee and waypoint
            blockError = math.sqrt(blockError)
            print(f"Block Error: {blockError}")
            print(f"Prev Error: {prevError}")
            
            if(abs(prevError - blockError) < 0.00005): #if the error between the timesteps is small, the EE is not moving
                staticError += 1				#increase increment
            print(f"static error counter: {staticError}")
            
            if(staticError > 75):	#if EE has been stationary for awhile, reset manipulation
                Manipulation = False		#reset flag
                target_pos = (0, 0, 0, 0.3, -0.5, -2.3, 2.15, 1.5, -1.39, -0.25, 'inf', 'inf')	#return to starting state

                for i in range(N_PARTS):
                    robot_parts[i].setPosition(float(target_pos[i]))										#set position
                    robot_parts[i].setVelocity(robot_parts[i].getMaxVelocity() / 4.0)		#set velocity
                    
            prevError = blockError		#reset block error to previous error 
                      
            if(blockError > 0.007) and (ikSkip > 6):		#if the error is large enough and hasnt been called in a couple timesteps
                ikResults = my_chain.inverse_kinematics(blockPos, initial_position=initial_position, target_orientation = [[0,0,-1],[-1,0,0],[0,1,0]], orientation_mode="all")	#calculate required pose
                ikSkip = 0	#reset counter
            
            if(blockError < 0.06) and (len(positionList) > 1): #reached first waypoint above block
                positionList.pop(0) # pop current waypoint and head to next
            elif(blockError < 0.055):   #if we arrive at block
                placingInBasket = False		#set proper flags to their states. in this case we want to grasp and no longer manipulate
                Manipulation = False
                Grasping = True
                delayStep = 0		#set the time delay to allow grasping
                robot.getDevice("gripper_right_finger_joint").setPosition(0) #grab item
                robot.getDevice("gripper_left_finger_joint").setPosition(0) #grab item
                

            for res in range(len(ikResults)):										#assing positions from ik calcualtions
                if my_chain.links[res].name in part_names:
                    robot.getDevice(my_chain.links[res].name).setPosition(ikResults[res])
          	
    # feedback for odometry curerntly commented out due to mapping not working
    # else:
        # rho = math.sqrt((pose_x - waypoints[state][0])**2 + (pose_y - waypoints[state][1])**2)
        # alpha = math.atan2((waypoints[state][1] - pose_y), (waypoints[state][0] - pose_x)) - pose_theta
        # if (state < len(waypoints)):
            # eta = math.atan2(waypoints[state+1][1] - pose_y, waypoints[state+1][0] - pose_x) - pose_theta
        # else:
            # eta = 0.0
    
        # ####### This was broken in lab 5 #######
        # if alpha < -3.1415: alpha += 6.283
        # if eta < -3.1415: eta += 6.283
        # p1 = 1.0
        # p2 = 4.0
        # p3 = 1.0
        # if (rho <= 0.1):
            # p1 = 0.25
            # p3 = 2.0
        # elif (rho >= 0.2):
            # p3 = 0.5  
        # dX = p1*rho
        # dTheta = p2*alpha + p3*eta

        # vL = (2*dX - (dTheta * AXLE_LENGTH))/2
        # vR = (2*dX + (dTheta * AXLE_LENGTH))/2
        
        # #Normalizing Wheel speed
        # ratio = vL/vR
        
        # if (abs(ratio) > 1):
            # left_v = 1
            # right_v = (1/ratio) 
        # elif (abs(ratio) < 1):
            # left_v = ratio
            # right_v = 1
        # else:
            # left_v = 1
            # right_v = 1

        # if (vL < 0):
            # vL = (-1*left_v*MAX_SPEED)/4
        # elif (vL > 0):
            # vL = (left_v*MAX_SPEED)/4
        # if (vR < 0):
            # vR = (-1*right_v*MAX_SPEED)/4
        # elif (vR > 0):
            # vR = (right_v*MAX_SPEED)/4

        # if (vL > MAX_SPEED):
            # vL = MAX_SPEED
        # if (vR > MAX_SPEED):
            # vR = MAX_SPEED
        # if (vL < -1*MAX_SPEED):
            # vL = -1 * MAX_SPEED
        # if (vR < -1*MAX_SPEED):
            # vR = -1 * MAX_SPEED
            
        # vL = 0.9*vL
        # vR = 0.9*vR

    # Odometry
    pose_x += (vL+vR)/2/MAX_SPEED*MAX_SPEED_MS*timestep/1000.0*math.cos(pose_theta)
    pose_y -= (vL+vR)/2/MAX_SPEED*MAX_SPEED_MS*timestep/1000.0*math.sin(pose_theta)
    pose_theta += (vR-vL)/AXLE_LENGTH/MAX_SPEED*MAX_SPEED_MS*timestep/1000.0
    
    if pose_theta > 6.28+3.14/2: pose_theta -= 6.28
    if pose_theta < -3.14: pose_theta += 6.28

    # print("X: %f Z: %f Theta: %f" % (pose_x, pose_y, pose_theta))
    
    if (rho <= 0.2) and (eta < 0.5) and (eta > -0.5) and (state < len(waypoints)):
        vL = 0
        vR = 0
        print("reached goal: ", waypoints[state])
        state += 1
    
    elif (rho <= 0.1) and (eta < 0.5) and (eta > -0.5):
        vL = 0
        vR = 0
        print("Reached final goal")
        state += 1

    # Actuator commands
    robot_parts[MOTOR_LEFT].setVelocity(vL)
    robot_parts[MOTOR_RIGHT].setVelocity(vR)

# Main Loop
while robot.step(timestep) != -1:
    
    robot.getDevice("wheel_left_joint").setVelocity(vL)
    robot.getDevice("wheel_right_joint").setVelocity(vR)
