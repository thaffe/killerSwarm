// File:          EPuckController.java
// Date:          
// Description:   
// Author:        
// Modifications: 

// You may need to add other webots classes such as
//  import com.cyberbotics.webots.controller.DistanceSensor;
//  import com.cyberbotics.webots.controller.LED;
// or more simply:
//  import com.cyberbotics.webots.controller.*;

import com.cyberbotics.webots.controller.DifferentialWheels;
import com.cyberbotics.webots.controller.Field;
import com.cyberbotics.webots.controller.Node;

// Here is the main class of your controller.
// This class defines how to initialize and how to run your controller.
// Note that this class derives Robot and so inherits all its functions
public class EPuckController extends DifferentialWheels {

    // You may need to define your own functions or variables, like
    //  private LED led;

    // EPuckController constructor
    public EPuckController() {
        // call the Robot constructor
        super();

        // You should insert a getDevice-like function in order to get the
        // instance of a device of the robot. Something like:
        //  led = getLED("ledName");

    }

    // This is the main program of your controller.
    // It creates an instance of your Robot subclass, launches its
    // function(s) and destroys it at the end of the execution.
    // Note that only one instance of Robot should be created in
    // a controller program.
    // The arguments of the main function can be specified by the
    // "controllerArgs" field of the Robot node
    public static void main(String[] args) {
        EPuckController controller = new EPuckController();
        controller.run();
    }

    // User defined function for initializing and running
    // the EPuckController class
    public void run() {
        this.setSpeed(100, -100);
        // Main loop:
        // Perform simulation steps of 64 milliseconds
        // and leave the loop when the simulation is over
        while (step(64) != -1) {

            // Read the sensors:
            // Enter here functions to read sensor data, like:
            //  double val = distanceSensor.getValue();

            // Process sensor data here

            // Enter here functions to send actuator commands, like:
            //  led.set(1);
        }
        ;

        // Enter here exit cleanup code
    }
}
