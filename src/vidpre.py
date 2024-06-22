import dataretriever
import vidpro
import os

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
  ):
    result = ct_int.get_session_videos(
      session,
      temp_work_dir
    )

    successful_list = Utils.clear_videos_list(
      session["papers"],
      result[1]
    )

    return successful_list

  @staticmethod
  def log_to_file(message: str, log_file: str) -> None:
    with open(log_file, "a") as file:
      file.write(message + "\n")


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
  
  for session_id in schedule:
    session_i += 1
    print(f"Processing session {session_i} of {total_sesions}.") # FIXME
    
    try:
      print("Downloading videos.") # FIXME
      schedule[session_id]['papers'] = Utils.get_videos(
        schedule[session_id], temp_work_dir, ct_int
      )

      print("Preparing video.") # FIXME
      vidpro.prepare_video_for_session(
        schedule[session_id],
        slides_instructions['times_info'],
        slides_instructions['opening_instructions'],
        slides_instructions['closing_instructions'],
        temp_work_dir,
        os.path.join(output_video_path, schedule[session_id]['session_title'] + '.mp4'),
        slides_instructions['path_to_banner_image'],
        slides_instructions['path_to_intro_audio']
      )

    except Exception as e:
      Utils.log_to_file(
        f"Error processing session {session_id}: {str(e)}",
        os.path.join(output_video_path, 'error-log.txt')
      )


  