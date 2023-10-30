


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
    c) 
        echo "calibration requested"
        echo " "
        calib_req=1
        ;;
    f) 
        echo "flashing firmware requested" 
        flash_req=1
        ;;
    s)  echo "set up configuration resquested" 
        echo " "
        config_req=1
        ;;
    t)
        echo "targets $OPTARG" 
        echo " "
        targets=$OPTARG
        ;;
    p) 
        echo "pi3hat trasnport requested with $OPTARG"
        echo " "
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
    cd ../..
    command_req="python3 -m moteus.moteus_tool --target $targets --flash $elf_name"
     
    if [ $trans_req == 1 ]; then
        python3 prova.py --target $targets --flash $elf_name --pi3hat-cfg $transport
    else 
        python3 prova.py --target $targets --flash $elf_name
    fi
    echo "$command_req"
    
    
    
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
    cfg_name="${cfg_v[$choise]}"
    cd ..
    ls
    command_req="python3 -m moteus.moteus_tool --target $targets --write-config $cfg_name"
    
    if [ $trans_req == 1 ]; then
        command_req+=" --pi3hat-cfg $transport"
        python3 prova.py --target $targets --write-config $cfg_name --pi3hat-cfg $transport
    else    
        python3 prova.py --target $targets --write-config $cfg_name
    fi
    echo "$command_req"
    
fi

if [ $calib_req == 1 ]; then 
    command_req="python3 -m moteus.moteus_tool --target $targets --calibrate"
    if [ $trans_req == 1 ]; then
        command_req+=" --pi3hat-cfg $transport"
        python3 prova.py --target $targets --calibrate --pi3hat-cfg $transport
    else
        python3 prova.py --target $targets --calibrate

    fi
    echo "$command_req"
fi