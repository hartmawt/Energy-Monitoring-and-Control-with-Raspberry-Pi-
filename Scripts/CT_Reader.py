#JMU 2017 Energy Monitoring & Control Senior Capstone
#Author Tyler Hartman

import psutil
import time
import pytz
from datetime import datetime
import Adafruit_ADS1x15

#Define ADC
adc = Adafruit_ADS1x15.ADS1115()
#Set Gain
GAIN = 1
#Main Loop
while True:
    #Hour Loop
    sum_pwr = 0
    for e in range (60):
        sum = 0
        #Minute Loop
        for i in range (599):
            adc.start_adc(0, gain=GAIN)
            cal_factor = 0.0092
            offset_factor = 0.0189
            current = ((abs(adc.get_last_result())*cal_factor)-offset_factor)
            #print('Current: {0}'.format(current))
            sum = sum + current
            time.sleep(0.084)
            adc.stop_adc()
        #Average Total Current / Minute
        avg = abs(sum / 600)
        #Average Total Power (watts) / Minute
        pwr = abs(avg * 220)
        #Sum of Power / Hour
        sum_pwr = (sum_pwr + pwr)
    #Energy Consumption (kWh)
    eng = (str(sum_pwr / 1000) / 60)
    #Define Date
    dt = datetime.now(tz=pytz.timezone('America/Costa_Rica'))
    fmt = "%Y-%m-%d %H:%M:%S"
    today = dt.strftime(fmt)
    #Print to Local File (2 Files)
    free_space = psutil.disk_usage(".").free
    #Temp File
    with open('/home/PL_Unit2/Documents/Scripts/Energy_Logs/temp_eng.txt', 'a') as t:
        t.write("%s\n %s\n" % (eng, today))
    #Perm File
    if free_space > 200:
        with open('/home/PL_Unit2/Documents/Scripts/Energy_Logs/Eng_Conc_Per_Hour.txt', 'a') as f:
            f.write("%s\n %s %s\n" % (today, eng, "kWh"))
    elif free_space < 200:
        with open('/home/PL_Unit2/Documents/Scripts/Energy_Logs/Eng_Conc_Per_Hour.txt', 'w') as wr:
            wr.write("%s\n %s %s\n" % (today, eng, "kWh"))
    else:
        print("Error... please wait.")
        continue





    
