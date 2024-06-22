import subprocess
import argparse
from moviepy.editor import VideoFileClip, concatenate_videoclips
import moviepy.audio.fx.all as afx

CONSTANT_FPS = 60

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

def concat_videos(videos: list[str], output: str):
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