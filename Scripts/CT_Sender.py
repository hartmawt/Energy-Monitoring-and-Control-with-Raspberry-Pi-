#JMU 2017 Energy Monitoring & Control Senior Capstone
#Authors Tyler Hartman & Alex Hansen

import time
import mysql.connector

#mysql connection inputs w/ ssl
db = {'user': 'back1', 'password': 'backpack',
      'host': 'smartroom.czjl1dned5qh.us-west-2.rds.amazonaws.com',
      'database': 'SMARTRoom', 'ssl_ca': '/home/PL_Unit2/Documents/Scripts/rds-ca-2015-us-west-2.pem',
      }

while True:
    try:
        with open('/home/PL_Unit2/Documents/Scripts/Energy_Logs/temp_eng.txt') as t:
            temp_data = t.read()
            list_eng = []
            list_date = []
            td_list = [y for y in (x.strip() for x in temp_data.splitlines()) if y]
            td_array = [td_list[i:i+2] for i in range(0, len(td_list), 2)]
            for a in range(len(td_array)):
                list_eng.append(td_array[a][0])
                list_date.append(td_array[a][1])
            t.close()

        if len(td_list) == 0:
            print("No writeable data!")
            time.sleep(10)
            continue
        
        elif len(td_list) > 0:
            conn = mysql.connector.connect(**db)
            cursor = conn.cursor()
            for l in range(len(list_eng)):
                cursor.execute(("""INSERT INTO Energy_Consumption (component_id, energy_consumption_per_hour, time_recorded) VALUES (%s, %s, '%s') """) % \
                                (2, list_eng[l], list_date[l]))
            conn.commit()        
            cursor.close()
            conn.close()
            print("Success")
            d = open('/home/PL_Unit2/Documents/Scripts/Energy_Logs/temp_eng.txt', 'w')
            d.close()
            continue
    except:
        print("Failure.. attempting to reconnect.")
        time.sleep(5)
        continue

