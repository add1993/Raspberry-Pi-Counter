import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)         #Read output from IR motion sensor
GPIO.setup(11, GPIO.IN)         #Read output from IR motion sensor

count = 0       #Total count of persons
both_high = 0   #Flag equals 1 when both sensors in HIGH state
isIncreased = 0         #Flag equals 1 when count increased
isDecreased = 0         #Flag equals 1 when count decreased

while True:
       k=GPIO.input(11)
       i=GPIO.input(7)

       if both_high:
                if k==0 and isIncreased:
                        count = count-1
                        print "Intruders decrease(Both sensors were blocked) =",count
                        time.sleep(.5)

                if i==0 and isDecreased:
                        count = count+1
                        print "Intruders increase(Both sensors were blocked) =",count
                        time.sleep(.5)

       if k and i:      #If both sensor values HIGH then check the values again
                both_high = 1
                continue

       j=0
       both_high = 0
       isIncreased = 0
       isDecreased = 0

       #i=GPIO.input(7)
       if k==1:                 #When output from 1st motion sensor is LOW
                 t_end=time.time()+2
                 while time.time()<t_end:
                       j=GPIO.input(7)
                       if j==1:                 #When output from 2nd motion sensor is LOW
                                count=count-1
                                isDecreased = 1
                                time.sleep(.5)
                                break

                 if isDecreased:
                        print "Intruders decrease =",count

                 time.sleep(0.1)

       elif i==1:              #When output from 2nd motion sensor is HIGH
                 t_end=time.time()+2
                 while time.time()<t_end:
                       j=GPIO.input(11)
                       if j==1:                 #When output from 1st motion sensor is LOW
                                count=count+1
                                isIncreased = 1
                                time.sleep(.5)
                                break

                 if isIncreased:
                        print "Intruders increase =",count

                 time.sleep(0.1)
                                           