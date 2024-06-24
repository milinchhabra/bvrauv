import time

# A PID controller is a piece of code which tries to bring a chaotic system to a specific
# value; eg. bring a sub to a specific depth or angle, manuevering against the chaotic water.
# it is based on three parts; one Proportional, Integral, and Derivative (P-I-D). The final
# output signal is a weighted sum of the three parts. To find the proportional piece, you just
# take the error between the current value and the wanted value. The integral piece is the sum
# of all the previous errors. The derivative piece is more complicated, being the rate of change
# between the current and previous errors; so, (error - prev_error) / (time - prev_time).
# once you have these three pieces, the output is just a weighted sum of them, using
# Kp, Ki, and Kd respectively

# as of the 2023 competition, the parameters were
# Kp = 0.6
# Ki = 0.0
# Kd = 0.1
# these will probably need to be retuned in the future

class PID:
    def __init__(self, proportional, integral, derivative, wanted, interval=None):
        # the first three params represent the weight of their respective part of the PID
        # interval is optional, if unset the PID time will be based on actual time, which is 
        # good in case of potential lag. if set, it will assume every call is `interval`
        # seconds apart. it's good for testing, but in a real scenario use timestamp

        self.Kp = proportional
        self.Ki = integral
        self.Kd = derivative

        self.wanted = wanted
        
        self.interval = interval

        self.integral = 0
        # integral represents the total error; the integral

        self.prev = 0
        # prev represents the previous error

        self.prevTime = time.time()
        # only used if interval is unset



    def predict(self, current):
      # return the predicted push, given a current value
      # this will update the saved data such as total error and previous error
      

      timeDiff = self.interval if self.interval is not None else time.time() - self.prevTime
      error = self.wanted - current
      self.integral += error
      derivative = (error-self.prev)/timeDiff

      self.prev = error
      signal = (self.Kp * error) + (self.Ki * self.integral) + (self.Kd * derivative)
      return signal