import math
import sys
from PIL import Image, ImageDraw

# pour une projection mercator

dot_color = (255, 0, 0)

coord = [ 48.85837174162911, 2.294481998444337 ]

def get_x(lng):
    return int(round((img_width / 2 ) + ( lng * img_width / 360 )))

def get_y(lat):
    lat_rad=lat / 180 * math.pi
    return int(round(( img_height / 2) - ( img_width / (2 * math.pi) * math.log( math.tan((math.pi / 4) + (lat_rad / 2)) ))))



with Image.open("carte-du-monde.png") as im:

    img_width, img_height = im.size

    x = get_x(coord[1])
    y = get_y(coord[0])
    print((x,y))
    draw = ImageDraw.Draw(im)
    draw.point( [ (x,y) ], dot_color )

    # write to stdout
    im.save("/Users/david.delgado/Documents/gitrepos/perso/worldmap/outfile.png", "PNG")
