import hashlib
import time
import requests

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
    # Vulnerabilities:
    # path-injection: The output_file parameter is directly used
    # to create a file on the system. An attacker could provide a
    # malicious path to overwrite arbitrary files.

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
  ):
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
