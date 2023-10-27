import asyncio
import math
from moteus.moteus_tool import Stream
import sys
import os

async def main(args):
    
    #operation list 
    update = False
    calibrate = False
    set_SE = False
    change_id = False
    target_id = None
    count_arg = 0
    firm_ver = os.listdir("Firmware_version")
    #find arguments 
    for arg in args:

        if(arg.find("--update")!=-1):
            print("the provided firmware version are:")
            for i in range(len(firm_ver)):
                print(f"{i} :: {firm_ver[i]}")
            fv = input(f"choose the firmware version you want flash, in range [0,{len(firm_ver)}): ")
            print(fv)
        elif(arg.find("--t")!= -1):
            if(target_id == None):
                target_id = args[count_arg+1]
            print(f"the target id is: {target_id}")
        
        count_arg = count_arg + 1

            
    s = Stream(target_id= target_id)
    await s.info()
    # if(arg.find("--update")!=-1):
    #     print(os.listdir())
    #     input("choose the firmware version ")
    
  



if __name__ == '__main__':
    asyncio.run(main(sys.argv[1:]))
