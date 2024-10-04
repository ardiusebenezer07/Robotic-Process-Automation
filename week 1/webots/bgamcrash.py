from controller import Robot

# Create the Robot instance
robot = Robot()

# Time step of the simulation (ms)
timestep = int(robot.getBasicTimeStep())

# Get the wheels motors
left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')

# Set the motors control to velocity mode
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

# Set the motors velocity to 0 initially
left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

# Main loop:
while robot.step(timestep) != -1:
    # Set forward velocity for both wheels
    left_motor.setVelocity(2.0)  # forward speed for left wheel
    right_motor.setVelocity(2.0)  # forward speed for right wheel
