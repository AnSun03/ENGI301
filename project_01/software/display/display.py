"""
--------------------------------------------------------------------------
Tapping Test
--------------------------------------------------------------------------
License:   
Copyright 2023 - Andrew Sun

Based on

Copyright 2021 ladyada for Adafruit Industries

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

Display Driver
    -This is the driver for the ILI9341 display

Software API
    Display(CS = board.P1_6, DC = board.P1_4, RST = board.P1_2, lite = "P1_20", baudrate = 24000000)
        -CS: chip select pin
        -DC: command selector pin
        -RST: reset pin
        -lite: backlight pin
        -baudrate: default is 24000000
    
    clear()
        -Clears the screen completly (blank white background)
        
    overlay()
        -Makes future drawings overlay on existing features
        
    disp_rectangle(x1, y1, x2, y2, outline, fill)
        -Draws a rectangle with upper left and lower right corners at (x1, y1) and (x2, y2)
        -Outline: tuple for color of the shape perimeter (R, G, B)
        -Fill: tuple for color of the area of the shape (R, G, B)
    
    disp_circle(x, y, r, outline, fill)
        -Draws a circle centered at x, y with radius r
        -Outline: tuple for color of the shape perimeter (R, G, B)
        -Fill: tuple for color of the area of the shape (R, G, B)
        
    disp_line(x1, y1, x2, y2, fill, width)
        -Draws a line connecting (x1, y1) to (x2, y2)
        -Fill: tuple for color of line (R, G, B)
        -width: integer for the thickness of the line (default = 2)
        
    disp_background(image_name)
        -Scales an image and displays it as the background 
        -image_name: string with image name (must be in the same folder)
    
    disp_sticker(x, y, width, height, image_name, mask = False)
        -Takes an image and scales and displays it in a specified circular area 
        -x, y: center coordinates for the sticker
        -width, height: width and height to which to scale the image
        -image_name: string with image name (must be in the same folder)
        -mask: boolean for whether to mask the sticker
    
    disp_text(text, alignment, line, fill , clear)
        -Displays text on screen
        -text: string of text to display (cannot have any new lines)
        -alignment: 
            -"UL", "UC", "UR": upper  left, upper  center, upper  right
            -"ML", "MC", "MR": middle left, middle center, middle right
            -"BL", "BC", "BR": bottom left, bottom center, bottom right
            
    turn_on()
        -Turns on backlight
    
    turn_off()
        -Turns off backlight
    
    cleanup()
        -Turns off the screen 
"""
import digitalio
import board
import time
from PIL import ImageDraw, Image, ImageFont
from adafruit_rgb_display import ili9341


