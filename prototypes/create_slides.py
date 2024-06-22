from moviepy.editor import *
from datetime import datetime
import os

session_information = {
  "Title": "W1F4-Virtual",
  "Date": "2024-07-17",
  "Times": [{
    "Timezone": "Costa Rica (CST)",
    "Start": "07:00",
    "End": "08:10"
  },
  {
    "Timezone": "Miami (EDT)",
    "Start": "09:00",
    "End": "10:10"
  }]
}

def convert_date_format(date_in: str) -> str:
  date_out = datetime.strptime(date_in, "%Y-%m-%d")
  return date_out.strftime("%A, %B %d, %Y")

def get_ratio(original: int, target: int) -> float:
  return target / original

def create_instructions_clip(
  duration: int,
  text: str,
  banner_img: str
) -> VideoClip:
  background = ColorClip(size=(1920, 1080), color=[255, 255, 255])
  banner_clip = ImageClip(banner_img)
  banner_clip = banner_clip.resize(get_ratio(banner_clip.size[0], 1880))
  instruction = TextClip(text, fontsize=48, color='black', align='center')
  return CompositeVideoClip([
    background.set_duration(duration),
    banner_clip.set_duration(duration).set_position(('center', 20)),
    instruction.set_duration(duration).set_position(('center', 540 + 60))
  ], use_bgclip = True)

def create_session_clip(
  duration: int,
  session_information: dict,
  banner_img: str
) -> VideoClip:
  background = ColorClip(size=(1920, 1080), color=[255, 255, 255])
  banner_clip = ImageClip(banner_img)
  banner_clip = banner_clip.resize(get_ratio(banner_clip.size[0], 1880))
  text = "Session: " + session_information["Title"] + "\n"
  text += "Date: " + convert_date_format(session_information["Date"]) + "\n\n"
  for time in session_information["Times"]:
    text += time["Timezone"] + ": "
    text += time["Start"] + "-"
    text += time["End"] + "\n"
  title = TextClip(text, fontsize=48, color='black', align='center')
  return CompositeVideoClip([
    background.set_duration(duration),
    banner_clip.set_duration(duration).set_position(('center', 20)),
    title.set_duration(duration).set_position(('center', 540 + 60))
  ], use_bgclip = True)

current_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.abspath(current_path + '/../sample-data/banner.jpg')

instructions = "Session discussion starting now!\n\n"
instructions += "Feel free to unmute your microphone\nand turn on your camera."
video_ins1 = create_instructions_clip(10, instructions, image_path)

video_ins2 = create_session_clip(10, session_information, image_path)

instructions = "Important information.\n\n"
instructions += "Please keep your microphone muted and camera turned off.\n"
instructions += "Please use the chat to ask questions, and keep in mind\n"
instructions += "that the session is being recorded. Enjoy!"
video_ins3 = create_instructions_clip(10, instructions, image_path)

output_path = current_path + '/../sample-data/session_sample.mp4'
output_video = concatenate_videoclips([video_ins1, video_ins2, video_ins3], method="compose")
output_video.write_videofile(output_path, fps=60)
