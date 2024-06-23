from moviepy.editor import *
import os

def get_duration(video_path: str) -> int:
  return VideoFileClip(video_path).duration

this_file_path = os.path.abspath(__file__)
relative_file_path = '../sample-data/output/W1F4-Virtual.mp4'
video_path = os.path.abspath(os.path.join(
  os.path.dirname(this_file_path), 
  relative_file_path
))

print("Duration type:", type(get_duration(video_path)))
print("Duration:", get_duration(video_path))