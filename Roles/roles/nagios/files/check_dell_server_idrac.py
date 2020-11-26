#!/usr/bin/python


# 2017-06-29 first version
# Author: DiXingYu

    #1,2  => $UNKNOWN,
      #3    => $OK,
      #4    => $WARNING,
      #5,6  => $CRITICAL,


import sys
import getopt
import netsnmp
import time
import Queue

WarningNum = int(0)
CriticalNum = int(0)
detail_option = int(0)
date_option = int(0)
date_output = []


opts, args = getopt.getopt(sys.argv[1:], 'H:C:',  
                           [ 
                               'host=',
                               'community=', 
                               'help',
                               'detail',
                               'date' 
                           ] 
                           ) 

for option, value in opts: 
    if option in ['--help']: 
        print """ 
    usage:%s -H host ip address -C snmpv2 community 
    """ 
        sys.exit()

    elif option in ['--detail']:
        detail_option = int(1)

    elif option in ['--date']:
        date_option = int(1)

    elif option in ['--host', '-H']: 
        hosts = value

    elif option in ['--community', '-C']: 
        communitys = value



###################################
#3. Memory Detail---Size
###################################
def Memory_Size_Check():
    memory_size_oid = str(".1.3.6.1.4.1.674.10892.5.4.1100.50.1.14.1.")
    total_memory_size = int(0)
    for i in range(1,32):
        memory_size_suboid = memory_size_oid + str(i)
        try:
            memory_size = netsnmp.snmpget(netsnmp.Varbind(memory_size_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
            total_memory_size = total_memory_size + int(memory_size[0])/1000000
        except TypeError:
             break    
    print "Total Memory size: "+str(total_memory_size)+str('GB,')


###################################
#4. Check Physical Disk 
###################################
def PhyDisk_Status():
    phydisk_name_oid = str(".1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.55.")
    phydisk_status_oid = str(".1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.24.")
    phydisk_problem_list = []
    phydisk_name_list = []
    phydisk_status_list = []
    phydisk_status_dict = {}

    for i in range(1,24):
        phydisk_name_suboid = phydisk_name_oid + str(i)
        phydisk_name = netsnmp.snmpget(netsnmp.Varbind(phydisk_name_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(phydisk_name[0]) != str("None"):
            phydisk_name_list.append(phydisk_name[0])
        else:
            break

    for i in range(1,24):
        phydisk_status_suboid = phydisk_status_oid + str(i)
        phydisk_status = netsnmp.snmpget(netsnmp.Varbind(phydisk_status_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(phydisk_status[0]) != str("None"):
            phydisk_status_list.append(phydisk_status[0])
        else:
            break

    phydisk_status_dict = dict(zip(phydisk_name_list,phydisk_status_list))
    
    for (k,i) in phydisk_status_dict.items():    
        if i[0] != str(3):
            phydisk_problem_list.append(k)

    if len(phydisk_problem_list) == 0:
        print "Physical Disk number %d"%int(len(phydisk_name_list))+" is OK,",
    else:
        WarningNum = WarningNum + 1
        for i in phydisk_problem_list:
          print i,
        print "is Problem,",


###################################
#5. Check Virtual Disk 
###################################
def VirDisk_Status():
    virdisk_status_oid = str(".1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.20.")
    virdisk_name_oid = str(".1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.36.")
    virdisk_name_list = []
    virdisk_status_list= []
    virdisk_problem_list = []
    virdisk_status_dict = {}

    for i in range(1,8):
        virdisk_status_suboid = virdisk_status_oid + str(i)
        virdisk_status = netsnmp.snmpget(netsnmp.Varbind(virdisk_status_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(virdisk_status[0]) != str("None"):
            virdisk_status_list.append(virdisk_status[0])
        else:
            break

    for i in range(1,8):
        virdisk_name_suboid = virdisk_name_oid + str(i)
        virdisk_name = netsnmp.snmpget(netsnmp.Varbind(virdisk_name_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(virdisk_name[0]) != str("None"):
            virdisk_name_list.append(virdisk_name[0])
        else:
            break

    virdisk_status_dict = dict(zip(virdisk_name_list,virdisk_status_list))

    for (k,i) in virdisk_status_dict.items():    
        if i[0] != str(3):
            virdisk_problem_list.append(k)


    if len(virdisk_problem_list) == 0:
        print "All VirDisk is OK,",
    else:
        for i in virdisk_problem_list:
          print i,
        print "is problem,",


###################################
#6. Battery Detail
###################################
def Battery_Status():

    battery_location_oid = str(".1.3.6.1.4.1.674.10892.5.4.600.50.1.7.1.")
    battery_status_oid = str(".1.3.6.1.4.1.674.10892.5.4.600.50.1.5.1.")
    battery_location_list = []
    battery_status_list = []
    battery_problem_list = []
    battery_status_dict = {}

    for i in range(1,8):
        battery_location_suboid = battery_location_oid + str(i)
        battery_location = netsnmp.snmpget(netsnmp.Varbind(battery_location_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(battery_location[0]) != str("None"):
            battery_location_list.append(battery_location[0])
        else:
            break

    for i in range(1,8):
        battery_status_suboid = battery_status_oid + str(i)
        battery_status = netsnmp.snmpget(netsnmp.Varbind(battery_status_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(battery_status[0]) != str("None"):
            battery_status_list.append(str(battery_status[0]))
        else:
            break

    battery_status_dict = dict(zip(battery_location_list,battery_status_list))

    for (k,i) in battery_status_dict.items():    
        if i[0] != str(3):
            battery_problem_list.append(k)

    if len(battery_problem_list) == 0:
        print "Battery is OK,",

    else:
        for i in battery_problem_list:
          print i,
        print "is problem,",



###################################
#7. Power Supply Detail
###################################
def Power_Supply_Status():

    global date_output

    ps_name_oid = str(".1.3.6.1.4.1.674.10892.5.4.600.12.1.15.1.")
    ps_status_oid = str(".1.3.6.1.4.1.674.10892.5.4.600.12.1.11.1.")
    ps_involtage_oid = str(".1.3.6.1.4.1.674.10892.5.4.600.20.1.6.1.")

    ps_name_list = []
    ps_status_list = []
    ps_involtage_list = []
    ps_problem_list = []
    ps_status_dict = {}

    for i in range(1,6):
        ps_name_suboid = ps_name_oid + str(i)
        ps_name = netsnmp.snmpget(netsnmp.Varbind(ps_name_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(ps_name[0]) != str("None"):
            ps_name_list.append(ps_name[0])
        else:
            break
    
    for i in range(1,6):
        ps_status_suboid = ps_status_oid + str(i)
        ps_status = netsnmp.snmpget(netsnmp.Varbind(ps_status_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(ps_status[0]) != str("None"):
            ps_status_list.append(ps_status[0])
        else:
            break

    for i in range (26,40):
        ps_involtage_suboid = ps_involtage_oid + str(i)
        ps_involtage = netsnmp.snmpget(netsnmp.Varbind(ps_involtage_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(ps_involtage[0]) != str("None"):
            ps_involtage_list.append(int(ps_involtage[0])/1000)
        else:
            continue 

    ps_num = len(ps_name_list)


    for i in range(0,ps_num):
        ps_status_dict.setdefault(ps_name_list[i],[]).append(ps_status_list[i])
        ps_status_dict.setdefault(ps_name_list[i],[]).append(ps_involtage_list[i])

#PS_Presence_Detected = int(1)
#PS_Failure_Detected = int(2)
#PS_Predictive_Failure = int(4)
#PS_AC_Lost = int(8)
#PS_AC_Lost_Out_of_Range = int(16)
#PS_AC_Out_of_Range_but_Present = int(32)
#PS_Configuration_Error = int(64)

    for (k,i) in ps_status_dict.items():    
        if i[0] != str(1):
            ps_problem_list.append(k)

    if len(ps_problem_list) == 0:
        print "All Power Supply is OK,",
        for i in range(0,ps_num):
          print ps_name_list[i],"involtage:%dV,"%int(ps_involtage_list[i]),
          date_output.append(ps_name_list[i]+" involtage=%dV,"%int(ps_involtage_list[i]))


    else:
        CriticalNum = CriticalNum + 1
        for i in range(0,len(ps_problem_list)):
            print ps_problem_list[i],
        print "is Critical ",
        for i in range(0,ps_num):
          print ps_name_list[i],"involtage:%dV,"%int(ps_involtage_list[i]),
          date_output.append(ps_name_list[i]+" involtage=%dV,"%int(ps_involtage_list[i]))



###################################
#8. Fan Detail
###################################
def Fan_Status():
    global date_output

    fan_name_oid = str(".1.3.6.1.4.1.674.10892.5.4.700.12.1.8.1.")
    fan_status_oid = str(".1.3.6.1.4.1.674.10892.5.4.700.12.1.5.1.")
    fan_speed_oid = str(".1.3.6.1.4.1.674.10892.5.4.700.12.1.6.1.")
    fan_problem_list = []
    fan_name_list = []
    fan_status_list = []
    fan_speed_list = []
    fan_status_dict = {}  

    for i in range(1,12):
        fan_name_suboid = fan_name_oid + str(i)
        fan_name = netsnmp.snmpget(netsnmp.Varbind(fan_name_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(fan_name[0]) != str("None"):
            fan_name_list.append(fan_name[0])
        else:
            break
    
    for i in range(1,12):
        fan_status_suboid = fan_status_oid + str(i)
        fan_status = netsnmp.snmpget(netsnmp.Varbind(fan_status_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(fan_status[0]) != str("None"):
            fan_status_list.append(fan_status[0])
        else:
            break

    for i in range(1,12):
        fan_speed_suboid = fan_speed_oid + str(i)
        fan_speed = netsnmp.snmpget(netsnmp.Varbind(fan_speed_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(fan_speed[0]) != str("None"):
            fan_speed_list.append(fan_speed[0])
        else:
            break        
            
    fan_num = len(fan_name_list)

    for i in range(0,fan_num):
        fan_status_dict.setdefault(fan_name_list[i],[]).append(fan_status_list[i])
        fan_status_dict.setdefault(fan_name_list[i],[]).append(fan_speed_list[i])

    for (k,i) in fan_status_dict.items():    
        if i[0] != str(3):
            fan_problem_list.append(k)

    if len(fan_problem_list) == 0:
        print "Fan OK,",
        for i in range(0,fan_num):
          print fan_name_list[i],"speed:%dRPM,"%int(fan_speed_list[i]),
          date_output.append(fan_name_list[i]+" speed=%dRPM,"%int(fan_speed_list[i]))

    else:
        print "Fan Warning,",
        for i in range(0,len(fan_problem_list)):
            print fan_problem_list[i],
        print "is Problem ",
        for i in range(0,fan_num):
          print fan_name_list[i],"speed:%dRPM,"%int(fan_speed_list[i]),
          date_output.append(fan_name_list[i]+" speed=%dRPM,"%int(fan_speed_list[i]))


###################################
#9. Check Disk Controller
###################################
def Disk_Controller():
    disk_controller_name_list = []
    disk_controller_status_list = []
    problem_disk_controller_list = []
    disk_controller_status_Dict = {}

    disk_controller_name_oid = str(".1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.2.")
    for i in range(1,4):
        disk_controller_name_suboid = disk_controller_name_oid + str(i)
        disk_controller_name = netsnmp.snmpget(netsnmp.Varbind(disk_controller_name_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(disk_controller_name[0]) != str("None"):
            disk_controller_name_list.append(disk_controller_name[0])
        else:
            break

    disk_controller_status_oid = str(".1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.38.")
    for i in range(1,4):
        disk_controller_status_suboid = disk_controller_status_oid + str(i)
        disk_controller_status = netsnmp.snmpget(netsnmp.Varbind(disk_controller_status_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(disk_controller_status[0]) != str("None"):
            disk_controller_status_list.append(disk_controller_status[0])
        else:
            break

    disk_controller_status_Dict = dict(zip(disk_controller_name_list,disk_controller_status_list))

    for (k,i) in disk_controller_status_Dict.items():    
        if i != str(3):
            problem_disk_controller_list.append(k)

    if len(problem_disk_controller_list) == 0:
        for i in disk_controller_name_list:
            print i,
        print "is OK,",

    else:
        for i in problem_disk_controller_list:
            print i,
        print "is problem,",


###################################
#10. Temperature Celsius
###################################
def Temperature_Status():

    global date_output

    temperature_name_list = []
    temperature_Celsius_list = []
    temperature_status_list =[]
    temperature_problem_list = []
    temperature_status_Dict = {}

    temperature_name_oid = str(".1.3.6.1.4.1.674.10892.5.4.700.20.1.8.1.")
    for i in range(1,9):
        temperature_name_suboid = temperature_name_oid + str(i)
        temperature_name = netsnmp.snmpget(netsnmp.Varbind(temperature_name_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(temperature_name[0]) != str("None"):
            temperature_name_list.append(temperature_name[0])
        else:
            break

    temperature_status_oid = str(".1.3.6.1.4.1.674.10892.5.4.700.20.1.5.1.")
    for i in range(1,9):
        temperature_status_suboid = temperature_status_oid + str(i)
        temperature_status = netsnmp.snmpget(netsnmp.Varbind(temperature_status_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(temperature_status[0]) != str("None"):
            temperature_status_list.append(temperature_status[0])
        else:
            break

    temperature_Celsius_oid = str(".1.3.6.1.4.1.674.10892.5.4.700.20.1.6.1.")
    for i in range(1,9):
        temperature_Celsius_suboid = temperature_Celsius_oid + str(i)
        temperature_Celsius = netsnmp.snmpget(netsnmp.Varbind(temperature_Celsius_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
        if str(temperature_Celsius[0]) != str("None"):
            temperature_Celsius_list.append(float(temperature_Celsius[0])/10)
        else:
            break

    for i in range(0,len(temperature_name_list)):
        temperature_status_Dict.setdefault(temperature_name_list[i],[]).append(temperature_status_list[i])
        temperature_status_Dict.setdefault(temperature_name_list[i],[]).append(temperature_Celsius_list[i])

    for (k,i) in temperature_status_Dict.items():    
        if i[0] != str(3):
            temperature_problem_list.append(k)

    if len(temperature_problem_list) == 0:
        print "Temperature OK,",
        for i in range(0,len(temperature_name_list)):
            print temperature_name_list[i],"temp:%.1fC,"%float(temperature_Celsius_list[i]),
            date_output.append(temperature_name_list[i]+" temp=%.1fC,"%float(temperature_Celsius_list[i]))

    else:
        print "Temperature Warning,",
        for i in range(0,len(temperature_problem_list)):
            print temperature_problem_list[i],
        print "is Problem,",
        for i in range(0,len(temperature_name_list)):
            print temperature_name_list[i],"temp:%.1fC,"%float(temperature_Celsius_list[i]),
            date_output.append(temperature_name_list[i]+" temp=%.1fC,"%float(temperature_Celsius_list[i]))


###################################
#1. Device Info
###################################

server_name = str(netsnmp.snmpget(netsnmp.Varbind('.1.3.6.1.4.1.674.10892.5.1.3.12.0'),Version = 2,DestHost=(hosts),Community=(communitys))[0])
server_tag = str(netsnmp.snmpget(netsnmp.Varbind('.1.3.6.1.4.1.674.10892.5.1.3.18.0'),Version = 2,DestHost=(hosts),Community=(communitys))[0])
software_version = str(netsnmp.snmpget(netsnmp.Varbind('.1.3.6.1.4.1.674.10892.5.1.3.6.0'),Version = 2,DestHost=(hosts),Community=(communitys))[0])

###################################
#2. Check CPU
###################################
CPU_status = netsnmp.snmpget(netsnmp.Varbind('.1.3.6.1.4.1.674.10892.5.4.200.10.1.50.1'),Version = 2,DestHost=(hosts),Community=(communitys))

CPU_ok = int(3)
CPU_warn = int(4)
CPU_crit_1 = int(5)
CPU_crit_2 = int(6)

if int(CPU_status[0]) == CPU_ok:
    CPU_output = str("CPU is OK,")

elif int(CPU_status[0]) == CPU_warn:
    CPU_output = str("CPU is Warning,")
    WarningNum = WarningNum + 1

else:
    CPU_output = str("CPU is Critical,")
    CriticalNum = CriticalNum + 1


###################################
#3. Check Memory
###################################
memory_status = netsnmp.snmpget(netsnmp.Varbind('.1.3.6.1.4.1.674.10892.5.4.200.10.1.27.1'),Version = 2,DestHost=(hosts),Community=(communitys))

memory_ok = int(3)
memory_warn = int(4)
memory_crit_1 = int(5)
memory_crit_2 = int(6)

if int(memory_status[0]) == memory_ok:
    memory_output = str("Memory is OK,")

elif int(memory_status[0]) == memory_warn:
    memory_output = str("Memory is Warning,")
    WarningNum = WarningNum + 1

else:
    memory_output = str("Memory is Critical,")
    CriticalNum = CriticalNum + 1


###################################
#4. Check Physical Disk 
###################################
phydisk_status_oid = str(".1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.24.")

for i in range(1,24):
    phydisk_status_suboid = phydisk_status_oid + str(i)
    phydisk_status = netsnmp.snmpget(netsnmp.Varbind(phydisk_status_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
    try:
       if int(phydisk_status[0]) != int(3):
           WarningNum = WarningNum + 1
    except TypeError:
       break


###################################
#5. Check Virtual Disk 
###################################
virdisk_status_oid = str(".1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.20.")


for i in range(1,8):
    virdisk_status_suboid = virdisk_status_oid + str(i)
    virdisk_status = netsnmp.snmpget(netsnmp.Varbind(virdisk_status_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
    try:
       if int(virdisk_status[0]) != int(3):
           WarningNum = WarningNum + 1
    except TypeError:
       break


###################################
#6. Check Battery
###################################
battery_status = netsnmp.snmpget(netsnmp.Varbind('.1.3.6.1.4.1.674.10892.5.4.200.10.1.52.1'),Version = 2,DestHost=(hosts),Community=(communitys))

#battery_ok = int(3)
#battery_absent = int(0)
#battery_Predictive_Failure = int(1)
#battery_failed = int(2)
#battery_Presence_Detected = int(4)

if int(battery_status[0]) == int(3):
    battery_output = str("All Bettery is OK,")

elif int(battery_status[0]) != int(3):
    battery_output = str("Battery is Warning,")
    WarningNum = WarningNum + 1


###################################
#7. Check Power Supply
###################################
powersupply_status = netsnmp.snmpget(netsnmp.Varbind('.1.3.6.1.4.1.674.10892.5.4.200.10.1.9.1'),Version = 2,DestHost=(hosts),Community=(communitys))

if int(powersupply_status[0]) == int(3):
    power_output = str("All Power Supply is OK,")

else:
    power_output = str("Power Supply is Critical,")
    CriticalNum = CriticalNum + 1



###################################
#8. Check Fan
###################################
fan_status = netsnmp.snmpget(netsnmp.Varbind('.1.3.6.1.4.1.674.10892.5.4.200.10.1.21.1'),Version = 2,DestHost=(hosts),Community=(communitys))

if str(fan_status[0]) == str("None"):
    fan_output = str("The Server not support Fan oid,")

elif int(fan_status[0]) == int(3):
    fan_output = str( "All Fan is OK,")


elif int(fan_status[0]) != int(3):
    fan_output = str("Fan is Warning,")
    WarningNum = WarningNum + 1


###################################
#9. Check Disk Controller
###################################
disk_controller_status_oid = str(".1.3.6.1.4.1.674.10892.5.5.1.20.130.1.1.38.")
for i in range(1,4):
    disk_controller_status_suboid = disk_controller_status_oid + str(i)
    disk_controller_status = netsnmp.snmpget(netsnmp.Varbind(disk_controller_status_suboid),Version = 2,DestHost=(hosts),Community=(communitys))
    try:
       if int(disk_controller_status[0]) != int(3):
           WarningNum = WarningNum + 1
    except TypeError:
       break


###################################
#10. Check Temperature
###################################
temperature_status = netsnmp.snmpget(netsnmp.Varbind('.1.3.6.1.4.1.674.10892.5.4.200.10.1.24.1'),Version = 2,DestHost=(hosts),Community=(communitys))

if int(temperature_status[0]) == int(3):
    temperature_output = str("Temperature is OK,")


elif int(temperature_status[0]) != int(3):
    temperature_output = str("Temperature is warning,")
    WarningNum = WarningNum + 1



###################################
#Status Output
###################################
if CriticalNum != int(0):
    print "Critical:","Name:"+server_name,"SerTag:"+server_tag,"Oper:"+software_version,
elif int(WarningNum) != int(0):
    print "Warning:","Name:"+server_name,"SerTag:"+server_tag,"Oper:"+software_version,
else:
    print "OK:","Name:"+server_name,"SerTag:"+server_tag,"Oper:"+software_version,
    

###################################
#Date Output
###################################
#2 CPU
    print CPU_output,
#3 Memory
    print memory_output,
    if detail_option == int(1):
        Memory_Size_Check()
#4 Phy Disk
    PhyDisk_Status()
#5 Vir Disk
    VirDisk_Status()
#6 Battery
    if detail_option == int(1):
        Battery_Status()
    else:
        print battery_output,
#7 Power
    if detail_option == int(1):
        Power_Supply_Status()  
    else: 
        print power_output,
#8 Fan
    if str(fan_status[0]) == str("None") and detail_option == int(1):
       print fan_output,
    elif detail_option == int(1):
        Fan_Status()
    else:
        print fan_output,
#9 Disk
    Disk_Controller()
#10 Temperature
    if detail_option == int(1):
        Temperature_Status()
    else:
        print temperature_output


#####################
#Nagios Data
#####################
if date_option == int(1):
    print "|",
    for i in range(0,len(date_output)):
        print date_output[i],


#######################
#Exit
#######################
if CriticalNum != int(0):
    sys.exit(2)

elif WarningNum != int(0):
    sys.exit(1)

else:
    sys.exit(0)