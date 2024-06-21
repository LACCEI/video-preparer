import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
abs_path = os.path.abspath(current_dir + '/' + '../src')
sys.path.insert(0, abs_path)

import dataretriever
import json

conference_endpoint = ""
password = ""

ct_int = dataretriever.CTInterface(conference_endpoint, password)

papers_temp_file = "papers.xml"
schedule = ct_int.get_schedule(papers_temp_file)
schedule_json = json.dumps(schedule)
with open('schedule.json', 'w') as file:
  file.write(schedule_json)
