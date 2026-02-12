import sys
import urllib.request
import json

HEALTH_URL = "http://127.0.0.1:8000/health"

print("Running post-deployment health check...")

try:
    with urllib.request.urlopen(HEALTH_URL, timeout=5) as response:
        data = json.loads(response.read().decode())

        if data.get("status") == "UP":
            print("Health check PASSED")
            sys.exit(0)
        else:
            print("Health check FAILED:", data)
            sys.exit(1)

except Exception as e:
    print("Health check ERROR:", str(e))
    sys.exit(1)
