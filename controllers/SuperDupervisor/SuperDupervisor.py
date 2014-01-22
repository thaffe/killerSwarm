# File:          SuperDupervisor.py
# Date:          
# Description:   
# Author:        
# Modifications: 

# You may need to import some classes of the controller module. Ex:
#  from controller import Robot, LED, DistanceSensor
#
# or to import the entire module. Ex:
#  from controller import *
from controller import *
import random as r
import math

# Here is the main class of your controller.
# This class defines how to initialize and how to run your controller.
# Note that this class derives Robot and so inherits all its functions
class SuperDupervisor (Supervisor):

  def get_random_pos(self):
      return [int(math.floor(r.random()*20)), int(math.floor(r.random()*20))]
  # User defined function for initializing and running
  # the SuperDupervisor class
  def run(self):
    poses = [ [ x > 5 and x < 15 and y > 5 and y < 15 for x in range(20)] for y in range(20)]

    for i in range(8):
        n = self.getFromDef("e"+str(i))
        f = n.getField("translation")
        pos = self.get_random_pos()
        while poses[pos[0]][pos[1]]:
            pos = self.get_random_pos()

        f.setSFVec3f([1.4* pos[0]/19-0.7, 0.1, 1.4 * pos[1]/19 - 0.7])
        poses[pos[0]][pos[1]] = True
        print([1.5* pos[0]/19-0.75, 1.5 * pos[1]/19 - 0.75, 0.1])



    print self.getFromDef("e")

    # You should insert a getDevice-like function in order to get the
    # instance of a device of the robot. Something like:
    #  led = self.getLed('ledname')
    
    # Main loop
    while True:
      # Perform a simulation step of 64 milliseconds
      # and leave the loop when the simulation is over
      if self.step(64) == -1:
        break
      
      # Read the sensors:
      # Enter here functions to read sensor data, like:
      #  val = ds.getValue()
      
      # Process sensor data here.
      
      # Enter here functions to send actuator commands, like:
      #  led.set(1)
    
    # Enter here exit cleanup code

# The main program starts from here

# This is the main program of your controller.
# It creates an instance of your Robot subclass, launches its
# function(s) and destroys it at the end of the execution.
# Note that only one instance of Robot should be created in
# a controller program.
controller = SuperDupervisor()
controller.run()
