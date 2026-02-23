from app import metrics

def slo_status():
    if metrics.TOTAL_REQUESTS == 0:
        return {
            "status": "NO DATA",
            "success_rate": 1.0,
            "error_budget_remaining": 1.0
        }

    success_rate = (
        metrics.TOTAL_REQUESTS - metrics.FAILED_REQUESTS
    ) / metrics.TOTAL_REQUESTS

    error_budget = 1 - metrics.SLO_TARGET
    error_budget_used = max(0, metrics.SLO_TARGET - success_rate)
    error_budget_remaining = max(0, error_budget - error_budget_used)

    return {
        "status": "SLO BREACHED" if success_rate < metrics.SLO_TARGET else "SLO OK",
        "success_rate": round(success_rate, 4),
        "error_budget_remaining": round(error_budget_remaining, 4)
    }