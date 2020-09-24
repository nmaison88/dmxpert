import pysimpledmx
import time
mydmx = pysimpledmx.DMXConnection('/dev/cu.usbserial-ALYX7Z1M')
# define color channels
RED=1
GREEN=2
BLUE=3
# mydmx.setChannel(1, 255,True) # set DMX channel 1 to full
# mydmx.setChannel(RED, 128, True) # set DMX channel 2 to 128
# mydmx.setChannel(3, 0)   # set DMX channel 3 to 0
# mydmx.render()    # render all of the above changes onto the DMX network

# mydmx.setChannel(4, 255, autorender=True) # set channel 4 to full and render to the network
while True:
	mydmx.setToFire()
	time.sleep(20)