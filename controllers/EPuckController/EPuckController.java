import com.cyberbotics.webots.controller.*;
import com.cyberbotics.webots.controller.Camera;
import com.cyberbotics.webots.controller.DifferentialWheels;
import com.cyberbotics.webots.controller.Field;
import com.cyberbotics.webots.controller.LED;
import com.cyberbotics.webots.controller.Node;

import java.lang.String;

public class EPuckController extends DifferentialWheels {

    private LED led;
    private Camera camera;

    private int[] image;
    private float[] rangeImage;

    public EPuckController() {
        super();
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
        }
    }

    private void avoidObjects(){

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
        String hex = "";

        this.led.set(Integer.parseInt(hex, 16));
    }
}