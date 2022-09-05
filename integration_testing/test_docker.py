import json

import requests
from deepdiff import DeepDiff

with open("event.json", "rb") as f:
    test_data = json.load(f)

url = "http://localhost:9696/predict"
actual_response = requests.post(url, json=test_data)
json_actual_response = actual_response.json()

print("actual response:")
print(json.dumps(json_actual_response, indent=2))

expected_response = {"credit_score": 1}


diff = DeepDiff(json_actual_response, expected_response, significant_digits=1)
print(f"diff={diff}")

assert "type_changes" not in diff
assert "values_changed" not in diff
