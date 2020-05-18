import pygame
from pygame.locals import *
import cv2 as cv
import numpy as np
import sys
import traceback
import os

face_cascade = cv.CascadeClassifier('/home/pi/workspace/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
eye_cascade = cv.CascadeClassifier('/home/pi/workspace/opencv/data/haarcascades/haarcascade_eye.xml')

def surface_to_string(surface):
    """Convert a pygame surface into string"""
    return pygame.image.tostring(surface, 'RGB')

def pygame_to_cvimage(surface):
    """Convert a pygame surface into a cv image"""
    cv_image = cv.CreateImageHeader(surface.get_size(), cv.IPL_DEPTH_8U, 3)
    image_string = surface_to_string(surface)
    cv.SetData(cv_image, image_string)
    return cv_image

def cvimage_grayscale(cv_image):
    """Converts a cvimage into grayscale"""
    grayscale = cv.CreateImage(cv.GetSize(cv_image), 8, 1)
    cv.CvtColor(cv_image, grayscale, cv.CV_RGB2GRAY)
    return grayscale

# def cvimage_to_pygame(image):
#     """Convert cvimage into a pygame image"""
#     image_rgb = cv.CreateMat(image.height, image.width, cv.CV_8UC3)
#     cv.CvtColor(image, image_rgb, cv.CV_BGR2RGB)
#     return pygame.image.frombuffer(image.tostring(), cv.GetSize(image_rgb),
#                                    "RGB")

def cvimage_to_pygame( frame, color=False ):
    if frame is None:
        return
    frame_size = frame.shape[1::-1]
    if color:
        conversion_type = cv.COLOR_GRAY2RGB
    else:
        conversion_type = cv.COLOR_BGR2RGB

    rgb_frame = cv.cvtColor( frame, conversion_type )
    pygame_frame = pygame.image.frombuffer( rgb_frame.tostring(), frame_size, 'RGB' )
    return pygame_frame

def detect_faces( cv_image ):
    """Detects faces based on haar. Returns points"""
    return face_cascade.detectMultiScale(cv_image, 1.3, 5)

def draw_from_points(cv_image, points):
    """Takes the cv_image and points and draws a rectangle based on the points.
    Returns a cv_image."""
    for (x, y, w, h) in points:
        print( "trace" )
        cv.rectangle(cv_image, (x, y), (x + w, y + h), 255)
    return cv_image


camera = cv.VideoCapture(0)
# https://techoverflow.net/2018/12/18/how-to-set-cv2-videocapture-image-size/
camera.set(cv.CAP_PROP_FRAME_WIDTH, 1280)
camera.set(cv.CAP_PROP_FRAME_HEIGHT, 720)
pygame.init()
pygame.display.set_caption("OpenCV camera stream on Pygame")
screen = pygame.display.set_mode([1280,720])

try:
    while True:
        ret, cv_image = camera.read()
        cv_image = cv2.flip( cv_image, 1 )
        screen.fill([0,0,0])

        #points = detect_eyes(cv_image, storage) + \
        #        detect_nose(cv_image, storage) + \
        #        detect_mouth(cv_image, storage)
        points = detect_faces( cv_image )  # Get points of faces.

        cv_image = draw_from_points(cv_image, points)  # Draw points

        screen.fill([0, 0, 0])  # Blank fill the screen
        
        try:
            screen.blit(cvimage_to_pygame(cv_image), (0, 0))  # Load new image on screen
        except:
            print( traceback.format_exc() )
        
        pygame.display.update()

except (KeyboardInterrupt,SystemExit):
    pygame.quit()
    cv.destroyAllWindows()