import sys
import RPi.GPIO as GPIO
import time
import urllib2

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(7, GPIO.IN)         #Read output from IR motion sensor
GPIO.setup(11, GPIO.IN)         #Read output from IR motion sensor

def main():
        count = 0       #Total count of persons
        both_high = 0   #Flag equals 1 when both sensors in HIGH state
        isIncreased = 0         #Flag equals 1 when count increased
        isDecreased = 0         #Flag equals 1 when count decreased
        send_time=time.time()+5

        # use sys.argv if needed
        if len(sys.argv) < 2:
                print('Usage: python file.py PRIVATE_KEY')
                exit(0)
        else:
                baseURL = 'https://api.thingspeak.com/update?api_key=%s' % sys.argv[1]  #Base URL for pushing data to upstream

        print 'starting...'

        while True:
                k=GPIO.input(11)
                i=GPIO.input(7)

                if both_high:
                        if k==0 and isIncreased:
                                count = count-1
                                print "Intruders decrease(Both sensors were blocked) =",count
                                time.sleep(.2)

                        if i==0 and isDecreased:
                                count = count+1
                                print "Intruders increase(Both sensors were blocked) =",count
                                time.sleep(.2)

                        #if k==0 and isIncreased or i==0 and isDecreased:
                                #f = urllib2.urlopen(baseURL +"&field1=%s" % count)
                                #print f.read()
                                #f.close()


                if k and i:     #If both sensor values HIGH then check the values again
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
                                        time.sleep(.2)
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
                                        time.sleep(.2)
                                        break

                        if isIncreased:
                                print "Intruders increase =",count

                        time.sleep(0.1)

                if time.time()>=send_time:
                        f = urllib2.urlopen(baseURL +"&field1=%s" % count)
                        print "Sending Data"
                        send_time=time.time()+5
                        print f.read()
                        f.close()

#main function
if __name__ == '__main__':
    main()

                   