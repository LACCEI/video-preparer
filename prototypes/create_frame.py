from moviepy.editor import *
from moviepy.video.VideoClip import TextClip
import os

# Create a TextClip with "Hello World" text.
text_clip = TextClip("Hello World", fontsize=70, color='white', size=(1920, 1080))

# Set the duration of the video to 3 seconds.
duration = 3

# Create a video clip with the TextClip
video_clip = CompositeVideoClip([text_clip.set_duration(duration)])

# Set the output file.
current_path = os.path.dirname(os.path.abspath(__file__))
output_path = current_path + '/../sample-data/hello_world.mp4'

# Write the video clip to the output file.
video_clip.write_videofile(output_path, fps=60)