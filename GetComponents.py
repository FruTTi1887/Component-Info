import wmi
import math
import subprocess
import requests

TOKEN = "YOUR_BOT_TOKEN"
chat_id = "YOUR_CHAT_ID"


computer = wmi.WMI()
os_info = computer.Win32_OperatingSystem()[0]
proc_info = computer.Win32_Processor()[0]
gpu_info = computer.Win32_VideoController()[0]
disk_info = computer.Win32_DiskDrive()
system_ram = float(os_info.TotalVisibleMemorySize) / 1048576  # KB to GB
motherboard = computer.Win32_BaseBoard()[0].SerialNumber
man_moth_com = 'WMIC BASEBOARD GET Manufacturer /VALUE'.split()
manufacturer = str(subprocess.check_output(man_moth_com, shell=True)).split("\\n")[2].replace("\\r", "").\
    split("=")[1]
# print(manufacturer)
prod_moth_com = 'WMIC BASEBOARD GET Product /VALUE'.split()
product = str(subprocess.check_output(prod_moth_com, shell=True)).split("\\n")[2].replace("\\r", "").\
    split("=")[1]
# print(product)
CPU = ('CPU: {0}'.format(proc_info.Name))
RAM = ('RAM: {0} GB'.format(math.ceil(system_ram)))
GPU = ('Graphics Card: {0}'.format(gpu_info.Name))
# print(CPU), print(RAM), print(GPU)
for disk in computer.Win32_DiskDrive():
    disk_model = disk.Model
    disk_size = int(disk.Size) // 1000000000
# print(disk_model)
# print(disk_size)
Components = {
    'Производитель': manufacturer,
    'Модель': product,
    'Процессор': CPU,
    'Оперативная память': RAM,
    'Видеокарта': GPU,
    'Модель диска': disk_model,
    'Объем диска': disk_size
}

f = open('D:/TT/start_sklad.bat', 'r')
lines = f.readlines()[1:2]
for line in lines:
    ttname = line[147:-6]

message = ttname, Components
url = f"https://api.telegram.org/bot{
    TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
requests.get(url).json()
