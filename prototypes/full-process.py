# This prototype goes through the whole process of creating a video for the
# conference. It uses the previous prototypes. It performs the following tasks:
#
# 1. It resamples the videos to have 60 FPS each.
# 2. It opens the files with moviepy.
# 3. Normalizes the audios and set them all to the same x-factor volume.
# 4. It concatenates the videos.
# 5. (Future version.) Creates the opening and closing info slides.
# 6. (Future version.) Adds the intro audio to the opening slides.

import subprocess
import argparse
from moviepy.editor import VideoFileClip, concatenate_videoclips

CONSTANT_FPS = 60

def resample_video(input_file: str, output_file: str, fps = CONSTANT_FPS):
  """
  This function resamples a video to a specific FPS using ffmpeg.

  Args:
      input_file: Path to the input video file (string).
      output_file: Path to the output resampled video file (string).
      fps: Desired frame rate (integer, default: 60).
  """
  command = ["ffmpeg", "-i", input_file, "-c:v", "libx264", "-c:a", "aac", "-r", str(fps), output_file]
  subprocess.run(command, check=True)

def concat_videos(videos: str, output: str, temp_folder: str):
  """
  This function concatenates multiple video files into a single video file.

  Args:
      videos: List of paths to the input video files (list of strings).
      output: Path to the output concatenated video file (string).
  """
  clips = [VideoFileClip(video) for video in videos]
  final_clip = concatenate_videoclips(clips, method="compose")
  final_clip.write_videofile(output, temp_audiofile='temp-audio.m4a',
    remove_temp=True, codec="libx264", audio_codec="aac", fps=CONSTANT_FPS)
  
  for clip in clips:
    clip.close()

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Video Preparer")
  parser.add_argument("input_files", nargs="+", help="Path to the input video files.")
  parser.add_argument("output_file", help="Path to the output concatenated video file.")
  parser.add_argument("temp_folder", help="Path to the temporary working directory.")
  parser.add_argument("--working_dir", help="Path to the working directory.")
  parser.add_argument("--fps", type=int, default=CONSTANT_FPS, help="Desired frame rate (default: 60)")
  args = parser.parse_args()

  input_files = args.input_files
  output_file = args.output_file
  temp_folder = args.temp_folder
  fps = args.fps
  
  working_dir = args.working_dir if args.working_dir else None

  # Call the functions with the provided arguments
  for input_file in input_files:
    input_filepath = f"{working_dir}{input_file}" if working_dir else input_file
    resampled_file = f"{temp_folder}/{input_file}"
    resample_video(input_filepath, resampled_file, fps)

  concat_videos(input_files, output_file, temp_folder)