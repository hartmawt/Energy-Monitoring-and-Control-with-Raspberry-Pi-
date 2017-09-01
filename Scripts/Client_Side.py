#JMU 2017 Energy Monitoring & Control Senior Capstone
#Author Tyler Hartman

import RPi.GPIO as GPIO
import time
from socket import *
from phpserialize import *
import Adafruit_ADS1x15
import mysql.connector
from datetime import datetime

#db connection inputs w/ ssl
db = {'user': 'back1', 'password': 'backpack',
      'host': 'smartroom.czjl1dned5qh.us-west-2.rds.amazonaws.com',
      'database': 'SMARTRoom', 'ssl_ca': '/home/PL_Unit2/Documents/Scripts/rds-ca-2015-us-west-2.pem',
      }

#GPIO pin assignment
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(13, GPIO.OUT)

#ADC Settings
adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

#Initial Check Back
conn = mysql.connector.connect(**db)
cursor = conn.cursor()
cursor.execute(("""SELECT component_status FROM Component WHERE component_id = '2'"""))
p_status = cursor.fetchone()
conn.commit()
cursor.close()

if p_status == ('ON'):
    GPIO.output(13, GPIO.HIGH)

elif p_status == ('OFF'):
    GPIO.output(13, GPIO.LOW)

#Socket

while 1:
    host = "34.208.206.63"
    port = 5001
    s = socket(AF_INET, SOCK_STREAM)
    total = 0
    
    try:
        s.connect((host, port))

    except:
        continue
    
    
    try:  
        raw_data = s.recv(1024)
        data = unserialize(raw_data)
        dict_list = []
        for key, value in data[1].items():
            dict_list.append([key, value])
        SD = (sorted(dict_list)[1][1])
        SD2 = (sorted(dict_list)[1][1])
        decoded = SD2.decode("utf-8")
        fmt = "%Y-%m-%d %H:%M:%S"
        date = datetime.strptime(decoded, fmt)
        print(data)
        print(date)

        dt = datetime.now(pytz.utc)
        today = dt.strftime(fmt)
        formatted_dt = datetime.strptime(today, fmt)
        print(formatted_dt)

        diff = (formatted_dt - date)
        print(diff.seconds)

        if diff.seconds > 8:
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()
            cursor.execute(("""UPDATE Component SET Comp_Check = 'W' WHERE component_id = '2'"""))
            conn.commit()
            cursor.close()
            conn.close()
            print("T")
            continue
        
        else:
            if SD == (b'ON'):
                GPIO.output(13, GPIO.HIGH)

            elif SD == (b'OFF'):
                GPIO.output(13, GPIO.LOW)
                
            time.sleep(23)
            
            for a in range(9):
                adc.start_adc(0, gain=GAIN)
                cal_factor = 0.0094
                offset_factor = 0.0185
                current = ((abs(adc.get_last_result())*cal_factor)-offset_factor)
                #print('Current: {0}'.format(current))
                total = (total + current)
                adc.stop_adc()
            avg_total = (total / 10)
            #print(total)
            #print (avg_total)
            
            if (SD == (b'ON') and avg_total > 0.03):

                try:
                    conn = mysql.connector.connect(**db)
                    cursor = conn.cursor()
                    cursor.execute(("""UPDATE Component SET Comp_Check = 'S' WHERE component_id = '2'"""))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    #print("S")

                except:
                    print("Failure to connect. Attempting to retry...")
                    continue
                
            elif (SD == (b'ON') and avg_total < 0.03):

                try:
                    conn = mysql.connector.connect(**db)
                    cursor = conn.cursor()
                    cursor.execute(("""UPDATE Component SET Comp_Check = 'F' WHERE component_id = '2'"""))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    #print("F")

                except:
                    print("Failure to connect. Attempting to retry...")
                    continue
                
            elif(SD == (b'OFF') and avg_total < 0.03):

                try:
                    conn = mysql.connector.connect(**db)
                    cursor = conn.cursor()
                    cursor.execute(("""UPDATE Component SET Comp_Check = 'S' WHERE component_id = '2'"""))
                    conn.commit()
                    cursor.close()
                    conn.close()
                    #print("S")

                except:
                    print("Failure to connect. Attempting to retry...")
                    continue
                

    except:
        continue 
            

    
            

