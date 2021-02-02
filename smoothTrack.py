import math
import json

startTS = 1604836920000
step = 20000000
boatID = "dadabato"

fileTrack = open("track.json")
fileSmoothTrack = "smoothTrack.json"

boatTrack = json.loads(fileTrack.read())["track"]

boatSteps = {}

def getSmoothTrack(startTS, step, boatSteps, boatID, boatTrack):
    # 1st timestamp = startTS + n * step and > 1st track TS
    ts = int(max(startTS, int(boatTrack[0]["ts"])) / step) * step
    trackLength = len(boatTrack)
    # Interpolate position in a track for every frame
    for trackDot in range(0, trackLength - 1):
        # current dot in the track
        currentTs = int(boatTrack[trackDot]["ts"])
        currentLon = boatTrack[trackDot]["lon"]
        currentLat = boatTrack[trackDot]["lat"]
        # next dot in the track
        nextTs = int(boatTrack[trackDot+1]["ts"])
        nextLon = boatTrack[trackDot+1]["lon"]
        nextLat = boatTrack[trackDot+1]["lat"]
        # east > west speed
        ewSpeed = (((nextLon + 360) % 360) - ((currentLon + 360) % 360)) / (nextTs - currentTs)
        # south > north speed
        snSpeed = (nextLat - currentLat) / (nextTs - currentTs)
        stepKey = str(currentTs) + "#" + boatID
        # create a location for the current track dot
        boatSteps[stepKey] = {}
        boatSteps[stepKey]["ts"] = currentTs
        boatSteps[stepKey]["boatID"] = boatID
        boatSteps[stepKey]["lon"] = currentLon
        boatSteps[stepKey]["lat"] = currentLat
        boatSteps[stepKey]["realDot"] = True
        # create locations for every steps until next track dot
        while ( ts < nextTs ):
            stepKey = str(ts) + "#" + boatID
            boatSteps[stepKey] = {}
            boatSteps[stepKey]["ts"] = ts
            boatSteps[stepKey]["boatID"] = boatID
            boatSteps[stepKey]["lon"] = (((currentLon + (ts - currentTs) * ewSpeed) + 180) % 360) - 180
            boatSteps[stepKey]["lat"] = currentLat + (ts - currentTs) * snSpeed
            ts = int( ts / step) * step + step
    return boatSteps

with open(fileSmoothTrack, "w") as write_file:
    json.dump(getSmoothTrack(startTS, step, boatSteps, boatID, boatTrack), write_file)
