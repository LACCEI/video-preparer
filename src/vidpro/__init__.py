import subprocess
import argparse
from moviepy.editor import *
from datetime import datetime
import pytz
import moviepy.audio.fx.all as afx

CONSTANT_FPS = 60

class Utils:
  @staticmethod
  def prepare_session_information(
    session_info: dict,
    times_info: dict
  ) -> dict:
    result = {
      'Title': session_info['session_title'],
      'Date': Utils.convert_date_format(session_info['session_start']),
      'Times': []
    }

    original_timezone = times_info['original']
    other_timezones = times_info['others']

    original_start_time = Utils.get_time_from_string(session_info['session_start'])
    original_end_time = Utils.get_time_from_string(session_info['session_end'])

    result['Times'].append({
      'Timezone': f"{times_info['original_title']} ({original_timezone})",
      'Start': original_start_time.strftime("%H:%M"),
      'End': original_end_time.strftime("%H:%M")
    })

    for timezone in other_timezones:
      start_time = Utils.convert_timezone(
        Utils.get_time_from_string(session_info['session_start']),
        original_timezone,
        timezone['timezone']
      ).strftime("%H:%M")
      end_time = Utils.convert_timezone(
        Utils.get_time_from_string(session_info['session_end']),
        original_timezone,
        timezone['timezone']
      ).strftime("%H:%M")

      result['Times'].append({
        'Timezone': f"{timezone['title']} ({timezone['timezone']})",
        'Start': start_time,
        'End': end_time
      })

    return result

  @staticmethod
  def convert_timezone(dt: datetime, from_tz: str, to_tz: str) -> datetime:
    from_timezone = pytz.timezone(from_tz)
    localized_time = from_timezone.localize(dt)
    to_timezone = pytz.timezone(to_tz)
    converted_dt = localized_time.astimezone(to_timezone)
    return converted_dt

  @staticmethod
  def get_time_from_string(time_string: str) -> datetime:
    return datetime.strptime(time_string, "%Y-%m-%d %H:%M")

  @staticmethod
  def convert_date_format(date_in: str) -> str:
    date_out = datetime.strptime(date_in, "%Y-%m-%d %H:%M")
    return date_out.strftime("%A, %B %d, %Y")
  
  @staticmethod
  def get_ratio(original: int, target: int) -> float:
    return target / original

def create_instructions_clip(
  duration: int,
  text: str,
  banner_img: str
) -> CompositeVideoClip:
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
) -> CompositeVideoClip:
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
    intro_music: AudioFileClip
  ) -> None:
  
  final_clip = concatenate_videoclips(videos, method="compose")
  final_clip = final_clip.set_audio(intro_music)
  final_clip.write_videofile(
    output, temp_audiofile='temp-audio.m4a',
    remove_temp=True, codec="libx264", audio_codec="aac",
    fps=CONSTANT_FPS
  )

def prepare_video_for_session(
  session_info: dict,
  times_info: dict,
  path_to_videos_folder: str,
  output_video_path: str,
  path_to_banner_image: str,
  path_to_intro_audio: str
):
  pass