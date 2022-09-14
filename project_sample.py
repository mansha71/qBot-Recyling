import sys
sys.path.append('../')
from Common.project_library import *

# Modify the information below according to you setup and uncomment the entire section

# 1. Interface Configuration
project_identifier = 'P3B' # enter a string corresponding to P0, P2A, P2A, P3A, or P3B
ip_address = '192.168.2.52' # enter your computer's IP address
hardware = False # True when working with hardware. False when working in the simulation

# 2. Servo Table configuration
short_tower_angle = 315 # enter the value in degrees for the identification tower 
tall_tower_angle = 90 # enter the value in degrees for the classification tower
drop_tube_angle = 180#270# enter the value in degrees for the drop tube. clockwise rotation from zero degrees

# 3. Qbot Configuration
bot_camera_angle = -21.5 # angle in degrees between -21.5 and 0

# 4. Bin Configuration
# Configuration for the colors for the bins and the lines leading to those bins.
# Note: The line leading up to the bin will be the same color as the bin 

bin1_offset = 0.18 # offset in meters
bin1_color = [1,0,0] # e.g. [1,0,0] for red
bin2_offset = 0.18
bin2_color = [0,1,0]
bin3_offset = 0.18
bin3_color = [0,0,1]
bin4_offset = 0.18
bin4_color = [0.1,0,0]

#--------------- DO NOT modify the information below -----------------------------

if project_identifier == 'P0':
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    bot = qbot(0.1,ip_address,QLabs,None,hardware)
    
elif project_identifier in ["P2A","P2B"]:
    QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
    arm = qarm(project_identifier,ip_address,QLabs,hardware)

elif project_identifier == 'P3A':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    configuration_information = [table_configuration,None, None] # Configuring just the table
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    
elif project_identifier == 'P3B':
    table_configuration = [short_tower_angle,tall_tower_angle,drop_tube_angle]
    qbot_configuration = [bot_camera_angle]
    bin_configuration = [[bin1_offset,bin2_offset,bin3_offset,bin4_offset],[bin1_color,bin2_color,bin3_color,bin4_color]]
    configuration_information = [table_configuration,qbot_configuration, bin_configuration]
    QLabs = configure_environment(project_identifier, ip_address, hardware,configuration_information).QLabs
    table = servo_table(ip_address,QLabs,table_configuration,hardware)
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    bins = bins(bin_configuration)
    bot = qbot(0.1,ip_address,QLabs,bins,hardware)
    

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------
import random #imports random library

def load_fun(load_count):
# the Load_fun() takes load_count as its argument and function moves the q-arm to pick up any containers from the table and place them in the hopper depending on the load_count
    
    time.sleep(2) #rests the arm for 2 seconds
    arm.move_arm(0.65,0,0.26) # moves arm to pick up location (table)
    time.sleep(1)
    arm.control_gripper(45) # grippers grab container
    time.sleep(2)
    arm.move_arm(0.4,0,0.4) # arm moves back
    time.sleep(2)
    arm.move_arm(0.4,0,0.7) # arm moves up
    time.sleep(1)
    arm.rotate_base(-90) # arm rotates 90 degrees
    time.sleep(1)
    arm.move_arm(0,-0.3,0.49) # amr moves over the hopper
    time.sleep(1)

    if load_count == 0: # if no containers have perviously been loaded than the arm moves to place the container in the middle position
        arm.move_arm(0,-0.55,0.49)
    elif load_count == 1: # if 1 container has been loaded than the arm moves to the middle position which will push the previously loaded container to the back
        arm.move_arm(0,-0.55,0.49)
    elif load_count == 2: # if 2 containers have been loaded than the arm moves to drop the container at the nearest position to the front
        arm.move_arm(0,-0.47,0.49)
    else: # if for some reason load function runs after more than 2 containers have been loaded than it prints error and resests
        print('error')
    time.sleep(1)
    arm.control_gripper(-45) # gripper lets go of the container and the arm returns home
    time.sleep(1)

    arm.home() #returns arm to its home position



