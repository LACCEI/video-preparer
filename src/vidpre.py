import dataretriever
import vidpro
import os
import json

class Utils:
  @staticmethod
  def clear_videos_list(papers: list[dict], failed: list) -> list:
    for paper in papers:
      if paper['paper_id'] in failed:
        papers.remove(paper)
    return papers

  @staticmethod
  def get_videos(
    session: dict, temp_work_dir: str, ct_int: dataretriever.CTInterface
  ) -> tuple[list, list]:
    result = ct_int.get_session_videos(
      session,
      temp_work_dir
    )

    successful_list = Utils.clear_videos_list(
      session["papers"],
      result[1]
    )

    return (successful_list, result[1])

  @staticmethod
  def log_to_file(message: str, log_file: str) -> None:
    with open(log_file, "a") as file:
      file.write(message + "\n")

  @staticmethod
  def update_json_log_file(data: dict, log_file: str) -> None:
    with open(log_file, "w") as file:
      file.write(json.dumps(data, indent=2))


def prepare_videos_for_conference(
  conference_endpoint: str,
  password: str,
  output_video_path: str,
  temp_work_dir: str,
  slides_instructions: dict,
  schedule_file: str,
  refresh_schedule: bool = False
):
  ct_int = dataretriever.CTInterface(conference_endpoint, password)
  schedule = ct_int.get_schedule(schedule_file, refresh_schedule)
  total_sesions = len(schedule.keys())
  session_i = 0

  total_durations = {
    'description': 'Total duration of all sessions and their videos.',
    'total_sessions': 0,
    'sessions': []
  }
  
  for session_id in schedule:
    session_i += 1
    print(f"Processing session {session_i} of {total_sesions}.") # FIXME

    if os.path.exists(os.path.join(output_video_path, schedule[session_id]['session_title'] + '.mp4')):
      print(f"Video {schedule[session_id]['session_title']} already exists.")
      continue
    
    try:
      print("Downloading videos.") # FIXME
      schedule[session_id]['papers'], not_downloaded = Utils.get_videos(
        schedule[session_id], temp_work_dir, ct_int
      )

      if len(not_downloaded) > 0:
        print("Some videos could not be downloaded.") # FIXME
        Utils.log_to_file(
          f"Videos not downloaded for session {schedule[session_id]['session_title']}: {not_downloaded}",
          os.path.join(output_video_path, 'error-log.txt')
        )

      print("Preparing video.") # FIXME
      session_durations = vidpro.prepare_video_for_session(
        schedule[session_id],
        slides_instructions['times_info'],
        slides_instructions['opening_instructions'],
        slides_instructions['closing_instructions'],
        temp_work_dir,
        os.path.join(output_video_path, schedule[session_id]['session_id'] + ' ' + schedule[session_id]['session_title'] + '.mp4'),
        slides_instructions['path_to_banner_image'],
        slides_instructions['path_to_intro_audio'],
        True
      )

      if session_durations is not None:
        total_durations['sessions'].append(session_durations)
        Utils.update_json_log_file(total_durations, os.path.join(output_video_path, 'total-durations.json'))

      print("Cleaning up files.") # FIXME
      for paper in schedule[session_id]['papers']:
        os.remove(os.path.join(temp_work_dir, paper['paper_id'] + '-resampled.mp4'))
        os.remove(os.path.join(temp_work_dir, paper['paper_id'] + '.mp4'))

    except Exception as e:
      Utils.log_to_file(
        f"Error processing session {schedule[session_id]['session_title']}: {str(e)}",
        os.path.join(output_video_path, 'error-log.txt')
      )
