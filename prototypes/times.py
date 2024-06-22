import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
abs_path = os.path.abspath(current_dir + '/' + '../src')
sys.path.insert(0, abs_path)

import vidpro

sessions = {
  '51': {
    'session_title': 'W1F4-Virtual',
    'session_start': '2024-07-17 07:00',
    'session_end': '2024-07-17 08:10',
    'papers': []
  }
}

times_info = {
  'original_title': 'Costa Rica',
  'original': 'America/Costa_Rica',
  'others': [
    {
      'title': 'Miami',
      'timezone': 'EST5EDT',
    }
  ]
}

output = vidpro.Utils.prepare_session_information(sessions['51'], times_info)
print("Output object: ", output)