import RPi.GPIO as GPIO
import time
import db

db.add_event('start')

GPIO.setmode(GPIO.BCM)
pin = 18
C = 420/float(1000)  #uF

def rc_time(pin):
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,GPIO.LOW)
    time.sleep(0.01)

    GPIO.setup(pin,GPIO.IN)
    t1 = time.time()
    while( GPIO.input(pin) == GPIO.LOW):
        pass
    t2 = time.time()

    return (t2-t1)*1000000

def avg_rc_time(pin,samples):
    total = 0
    for i in range(1,samples):
        total += rc_time(pin)
    t = total/float(samples)
    return t

def r(pin):
    t = avg_rc_time(pin,5)
    T = t * 3.3 * 0.632
    r = (T/C)
    return r

try:
    count = 0
    last_state = False
    while True:
        rval = r(18)
        current_state = rval<13000
	print rval
        if(current_state != last_state):
            last_state = current_state
            if(current_state == False):
                count += 1
                db.add_event('1wh')
                #print(count)


except KeyboardInterrupt:
    pass
finally:
    db.add_event('exit')
    GPIO.cleanup()
