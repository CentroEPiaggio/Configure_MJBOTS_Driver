


echo "welcome in MJBOTS driver confguration sript"
#set up request varible
calib_req=0
config_req=0
flash_req=0
trans_req=0
transport=" "
target=" "

# get options
while getopts 'cfst:p:' opt
do 
case $opt in
    c) echo "calibration requested"
       calib_req=1
       ;;
    f) echo "flashing firmware requested" 
       flash_req=1
       ;;
    s) echo "set up configuration resquested" 
       config_req=1
       ;;
    t) echo "targets $OPTARG" 
       targets=$OPTARG
       ;;
    p) echo "pi3hat trasnport requested with $OPTARG"
       transport=$OPTARG
       trans_req=1
       ;;
esac
done

#ask to be selected command
echo "are you sure about options?[y/n]"
read sure

if [ "$sure" == "n" ]; then
    echo "interrupt script"
    exit 0
fi
if [ "$targets" = " " ]; then
    echo "ERROR no target provided"
    exit 1
fi
if [ $trans_req == 1 ]; then
    if [ "$transport" == " " ]; then
        echo "ERROR pi3hat config syntax not correct"
        exit 1
    fi    
fi


declare -i ind=0
declare -i choise

#manage firmware flash
if [ $flash_req == 1 ]; then
    cd Firmware_Version
    fw_v=()
    for ver in *
    do
        fw_v+=($ver)
        echo "$ind : $ver"
        ind+=1
    done
    echo ""
    echo "choose a version inputting the right integer number"
    read choise
    echo ""
    if [ $choise -lt 0 ] ;
    then 
        echo "index out of range"
        exit 1
    else
        if [ $choise -gt $ind ];
        then 
            echo "index out of range"
            exit 1
        fi
    fi
    version="${fw_v[$choise]}"
    cd $version
    elf_name=(*)
    echo "$elf_name"
    echo "python3 -m moteus.moteus_tool --target $targets $elf_name"
    python3 ../../prova.py -target $targets $elf_name
    cd ../..
    
fi

if [ $config_req == 1 ]; then
    cd Configuration_FIle
    ind=0
    cfg_v=()
    for cfg in *
    do
        cfg_v+=($cfg)
        echo "$ind : $cfg"
        ind+=1
    done
    echo ""
    echo "choose a configuration file to setup the drivers inputting the right integer number"
    read choise
    echo ""
    if [ $choise -lt 0 ] ;
    then 
        echo "index out of range"
        exit 1
    else
        if [ $choise -gt $ind ];
        then 
            echo "index out of range"
            exit 1
        fi
    fi
    version="${fw_v[$choise]}"
    cfg_name=(*)
    echo "$cfg_name"
    echo "$transport"
    echo "python3 -m moteus.moteus_tool --target $targets $cfg_name -pi3hat-cfg $transport"
    cd ..
    python3 prova.py -target $targets $cfg_name -pi3hat-cfg $transport
fi

if [ $config_req == 1 ]; then 
    echo "python3 -m moteus.moteus_tool --target $targets $cfg_name -pi3hat-cfg $transport --calibrate"
    
    python3 prova.py -target $targets $cfg_name -pi3hat-cfg $transport --calibrate
fi