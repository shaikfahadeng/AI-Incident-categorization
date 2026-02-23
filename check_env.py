import os
from dotenv import load_dotenv
load_dotenv()
print("EMAIL:", os.getenv("ALERT_EMAIL"))