# Elise Pitre
# Final Project - Double Pendulum

# Imports
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import scipy.integrate as integrate
import matplotlib.animation as animation
import numpy as np


# Creates a function that calculates angular accelerations with angular velocities and the angles
def calculations(state, t):
    # Making an empty list of values for angular velocity and new angular acceleration
    values_list = [0,0,0,0]

    # Pulling out values for angles and velocities from current state
    theta_1 = state[0]
    vel_1 = state[1]
    theta_2 = state[2]
    vel_2 = state[3]

    # Moving angular velocities to the spot of angles
    # This is done so that when the antiderivatives (opposite of derivatives) are calculated, it's in the correct place
    # Angular velocity is the derivative of the angle
    values_list[0] = state[1]
    values_list[2] = state[3]

    # Using equations derived at https://www.myphysicslab.com/pendulum/double-pendulum-en.html
    # Solving for the angular acceleration of each bob

    # Solving bob 1
    # Breaking up numerator 1 into parts
    num1a = (-g * ((2 * m1) + m2) * np.sin(theta_1))
    num1b = (-m2 * g * np.sin(theta_1 - (2 * theta_2)))
    num1c = (-2 * np.sin(theta_1 - theta_2) * m2)
    num1d = (((vel_2 ** 2) * l2) + (vel_1 ** 2) * l1 * np.cos(theta_1 - theta_2))
    # Putting numerator 1 together
    num1 = num1a + num1b + (num1c * num1d)
    # Creating denominator1
    den1 = l1 * ((2 * m1) + m2 - (m2 * np.cos((2 * theta_1) - (2 * theta_2))))

    # Solving bob 2
    # Breaking up numerator 2 into parts
    num2a = (2 * np.sin(theta_1 - theta_2))
    num2b = l1 * (vel_1 ** 2) * (m1 + m2)
    num2c = g * (m1 + m2) * np.cos(theta_1)
    num2d = (vel_2 ** 2) * l2 * m2 * np.cos(theta_1 - theta_2)
    # Putting numerator 2 together
    num2 = num2a * (num2b + num2c + num2d)
    # Creating denominator 2
    den2 = l2 * ((2 * m1) + m2 - (m2 * np.cos((2 * theta_1) - (2 * theta_2))))

    # Putting together the numerator and denominator together for angular acceleration
    # Adds the values for angular acceleration into the appropriate spots in the list of new values
    values_list[1] = num1 / den1
    values_list[3] = num2 / den2

    # returns list that looks like: [velocity1, acceleration1, velocity2, acceleration2]
    return values_list

# User chooses length of animation
print("Please choose a number of frames between 500 and 5,000 at incriments of 100")
print("For example: 200 or 521 would not work")
accept1 = False
# Only accepts values in the correct range
while accept1 == False:
    num_frames = int(input("Input the number of frames for the animation here: "))
    remainder = num_frames % 100
    if num_frames <= 5000 and num_frames >= 500 and remainder == 0:
        accept1 = True
    else:
        print("That number is not an option, please choose a number between 500 and 5,000 at incriments of 100")

# User chooses the angle of the first bob
print("")
print("Please choose the angle for the first pendulum arm")
print("All option are measured in degrees from the NEGATIVE Y axis")
print("Your options are 45, 90, 135 or 180")
accept2 = False
while accept2 == False:
    angle1 = int(input("Input the angle you want here: "))
    # If angle is valid, the angle is put into radians and saved
    if angle1 == 45 or angle1 == 90 or angle1 == 135 or angle1 == 180:
        accept2 = True
        if angle1 == 45:
            theta1 = np.pi / 4
        elif angle1 == 90:
            theta1 = np.pi / 2
        elif angle1 == 135:
            theta1 = (3 * np.pi) / 4
        elif angle1 == 180:
            theta1 = np.pi
    # If the angle is not valid, it asks again and clarifies
    else:
        print("That angle is not an option, please choose one from the list: 45, 90, 135 or 180")

