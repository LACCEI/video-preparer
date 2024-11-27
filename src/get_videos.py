# Sample script to download videos.

import dataretriever as dr
from dotenv import dotenv_values
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
path_to_env = os.path.abspath(current_dir + '/' + '../.env')
config = dotenv_values(path_to_env)

output_dir = os.path.abspath(current_dir + '/' + '../sample-data/videos')

# Videos to download.
videos_ids = [1172, 1366, 1378, 1424, 1448, 1471]

conf = dr.CTInterface(config["CONFERENCE_ENDPOINT"], config["PASSWORD"])

for video_id in videos_ids:
  print(f'Downloading video {video_id}.', end='\r')
  conf.get_video(video_id, output_dir + f'/{video_id}.mp4')
  print(f'Downloaded video {video_id}.     ')