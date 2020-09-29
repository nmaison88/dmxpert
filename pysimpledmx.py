import serial
import sys
import os
import time
from sys import platform
if platform == "linux" or platform == "linux2":
    print("linux detected, you must be a hacker")
    devices = os.system("lsusb")
elif platform == "darwin":
    print("osx detected, you fancy fancy person")
    devices = os.system("ls /dev/cu.*")
elif platform == "win32":
  print("windows Yucky.. check for com port in device manager")

print(devices)
START_VAL = 0x7E
END_VAL = 0xE7

COM_BAUD = 57600
COM_TIMEOUT = 1
COM_PORT = 7
DMX_SIZE = 512

LABELS = {
    'GET_WIDGET_PARAMETERS': 3,  # unused
    'SET_WIDGET_PARAMETERS': 4,  # unused
    'RX_DMX_PACKET': 5,  # unused
    'TX_DMX_PACKET': 6,
    'TX_RDM_PACKET_REQUEST': 7,  # unused
    'RX_DMX_ON_CHANGE': 8,  # unused
}

# define color channels
RED = 1
GREEN = 2
BLUE = 3


class DMXConnection(object):
    def __init__(self, comport=None):
        '''
        On Windows, the only argument is the port number. On *nix, it's the path to the serial device.
        For example:
            DMXConnection(4)              # Windows
            DMXConnection('/dev/tty2')    # Linux
            DMXConnection("/dev/ttyUSB0") # Linux
        '''
        self.dmx_frame = [0] * DMX_SIZE
        try:
            self.com = serial.Serial(
                comport, baudrate=COM_BAUD, timeout=COM_TIMEOUT)
        except:
            com_name = 'COM%s' % (
                comport + 1) if type(comport) == int else comport
            print("Could not open device %s. Quitting application." % com_name)
            sys.exit(0)

        print("Opened %s." % (self.com.portstr))

    def setChannel(self, chan, val, autorender=False):
        '''
        Takes channel and value arguments to set a channel level in the local
        DMX frame, to be rendered the next time the render() method is called.
        '''
        if not chan >= 1 and chan <= DMX_SIZE:
            print('Invalid channel specified:')
            return

        # clamp value
        val = max(0, min(val, 255))
        self.dmx_frame[chan] = val
        if autorender:
            self.render()

    def clear(self, chan=0):
        '''
        Clears all channels to zero. blackout.
        With optional channel argument, clears only one channel.
        '''
        if chan == 0:
            self.dmx_frame = [0] * DMX_SIZE
        else:
            self.dmx_frame[chan-1] = 0

    def render(self):
        ''''
        Updates the DMX output from the USB DMX Pro with the values from self.dmx_frame.
        '''
        packet = [
            START_VAL,
            LABELS['TX_DMX_PACKET'],
            len(self.dmx_frame) & 0xFF,
            (len(self.dmx_frame) >> 8) & 0xFF,
        ]
        packet += self.dmx_frame
        packet.append(END_VAL)

        packet = map(chr, packet)
        self.com.write(''.join(packet))

    def close(self):
        self.com.close()

    def fadeUp(self, channel, startValue, stopValue, duration):
        begin = 0
        value = startValue
        increment = ((stopValue - startValue) / duration) 
        while begin < duration:
          if(value >255):
            value = 0
          self.setChannel(channel, value, True)
          begin += 1
          value += increment
          print(begin, increment, value, duration)
          time.sleep(1)

    def setToOrange(self):
        # make orange
        self.setChannel(RED, 255)
        self.setChannel(GREEN, 69)
        self.setChannel(BLUE, 0)
        self.render()

    def setToYellow(self):
        self.setChannel(RED, 150)  # set DMX channel 2 to 128
        self.setChannel(GREEN, 100, True)  # set DMX channel 2 to 128

    def setToRed(self):
        # make orange
        self.setChannel(RED, 255)
        self.setChannel(GREEN, 0)
        self.render()

    def setToFire(self):
        while True:
            self.setToOrange()
            time.sleep(2)
            self.setToRed()
            time.sleep(2)
