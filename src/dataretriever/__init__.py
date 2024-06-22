import hashlib
import time
import requests
import os
import xml.etree.ElementTree as ET

class Utils:
  @staticmethod
  def generate_passhash(nonce: str, password: str) -> str:
    if not nonce.isdigit():
      raise ValueError("Nonce must contain only digits.")
    passhash = hashlib.sha256((nonce + password).encode()).hexdigest()
    return passhash

  @staticmethod
  def generate_nonce() -> str:
    nonce = str(int(time.time()))
    return nonce

  @staticmethod
  def send_get_request(
    url: str,
    params: dict,
    password: str
  ) -> requests.Response:
    nonce = Utils.generate_nonce()
    required = {
      "nonce": nonce,
      "passhash": Utils.generate_passhash(nonce, password)
    }
    response = requests.get(url, params={**required, **params})
    return response

  @staticmethod
  def save_file_from_response(
    response: requests.Response,
    output_file: str
  ) -> None:
    with open(output_file, "wb") as file:
      file.write(response.content)

class UtilConferenceData:
  def __init__(self):
    self.sessions = {}

  @staticmethod
  def paper_sort_key(paper: dict) -> int:
    return paper["order"]

  def add_session(self, session_data: dict) -> None:
    if session_data["session_id"] not in self.sessions:
      self.sessions[session_data["session_id"]] = {
        "session_title": session_data["session_title"],
        "session_start": session_data["session_start"],
        "session_end": session_data["session_end"],
        "papers": []
      }
    
    self.sessions[session_data["session_id"]]["papers"].append({
      "order": session_data["order"],
      "paper_id": session_data["paper_id"]
    })
  
  def sort_papers(self) -> None:
    for session_id in self.sessions:
      self.sessions[session_id]["papers"].sort(
        key = UtilConferenceData.paper_sort_key
      )
  
  def get_schedule(self) -> dict:
    self.sort_papers()
    return self.sessions

class CTInterface:
  def __init__(self, conference_endpoint: str, ct_password: str):
    self.endpoint = conference_endpoint
    self.password = ct_password

  def get_data(
    self,
    output_file: str,
    export_select: str = "users",
    format: str = "xml",
    form_export_x_options: dict = {}
  ) -> None:
    resp = Utils.send_get_request(self.endpoint, {
      "page": "adminExport",
      "export_select": export_select,
      "form_include_deleted": 0,
      "form_export_format": format,
      "form_export_header": "default",
      "cmd_create_export": "true",
      **form_export_x_options
    }, self.password)
    Utils.save_file_from_response(resp, output_file)

  def get_schedule(
    self,
    temp_papers_file: str,
    refresh: bool = False
  ) -> None:
    if not os.path.exists(temp_papers_file) and not refresh:
      self.get_data(
        temp_papers_file,
        export_select = "papers",
        form_export_x_options = {
          # "form_export_papers_options[]": ["session", "downloads"]
          "form_export_papers_options[]": ["session"]
        }
      )
    papers_tree = ET.parse(temp_papers_file)
    papers_node = papers_tree.getroot()

    sessions_data = UtilConferenceData()

    for paper in papers_node:
      acceptance = paper.find('acceptance').text
      if acceptance == 'Accepted (V)':
        paper_data = {
          "paper_id": paper.find("paperID").text,
          "session_id": paper.find("session_ID").text,
          "session_title": paper.find("session_title").text,
          "session_start": paper.find("session_start").text,
          "session_end": paper.find("session_end").text,
          "order": paper.find("session_numberInSession").text
        }

        sessions_data.add_session(paper_data)
    
    return sessions_data.get_schedule()
  
  def get_video(
    self,
    submission_id: int,
    output_filename: str
  ) -> tuple[bool, requests.Response]:
    resp = Utils.send_get_request(self.endpoint, {
      "page": "downloadPaper",
      "form_id": submission_id,
      "form_index": 2,
      "form_version": "final"
    }, self.password)
    if (
      resp.status_code == 200 and 
      resp.headers["Content-Type"] == "video/mp4"
    ):
      Utils.save_file_from_response(resp, output_filename)
      return (True, resp)
    return (False, resp)