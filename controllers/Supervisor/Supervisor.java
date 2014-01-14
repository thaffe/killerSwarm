import com.cyberbotics.webots.controller.Field;
import com.cyberbotics.webots.controller.Node;

public class Supervisor extends com.cyberbotics.webots.controller.Supervisor {
    private static final int ROBOTS = 1;
    private static final double BOARD_DIM = 1;

    public Supervisor() {

        super();

    }

    public static void main(String[] args) {
        Supervisor controller = new Supervisor();
        controller.run();
    }

    public void run() {
        for (int i = 1; i <= ROBOTS; i++) {
            Node node = getFromDef("EPuck" + i);
            Field field = node.getField("translation");
            double x = Math.random() * BOARD_DIM - BOARD_DIM / 2.0,
                    y = Math.random() * BOARD_DIM - BOARD_DIM / 2.0;
            field.setSFVec3f(new double[]{x, 0, y});

        }
        while (step(64) != -1) {

            // Read the sensors:
            // Enter here functions to read sensor data, like:
            //  double val = distanceSensor.getValue();

            // Process sensor data here

            // Enter here functions to send actuator commands, like:
            //  led.set(1);
        }

        // Enter here exit cleanup code
    }
}
