#!/bin/bash
VIDSOURCE="rtsp://192.168.194.141:8554/video"
VIDEO_OPTS="-vcodec libx264"
# VIDEO_OPTS="-s 854x480 -c:v libx264 -b:v 800000"
# OUTPUT_HLS="-hls_time 10 -hls_list_size 10 -start_number 1"
ffmpeg -y -i "$VIDSOURCE" $VIDEO_OPTS vid.mp4
