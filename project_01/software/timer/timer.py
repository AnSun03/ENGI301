"""
--------------------------------------------------------------------------
License:   
Copyright 2023 - Erik Welsh

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
import numpy as np
import warnings

class Timer():
    times = None
    periods = None
    start_time = None
    
    def __init__(self):
        self.start_time = time.time()
        self.times = []
        self.periods = []
        
    def record_time(self):
        self.times.append(time.time() - self.start_time)
        if len(self.times) > 1:
            self.periods.append(self.times[-1] - self.times[-2])

        
    def get_times(self):
        return self.times
        
    def get_periods(self):
        return self.periods
    
    def start(self):
        if not self.times:
            self.start_time = time.time()
       

    def reset(self):
        self.times   = []
        self.periods = []
        
        
if __name__ == '__main__':
    myTimer = Timer()
    
    myTimer.record_time()
    time.sleep(1.0)
    myTimer.record_time()
    time.sleep(1.5)
    myTimer.record_time()
    time.sleep(2.0)
    myTimer.record_time()
    print(myTimer.get_times())
    print(myTimer.get_periods())



    
    