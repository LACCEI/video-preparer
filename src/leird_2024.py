import vidpre
import os

from dotenv import dotenv_values

current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_env = os.path.abspath(current_dir + '/' + '../.env')
config = dotenv_values(path_to_env)

times_info = {
  'original_title': 'Virtual',
  'original': 'US/Eastern',
  'others': [
    # {
    #   'title': 'Miami',
    #   'timezone': 'EST5EDT',
    # }
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

vidpre.prepare_videos_for_conference(
  config['CONFERENCE_ENDPOINT'],
  config['PASSWORD'],
  out_work_dir,
  temp_work_dir,
  slides_instructions,
  schedule_file
)