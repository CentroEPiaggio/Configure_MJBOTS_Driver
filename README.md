# Configure_MJBOTS_Driver
## Introduction
This repository provide a bash script to execute the basic operation to use a MJBOTS Driver, the features provided are:
<ol>
  <li> Flash the Driver Firmware</li>
  <li> Set up the Driver configuration file</li>
  <li> Calibrate the driver</li>
  <li> Get Information about each driver  </li>
  <li> Set Python Interpreter  </li>
  <li> Set Transport Pi3Hat  </li>
</ol>

## Firmware Version and Configuration File
The repo provide two folders contain the available option to both flash and set up the driver. The **Firmware_version** folder must contain a folder with the id of the firmware version, for example the realase data. The subfolder must contains the firmware elf file.
The **Configuration_FIle** folder contains the different configuration file. Each of them must contain the list of **conf set** command to set up a desired dirver paramters list and the **conf write** at the end if this parameter should be reload at dirver switch on.

## Usage
Open a terminal in the repository's folder and call the bash script **sudo bash configure_MJBOTS_driver.sh [- opt arg]**. the options are:
<ul>
  <li>targets option is necessary to choose the targets of the disired operation, the option is -t followed by the list of ids delimited by ','. For example if the target motor have ids 1,2,3 the option syntax is -t 1,2,3</li>
  <li>transport option is necessary to choose the bus and the connected driver id of the disired operation, the option is -p followed by the list the list of channel sperated by ";", each channel is -bus_id-=-list of id separeted by ','- . For example if the bus are 1 and 2 are connect with motors having respectively ids 1,2,3 and 4,5,6 the option syntax is -p 1=1,2,3;2=4,5,6</li>
  <li> Flash option is enable by using the option -f without arguments and will schedule the flashing process into the script. The user can choose the desired version between the provided ones</li>
  <li> Configuration option is enable by using the option -s without arguments, it will schedule the configuretion process into the script.The user can choose the desired configuration file between the provided ones  </li>
  <li>Calibration option is enable by using the option -c without arguments and will schedule the calibration process into the script.</li>
  <li>Info option is enable by using the option -i without arguments and will schedule the calibration process into the script.</li> 
  <li>Python Interpreter version can be set by using the option -v following by the intepreter global path. NB for internal the Mulinex Raspberry are setted up with the correct python intepreter in the folder "../mul_env/bin/python3"</li>
</ul>


## Example 

### Info Request to motor  with Pi3hat on channel 

```sudo bash configure_MJBOTS_driver.sh -t <-motor id-> -p "<-pi3hat-bus->=<-motor id->" -v ../mul_env/bin/python3 -i```

For instance, if we want to send info request to a kinematic chain composed by 3 motor, with id 4,5 and 6, connected to the bus 1 then the command is:

```sudo bash configure_MJBOTS_driver.sh -t 4,5,6 -p "1=4,5,6" -v ../mul_env/bin/python3 -i```

if we immagine to add another 2 motor kinematic chain, with id 8,9, to the bus 2:

```sudo bash configure_MJBOTS_driver.sh -t 4,5,6,8,9 -p "1=4,5,6;2=8,9" -v ../mul_env/bin/python3 -i```


### MJBOT driver complete set up

```sudo bash configure_MJBOTS_driver.sh -t <-motor id-> -p "<-pi3hat-bus->=<-motor id->" -v ../mul_env/bin/python3 -c -s -f```

For instance, if we want to send info request to a kinematic chain composed by 3 motor, with id 4,5 and 6, connected to the bus 1 then the command is:

```sudo bash configure_MJBOTS_driver.sh -t 4,5,6 -p "1=4,5,6" -v ../mul_env/bin/python3  -c -s -f```

if we immagine to add another 2 motor kinematic chain, with id 8,9, to the bus 2:

```sudo bash configure_MJBOTS_driver.sh -t 4,5,6,8,9 -p "1=4,5,6;2=8,9" -v ../mul_env/bin/python3 -c -s -f```

