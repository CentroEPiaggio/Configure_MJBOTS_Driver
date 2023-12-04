# Configure_MJBOTS_Driver
## Introduction
This repository provide a bash script to execute the basic operation to use a MJBOTS Driver, the features provided are:
<ol>
  <li> Flash the Driver Firmware</li>
  <li> Set up the Driver configuration file</li>
  <li> Calibrate the driver</li>
  <li> Get Information about each driver  </li>
</ol>

## Firmware Version and Configuration File
The repo provide two folders contain the available option to both flash and set up the driver. The **Firmware_version** folder must contain a folder with the id of the firmware version, for example the realase data. The subfolder must contains the firmware elf file.
The **Configuration_FIle** folder contains the different configuration file. Each of them must contain the list of **conf set** command to set up a desired dirver paramters list and the **conf write** at the end if this parameter should be reload at dirver switch on.

## Usage
Open a terminal in the repository's folder and call the bash script **bash configure_MJBOTS_driver.sh [- opt arg]**. the options are:
<ul>
  <li>targets option is necessary to choose the targets of the disired operation, the option is -t followed by the list of ids delimited by ','. For example if the target motor have ids 1,2,3 the option syntax is -t 1,2,3</li>
  <li> Flash option is enable by using the option -f without arguments and will schedule the flashing process into the script. The user can choose the desired version between the provided ones</li>
  <li> Configuration option is enable by using the option -s without arguments, it will schedule the configuretion process into the script.The user can choose the desired configuration file between the provided ones  </li>
  <li>Flash option is enable by using the option -c without arguments and will schedule the calibration process into the script.</li>
  <li>Info option is enable by using the option -i without arguments and will schedule the calibration process into the script.</li>
</ul>
