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

Tapping Test

    This initiates the administration of tapping tests
    
Software API
    TappingTest(buzzer, button, display, tsc2007, sound)
        -buzzer:  tuple in the format (PWM pin (e.g., "P2_1"), sound frequency (Hz))
        -button:  tuple in the format (GPIO pin, sleep_time, active_high (bool))
        -display: tuple in the format (CS pin (e.g., board.P1_6), DC pin, RST pin, backlight pin, baudrate)
        -tsc2007: tuple in the foramt (I2C bus #, address, irq_dio, display_width, display_height, pressure_threshold)
        -sound:   bool for whether the buzzer plays when a bubble is tapped
        
    run()
        -starts the program
    cleanup()
        -cleans up all the hardware components
    
    *Following functions should not be called by the user
    score(periods)
        -calcualates mean, root mean squared, and standard deviation from "periods" (tap interval data)
    
    disp_instructions(test)
        -displays instructions for the specified test (rhythm or reaction tests)
    
    Tests:
    rhythm_test()
        -tests for rhythm and motor control
    reaction_test()    
        -tests for reaction speed and motor control
    speed_test()
        -tests for motor control
    
"""

import time
import threading
import statistics 
import math
import numpy as np
import random
import board

import buzzer as BUZZER
import timer as TIMER
import threaded_button as BUTTON
import display as DISPLAY
import tsc2007 as TSC2007

class TappingTest():
    buzzer  = None
    button  = None
    timer   = None
    stop    = None
    display = None
    tsc2007 = None
    sound   = None
   
    
    def __init__(self, buzzer = ("P2_1", 750), button = ("P2_2", 0.1, True), display = (board.P1_6, board.P1_4, board.P1_2, "P1_20", 24000000),
                 tsc2007 = (1, 0x48, None, 320, 240, 80), sound = True):
        self.buzzer  = BUZZER.Buzzer(*buzzer)
        self.button  = BUTTON.ThreadedButton(*button)
        self.timer   = TIMER.Timer()
        self.display = DISPLAY.Display(*display)
        self.tsc2007 = TSC2007.TSC2007(*tsc2007)
        self.sound   = sound
        
        self.stop   = False
    
        self._startup()
    # End def
    
    def _startup(self):
        self.button.set_on_press_callback(self.timer.record_time)
        self.buzzer.start()
        self.button.start()

        
    # End def
    
    def score(self, periods):
        
        #target = 1 / tempo * 60
        #delay = [(x-target)**2 for x in periods]
        #error = [(x-target) for x in periods]
        #count = [i for i in range(len(delay))]
        periods = [abs(x) for x in periods]
        square_periods = [(x**2) for x in periods]
        
        mean_error = statistics.mean(periods)
        rms   = math.sqrt(statistics.mean(square_periods))
        stdev = statistics.stdev(periods)
        #r     = np.corrcoef(count, delay)[0,1]
        
        return mean_error, rms, stdev
    
    def disp_instructions(self, test):
        if test is "rhythm":
            self.display.disp_text("The Tapping Test:",line = -1)
            self.display.disp_text("Tap to Buzzer Rhythm",line =  0)
            self.display.disp_text("Press Button to Start", line =  2)
        elif test is "reaction":
            self.display.disp_text("The Tapping Test:",line = -1)
            self.display.disp_text("Tap bubbles as soon as possible",line =  0)
            self.display.disp_text("Press to Start", line =  2)
        else:
            raise ValueError("invalid test specified")
    
    
    def run(self):
        """ Execute Main Program """
        
        #Locations of buttons
        b_width  = 66
        b_height = 40
        b1_x     = 30
        b2_x     = 126
        b3_x     = 223
        b_y      = 180
        button_color = (255, 255, 0)
        
        self.stop = False #controls whether entire program ends
        
        while True:
            if self.stop:
                break
            
            #Display instructions
            self.display.disp_text("Welcome!", line =  -3)
            self.display.disp_text("Choose a game to get started:", line =  0)
            
            #Show buttons
            self.display.disp_text("Rhythm     Reaction     Speed", line =  2)
            self.display.disp_rectangle(b1_x, b_y, b1_x+b_width, b_y+b_height, fill = button_color)
            self.display.disp_rectangle(b2_x, b_y, b2_x+b_width, b_y+b_height, fill = button_color)
            self.display.disp_rectangle(b3_x, b_y, b3_x+b_width, b_y+b_height, fill = button_color)
            
            self.display.disp_sticker(290, 5, 30, 30, "power.jpg") #Power button in the corner
            
            while True:
                x_tap, y_tap = self.tsc2007.wait_for_tap()[:2]
                
                if x_tap > 290 and y_tap < 30: #power button pressed
                    self.stop = True
                    break
                else:
                    if y_tap > b_y and y_tap < b_y + b_height:
                        if  x_tap > b1_x and x_tap  < b1_x+b_width: #left button
                            self.rhythm_test()
                            break
                            
                        if x_tap > b2_x and x_tap  < b2_x+b_width: #center button
                            self.reaction_test()
                            break
                        
                        if x_tap > b3_x and x_tap  < b3_x+b_width: #right button
                            self.speed_test()
                            break

        # End def
    def speed_test(self):
        """ Starts the speed test sequence """
        
        bubble_radius = 15
        
        #Give instructions
        self.display.clear()
        self.display.disp_text("Pop all bubbles in sequence fast!", line = -1)
        self.display.disp_text("Start with the blue bubble", line = 0)
        self.display.disp_text("End with the red bubble", line = 1)
        self.display.disp_text("Time starts with first tap", line = 2)
        self.display.disp_text("Tap to continue", alignment = "BC")
        
        time.sleep(1)
        self.tsc2007.wait_for_tap(function = self.display.clear)
        
        #Horizontally traveling bubbles
        bubbles = int( (self.display.width / (bubble_radius*3))) #space the bubbles 

        x = []
        y = []
        for bubble in range(bubbles):
            if bubble is 0: #first bubble
                color = (0, 0, 255) #blue
            elif bubble is (bubbles-1): #last bubble
                color = (255, 0, 0) #red
            else:  
                color = (255, 0, 255) #purple
            
            x.append(bubble_radius + (bubble_radius*3)*bubble) #bubble_radius amount of gap 
            y.append(random.randint(0, 240))
            
            self.display.disp_circle(x[bubble], y[bubble], bubble_radius, outline = None, fill = color)
            if bubble > 0:
                self.display.disp_line(x[bubble],y[bubble],x[bubble-1],y[bubble-1])
        
        tap = 0
        self.timer.reset()
       
       #Ensure user taps all bubbles sequentially 
        while tap < bubbles:
            x_tap, y_tap = self.tsc2007.wait_for_tap()[:2]
            if  x_tap < (x[tap] + bubble_radius*2) and x_tap > (x[tap] - bubble_radius*2) \
            and y_tap < (y[tap] + bubble_radius*2) and y_tap > (y[tap] - bubble_radius*2):
                if tap < 1:
                    self.timer.start() #Start timer when first bubble popped
                else:
                    self.timer.record_time()
                self.timer.record_time()
                
                #Cover up tapped bubbles 
                self.display.disp_rectangle(0, 0, x[tap]+bubble_radius*2-2, self.display.height, outline = None, fill = (255, 255, 255))
                tap = tap + 1
                
        
        #Get times
        times = self.timer.get_times()
        periods = self.timer.get_periods()
        
        #Calculate Scores
        time_elapsed = []
        time_elapsed.append(times[-1] - times[0])
        
        #Ending sequence
        self.display.clear()
        self.display.disp_text("First Round Complete!", line = -1)
        self.display.disp_text("Your time is {:.3f} seconds!".format(time_elapsed[0]), line = 0)
        self.display.disp_text("Speed: {:.3f} bubbles/sec!".format(bubbles/time_elapsed[0]), line = 1)
        self.display.disp_text("Tap to Continue", alignment = "BC")
        
        self.tsc2007.wait_for_tap(function = self.display.clear)
        self.display.disp_text("Second Round!", line = -1)
        self.display.disp_text("Tap to Proceed", alignment = "BC")
        
        self.tsc2007.wait_for_tap(function = self.display.clear)
        
        
        #Vertical test
        bubbles = int( (self.display.height / (bubble_radius*3))) #space the bubbles 

        x = []
        y = []
        for bubble in range(bubbles):
            if bubble is 0: #first bubble
                color = (0, 0, 255) #blue
            elif bubble is (bubbles-1): #last bubble
                color = (255, 0, 0) #red
            else:  
                color = (255, 0, 255) #purple
            
            y.append(bubble_radius + (bubble_radius*3)*bubble) #bubble_radius amount of gap 
            x.append(random.randint(0, 320))
            
            self.display.disp_circle(x[bubble], y[bubble], bubble_radius, outline = None, fill = color)
            if bubble > 0:
                self.display.disp_line(x[bubble],y[bubble],x[bubble-1],y[bubble-1])
        
        tap = 0
        self.timer.reset()
        while tap < bubbles:
            x_tap, y_tap = self.tsc2007.wait_for_tap()[:2]
            
            if  x_tap < (x[tap] + bubble_radius*2) and x_tap > (x[tap] - bubble_radius*2) \
            and y_tap < (y[tap] + bubble_radius*2) and y_tap > (y[tap] - bubble_radius*2):
                if tap < 1:
                    self.timer.start()
                else:
                    self.timer.record_time()
                self.display.disp_rectangle(0, 0, self.display.width, y[tap]+bubble_radius*2-2, outline = None, fill = (255, 255, 255))

                tap = tap + 1
                
        
        #Get times
        times = self.timer.get_times()
        periods = self.timer.get_periods()
        
        #Ending sequence
        time_elapsed.append(times[-1] - times[0])
        self.display.clear()
        self.display.disp_text("Second Round Complete!", line = -1)
        self.display.disp_text("Your time is {:.3f} seconds!".format(time_elapsed[1]), line = 0)
        self.display.disp_text("Speed: {:.3f} bubbles/sec!".format(bubbles/time_elapsed[1]), line = 1)
        self.display.disp_text("Tap to Continue", alignment = "BC")
        
        self.tsc2007.wait_for_tap(function = self.display.clear)

        
        
    def reaction_test(self):
        """ Starts the reaction test game """
        test_duration = 15.0
        margin        = 25
        bubble_radius = 15
        
        self.display.clear()
        
        #Before game starts
        self.disp_instructions("reaction")
        self.tsc2007.wait_for_tap()
        self.display.clear()
        
        #Start the game
        self.timer.start() 
        game_start = time.time()
        while time.time() - game_start < test_duration:
            #random bubble location and color 
            x = random.randint(margin, self.display.width - margin)
            y = random.randint(margin, self.display.height - margin)
            color = [random.randint(0, 255) for _ in range(3)]

            self.display.disp_circle(x, y, bubble_radius, fill = tuple(color))
            while True:
                x_tap, y_tap = self.tsc2007.wait_for_tap()[:2]
                
                #Check if bubble is tapped 
                if  x_tap < (x + bubble_radius*2) and x_tap > (x - bubble_radius*2) \
                and y_tap < (y + bubble_radius*2) and y_tap > (y - bubble_radius*2):
                    
                    if self.sound:
                        self.buzzer.turn_on(0.05)
                    self.timer.record_time()
                    break
                
            #Make previous bubble disappear 
            self.display.disp_circle(x, y, bubble_radius, outline = None, fill = (255, 255, 255))
        
        #Calculate Scores
        time_between_taps = self.timer.get_periods()
        mean_rxn_time = statistics.mean(time_between_taps) 
        fastest_rxn   = min(time_between_taps)
        slowest_rxn   = max(time_between_taps)
        avg_varation  = statistics.stdev(time_between_taps)
        score         = int(len(time_between_taps) + 1) # account for additonal tap
        self.timer.reset() 
        
        #Show scores and ending sequence
        self.display.disp_text("The game is complete!", line = -1)
        self.display.disp_text("Your score is {} bubbles!".format(score), line = 0)
        self.display.disp_text("Press to continue", alignment = "BC")
        
        self.tsc2007.wait_for_tap(function = self.display.clear)
        
        self.display.disp_text("Mean reaction time: {:.3f} sec".format(mean_rxn_time), line = -2)
        self.display.disp_text("Fastest reaction time: {:.3f} sec".format(fastest_rxn), line = -1)
        self.display.disp_text("Slowest reaction time: {:.3f} sec".format(slowest_rxn), line = 0)
        self.display.disp_text("Variation of taps: {:.3f} sec".format(avg_varation), line = 1)
        
        self.display.disp_text("Press to return", alignment = "BC")
        self.tsc2007.wait_for_tap(function = self.display.clear)
            
            
    
    def rhythm_test(self):
        """ Starts the rhythm test game """
        self.display.clear()
        self.disp_instructions("rhythm")
    
        while(not self.button.is_pressed()):
            pass
        
        #Start sequence
        self.display.clear()
        self.display.disp_text("The test is beginning in 3", line = -1)
        time.sleep(1)

        self.display.disp_text("The test is beginning in 2")
        time.sleep(1)

        self.display.disp_text("The test is beginning in 1", line = 1)
        time.sleep(1)
        
        self.display.clear()
        self.display.disp_text("Listen.")
        time.sleep(0.5)
        
        rhythm = []
        timing = []
        groups = 2
        #Generate a randomized rhythm
        for group in range(groups):
            group_length = random.randint(2,4) #Number of notes in each group
            note_length = 0.1
            pause_length = random.uniform(0.15,0.8) #Randomize tempo for the group
            
            #Record randomly generated rhythms  
            for note in range(group_length):
                rhythm.append(note_length)
                rhythm.append(pause_length)
                timing.append(note_length + pause_length)
            rhythm.append(0)
            rhythm.append(1.25)
            
        #Play rhythm and get user input 
        self.buzzer.tune(rhythm)
        self.display.clear()
        self.display.disp_text("Recreate the rhythm.", line = -1)
        self.timer.reset()
        self.timer.start()
        
        #Stop when user taps once for every note 
        while len(self.timer.get_times()) < len(timing):
            pass
        
        #Get statistics 
        button_press_periods = self.timer.get_periods()
        delay = []
        for i in range(len(button_press_periods)):
            delay.append(button_press_periods[i] - timing[i])
            
        #Calculate scores 
        mean, rms, variation = self.score(delay)
        score = int(100 - (mean - 0.05)*(100/(0.8-0)))
        if score < 0:
            score = 0            
        
        # Display scores and statistics 
        self.display.clear()
        self.display.disp_text("Great Job!", line = -1)
        self.display.disp_text("You scored a {}/100.".format(score))
        self.display.disp_text("Press to continue", alignment = "BC")
    
        self.tsc2007.wait_for_tap(function = self.display.clear)
    
        self.display.disp_text("Mean discrepancy: {:.3f} sec".format(mean), line = -1)
        self.display.disp_text("Root mean square error: {:.3f} sec".format(rms), line = 0)
        self.display.disp_text("Variation of discrepancy: {:.3f} sec".format(variation), line = 1)


        self.display.disp_text("Press to Return", alignment = "BC")
        
        self.tsc2007.wait_for_tap(function = self.display.clear)
            
    # End def
            
    
    def cleanup(self):
        """ Cleans up all the hardware and ends threads """
        self.button.cleanup()
        self.display.cleanup()
        self.tsc2007.cleanup()
        self.buzzer.cleanup()
    # End def 

# ------------------------------------------------------------------------
# Main script
# ------------------------------------------------------------------------

if __name__ == '__main__':
    print("Program Start")

    tap_test = TappingTest()
    #tap_test.tsc2007.start()
    
    main_thread = threading.currentThread()
    try:
        # Run the lock
         #tap_test.display.clear()
        tap_test.run()
        raise KeyboardInterrupt
            
    except KeyboardInterrupt:
        # Clean up hardware when exiting
        tap_test.cleanup()
    
    for t in threading.enumerate():
        if t is not main_thread:
            t.join()
    
    print("Program Complete")
        
        
        
        
