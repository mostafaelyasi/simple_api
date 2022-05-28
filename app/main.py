#main.py 
from fastapi import FastAPI 
from dmidecode import DMIDecode
import subprocess
import os 
app = FastAPI(title="Simple API") 

@app.get("/{item_id}") 
async def read_item(item_id: str): 
    result={}
    itemid = item_id.lower()
    host_name = ''
    dmi = DMIDecode()
    if os.path.exists('/host_name'):
      host_name = os.popen("cat /host_name").read().strip()
    if itemid == "meminfo" :
      total_memory = os.popen("cat /proc/meminfo | grep -i 'memtotal' | grep -o '[[:digit:]]*' ").read().strip()
      free_memory = os.popen("cat /proc/meminfo | grep -i 'memavailable' | grep -o '[[:digit:]]*' ").read().strip()
      result = {"Total Memory":total_memory,"Free Memory":free_memory}
    elif itemid == "hw" :
      bios_info = {'Manufacturer:': dmi.manufacturer(), \
              'Model:': dmi.model(), \
              'Firmware:': dmi.firmware(), \
              'Serial number:': dmi.serial_number(), \
              'Processor type:': dmi.cpu_type(), \
              'Number of CPUs:': dmi.cpu_num(), \
              'Cores count:': dmi.total_enabled_cores(), \
              'Total RAM:':'{} GB'.format(dmi.total_ram())}
      result = {"HW_Info from BIOS:":bios_info}
    elif itemid == "dmidecode":
      dmi_info = os.popen("dmidecode -t 0").readlines()
      list_info = []
      for line in dmi_info:
        list_info.append(line.strip())
      result = {"DMIDecode:":list_info}
    elif itemid == "ofh" :
      ofh_info = os.popen("cat /proc/sys/fs/file-max").read().strip()
      result = {"Maximum Open Files Limit:":ofh_info}
    return {"Info of {}".format(host_name):result}