import Adafruit_BBIO.SPI as SPI
import Adafruit_BBIO.GPIO as GPIO
from Adafruit_BBIO.SPI import SPI
    
    
class Display():
    cs_pin    = None
    dc_pin    = None
    reset_pin = None
    BAUDRATE  = None
    spi       = None
    disp      = None
    width     = None
    height    = None
    image     = None
    draw      = None
    font      = None
    lite_pin  = None

    def __init__(self, CS = board.P1_6, DC = board.P1_4, RST = board.P1_2, lite = "P1_20", baudrate = 24000000):
        self.cs_pin    = digitalio.DigitalInOut(CS)
        self.dc_pin    = digitalio.DigitalInOut(DC)
        self.reset_pin = digitalio.DigitalInOut(RST)
        self.lite_pin  = lite
        self.BAUDRATE  = baudrate
        self.spi       = board.SPI()
        self.font      = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 18)
        
        self.disp = ili9341.ILI9341(
        self.spi,
        rotation=90,  # 2.2", 2.4", 2.8", 3.2" ILI9341
        cs=self.cs_pin,
        dc=self.dc_pin,
        rst=self.reset_pin,
        baudrate=self.BAUDRATE,
        )
        
        #Rotate to be landscape 
        if self.disp.rotation % 180 == 90:
            self.height = self.disp.width
            self.width = self.disp.height
        else:
            self.width = self.disp.width  
            self.height = self.disp.height
        
        self.image = Image.new("RGB", (self.width, self.height))
        self.draw  = ImageDraw.Draw(self.image)
        self._setup()
        
    def _setup(self):
        GPIO.setup(self.lite_pin, GPIO.OUT)
        self.turn_on()
        self.clear()
        
        
        
            
    def clear(self):
        """ Clear the screen and show white background """
        self.image = Image.new("RGB", (self.width, self.height))
        self.disp.image(self.image)
        self.disp_rectangle(0, 0, self.width, self.height, fill = (255, 255, 255))
        
        
    def overlay(self):
        """ Overlay the drawing """
        self.draw  = ImageDraw.Draw(self.image)


    def disp_rectangle(self, x1, y1, x2, y2, outline = 0, fill = (255, 255, 255)):
        """ Displays a rectangle overlayed on the screen """
    
        #Catch out of bounds 
        if any(x > self.width or x < 0 for x in [x1, x2]) or any(y > self.height or y < 0 for y in [y1, y2]):
            raise ValueError("the coordinates are out of bounds")
        
        self.overlay()
        self.draw.rectangle((x1, y1, x2, y2), outline=outline, fill=fill)
        self.disp.image(self.image)
    
    def disp_circle(self, x, y, r, outline = 0, fill = (255, 255, 0)):
        """ Display a rectangle overlayed on the screen """
        if (x > self.width or x < 0) or (y > self.height or y < 0):
            raise ValueError("the coordinates are out of bounds")
        
        self.overlay()
        self.draw.ellipse((x-r,y-r,x+r,y+r), outline=outline, fill=fill)
        self.disp.image(self.image)
        
        #x and y are for upper left coordinates of the circle
        
    def disp_line(self, x1, y1, x2, y2, fill = 0, width = 2):
        """ Display a line """
        #Catch out of bounds 
        if any(x > self.width or x < 0 for x in [x1, x2]) or any(y > self.height or y < 0 for y in [y1, y2]):
            raise ValueError("the coordinates are out of bounds")
            
        
        self.overlay()
        self.draw.line((x1, y1, x2, y2), fill=fill, width = width )
        self.disp.image(self.image)
        
    def disp_background(self, image_name):
        """ Display an image as the background """
        
        #Open the image
        self.image = Image.open(image_name)
        
        # Scale the image 
        image_ratio = self.image.width / self.image.height
        screen_ratio = self.width / self.height
        if screen_ratio < image_ratio:
            scaled_width = self.image.width * self.height // self.image.height
            scaled_height = self.height
        else:
            scaled_width = self.width
            scaled_height = self.image.height * self.width // self.image.width
        self.image = self.image.resize((scaled_width, scaled_height), Image.Resampling.BICUBIC)
        
        # Crop and center the image
        x = scaled_width // 2 - self.width // 2
        y = scaled_height // 2 - self.height // 2
        self.image = self.image.crop((x, y, x + self.width, y + self.height))
        
        # Display image.
        self.disp.image(self.image)
        
        
    def disp_sticker(self, x, y, width, height, image_name, mask = False):
        """ Display a sticker with an image """
        
        sticker = Image.open(image_name)
        sticker = sticker.resize((width, height), Image.Resampling.BICUBIC)
        
        if(mask):
            mask = Image.new("L", sticker.size, 0)
            draw = ImageDraw.Draw(mask)
            draw.ellipse((x, y) + sticker.size, fill = 255)
        else:
            mask = None
        
        self.image.paste(sticker, box = [x, y], mask = mask)
        self.disp.image(self.image)
    
    def disp_text(self, text, alignment = None, line = 0, fill = (0, 0, 0), clear = False):
        """ Displays text on screen """
        
        (x0,y0,x1,y1) = self.font.getbbox(text)
        
        font_width  = x1-x0
        font_height = y1-y0
        
        
        #font_width, font_height = self.font.getsize(text)
        if clear:
            self.clear()
        
        margin = 15
        
        if alignment is not None:
            if   alignment[0] == 't' or alignment[0] == 'T':
                y = margin
            elif alignment[0] == 'm' or alignment[0] == 'M':
                y = self.height // 2 - font_height // 2
            elif alignment[0] == 'b' or alignment[0] == 'B':
                y = self.height - font_height - margin
            else:
                raise ValueError("invalid vertical alignment")
            
            if len(alignment) > 1:
                if   alignment[1] == 'l' or alignment[1] == 'L':
                    x = margin
                elif alignment[1] == 'c' or alignment[1] == 'C':
                    x = self.width // 2 - font_width // 2
                elif alignment[1] == 'r' or alignment[1] =='R':
                    x = self.width - font_width - margin
                else:
                    raise ValueError("invalid horizontal alignment")
            else:
                x = self.width // 2 - font_width // 2 #center as default 
        else:
         
            y = self.height // 2 - font_height // 2
            x = self.width // 2 - font_width // 2 
            
            
        y = y + (font_height+5)*line
        

        position = (x,y)
        
        self.overlay()
        self.draw.text(
            position,
            text,
            font = self.font,
            fill = fill
            )

        self.disp.image(self.image)
            
    def turn_on(self):
        GPIO.output(self.lite_pin, GPIO.HIGH)
        
    def turn_off(self):
        GPIO.output(self.lite_pin, GPIO.LOW)
        
    def cleanup(self):
        """ Cleanup hardware """
        self.clear()
        self.disp_rectangle(0, 0, self.width, self.height, fill = (0, 0, 0))
        self.turn_off()
        GPIO.cleanup()
        

if __name__ == '__main__':
    
    display = Display()

    time.sleep(2)
    display.disp_rectangle(0, 0, 320/2, 240/2, fill = (255, 0, 0))
    display.disp_rectangle(320/2, 240/2, 320, 240, fill = (0, 255, 0))
    
    time.sleep(2)
    display.disp_sticker(0, 0, 200, 200, "sun.jpeg", True)
    
    time.sleep(2)
    
    
    display.disp_text(text = "Hello World", alignment = "MC")
    display.disp_text(text = "TL", alignment = "TL")
    display.disp_text(text = "TC", alignment = "TC")
    display.disp_text(text = "TR", alignment = "TR")
    
    display.disp_text(text = "ML", alignment = "ML")
    display.disp_text(text = "MR", alignment = "MR")
    
    display.disp_text(text = "BL", alignment = "BL")
    display.disp_text(text = "BC", alignment = "BC")
    display.disp_text(text = "BR", alignment = "BR")
    
    text = "tl"
    
    display.disp_line(320/2, 240/2, 320, 240)
    print("Program Successful")


    