# This is a prototype program that takes a video a resamples it to 60 FPS. This
# solution uses the ffmpeg program called using a Python subprocess.

import subprocess
from moviepy.editor import VideoFileClip

def resample_video(input_file, output_file, fps = 60):
  """
  This function resamples a video to a specific FPS using ffmpeg.

  Args:
      input_file: Path to the input video file (string).
      output_file: Path to the output resampled video file (string).
      fps: Desired frame rate (integer, default: 60).
  """
  command = ["ffmpeg", "-i", input_file, "-c:v", "libx264", "-c:a", "aac", "-r", str(fps), output_file]
  subprocess.run(command, check=True)

def print_video_fps(path_to_video: str, video_filename: str):
  """
  This function prints the FPS of a video using the moviepy library.

  Args:
      path_to_video: Path to the video file (string).
  """
  video = VideoFileClip(path_to_video + video_filename)
  fps = video.fps
  print(f"Video \"{video_filename}\" FPS: {fps}")
  video.close()

# Example usage.
path_to_file = "../sample-data/"
input_file = "Contribution_100_b.mp4"
output_file = "Contribution_100_b_resampled.mp4"

print_video_fps(path_to_file, input_file)
print("Performing resampling.")
resample_video(path_to_file + input_file, path_to_file + output_file)
print_video_fps(path_to_file, output_file)
