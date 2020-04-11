
GAS_DENSITY = 2.858
ONE_MPH = 0.44704


class Controller(object):
    def __init__(self, vehicle_details):
        # TODO: Implement
        self.vd = vehicle_details
        self.vd["min_speed"] = 0.1
        vd = self.vd

        self.yaw_controller = YawController(vd["wheel_base"], vd["steer_ratio"], vd["min_speed"], vd["max_lat_accel"], vd["max_steer_angle"])

        kp = 0.3
        ki = 0.1
        kd = 0
        min_throttle = 0
        max_throttle = 0.2

        self.throttle_controller = PID(kp, ki, kd, min_throttle, max_throttle)

        tau = 0.5
        sample_time = 0.02

        self.vel_lpf = LowPassFilter(tau, sample_time)

        self.last_time = rospy.get_time()


    def control(self, current_vel, dbw_enabled, linear_vel, angular_vel):
        # TODO: Change the arg, kwarg list to suit your needs
        # Return throttle, brake, steer
        if dbw_enabled == False:
            self.throttle_controller.reset()
            return 0., 0., 0.

        current_vel = self.vel_lpf.filt(current_vel)

        steering = self.yaw_controller.get_steering(linear_vel, angular_vel, current_vel)

        val_error = linear_vel - current_vel
        self.last_vel = current_Vel

        current_time = rospy.get_time()
        sample_time = current_time - self.last_time
        self.last_time = current_time

        throttle = self.throttle_controller.step(val_error, sample_time)
        brake = 0

        if linear_vel == 0. and current_vel  < self.vd["min_speed"]:
            throttle = 0
            brake = 400

        elif throttle < self.vd["min_speed"] and vel_error < 0:
            throttle = 0
            decel = max(val_error, self.vd["decel_limit"])
            brake = abs(decel)*self.vd["vehicle_mass"]*self.vd["wheel_radius"]

        return throttle, brake, steering
