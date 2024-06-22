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

demo_session_id = list(schedule.keys())[0]

output_video_path = current_dir + '/../sample-data/original-videos'
os.makedirs(output_video_path, exist_ok=True)

paper_i = 0
total_papers = len(schedule[demo_session_id]["papers"])

print("Starting downloads.")

for paper in schedule[demo_session_id]["papers"]:
  paper_i += 1
  print(f"\nDownloading video {paper_i}/{total_papers}.")
  paper_id = paper["paper_id"]
  success = ct_int.get_video(
    paper_id,
    output_video_path + '/' + paper_id + '.mp4'
  )[0]
  print("Successful.") if success else print("Failed.")

print("\nDownloading faulty video.")
success = ct_int.get_video(
  "10",
  output_video_path + '/faulty.mp4'
)[0]
print("Successful.") if success else print("Failed.")

print("\nPrototype complete.")