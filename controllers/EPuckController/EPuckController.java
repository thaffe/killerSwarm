import com.cyberbotics.webots.controller.*;
import com.cyberbotics.webots.controller.Camera;
import com.cyberbotics.webots.controller.DifferentialWheels;
import com.cyberbotics.webots.controller.DistanceSensor;
import com.cyberbotics.webots.controller.Field;
import com.cyberbotics.webots.controller.LED;
import com.cyberbotics.webots.controller.Node;

import java.lang.String;

public class EPuckController extends DifferentialWheels {

    private Camera camera;
    private DistanceSensor pSensorL, pSensorFL, pSensorFR, pSensorR;

    private double rSpeed, lSpeed;
    private double rx1 = 250, rx2 = 250, rx3 = 250, rx4 = 250;
    private double lx1 = 250, lx2 = 250, lx3 = 250, lx4 = 250;

    private int[] image;
    private float[] rangeImage;

    public EPuckController() {
        super();
        this.camera = this.getCamera("camera");
        this.pSensorL = this.getDistanceSensor("ps6");
        this.pSensorFL = this.getDistanceSensor("ps7");
        this.pSensorFR = this.getDistanceSensor("ps0");
        this.pSensorR = this.getDistanceSensor("ps1");
        this.pSensorFL.enable(16);
        this.pSensorL.enable(16);
        this.pSensorR.enable(16);
        this.pSensorFR.enable(16);
        this.camera.enable(16);
    }

    public static void main(String[] args) {
        EPuckController controller = new EPuckController();
        controller.run();
    }

    public void run() {
        this.setSpeed(100, -100);
        while (step(16) != -1) {
            this.rangeImage = this.camera.getRangeImage();
            this.image = this.camera.getImage();

            this.avoidObjects();
            this.setSpeed(rSpeed,lSpeed);
        }
    }

    private void avoidObjects(){
        double left = pSensorL.getValue() + pSensorFL.getValue();
        double right = pSensorR.getValue() + pSensorFR.getValue();
        if(left > 300 || right > 300){
            if(left > right && rSpeed != -300){
                rSpeed = 1000;
                lSpeed = -300;
            }
            else if(lSpeed != -300){
                rSpeed = -300;
                lSpeed = 1000;
            }

        }
        else{
            lSpeed = 1000;
            rSpeed = 1000;
        }

        //rSpeed = rx1 / pSensorL.getValue() + rx2 / pSensorFL.getValue() + rx3 / pSensorFR.getValue() + rx4 / pSensorR.getValue();
        //lSpeed = lx1 / pSensorL.getValue() + lx2 / pSensorFL.getValue() + lx3 / pSensorFR.getValue() + lx4 / pSensorR.getValue();
     }

    private void wander(){

    }

    private void explore(){

    }

    private void buildMaps(){

    }

    private void monitorChanges(){

    }

    private void identifyObjects(){

    }

    private void planChangesToTheWorld(){

    }

    private void reasonAboutBehaviourOfObject(){

    }

    private void setLed(int red, int green, int blue){
    }
}