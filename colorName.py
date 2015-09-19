from collections import namedtuple
from math import sqrt
import random
try:
    import Image
except ImportError:
    from PIL import Image


from naoqi import ALProxy
import os
import sys
import time
import webcolors


Point = namedtuple('Point', ('coords', 'n', 'ct'))
Cluster = namedtuple('Cluster', ('points', 'center', 'n'))
PORT = 9559

def get_points(img):
    points = []
    w, h = img.size
    for count, color in img.getcolors(w * h):
        points.append(Point(color, 3, count))
    return points

rtoh = lambda rgb: '#%s' % ''.join(('%02x' % p for p in rgb))

def colorz(img, n=3):
    img.thumbnail((200, 200))
    w, h = img.size

    points = get_points(img)
    clusters = kmeans(points, n, 1)
    rgbs = [map(int, c.center.coords) for c in clusters]
    return map(rtoh, rgbs)

def euclidean(p1, p2):
    return sqrt(sum([
        (p1.coords[i] - p2.coords[i]) ** 2 for i in range(p1.n)
    ]))

def calculate_center(points, n):
    vals = [0.0 for i in range(n)]
    plen = 0
    for p in points:
        plen += p.ct
        for i in range(n):
            vals[i] += (p.coords[i] * p.ct)
    return Point([(v / plen) for v in vals], n, 1)

def kmeans(points, k, min_diff):
    clusters = [Cluster([p], p, p.n) for p in random.sample(points, k)]

    while 1:
        plists = [[] for i in range(k)]

        for p in points:
            smallest_distance = float('Inf')
            for i in range(k):
                distance = euclidean(p, clusters[i].center)
                if distance < smallest_distance:
                    smallest_distance = distance
                    idx = i
            plists[idx].append(p)

        diff = 0
        for i in range(k):
            old = clusters[i]
            center = calculate_center(plists[i], old.n)
            new = Cluster(plists[i], center, old.n)
            clusters[i] = new
            diff = max(diff, euclidean(old.center, new.center))

        if diff < min_diff:
            break

    return clusters







IP = "192.168.0.1" #The IP address of NAO robot
PORT = 9559


cam = ALProxy("ALVideoDevice", IP, PORT)
resolution = 2 # VGA (640*480px)
colorSpace = 11 # RGB
videoClient = cam.subscribe("python_client", resolution, colorSpace, 5)

t0 = time.time()
# get image from camera.
naoImage = cam.getImageRemote(videoClient)

t1 = time.time()
# Time the image transfer.
print "acquisition delay ", t1 - t0
cam.unsubscribe(videoClient)

# Width is the width of the image.
Width = naoImage[0]

# Height is the height of the image.
Height = naoImage[1]

# image[6] is an array of ASCII chars which is used for saving image data.
array = naoImage[6]

# PIL Image is created by using fromstring() method
image = Image.fromstring("RGB", (Width, Height), array)



import re
re_color = re.compile('#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})')
from math import sqrt

def color_to_rgb(color):
    return tuple(int(x, 16) / 255.0 for x in re_color.match(color).groups())

def similarity(color1, color2):
    """Computes the pearson correlation coefficient for two colors. The result
    will be between 1.0 (very similar) and -1.0 (no similarity)."""
    c1 = color_to_rgb(color1)
    c2 = color_to_rgb(color2)

    s1 = sum(c1)
    s2 = sum(c2)
    sp1 = sum(map(lambda c: pow(c, 2), c1))
    sp2 = sum(map(lambda c: pow(c, 2), c2))
    sp = sum(map(lambda x: x[0] * x[1], zip(c1, c2)))

    return (sp - (s1 * s2 / 3.0)) / sqrt((sp1 - pow(s1, 2) / 3.0) * (sp2 - pow(s2, 2) / 3.0))

color_names = {
    '#ff0000': 'red',
    '#00ff00': 'green',
    '#0000ff': 'blue',
    '#ffff00': 'yellow'
    # add more color definitions here
}

def find_name(color):
    sim = [(similarity(color, c), name) for c, name in color_names.items()]
    return max(sim, key=lambda x: x[0])[1]

def main(IP, PORT):
    defx,y,z = colorz(image, 3)
    print colorz(image, 3)

    tts = ALProxy("ALTextToSpeech",IP, PORT)
    tts.say("The color is" + find_name(z))
 



