#JMU 2017 Energy Monitoring & Control Senior Capstone
#Author Tyler Hartman

import time
import Adafruit_ADS1x15

#Define ADC
adc = Adafruit_ADS1x15.ADS1115()
#Set Gain
GAIN = 1
#Main Loop
while True:
    sum = 0
    sum_pwr = 0
    print('Reading ADS1x15 Channel 1...')
    #Minute Loop
    for i in range (100):
        adc.start_adc(0, gain=GAIN)
        current = (abs(adc.get_last_result()))
        print('Current: {0}'.format(current))
        sum = sum + current
        time.sleep(.01)
        adc.stop_adc()
    #Average Total Current / Minute
    avg = abs(sum / i)
    #Average Total Power (watts) / Minute
    pwr = abs(avg * 120)
    time.sleep(.5)
    print ('Average Current =',avg)
    time.sleep(15)
