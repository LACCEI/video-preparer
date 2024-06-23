import os
from moviepy.editor import *
# from moviepy.video.fx.resize import resize

def get_largest_dimension(list_of_sizes: list[list[int, int]]) -> list[int, int]:
  max_width = 0
  max_height = 0

  for size in list_of_sizes:
    if size[0] > max_width:
      max_width = size[0]
    if size[1] > max_height:
      max_height = size[1]

  return [max_width, max_height]

def get_resize_ratio_to_fit_max_dimension(
  original_size: list[int, int],
  max_dimension: list[int, int]
) -> float:
  smallest_width_difference = max_dimension[0] - original_size[0]
  smallest_height_difference = max_dimension[1] - original_size[1]

  if smallest_height_difference > smallest_width_difference:
    return max_dimension[0] / original_size[0]
  else:
    return max_dimension[1] / original_size[1]

def get_ratio(width: int, height: int) -> float:
  return width / height

current_dir = os.path.dirname(os.path.abspath(__file__))
videos_folder = os.path.abspath(os.path.join(current_dir, '../sample-data/temp'))

video_1 = os.path.join(videos_folder, '116-resampled.mp4')
video_2 = os.path.join(videos_folder, '831-resampled.mp4')
video_3 = os.path.join(videos_folder, '579-resampled.mp4')

video_1 = VideoFileClip(video_1)
video_2 = VideoFileClip(video_2)
video_3 = VideoFileClip(video_3)

print("Details of videos for testing.")
print(f"Video 1 Size: {video_1.size}")
print(f"Ratio: {get_ratio(video_1.size[0], video_1.size[1])}")
print(f"Video 2 Size: {video_2.size}")
print(f"Ratio: {get_ratio(video_2.size[0], video_2.size[1])}")
print(f"Video 3 Size: {video_3.size}")
print(f"Ratio: {get_ratio(video_3.size[0], video_3.size[1])}")

larget_sizes = get_largest_dimension([video_1.size, video_2.size, video_3.size])
print(f"\nLargest size: {larget_sizes}")

# Change the FPS of the videos.
video_1 = video_1.subclip(0, 10)
video_2 = video_2.subclip(0, 10)
video_3 = video_3.subclip(0, 10)

videos = [video_1, video_2, video_3]

print("")
for i in range(len(videos)):
  videos[i] = videos[i].resize(get_resize_ratio_to_fit_max_dimension(videos[i].size, larget_sizes))

print("\nDetails of videos after resizing.")
print(f"Video 1 Size: {videos[0].size}")
print(f"Video 2 Size: {videos[1].size}")
print(f"Video 3 Size: {videos[2].size}")

final_clip = concatenate_videoclips(videos, method="compose")


# Concatenate the videos.
final_clip.write_videofile(
  os.path.abspath(os.path.join(current_dir, '../sample-data/resizing-output.mp4')),
  codec="libx264", audio_codec="aac", fps=24
)


