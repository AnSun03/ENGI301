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
import threading

MIN_X = 500
MAX_X = 3700
MIN_Y = 600
MAX_Y = 3600

class TSC2007(threading.Thread):
    bus         = None
    address     = None
    command     = None
    irq_dio     = None
    tsc         = None
    i2c         = None
    point       = None
    old_point   = None
    disp_width  = None
    disp_height = None
    stop        = None
    
    def __init__(self, bus = 1, address = 0x48, irq_dio = None, disp_width = 320, disp_height = 240):
        self.bus         = bus
        self.address     = address
        self.irq_dio     = irq_dio
        self.disp_width  = disp_width
        self.disp_height = disp_height
        self.command     = "/usr/sbin/i2cset -y {0} {1}".format(bus, address)
        self.i2c         = board.I2C()
        self.stop        = False

        threading.Thread.__init__(self)
    
        self._setup()
        
    def _setup(self):
        self.tsc = adafruit_tsc2007.TSC2007(self.i2c, irq=self.irq_dio)
        
        
    def run(self):
        while not self.stop:
            if self.tsc.touched:
                self.point = self.tsc.touch
            
                if self.point["pressure"] > 100:  
                    x, y, z = self.tap_loc()
                    #print("Touchpoint: (%d, %d, %d)" % (self.point["y"], self.point["x"], self.point["pressure"]))
                    print("Touchpoint: (%d, %d, %d)" % (x, y, z))
                
                    
                    
    def tap_loc(self):
        if self.point is not None:
            y = (-self.point["x"] + MAX_Y)*self.disp_height/(MAX_Y-MIN_Y)
            x = (self.point["y"]  - MIN_X)*self.disp_width /(MAX_X-MIN_X)
            z = self.point["pressure"]
            
            if y < 0: 
                y = 0
            if y > self.disp_height:
                y = self.disp_height
            if x < 0: 
                x = 0
            if x > self.disp_width:
                x = self.disp_width
            return x, y, z
        else:
            return None
    
        
        
    def wait_for_tap(self, function = None):
        pressure_threshold = 100
        
        function_return_value = None
        while True:
            if self.tsc.touched:
                self.point = self.tsc.touch
                start_time = time.time()
            
                if self.point["pressure"] > 100:  
                    if function is not None:
                        function_return_value = function()
                    tap_dur = time.time() - start_time
                    break
                
        x, y, z = self.tap_loc() 
        return x, y, z, tap_dur, function_return_value
        
    def cleanup(self):
        self.stop = True
        
        
if __name__ == '__main__':
    ts = TSC2007()
    #ts.wait_for_tap()
    #x, y = ts.wait_for_tap()[0:2]
    ts.start()
    point = ts.tap_loc()
    while True:
        if point is not None:
            x, y, z = ts.tap_loc()
    
    print("tapped")
    print("tapped")
    """
    ts.start()
    
    main_thread = threading.currentThread()
    try:
        while (True):
            # Do nothing in the main thread
            time.sleep(1)
    except KeyboardInterrupt:
        # Clean up the hardware
        print("keyboard interrupt")
    
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
            
    print("Program End")
    """
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