# Sample script to generate slides for a session.

import vidpre
import os
from moviepy.editor import *
import vidpro

from dotenv import dotenv_values

current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_env = os.path.abspath(current_dir + '/' + '../.env')
config = dotenv_values(path_to_env)

times_info = {
  'original_title': 'Costa Rica',
  'original': 'America/Costa_Rica',
  'others': [
    {
      'title': 'Miami',
      'timezone': 'EST5EDT',
    }
  ]
}

slides_instructions = {
  'opening_instructions': "",
  'closing_instructions': "",
  'times_info': times_info,
  'path_to_banner_image': \
    os.path.abspath(current_dir + '/../sample-data/banner.jpg'),
  'path_to_intro_audio': \
    os.path.abspath(current_dir + '/../sample-data/intro-audio.m4a')
}

slides_instructions['opening_instructions'] = \
"""Important information.

Please keep your microphone muted and camera turned off.
Please use the chat to ask questions, and keep in mind
that the session is being recorded. Enjoy!"""

slides_instructions['closing_instructions'] = \
"""Session discussion starting now!

Feel free to unmute your microphone
and turn on your camera."""

out_work_dir = os.path.abspath(current_dir + '/../sample-data/output')
temp_work_dir = os.path.abspath(current_dir + '/../sample-data/temp')
schedule_file = os.path.abspath(current_dir + '/../sample-data/schedule-temp.xml')

# clip = vidpro.create_instructions_clip(10, slides_instructions['closing_instructions'], slides_instructions['path_to_banner_image'])
# clip.write_videofile(os.path.abspath(current_dir + '/../sample-data/closing.mp4'), codec="libx264", audio_codec="aac", fps=24)

intro = vidpro.create_instructions_clip(10, slides_instructions['opening_instructions'], slides_instructions['path_to_banner_image'])
session = vidpro.create_session_clip(10, vidpro.Utils.prepare_session_information({
  'session_title': 'T5F5-Virtual',
  'session_id': 'Session ID',
  'session_start': '2024-7-18 13:20',
  'session_end': '2024-7-18 14:30',
  # 'papers': [
  #   {
  #     'paper_id': 'Paper ID',
  #     'paper_title': 'Paper Title',
  #     'video_url': 'Video URL'
  #   }
  # ]
}, times_info), slides_instructions['path_to_banner_image'])

intro_music = AudioFileClip(slides_instructions['path_to_intro_audio']).subclip(0, 20)
intro_music = intro_music.fx(afx.audio_normalize).audio_fadein(4).audio_fadeout(2)

intro_video = concatenate_videoclips([session, intro], method='compose').set_audio(intro_music)
intro_video.write_videofile(os.path.abspath(current_dir + '/../sample-data/t5f5-intro.mp4'), codec="libx264", audio_codec="aac", fps=24)