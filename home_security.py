import subprocess
import RPi.GPIO as GPIO
import time


#HIGH = 1
#LOW = 0
#LED_PIN = 10
PIR_PIN = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIR_PIN, GPIO.IN)            # initialize GPIO Pin as input
#GPIO.setup(LED_PIN, GPIO.OUT)            # initialize GPIO Pin as output


print ("PIR Module Test (CTRL+C to exit)")
print ("Loading ...")
time.sleep (2)
print ("System Started")

def MOTION(PIR_PIN):	
	#GPIO.output(LED, HIGH)
	print ("Motion Detected!")
	subprocess.run(['python', 'python_picam.py'])
	
try:
	GPIO.add_event_detect(PIR_PIN, GPIO.RISING, callback=MOTION)
	while 1:
	   time.sleep (10)
   else:
		#GPIO.output(LED, LOW)
		print('Again')
except KeyboardInterrupt:
   print(" Quit" )

GPIO.cleanup()
