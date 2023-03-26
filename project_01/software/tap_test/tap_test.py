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
import time
import threading
import statistics 
import math
import numpy as np

import buzzer as BUZZER
import timer as TIMER
import threaded_button as BUTTON

class TappingTest():
    buzzer  = None
    button  = None
    timer   = None
    stop    = None
    
    def __init__(self, buzzer = "P2_1", button = "P2_2"):
        self.buzzer = BUZZER.Buzzer(buzzer)
        self.button = BUTTON.ThreadedButton(button)
        self.timer  = TIMER.Timer()
        self.stop   = False
    
        self._startup()
    # End def
    
    def _startup(self):
        self.button.set_on_press_callback(self.timer.record_time)
        
    # End def
    
    def score(self, periods, times, tempo):
        target = 1 / tempo * 60
        delay = [(x-target)**2 for x in periods]
        error = [(x-target) for x in periods]
        count = [i for i in range(len(delay))]
        
        mean_error = statistics.mean(error)
        rms   = math.sqrt(statistics.mean(delay))
        stdev = statistics.stdev(periods)
        r     = np.corrcoef(count, delay)[0,1]
        
        return mean_error, rms, stdev, r
        
    
    def run(self):
        """ Execute Main Program """
        
        #Display instructions and get user input 
        print("For the tapping test, please tap to the rhythm of the buzzer.")
        print("Press the button once to start:")
        
        self.button.start()
        
        while True: 
            while(not self.button.is_pressed()):
                pass
            
            #Start sequence
            print("The test is beginning in 3...")
            time.sleep(1)
            print("The test is beginning in 2...")
            time.sleep(1)
            print("The test is beginning in 1...")
            time.sleep(1)
            
            tempo = 60
            length = 10
            self.buzzer.rhythm(tempo = tempo, length = length)
            
            periods = self.timer.get_periods()
            times   = self.timer.get_times()
            
            print("Test Complete, here is your score (root mean square error, standard deviation, r coefficient)")
            print(self.score(periods,times,tempo))
            
            time.sleep(2)
            print("Press button again to restart test")
            
            while(not self.button.is_pressed()):
                pass
        
    # End def

    
    def cleanup(self):
        self.button.cleanup()

if __name__ == '__main__':
    print("Program Start")

    # Create instantiation of the lock
    tap_test = TappingTest()
    main_thread = threading.currentThread()
    try:
        # Run the lock
        tap_test.run()

    except KeyboardInterrupt:
        # Clean up hardware when exiting
        tap_test.cleanup()
    
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()

    print("Program Complete")
        
        
        
        
