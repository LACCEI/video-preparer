import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
abs_path = os.path.abspath(current_dir + '/' + '../src')
sys.path.insert(0, abs_path)

import dataretriever
from dotenv import dotenv_values

path_to_env = os.path.abspath(current_dir + '/' + '../.env')

config = dotenv_values(path_to_env)

ct_int = dataretriever.CTInterface(
  config['CONFERENCE_ENDPOINT'],
  config['PASSWORD']
)

schedule = ct_int.get_schedule(
  current_dir + '/../sample-data/schedule-temp.xml'
)

demo_session_id = list(schedule.keys())[2]
output_video_path = current_dir + '/../sample-data/original-videos'

print("Starting downloads.")

def print_status(paper_i, status):
  print(f"Paper {schedule[demo_session_id]['papers'][paper_i]['paper_id']} downloaded: {status}.")

result = ct_int.get_session_videos(
  schedule[demo_session_id],
  output_video_path,
  print_status
)

if result[0] == 0:
  print("All videos downloaded successfully.")

print("Prototype complete.")