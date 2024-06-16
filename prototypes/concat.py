# This is a demonstration on how to concatenate two clips using
# the moviepy library. I use subclip to limit the duration of the
# clips to 10 seconds becuase it takes too long in the dev
# environment. The output is saved as output.mp4 in the
# sample-data folder.

# Developer notes:
# This implementation solves many issues:
# 1. There is a glitch in the output video if not using the method="compose"
#   parameter in the concatenate_videoclips function.
# 2. There is no audio in the output video. This is because the audio codec
#   is not specified in the write_videofile function. The audio codec is
#   specified as "aac" in the write_videofile function.
# 3. The output video has a different frame rate than the input videos. This
#   issue hasn't been solved yet. However, resampling the videos with ffmpeg
#   is believed to be a solution.

# Issues that would/may still need a solution:
# 1. Videos many times have different sizes. The moviepy module can handle
#   those cases by using the size of the biggest video. However, there should
#   be consistency through the videos. There should be a mechanisms that
#   ensures the videos size even if all of them are different and not the
#   standard with 16:9 ratio.
# 2. The volume across videos has been a repeating issue through all the
#   conferences. Ensure there is a mechanism that tries to keep the volume at
#   the same level through the videos and among them.

from moviepy.editor import VideoFileClip, concatenate_videoclips

def get_lowest_fps(videos: VideoFileClip):
  lowest_fps = videos[0].fps
  for video in videos:
    if video.fps < lowest_fps:
      lowest_fps = video.fps
  return lowest_fps

def concat_videos(videos, output):
  clips = [VideoFileClip(video).subclip(0, 20) for video in videos]
  final_clip = concatenate_videoclips(clips, method="compose")

  # for clip in clips:
  #   print(f"Clip {clip.filename} fps:", clip.fps)

  fps = get_lowest_fps(clips)

  # final_clip.write_videofile(output, fps=60)
  final_clip.write_videofile(output, temp_audiofile='temp-audio.m4a',
    remove_temp=True, codec="libx264", audio_codec="aac", fps=fps)
  
  for clip in clips:
    clip.close()

path = '../sample-data/'
test_videos = []
test_videos.append(path + 'Contribution_100_b.mp4')
test_videos.append(path + 'Contribution_103_b.mp4')

concat_videos(test_videos, path + 'output7.mp4')