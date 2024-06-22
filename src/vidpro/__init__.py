import subprocess
import argparse
import pytz
import moviepy.audio.fx.all as afx

from moviepy.editor import *
from datetime import datetime

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

def resample_video(input_file: str, output_file: str, fps = CONSTANT_FPS):
  command = ["ffmpeg", "-i", input_file, "-c:v", "libx264",
  "-c:a", "aac", "-r", str(fps), output_file]
  subprocess.run(command, check=True)

def create_instructions_clip(
  duration: int,
  text: str,
  banner_img: str
) -> CompositeVideoClip:
  background = ColorClip(size=(1920, 1080), color=[255, 255, 255])
  banner_clip = ImageClip(banner_img)
  banner_clip = banner_clip.resize(Utils.get_ratio(banner_clip.size[0], 1880))
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
  banner_clip = banner_clip.resize(Utils.get_ratio(banner_clip.size[0], 1880))
  text = "Session: " + session_information["Title"] + "\n"
  text += "Date: " + session_information["Date"] + "\n\n"
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
  opening_instructions: str,
  closing_instructions: str,
  path_to_videos_folder: str,
  output_video_path: str,
  path_to_banner_image: str,
  path_to_intro_audio: str,
  fps: int = CONSTANT_FPS
) -> None:
  session_information_slide = Utils.prepare_session_information(
    session_info, times_info
  )

  opening_clip = create_instructions_clip(
    10, opening_instructions, path_to_banner_image
  )

  session_clip = create_session_clip(
    10, session_information_slide, path_to_banner_image
  )

  closing_clip = create_instructions_clip(
    10, closing_instructions, path_to_banner_image
  )

  intro_music = AudioFileClip(path_to_intro_audio).subclip(0, 20)
  intro_music = intro_music.fx(afx.audio_normalize).audio_fadein(4).audio_fadeout(2)

  videos_clips = []
  for paper in session_info['papers']:
    if not os.path.exists(os.path.join(path_to_videos_folder, paper['paper_id'] + '-resampled.mp4')):
      resample_video(
        os.path.join(path_to_videos_folder, paper['paper_id'] + '.mp4'),
        os.path.join(path_to_videos_folder, paper['paper_id'] + '-resampled.mp4'),
        fps
      )
    
    video_clip = VideoFileClip(
      os.path.join(path_to_videos_folder, paper['paper_id'] + '-resampled.mp4')
    ).fx(afx.audio_normalize)
    videos_clips.append(video_clip)
  
  concat_videos(
    [opening_clip, session_clip] + videos_clips + [closing_clip],
    output_video_path,
    intro_music
  )