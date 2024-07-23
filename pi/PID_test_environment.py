import matplotlib.pyplot as plt
import PID

# just a test environment to make sure the PID is pretty much working.
# this isn't a replacement for water testing! you still need test in an actual scenario
# to tune the paramaters, this is pretty minor

class WaterSimulation():
    def __init__(self, pid):
        self.pid = pid
        self.vel = 0
        self.pos = 0
        self.min = 0
        self.gravity = 9.8
        self.damping = 2

    def tick(self):
        self.vel -= self.gravity
        self.vel /= self.damping
        signal = self.pid.predict(self.pos)
        self.vel += signal
        self.pos += self.vel


    def test_and_display(self, iterations):
        positions = []
        velocities = []
        for i in range(iterations):
            self.tick()
            positions.append(self.pos)
            velocities.append(self.vel)
        
        plt.plot(range(iterations), positions)
        # plt.show()

sim = WaterSimulation(PID.PID(0.6, 0.0, 0.1, 20, 0.1))
sim.test_and_display(100)

plt.savefig("pid_test.png")
# this will be made better
# or maybe not, ha