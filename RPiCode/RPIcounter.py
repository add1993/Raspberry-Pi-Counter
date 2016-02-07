import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)         #Read output from IR motion sensor
GPIO.setup(11, GPIO.IN)         #Read output from IR motion sensor

count = 0;
while True:
       k=GPIO.input(11)
       i=GPIO.input(7)
       if k and i:
                continue
       j=0
       #i=GPIO.input(7)
       if k==1:                 #When output from 1st motion sensor is HIGH
                 t_end=time.time()+2  #2 Second window for detection
                 while time.time()<t_end:
                       j=GPIO.input(7)
                       if j==1:                 #When output from 2nd motion sensor is HIGH
                                count=count-1
                                time.sleep(1)
                                break
                 print "Intruders decrese",count

                 time.sleep(0.1)

       elif i==1:              #When output from 2nd motion sensor is HIGH
                 t_end=time.time()+2   #2 Second window for detection
                 while time.time()<t_end:
                       j=GPIO.input(11)
                       if j==1:                 #When output from 1st motion sensor is HIGH
                                count=count+1
                                time.sleep(1)
                                break
                 print "Intruders increase",count

                 time.sleep(0.1)
