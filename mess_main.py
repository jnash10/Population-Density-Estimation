import subprocesses 
import time

while True:
    p1 = subprocesses.Popen(['sudo','airmon-ng','start','wlan1'])
    p2 = subprocesses.Popen(['sudo', 'python' , 'prob5.py','-i','wlan1mon','-r','-f','-l','-d','";"','-o','problog.csv'])
    p3 = subprocesses.Popen(['python','mess2.py'])


    ##timed condition

    p2.terminate()
    p3.terminate()


