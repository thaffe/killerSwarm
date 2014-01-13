import com.cyberbotics.webots.controller.DifferentialWheels;
import com.cyberbotics.webots.controller.Field;
import com.cyberbotics.webots.controller.Node;

public class EPuckController extends DifferentialWheels {

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

        }
    }
}
