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
import digitalio
import board
import time
from PIL import ImageDraw, Image, ImageFont
from adafruit_rgb_display import ili9341
from adafruit_rgb_display import st7789  # pylint: disable=unused-import
from adafruit_rgb_display import hx8357  # pylint: disable=unused-import
from adafruit_rgb_display import st7735  # pylint: disable=unused-import
from adafruit_rgb_display import ssd1351  # pylint: disable=unused-import
from adafruit_rgb_display import ssd1331  # pylint: disable=unused-import

import Adafruit_BBIO.SPI as SPI
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

    def __init__(self, CS = board.P1_6, DC = board.P1_4, RST = board.P1_2, baudrate = 24000000):
        self.cs_pin    = digitalio.DigitalInOut(CS)
        self.dc_pin    = digitalio.DigitalInOut(DC)
        self.reset_pin = digitalio.DigitalInOut(RST)
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
        
        if self.disp.rotation % 180 == 90:
            self.height = self.disp.width  # we swap height/width to rotate it to landscape!
            self.width = self.disp.height
        else:
            self.width = self.disp.width  # we swap height/width to rotate it to landscape!
            self.height = self.disp.height
        
        self.image = Image.new("RGB", (self.width, self.height))
        self.draw  = ImageDraw.Draw(self.image)

        
        self._setup()
        
    def _setup(self):
        self.clear()
        
            
    def clear(self):
        self.image = Image.new("RGB", (self.width, self.height))
        self.disp.image(self.image)
        self.disp_rectangle(0, 0, self.width, self.height, fill = (255, 255, 255))
        
        
    def overlay(self):
        self.draw  = ImageDraw.Draw(self.image)


    """
    def landscape(self):
        if self.disp.rotation % 180 == 90:
            height = self.disp.width  # we swap height/width to rotate it to landscape!
            width = self.disp.height
            print("TRue")
        else:
            width = self.disp.width  # we swap height/width to rotate it to landscape!
            height = self.disp.height
            print("False")
        
        return width, height
        
    """
        
    def disp_rectangle(self, x1, y1, x2, y2, outline = 0, fill = (255, 255, 255)):
        #image = Image.new("RGB", (self.width, self.height))
        
        #Catch out of bounds 
        if any(x > self.width or x < 0 for x in [x1, x2]) or any(y > self.height or y < 0 for y in [y1, y2]):
            raise ValueError("the coordinates are out of bounds")
        
        self.overlay()
        self.draw.rectangle((x1, y1, x2, y2), outline=outline, fill=fill)
        self.disp.image(self.image)
    
    def disp_circle(self, x, y, r, outline = 0, fill = (255, 255, 0)):
        
        if (x > self.width or x < 0) or (y > self.height or y < 0):
            raise ValueError("the coordinates are out of bounds")
        
        self.overlay()
        self.draw.ellipse((x-r,y-r,x+r,y+r), outline=outline, fill=fill)
        self.disp.image(self.image)
        
        #x and y are for upper left coordinates of the circle
        
    def disp_line(self, x1, y1, x2, y2, fill = 0, width = 2):
        #Catch out of bounds 
        if any(x > self.width or x < 0 for x in [x1, x2]) or any(y > self.height or y < 0 for y in [y1, y2]):
            raise ValueError("the coordinates are out of bounds")
            
        
        self.overlay()
        self.draw.line((x1, y1, x2, y2), fill=fill, width = width )
        self.disp.image(self.image)
        
    def disp_background(self, image_name = "blinka.jpg"):
            
        #image = Image.new("RGB", (self.width, self.height))
        
         # Get drawing object to draw on image.
        #draw = ImageDraw.Draw(image)
        
        # Draw a black filled box to clear the image.
        
        #self.overlay()
        
        """
        self.draw.rectangle((0, 0, self.width, self.height), outline=0, fill=(0, 0, 0))
        self.disp.image(self.image)
        
        """
        
        self.image = Image.open(image_name)
        
        # Scale the image to the smaller screen dimension
        
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
        
        
    def disp_sticker(self, x, y, width, height, image_name = "blinka.jpg", mask = False):
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
    
    def disp_text(self, text = "Hello World", alignment = None, line = 0, fill = (0, 0, 0), clear = False):
        
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
        
        
    def cleanup(self):
        self.clear()
        self.disp_rectangle(0, 0, self.width, self.height, fill = (0, 0, 0))
        

if __name__ == '__main__':
    display = Display()
    """
    time.sleep(2)
    display.disp_rectangle(0, 0, 320/2, 240/2, fill = (255, 0, 0))
    display.disp_rectangle(320/2, 240/2, 320, 240, fill = (0, 255, 0))
    
    time.sleep(2)
    display.disp_sticker(0, 0, 200, 200, "sun.jpeg", True)
    
    time.sleep(2)
    """
    """
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
    """
    display.disp_line(320/2, 240/2, 320, 240)
    #print(text[3])
    
    
   # display.disp_background("blinka.jpg")
    #display.disp_rectangle(0, 0, 320/2, 240/2, fill = (255, 0, 0))

    #display.disp_circle(320/2, 240/2, 50)
    
    
    
    
    


    
    
    print("Program Successful")
    
    

    