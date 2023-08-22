
#!/usr/bin/env python
# coding=utf-8 

# juneleungchan@163.com 
# 20230819

####################
# 从开始时间码到结束时间码之间，每隔指定时间截图静帧到图库
# From the start timecode to the end timecode, grab still frames to the gallery every specified time
####################

import os,sys
sys.path.append("/Library/Application Support/Blackmagic Design/DaVinci Resolve/Developer/Scripting/Modules")
import DaVinciResolveScript as dvr_script

def timecode_to_frames(timecode):
    return sum(f * int(t) for f,t in zip((3600*framerate, 60*framerate, framerate, 1), timecode.split(':')))

def frames_to_timecode(frames):
    timecode = '{0:02d}:{1:02d}:{2:02d}:{3:02d}'.format(int(frames / (3600*framerate)),
                                                        int(frames / (60*framerate) % 60),
                                                        int(frames / framerate % 60),
                                                        int(frames % framerate))
    return timecode


####################
# params input
####################
timecode_begin = '00:00:00:00' #hrs,min,sec,frm
timecode_end   = '00:02:00:19'
framerate = 24
stepDuration = 10

####################
# DR
####################
resolve = dvr_script.scriptapp("Resolve")
project = resolve.GetProjectManager().GetCurrentProject()

if not project:
    print("No project is loaded")
    sys.exit()

timeline = project.GetCurrentTimeline()

print("working on "+timeline.GetName())

for frms in range(timecode_to_frames(timecode_begin),timecode_to_frames(timecode_end)+1, stepDuration):
    timecode = frames_to_timecode(frms)
    print(timecode)
    timeline.SetCurrentTimecode(timecode)
    galleryStill = timeline.GrabStill()

# Gallery = project.GetGallery()
# galleryStillAlbum = Gallery.GetCurrentStillAlbum()
# galleryStillAlbum.ExportStills([galleryStill], folderPath, filePrefix, format)
