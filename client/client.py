#!/usr/bin/env python3

import os
import sys

CURRENT_DIRECTORY = os.path.dirname( __file__ )
sys.path.append( CURRENT_DIRECTORY )

from omron6dt import *
from pygame.locals import *
#import picamera
import pygame.camera
import io

def read_ambient_temp():
    # Get I2C bus
    bus = smbus.SMBus(1)
    # MCP9808 address, 0x18(24)
    # Select configuration register, 0x01(1)
    #       0x0000(00)  Continuous conversion mode, Power-up default
    config = [0x00, 0x00]
    bus.write_i2c_block_data(0x18, 0x01, config)
    # MCP9808 address, 0x18(24)
    # Select resolution rgister, 0x08(8)
    #       0x03(03)    Resolution = +0.0625 / C
    bus.write_byte_data(0x18, 0x08, 0x03)
    time.sleep(0.5)
    # MCP9808 address, 0x18(24)
    # Read data back from 0x05(5), 2 bytes
    # Temp MSB, TEMP LSB
    data = bus.read_i2c_block_data(0x18, 0x05, 2)
    # Convert the data to 13-bits
    ctemp = ((data[0] & 0x1F) * 256) + data[1]
    if ctemp > 4095 :   
        ctemp -= 8192
    ctemp = ctemp * 0.0625
    ftemp = ctemp * 1.8 + 32
    return ftemp

omron = OmronD6T(arraySize=8)

SCREEN_DIMS = [1280, 1000]
xSize = 8
ySize = 1
arraySize = xSize * ySize

#init pygame screen
screen = pygame.display.set_mode(SCREEN_DIMS)
pygame.display.set_caption('DreamPort TBot')
pygame.mouse.set_visible(False)
pygame.init()
font = pygame.font.Font(None, 36)
font2 = pygame.font.Font(None, 72)

# Init camera
#-camera = picamera.PiCamera()
#-camera.resolution = (1280, 720)
pygame.camera.init()



# Init buffer
#-rgb = bytearray(camera.resolution[0] * camera.resolution[1] * 3)

# init v2
cam_list = pygame.camera.list_cameras()
cam = pygame.camera.Camera(cam_list[0],(1280,720))
cam.start()
# flip horizontal to match the themral sensor
cam.set_controls(hflip = True, vflip = False)

X = []
Y = []
temp_hit = 0
square = []
center = []
rect = [Rect] * arraySize

cellWidth = SCREEN_DIMS[0] / xSize
cellHeight = SCREEN_DIMS[1] / ySize
cellWidthCenter = cellWidth / 2
if cellHeight > cellWidth:
  cellHeight = cellWidth
cellHeightCenter = cellHeight / 2

for x in range(xSize):
    X.append(x * cellWidth)

for y in range(ySize):
    Y.append((y * cellHeight) + (SCREEN_DIMS[1] - cellHeight))

for x in range(xSize):
  for y in range(ySize):
    square.append((X[x], Y[y], cellWidth, cellHeight))
    center.append((X[x] + cellWidthCenter, Y[y] + cellHeightCenter))

def temp_to_rgb(temp):
  if temp < 80:
    return (0, 0, 192)
  elif temp >= 80 and temp < 90:
    return (255, 128, 0)
  elif temp > 90:
    return (255, 0, 0)

hit_start_time = time.time()
hit_time = 11
person_detect = False

text = font.render('DreamPort TBot', 1, (255,255,255))
text_pos = text.get_rect()
text_pos.center = (SCREEN_DIMS[0]/2,SCREEN_DIMS[1] - cellHeight - 250)
screen.blit(text, text_pos)


while True:
  for event in pygame.event.get():
    if event.type == QUIT:
      pygame.display.quit()
      sys.exit(0)
    if event.type == KEYDOWN:
      if event.key == K_q or event.key == K_ESCAPE:
        pygame.display.quit()
        sys.exit(0)

  # read OMRON data
  bytes_read, temperature = omron.read()

  #read camera data
  
  #v1stream = io.BytesIO()
  #v1camera.capture(stream, use_video_port=True, format='rgb')
  #v1stream.seek(0)
  #v1stream.readinto(rgb)
  #v1stream.close()
  #v1img = pygame.image.frombuffer(rgb[0:
  #v1  (camera.resolution[0] * camera.resolution[1] * 3)],
  #v1  camera.resolution, 'RGB')
  
  
  temp_hit = 0
  for i in range(arraySize):
    if temperature[i] >= 80:
      temp_hit += 1
    
    screen.fill(temp_to_rgb(temperature[i]), square[i])
    
    text = font.render(str(i+1), 1, (255,255,255))
    text_pos = text.get_rect()
    text_pos.center = (center[i][0], SCREEN_DIMS[1] - cellHeight + 18)
    screen.blit(text, text_pos)
    
    text = font.render(str(int(temperature[i])) + chr(0xb0) + "F", 1, (255,255,255))
    text_pos = text.get_rect()
    text_pos.center = center[i]
    screen.blit(text, text_pos)

  hit_time = time.time() - hit_start_time

  if temp_hit > 3:
    person_detect = True
    hit_start_time = time.time()
  elif temp_hit <= 3 and hit_time > 10:
    person_detect = False

  if person_detect:    
    screen.fill((0,0,0), (0,180,SCREEN_DIMS[0],120))
    screen.fill((255,0,0), (0,0,SCREEN_DIMS[0],120))
    text = font2.render('RESERVED ({})'.format(read_ambient_temp()), 1, (255,255,255))
    text_pos = text.get_rect()
    text_pos.center = (SCREEN_DIMS[0]/2,60)
    screen.blit(text, text_pos)
  else:
    screen.fill((0,0,0), (0,180,SCREEN_DIMS[0],120))
    screen.fill((0,192,0), (0,0,SCREEN_DIMS[0],120))
    text = font2.render('AVAILABLE({})'.format(read_ambient_temp()), 1, (255,255,255))
    text_pos = text.get_rect()
    text_pos.center = (SCREEN_DIMS[0]/2,60)
    screen.blit(text, text_pos)
    
    
  img = cam.get_image()
  if img:
    img_pos = img.get_rect(topleft=(0,120))
    #img_pos.center = (SCREEN_DIMS[0]/2, (SCREEN_DIMS[1]-cellHeight)/2)
    screen.blit(img, img_pos)

  pygame.display.update()
  #time.sleep(0.01)