# User chooses the angle of the second bob
print("")
print("Please choose the angle for the second pendulum arm")
print("All option are measured in degrees from the NEGATIVE Y axis")
print("Your options are 45, 90, 135 or 180")
# Do not accept 180 if the first angle is 180 since the pendulum will get stuck
print("If you picked 180 for the first arm, you may not pick it again")
accept3 = False
while accept3 == False:
    angle2 = int(input("Input the angle you want here: "))
    # If angle is valid, the angle is put into radians and saved
    if angle2 == 45 or angle2 == 90 or angle2 == 135:
        accept3 = True
        if angle2 == 45:
            theta2 = np.pi / 4
        elif angle2 == 90:
            theta2 = np.pi / 2
        elif angle2 == 135:
            theta2 = (3 * np.pi) / 4
    elif angle2 == 180 and theta1 != np.pi:
        accept3 = True
        theta2 = np.pi
    # If the angle is not valid, it asks again and clarifies
    else:
        print("That angle is not an option, please choose one from the list: 45, 90, 135 or 180")
        if theta1 == np.pi:
            print("Remember, you may not pick 180 since you picked 180 for the first arm")

# User chooses the length of the first pendulum
print("")
print("Please choose a length for the first pendulum")
print("Your options are: 0.1, 0.5 and 1")
accept4 = False
while accept4 == False:
    length1 = input("Enter the length here: ")
    if length1 == 0.1 or length1 == 0.5 or length1 == 1:
        l1 = length1
        accept4 = True
    else:
        print("That length is not valid. Please choose 0.1, 0.5 or 1")

# User chooses the length of the second pendulum
print("")
print("Please choose a length for the second pendulum")
print("Your options are: 0.1, 0.5 and 1")
accept5 = False
while accept5 == False:
    length2 = input("Enter the length here: ")
    if length2 == 0.1 or length2 == 0.5 or length2 == 1:
        l2 = length2
        accept5 = True
    else:
        print("That length is not valid. Please choose 0.1, 0.5 or 1")

# Creates variable for the total length of the two pendulums together plus 0.1
total_l = l1 + l2 + 0.1

# Setting variables for masses of bobs and gravity
g = 1
m1 = 1
m2 = 1
# Creates variables for initial angular velocities
av1 = 0.0
av2 = 0.0
# Creates list of values for the initial state of the pendulum
state = ([theta1, av1, theta2, av2])

# Creates a time array from 0 to 100 at 0.05 second steps
# The second number in the brackets relates to how long the animation is
# The third number in the brackets relates to how smooth the animation is
t = np.arange(0.0, (num_frames/20), 0.05)
# Calls on the function to calculate angular velocity
# And calculates the antiderivatives of velocities and accelerations to get angles and new velocities
# This creates a list containing the lists of velocities and angles for every frame
a_derivs = integrate.odeint(calculations, state, t)

# Extracts all the angle values from a_derivs and adds them to two lists
def Extract(list1):
    return [item[0] for item in list1]
def Extract2(list2):
    return [item[2] for item in list2]
the1_list = Extract(a_derivs)
the2_list = Extract2(a_derivs)
# Creates a list of x and y values from the lists with calculated angles
# These lists are all the data points needed for the simulation
x1 = l1 * np.sin(the1_list)
y1 = -l1 * np.cos(the1_list)
x2 = x1 + (l2 * np.sin(the2_list))
y2 = y1 + (-l2 * np.cos(the2_list))

# Creates a plot to graph on
fig = plt.figure()
ax = fig.add_subplot(111, autoscale_on=False, xlim=(-total_l, total_l), ylim=(-total_l, total_l))
# Fixes scaling issues of graph
ax.set_aspect('equal')
# Adds a title to graph
ax.set_title('Double Pendulum')
# Turns off the axis lines of graph
ax.axis("off")
# Creates a line with circles at the ends that will be the pendulum
line, = ax.plot([], [], 'o-', lw=2, color="black")

# Creates function to initialize the animation
def init():
    line.set_data([], [])
    return line,

# Creates function to animate (runs through the coordinate values)
def animate(frame):
    # Giving 3 x values to a line creates 2 connected line segments (the pendulum)
    # Takes x and y values from lists corresponding to the frame number
    current_x = [0, x1[frame], x2[frame]]
    current_y = [0, y1[frame], y2[frame]]
    line.set_data(current_x, current_y)
    return line,

# Does the animation using FuncAnimation
# "fig" - calls the plot that is being animated
# "animate" - calls the function to animate
# "frames=num_frames" - sets the number of frames for the animation/ sets the number of times the animate function is looped
# "interval=20" - sets the speed of the animation
# "blit=True" - means that only parts of the graph that changed will be re-drawn
# "init_func=init" - calls the function to initialize the animation
ani = animation.FuncAnimation(fig, animate, frames=num_frames, interval=20, blit=True, init_func=init)

# Shows the animation
plt.show()