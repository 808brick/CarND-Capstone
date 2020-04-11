# Self Driving Car Capstone Project
This project implements multiple aspects of general autonomous car functionality to have a self driving car traverse along a simulated highway safely. This project is the final project in the Udacity Self Driving Car Engineer Nanodegree program. 

### Way Point Generation

### Throttle, Braking, And Steering

The main actuation function of the autonomous car is it's throttle, braking, and steering state.

##### PID Controller


### Traffic Light Detection

One of the capabilities of an autonomous car is to be able to identify street lights and be able to decide if it can traverse through an intersection or stop. <More info....>

###### Neural Network Description

###### Different Data Sets
There are two different data sets utilized when training the neural network. One is trained with image data from the simulation to detect the state of a simulation traffic light. The other data set is trained on real traffic light images. These different data sets allow for the autonomous car to identify traffic lights in both the simulation and when implemented on a real self driving car. <More info....>

### ROS Topic Desciption

| Topic Name  | Topic Type  | Topic Description |
| ---         |    ---      |     ---           |
| /base_waypoints       |   styx_msgs/Lane      |     Waypoints as provided by a static .csv file.          |
| /final_waypoints         |    styx_msgs/Lane      |    This is a subset of /base_waypoints. The first waypoint is the one in /base_waypoints which is closest to the car.         |
| /current_pose        |    geometry_msgs/PoseStamped      |
| /current_velocity        |    ---      |     ---           |   Current position of the vehicle, provided by the simulator or localization.          |
| /vehicle/throttle_cmd         |    ---      |     ---           |
| /vehicle/brake_cmd        |    ---      |     ---           |
| /vehicle/steering_cmd       |    ---      |     ---      |
| /vehicle/dbw_enabled  |    ---      |     ---           |
| /twist_cmd        |    ---      |     ---           |
| /image_color      |    ---      |    Provides an image stream from the car's camera. These images are used to determine the color of upcoming traffic lights.        |
| /vehicle/traffic_lights |    ---      | provides the (x, y, z) coordinates of all traffic lights. |
| /traffic_waypoint |    ---      |     ---           |

### Running The Project
