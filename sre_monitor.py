import time
from app.alerting import send_alert
from app.slo import slo_status

CHECK_INTERVAL = 30
incident_active = False


def monitor():
    global incident_active

    print("SRE Monitor running...")

    while True:
        status = slo_status()

        if status["status"] == "SLO BREACHED":
            if not incident_active:
                send_alert(
                    "🚨 SRE INCIDENT: SLO BREACHED",
                    f"""
Service reliability degraded

Success rate: {status['success_rate']}
Error budget remaining: {status['error_budget_remaining']}
"""
                )
                incident_active = True
        else:
            incident_active = False

        time.sleep(CHECK_INTERVAL)