def cont_transfer(desti_bin): # the cont_transfer() function transfers the containers to the bins by moving the q-bot along the yellow line
    bin_1 = 0 # initializes a counter for each bin location
    bin_2 = 0
    bin_3 = 0
    bin_4 = 0
    while True: # this loop uses the line following algorithm to allow the q-bot to navigate to each bin
        y_line = bot.line_following_sensors() #stores the line following sensor's information in y_line
        bot.activate_color_sensor() #activates the color sensor
        print(bot.read_color_sensor()) #prints the color sensor data
        colour_read = bot.read_color_sensor() #stores the color sensor's output in colour_read
        rgb = colour_read[0] #stores the rgb info into the variabel rgb
        
        #The line following algorith
        if y_line[0] == 1 and y_line[1] == 1: #if line is fully seen
            bot.set_wheel_speed([0.035,0.035]) #both wheels have the same speed
        elif y_line[0] == 1 and y_line[1] == 0: #if only one sensor sees the line
            bot.set_wheel_speed([0.02,0.035]) #one wheel's speed decreases so the bot can turn
        elif y_line[0] == 0 and y_line[1] == 1:
            bot.set_wheel_speed([0.035,0.02])
        else:
            break
        if desti_bin == "Bin01" and rgb[0] == 1: #If the container's destination is Bin 1
            bin_1 = bin_1 +1 #adds one to bin_1
            if bin_1 > 14: #works as a time so when it detects the bin's color this many times the bot stops
                bot.stop() #bot stops
                break #breaks the while loop
        if desti_bin == "Bin02" and rgb[1] == 1:
            bin_2 = bin_2 +1 
            if bin_2 > 18:
                bot.stop()
                break
        if desti_bin == "Bin03" and rgb[2] == 1:
            bin_3 = bin_3 +1
            if bin_3 > 15:
                bot.stop()
                break
        if desti_bin == "Bin04" and rgb[0] == 0.1:
            bin_4 = bin_4 +1
            if bin_4 > 15:
                bot.stop()
                break

def deposit_cont(desti_bin): #function used to load 
    cont_transfer(desti_bin)
    bot.activate_linear_actuator()
    bot.dump()
    bot.deactivate_linear_actuator()

    
t_count = 0 # variable that counts how many times the main loop has ran
while True:

    if t_count >= 1: # if this is not the first time the loop has ran then the container left on teh table is loaded
        load_fun(0) #runs load_fun with a load_count of 0
        bot_position = bot.position() #records the bots initial position
        print(bot.position())
        bin_Loc = sbin_Loc
        mass = smass
        c_count = 1 #sets the container count to 1 
        t_mass = mass # and the total mass counter to the mass of the container
    else: # if this is the first time the main loop has ran than this condition runs
        bot_position = bot.position() #records the q-bots position
        print(bot.position())
        randcont1 = random.randint(1,6) # generates a random integer from 1-6
        info = table.dispense_container(randcont1,True) # dispenses a random container and stores its data as a list in info
        mass = info[1] # stores the mass
        bin_Loc = info[2] # stores the bin location
        c_count = 0 # initalizes a count for how many containers have been loaded
        load_fun(c_count) #loads the container
        t_mass = mass # sets the total mass to the mass of the first container
    while c_count < 2 and t_mass < 90: #while loop executes as long as the total < 90 and the number of loaded containers is less than 3
        randcont2 = random.randint(1,6) # creates a new random number
        sinfo = table.dispense_container(randcont2,True) #dispenses a new random container and stores the data as a list to sinfo
        smass = sinfo[1] # stores the new containers mass in smass
        sbin_Loc = sinfo[2] # stores new containers bin location in sbin_Loc
        t_mass = t_mass + smass # increments the total mass by adding the new mass to the total
        c_count = c_count + 1 #container count increments by 1 
        if sbin_Loc == bin_Loc: # if the bin location of the new container is the same as the previously loaded container
            load_fun(c_count) #loads new container
            time.sleep(4)
            if c_count == 2: #if three containers have been loaded
                randcont2 = random.randint(1,6) # generates a new random integer
                sinfo = table.dispense_container(randcont2,True) # dispenses a new contianer and stores its data to sinfo as a list
                smass = sinfo[1] # stores the mass of the new container
                sbin_Loc = sinfo[2] # stores the bin location of the new contianer
        else: 
            break

    print(bin_Loc)
    print(sbin_Loc)
    deposit_cont(bin_Loc) # once the contianers have been loaded the load_cont function fires which moves the bot to the bin location and deposits it

    while True: #While loop used to return bot home
        
        #Same line following algorith as above
        y_line = bot.line_following_sensors()
        print(bot.read_color_sensor())
            
        if y_line[0] == 1 and y_line[1] == 1:
                bot.set_wheel_speed([0.035,0.035])
        elif y_line[0] == 1 and y_line[1] == 0:
                bot.set_wheel_speed([0.02,0.035])
        elif y_line[0] == 0 and y_line[1] == 1:
                bot.set_wheel_speed([0.035,0.02])
        else:
            break
        
        new_position = bot.position() #stores bot's new position into new_position
        print(new_position) #prints the position
        x_value = bot_position[0] #Stores initial x coordinate in x_value
        y_value = bot_position[1] #Stores initial y coordinate in y_value
        newx = new_position[0] #stores new x coordinate in newx
        newy = new_position[1] #Stores new y coordinate in newy
        if (abs(newx - x_value) + abs(newy - y_value)) <= 0.05: #Creates an error region for the bot to stop in
            bot.stop() #If the bot comes within that range, it stops
            time.sleep(1)
            bot.rotate(5) #Bot rotates 15 degrees to fix angle of hopper
            break
    t_count += 1 #adds one to t_count so the container on the table is picked up first

    
#---------------------------------------------------------------------------------
# STUDENT CODE ENDS
#---------------------------------------------------------------------------------
