import math
import sys
from PIL import Image, ImageDraw

import json

# frames to video
import cv2
import numpy as np
import glob

imageWorldMap = "carte-du-monde.png"
file_track = open("track.json")
track = json.loads(file_track.read())["track"]
fileSmoothedTrack = open("smoothTrack.json")
smoothedTrack = json.loads(fileSmoothedTrack.read())

# pour une projection mercator

dot_color = (255, 0, 0)

coord = [ 48.85837174162911, 2.294481998444337 ]

def getX(lng, img_width):
    return int(round((img_width / 2 ) + ( lng * img_width / 360 )))

def getY(lat, img_width, img_height):
    lat_rad=lat / 180 * math.pi
    return int(round(( img_height / 2) - ( img_width / (2 * math.pi) * math.log( math.tan((math.pi / 4) + (lat_rad / 2)) ))))


def drawTrack(track):
    with Image.open(imageWorldMap) as im:

        img_width, img_height = im.size

        for pos in track:
            x = getX(float(pos["lon"]), img_width)
            y = getY(float(pos["lat"]), img_width, img_height)
            draw = ImageDraw.Draw(im)
            draw.point( [ (x,y) ], dot_color )

        im.save("/Users/david.delgado/Documents/gitrepos/perso/worldmap/outfile.png", "PNG")

def drawSmoothedTrack(smoothedTrack):
    with Image.open(imageWorldMap) as im:

        img_width, img_height = im.size

        for key in smoothedTrack.keys():
            pos = smoothedTrack[key]
            x = getX(float(pos["lon"]), img_width)
            y = getY(float(pos["lat"]), img_width, img_height)
            draw = ImageDraw.Draw(im)
            draw.point( [ (x,y) ], dot_color )

        im.save("/Users/david.delgado/Documents/gitrepos/perso/worldmap/outfile.png", "PNG")


def generateFrames(smoothedTrack):
    with Image.open(imageWorldMap) as img:

        img_width, img_height = img.size
        frame = 0

        for key in smoothedTrack.keys():
            im = img.copy()
            img_width, img_height = im.size
            pos = smoothedTrack[key]
            x = getX(float(pos["lon"]), img_width)
            y = getY(float(pos["lat"]), img_width, img_height)
            draw = ImageDraw.Draw(im)
            draw.point( [ (x,y) ], dot_color )
            frame = frame + 1
            im.save(f'/Users/david.delgado/Documents/gitrepos/perso/worldmap/frames/{str(frame).zfill(10)}.png', "PNG")

def framesToVideo():
    img_array = []
    for filename in glob.glob('/Users/david.delgado/Documents/gitrepos/perso/worldmap/frames/*.png'):
        img = cv2.imread(filename)
        height, width, layers = img.shape
        size = (width,height)
        img_array.append(img)
    out = cv2.VideoWriter('/Users/david.delgado/Documents/gitrepos/perso/worldmap/project.avi',cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
    for i in range(len(img_array)):
        out.write(img_array[i])
    out.release()

generateFrames(smoothedTrack)
# framesToVideo
