"""
--------------------------------------------------------------------------
Tapping Test
--------------------------------------------------------------------------
License:   
Copyright 2023 - Andrew Sun

Redistribution and use in source and binary forms, with or without 
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this 
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice, 
this list of conditions and the following disclaimer in the documentation 
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors 
may be used to endorse or promote products derived from this software without 
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" 
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE 
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE 
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE 
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL 
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR 
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER 
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, 
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
--------------------------------------------------------------------------

"""

import board
import adafruit_tsc2007
import time

class TSC2007():
    bus     = None
    address = None
    command = None
    irq_dio = None
    tsc     = None
    i2c     = None
    def __init__(self, bus = 1, address = 0x48, irq_dio = None):
        self.bus     = bus
        self.address = address
        self.irq_dio = irq_dio
        self.command = "/usr/sbin/i2cset -y {0} {1}".format(bus, address)
        self.i2c     = board.I2C()
        
        self._setup()
        
    def _setup(self):
        self.tsc = adafruit_tsc2007.TSC2007(self.i2c, irq=self.irq_dio)
        
    def touch_loc(self):
        if self.tsc.touched:
            point = self.tsc.touch
            if point["pressure"] > 100:  # ignore touches with no 'pressure' as false
                print("Touchpoint: (%d, %d, %d)" % (point["x"], point["y"], point["pressure"]))

if __name__ == '__main__':
    ts = TSC2007()
    while True:
        ts.touch_loc()
    """
    import board
    import adafruit_tsc2007

    # Use for I2C
    i2c = board.I2C()  # uses board.SCL and board.SDA
    # i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
    
    irq_dio = None  # don't use an irq pin by default
    # uncomment for optional irq input pin so we don't continuously poll the I2C for touches
    # irq_dio = digitalio.DigitalInOut(board.A0)
    tsc = adafruit_tsc2007.TSC2007(i2c, irq=irq_dio)
    
    while True:
        if tsc.touched:
            point = tsc.touch
            if point["pressure"] < 100:  # ignore touches with no 'pressure' as false
                continue
            print("Touchpoint: (%d, %d, %d)" % (point["x"], point["y"], point["pressure"]))
    """