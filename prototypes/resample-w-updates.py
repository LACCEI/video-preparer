# FAILED PROTOTYPE.

import subprocess
import shlex

def resample_video(input_file, output_file, fps=24):
  """
  This function resamples a video to a specific FPS using ffmpeg with progress updates.

  Args:
      input_file: Path to the input video file (string).
      output_file: Path to the output resampled video file (string).
      fps: Desired frame rate (integer, default: 24).
  """

  # Build the ffmpeg command with progress reporting option
  command_str = f"ffmpeg -i {input_file} -c:v libx264 -c:a aac -r {fps} {output_file} -progress -"
  command = shlex.split(command_str)  # Split string into command list

  # Define a function to handle output lines
  def handle_output(output):
    # Split the output into lines
    lines = output.split("\n")
    # Find the last line that starts with "frame="
    for line in reversed(lines):
      if line.startswith("frame="):
        # Split the line into words
        words = line.split()
        # Check that the line contains at least two words
        if len(words) < 2:
          return
        # Split the second word on colons
        progress_data = words[1].split(":")
        # Check that the second word contains a colon
        if len(progress_data) < 2:
          return
        # Extract progress information from relevant lines
        processed_frames = int(progress_data[0])
        total_frames = int(progress_data[1])
        # Calculate and print progress percentage
        progress = (processed_frames / total_frames) * 100
        print(f"Resampling progress: {progress:.2f}%")
        return

  # Execute the ffmpeg command and capture the output
  result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)
  # Handle the output
  handle_output(result.stdout)

  # Print success message after completion
  print(f"\nVideo resampled to {fps} fps and saved as {output_file}")

# Example usage
input_file = "../sample-data/Contribution_103_b.mp4"
output_file = "../sample-data/Contribution_103_b_resampled2.mp4"
resample_video(input_file, output_file)
