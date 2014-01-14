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
    private double rx1 = 0.3, rx2 = 0.3, rx3 = 0.3, rx4 = 0.3;
    private double lx1 = 0.3, lx2 = 0.3, lx3 = 0.3, lx4 = 0.3;

    private int[] image;
    private float[] rangeImage;

    public EPuckController() {
        super();
        this.camera = this.getCamera("camera");
        this.pSensorL = this.getDistanceSensor("ps1");
        this.pSensorFL = this.getDistanceSensor("ps2");
        this.pSensorFR = this.getDistanceSensor("ps3");
        this.pSensorR = this.getDistanceSensor("ps4");
        this.pSensorFL.enable(64);
        this.pSensorL.enable(64);
        this.pSensorR.enable(64);
        this.pSensorFR.enable(64);
        this.camera.enable(64);
    }

    public static void main(String[] args) {
        EPuckController controller = new EPuckController();
        controller.run();
    }

    public void run() {
        this.setSpeed(100, -100);
        while (step(64) != -1) {
            this.rangeImage = this.camera.getRangeImage();
            this.image = this.camera.getImage();

            this.avoidObjects();
            this.setSpeed(rSpeed,lSpeed);
        }
    }

    private void avoidObjects(){
        rSpeed = rx1 * pSensorL.getValue() + rx2 * pSensorFL.getValue() + rx3 * pSensorFR.getValue() + rx4 * pSensorR.getValue();
        lSpeed = lx1 * pSensorL.getValue() + lx2 * pSensorFL.getValue() + lx3 * pSensorFR.getValue() + lx4 * pSensorR.getValue();
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