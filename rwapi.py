#!/usr/bin/env python3
# Calls the Railway public GraphQL API using the local CLI user token.
# Usage: echo '<query>' | rwapi.py '<json-vars>'
import json, sys, os, urllib.request

cfg = json.load(open(os.path.expanduser("~/.railway/config.json")))
u = cfg.get("user", {})
tok = u.get("accessToken") or u.get("token")
if not tok:
    sys.exit("no token in ~/.railway/config.json")

query = sys.stdin.read()
variables = json.loads(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1] else {}

endpoint = os.environ.get("RW_ENDPOINT", "https://backboard.railway.com/graphql/v2")
body = json.dumps({"query": query, "variables": variables}).encode()
req = urllib.request.Request(
    endpoint,
    data=body,
    headers={
        "Authorization": f"Bearer {tok}",
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    },
)
try:
    with urllib.request.urlopen(req, timeout=45) as r:
        print(json.dumps(json.load(r), indent=2))
except urllib.error.HTTPError as e:
    print(f"HTTP {e.code}: {e.read().decode()[:1000]}")
