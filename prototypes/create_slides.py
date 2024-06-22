from moviepy.editor import *
import os

session_information = {
  "Title": "Session Title"
}

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

def create_banner_clip(banner_img: str) -> VideoClip:
  clip = ImageClip(banner_img)
  return clip

current_path = os.path.dirname(os.path.abspath(__file__))
image_path = os.path.abspath(current_path + '/../sample-data/banner.jpg')

output_path = current_path + '/../sample-data/instructions1.mp4'
instructions = "Session discussion starting now!\n\n"
instructions += "Feel free to unmute your microphone\nand turn on your camera."
video = create_instructions_clip(10, instructions, image_path)
video.write_videofile(output_path, fps=60)

output_path = current_path + '/../sample-data/instructions2.mp4'
instructions = "Important information.\n\n"
instructions += "Please keep your microphone muted and camera turned off.\n"
instructions += "Please use the chat to ask questions, and keep in mind\n"
instructions += "that the session is being recorded. Enjoy!"
video = create_instructions_clip(10, instructions, image_path)
video.write_videofile(output_path, fps=60)
