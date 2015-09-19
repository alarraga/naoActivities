import sys

from naoqi import ALProxy


def main(robotIP):

    try:
        postureProxy = ALProxy("ALRobotPosture", robotIP, 9559)
    except Exception, e:
        print "Could not create proxy to ALRobotPosture"
        print "Error was: ", e

    postureProxy.goToPosture("LyingBelly", 1.0)
    
    print postureProxy.getPostureFamily()
