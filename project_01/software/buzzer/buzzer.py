# -*- coding: utf-8 -*-
"""
--------------------------------------------------------------------------
Buzzer
--------------------------------------------------------------------------
License:   
Copyright 2021-2023 Erik Welsh

Based on library from

Copyright 2018 Nicholas Lester

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
This file provides an interface to a PWM controllered buzzer.
  - Ex:  https://www.adafruit.com/product/1536


APIs:
  - Buzzer(pin)
    - play(frequency, length=1.0, stop=False)
      - Plays the frequency for the length of time

    - stop(length=0.0)
      - Stop the buzzer (will cause breaks between tones)
      
    - cleanup()
      - Stop the buzzer and clean up the PWM

"""
import time

import Adafruit_BBIO.PWM as PWM
import threading

# ------------------------------------------------------------------------
# Global variables
# ------------------------------------------------------------------------


# ------------------------------------------------------------------------
# Main Tasks
# ------------------------------------------------------------------------

class Buzzer(threading.Thread):
    pin       = None
    debug     = None
    on        = None
    frequency = None
    duration  = None
    stop      = None
    
    def __init__(self, pin, frequency = 60):
        self.pin       = pin
        self.debug     = False
        self.on        = False
        self.frequency = frequency
        self.stop      = False
        threading.Thread.__init__(self)
 
        self._setup()
        
    def _setup(self):
        PWM.start(self.pin, 0, self.frequency)
 
    # End def
    
    
    def play(self, frequency, length=1.0, stop=False):
        """ Plays the frequency for the length of time.
            frequency - Value in Hz or None for no tone
            length    - Time in seconds (default 1.0 seconds)
            stop      - Stop the buzzer (will cause breaks between tones)
        """
        
        if self.debug:
            start_time = time.time()
        
        if frequency is not None:
            # !!! FIX !!! 
            PWM.start(self.pin, 50, frequency)
            # !!! FIX !!! 
        
        
        time.sleep(length)
        
        if (stop):
            self.stop()
         
        if self.debug:  
            print("--- %s seconds ---" % (time.time() - start_time))

    # End def
    
    def run(self):
        while not self.stop:
            if self.on:
                PWM.set_duty_cycle(self.pin, 50)
                if self.duration is not None:
                    time.sleep(self.duration)
                    self.duration = None
                    self.on = False
            else:
                PWM.set_duty_cycle(self.pin, 0)
            time.sleep(0.01)
    
    def turn_on(self, length):
        self.on = True
        #PWM.set_duty_cycle(self.pin, 50)
        
        if length is not None:
            self.duration = length
            #time.sleep(length)
            #self.turn_off()
            
            
            
    def turn_off(self):
        self.on = False
        #PWM.set_duty_cycle(self.pin, 0)
    
    def set_frequency(self, frequency):
        self.frequency = frequency
    
    def stop(self, length=0.0):
        """ Stops the buzzer (will cause breaks between tones)
            length    - Time in seconds (default 0.0 seconds)
        """
        # !!! FIX !!! 
        PWM.stop(self.pin)
        
        #print("Stopping the buzzer")
        # !!! FIX !!! 

        time.sleep(length)
        
    # End def
    def rhythm(self, frequency = 50, tempo = 60, length = 1.0):
        
        period    = 1 / (tempo/60) 
        buzzCount = int( length // period )
        buzzDur   = 0.1; 
        
        
        self.play(frequency, 0)

        for i in range(buzzCount):
            start_time = time.time()
            #PWM.set_duty_cycle(self.pin, 50)
            self.turn_on(buzzDur)
            #time.sleep(buzzDur)
            #PWM.set_duty_cycle(self.pin, 0)
            while (time.time() - start_time) < period:
                pass
                
            print("--- %s seconds ---" % (time.time() - start_time))
            
        #self.stop()
    
    def tune(self, rhythm, frequency = 50, length = 1.0):
        """  Plays a series of buzzes based on rhythm  """

        for i in range(0, len(rhythm)-1, 2):
            start_time = time.time()
            if rhythm[i] > 0:
                self.turn_on(rhythm[i])
            
            while (time.time() - start_time) < rhythm[i+1] + rhythm[i]: #add times because threadednesses
                pass
                
            print("--- %s seconds ---" % (time.time() - start_time))
        
        
    
    def cleanup(self):
        """Stops the buzzer and cleans up the PWM.
             *** This function must be called during hardware cleanup ***
        """
        self.stop()
        PWM.cleanup()
        self.stop = True
    # End def
    
# End class

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    print("Buzzer Test")
    
    buzzer = Buzzer("P2_1")
    
    
    try:
        buzzer.start()
        
        rhythm = []
        import random
        for i in range(3):
            group = random.randint(1,4)
            print(group)
            note_length = 0.1
            pause_length = random.uniform(0.25,1.5)
            for j in range(group):
                rhythm.append(note_length)
                rhythm.append(pause_length)
            rhythm.append(0)
            rhythm.append(1)
        print(rhythm)
            
        buzzer.tune(rhythm)
        
        
            
    except KeyboardInterrupt:
        print("Keyboard Interrupt")
    
    
    main_thread = threading.currentThread()

    # Wait for threads to complete
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    print("Program End")
    
    
    """
    
    print("Play tone")
    start_time = time.time()
    
    buzzer.rhythm(440, 360, 5)
    print("--- %s seconds ---" % (time.time() - start_time))
    """
    
    """
    buzzer.play(440, 1.0, False)      # Play 440Hz for 1 second
    time.sleep(1.0)
    buzzer.play(880, 1.0, True)       # Play 880Hz for 1 second
    time.sleep(1.0)   
    """
    buzzer.cleanup()
    
    print("Test Complete")

