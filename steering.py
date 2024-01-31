

from hardware import MotionData


def compute_steering(speed: float, direction: float) -> MotionData:
    # motor speed is simple, we just set all motors to the same speed
    motion_data = MotionData()
    motion_data['motor_back_left'] = speed
    motion_data['motor_back_right'] = speed
    motion_data['motor_center_left'] = speed
    motion_data['motor_center_right'] = speed
    motion_data['motor_front_left'] = speed
    motion_data['motor_front_right'] = speed

    # when turning left (-1) we want the front servos to turn 45 degrees to the left, and the back servos to turn 45 degrees to the right
    # technically, 90 degrees is straight, so we want to map [-90, 90] to [45, 135]
    max_input_turn_angle = 90
    max_turn_angle = 60
    direction = max_turn_angle * direction / max_input_turn_angle
    direction += 90  # 0 is now left, 180 is now right
    # direction is now in the range [45, 135]
    # TODO: if we find out that direction is backwards, we need to reverse the direction of the servos

    motion_data['servo_front_left'] = direction
    motion_data['servo_front_right'] = direction
    motion_data['servo_back_left'] = 180 - direction
    motion_data['servo_back_right'] = 180 - direction

    return motion_data
