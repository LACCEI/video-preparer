import subprocess
import argparse
from moviepy.editor import *
import moviepy.audio.fx.all as afx

CONSTANT_FPS = 60

class Utils:
  @staticmethod
  def resample_video(
    input_file: str,
    output_file: str,
    fps: int = CONSTANT_FPS
  ):
    command = [
      "ffmpeg", "-i", input_file, "-c:v", "libx264", "-c:a",
      "aac", "-r", str(fps), output_file
    ]
    subprocess.run(command, check=True)

  @staticmethod
  def convert_date_format(date_in: str) -> str:
    date_out = datetime.strptime(date_in, "%Y-%m-%d")
    return date_out.strftime("%A, %B %d, %Y")
  
  @staticmethod
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

def concat_videos(
  videos: list[VideoClip|CompositeVideoClip],
  output: str,
  intro_music_path: AudioFileClip):
  clips = [
    VideoFileClip(video).fx(afx.audio_normalize)
    for video in videos
  ]

  final_clip = concatenate_videoclips(clips, method="compose")
  final_clip.write_videofile(
    output, temp_audiofile='temp-audio.m4a',
    remove_temp=True, codec="libx264", audio_codec="aac",
    fps=CONSTANT_FPS
  )

  for clip in clips:
    clip.close()

def prepare_video_for_session():
  pass