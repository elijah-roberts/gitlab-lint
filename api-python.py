import sys
import requests

with open(sys.argv[1]) as f:
    r = requests.post(f"https://gitlab.com/api/v4/projects/23152621/ci/lint", json={'content': f.read()}, params={'private_token': 'a1rFztcLehAc6cAzJexf'})

print(r)
print(r.json())
