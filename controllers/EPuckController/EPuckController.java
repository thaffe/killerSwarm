import com.cyberbotics.webots.controller.Camera;
import com.cyberbotics.webots.controller.DifferentialWheels;
import com.cyberbotics.webots.controller.DistanceSensor;

public class EPuckController extends DifferentialWheels {
    private final static int DIST_SENSOR_FL = 6, DIST_SENSOR_FFL = 7, DIST_SENSOR_L = 5,
            DIST_SENSOR_FR = 1, DIST_SENSOR_FFR = 0, DIST_SENSOR_R = 2;
    private final static int DIST_THRESHOLD = 300;
    private final static int TIME_STEP = 32;
    private final static int MAX_SPEED = 1000;
    private Camera camera;
    private double rSpeed, lSpeed;
    private int[] image;
    private float[] rangeImage;
    private DistanceSensor[] distSensors;
    private double[] distValues;

    public EPuckController() {
        super();
        this.distSensors = new DistanceSensor[8];
        this.distValues = new double[8];
        for (int i = 0; i < distSensors.length; i++) {
            distSensors[i] = this.getDistanceSensor("ps" + i);
            distSensors[i].enable(TIME_STEP);
        }
        this.camera = this.getCamera("camera");
        this.camera.enable(TIME_STEP);
    }

    public static void main(String[] args) {
        EPuckController controller = new EPuckController();
        controller.run();
    }

    public void run() {
        this.setSpeed(100, -100);
        while (step(TIME_STEP) != -1) {
            //Update distances sensors
            for (int i = 0; i < distSensors.length; i++) {
                distValues[i] = distSensors[i].getValue();
            }
            this.rangeImage = this.camera.getRangeImage();
            this.image = this.camera.getImage();

            this.avoidObjects();
            this.setSpeed(lSpeed, rSpeed);
        }
    }

    private void avoidObjects() {
        double left = distValues[DIST_SENSOR_FL] + distValues[DIST_SENSOR_FFL];
        double right = distValues[DIST_SENSOR_FR] + distValues[DIST_SENSOR_FFR];

        if (left > DIST_THRESHOLD || right > DIST_THRESHOLD) {
            if(left > right && lSpeed > 0)
                turn(true);
            else if(rSpeed > 0)
                turn(false);
        } else {
            drive(true);
        }
    }

    private void wander() {

    }

    private void explore() {

    }

    private void buildMaps() {

    }

    private void monitorChanges() {

    }

    private void identifyObjects() {

    }

    private void planChangesToTheWorld() {

    }

    private void reasonAboutBehaviourOfObject() {

    }

    private void setLed(int red, int green, int blue) {
    }

    private void turn(boolean right) {
        this.lSpeed = right ? MAX_SPEED : -MAX_SPEED * 0.5;
        this.rSpeed = !right ? MAX_SPEED : -MAX_SPEED * 0.5;
    }

    private void drive(boolean forward) {
        this.lSpeed = forward ? MAX_SPEED : -MAX_SPEED;
        this.rSpeed = forward ? MAX_SPEED : -MAX_SPEED;
    }

    private void stop() {
        this.lSpeed = 0;
        this.rSpeed = 0;
    }


}