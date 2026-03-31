"""
Generate new sample data for sharing request status tracking
Inspired by csvdata-1.csv with real SP names and patterns
"""
import csv
import random
from datetime import datetime, timedelta
import json

# Real SPs from csvdata-1.csv
SERVICE_PROVIDERS = [
    "AAE", "ADCB", "ADIB", "ADNIC", "Arab Bank", "Baraka", "Beyon Money",
    "Botim", "Commercial Bank of Dubai - Mobile", "DU", "Du Esim",
    "Emirates Islamic", "ENBD Tablet Banking", "Etisalat Retail",
    "Etisalat Business", "FAB Retail Banking", "GIG", "Lulu",
    "National Bank of Fujairah", "National Bonds Corporation Sole Proprietorship P.S.C.",
    "Noor Capital", "InsureOne (Premier Insurance Brokers L.L.C-O.P.C)"
]

# Document types from original data
DOCUMENT_TYPES = [
    ["Emirates ID Card"],
    ["Passport"],
    ["Residence Visa"],
    ["Emirates ID Card", "Passport"],
    ["Emirates ID Card", "Residence Visa"],
    ["Emirates ID Card", "Passport", "Residence Visa"],
    ["Emirates ID Card", "Driving License"],
    ["Emirates ID Card", "Vehicle Registration"]
]

# App versions from original data
APP_VERSIONS = ["6.4.0", "6.4.1", "6.3.0", "6.2.2", "6.2.1", "6.2.0", "6.1.3", "6.0.0", "5.10.1"]

# Status transitions for different journey paths
JOURNEY_PATTERNS = {
    # Successful notification flow with docs ready
    "notification_success_ready": [
        ("S00", None, 0),
        ("S01", "S00", 3000),
        ("S02", "S01", 4000),
        ("S03", "S02", 5000),
        ("S08", "S03", 7000),
        ("S10", "S08", 2000),
        ("S20", "S10", 18000),
        ("S21", "S20", 8000),
        ("S30", "S21", 2000),
        ("S31", "S30", 7000),
        ("S40", "S31", 3000)
    ],

    # Successful notification flow with missing docs
    "notification_success_missing": [
        ("S00", None, 0),
        ("S01", "S00", 3000),
        ("S02", "S01", 5000),
        ("S03", "S02", 4000),
        ("S08", "S03", 8000),
        ("S11", "S08", 2000),
        ("S12", "S11", 15000),
        ("S13", "S12", 10000),
        ("S20", "S13", 16000),
        ("S21", "S20", 9000),
        ("S30", "S21", 2000),
        ("S31", "S30", 8000),
        ("S40", "S31", 4000)
    ],

    # QR flow success
    "qr_success": [
        ("S00", None, 0),
        ("S06", "S00", 2000),
        ("S07", "S06", 12000),
        ("S08", "S07", 5000),
        ("S10", "S08", 1000),
        ("S20", "S10", 15000),
        ("S21", "S20", 7000),
        ("S30", "S21", 2000),
        ("S31", "S30", 6000),
        ("S40", "S31", 3000)
    ],

    # Redirect flow success
    "redirect_success": [
        ("S00", None, 0),
        ("S04", "S00", 2000),
        ("S05", "S04", 3000),
        ("S08", "S05", 5000),
        ("S10", "S08", 1000),
        ("S20", "S10", 17000),
        ("S21", "S20", 8000),
        ("S30", "S21", 2000),
        ("S31", "S30", 7000),
        ("S40", "S31", 3000)
    ],

    # User abandoned (notification)
    "notification_abandoned": [
        ("S00", None, 0),
        ("S01", "S00", 3000),
        ("S02", "S01", 4000),
        ("S03", "S02", 5000),
        ("S08", "S03", 7000),
        ("S10", "S08", 2000),
        ("S20", "S10", 18000),
        ("S21", "S20", 8000),
        ("S43", "S21", 25000)
    ],

    # PIN failed
    "pin_failed": [
        ("S00", None, 0),
        ("S01", "S00", 3000),
        ("S02", "S01", 4000),
        ("S03", "S02", 5000),
        ("S08", "S03", 7000),
        ("S10", "S08", 2000),
        ("S20", "S10", 17000),
        ("S21", "S20", 8000),
        ("S30", "S21", 2000),
        ("S32", "S30", 12000),
        ("S43", "S32", 3000)
    ],

    # Technical error after PIN
    "tech_error": [
        ("S00", None, 0),
        ("S01", "S00", 3000),
        ("S02", "S01", 4000),
        ("S03", "S02", 5000),
        ("S08", "S03", 7000),
        ("S10", "S08", 2000),
        ("S20", "S10", 16000),
        ("S21", "S20", 8000),
        ("S30", "S21", 2000),
        ("S31", "S30", 7000),
        ("S41", "S31", 8000)
    ],

    # Missing doc - not found at issuer
    "missing_not_found": [
        ("S00", None, 0),
        ("S01", "S00", 3000),
        ("S02", "S01", 4000),
        ("S03", "S02", 5000),
        ("S08", "S03", 7000),
        ("S11", "S08", 2000),
        ("S12", "S11", 12000),
        ("S15", "S12", 10000),
        ("S44", "S15", 5000)
    ],

    # Missing doc - technical error
    "missing_tech_error": [
        ("S00", None, 0),
        ("S01", "S00", 3000),
        ("S02", "S01", 4000),
        ("S03", "S02", 5000),
        ("S08", "S03", 7000),
        ("S11", "S08", 2000),
        ("S12", "S11", 15000),
        ("S14", "S12", 9000),
        ("S43", "S14", 8000)
    ],

    # Expired before consent
    "expired_before_consent": [
        ("S00", None, 0),
        ("S01", "S00", 3000),
        ("S02", "S01", 4000),
        ("S03", "S02", 5000),
        ("S08", "S03", 7000),
        ("S10", "S08", 2000),
        ("S42", "S10", 900000)  # 15 minutes
    ],

    # QR not scanned (abandoned at QR stage)
    "qr_not_scanned": [
        ("S00", None, 0),
        ("S06", "S00", 2000),
        ("S42", "S06", 900000)  # Expired
    ],

    # User rejected at consent
    "consent_rejected": [
        ("S00", None, 0),
        ("S01", "S00", 3000),
        ("S02", "S01", 4000),
        ("S03", "S02", 5000),
        ("S08", "S03", 7000),
        ("S10", "S08", 2000),
        ("S20", "S10", 18000),
        ("S43", "S20", 5000)
    ],

    # QR success with missing docs
    "qr_success_missing": [
        ("S00", None, 0),
        ("S06", "S00", 2000),
        ("S07", "S06", 10000),
        ("S08", "S07", 5000),
        ("S11", "S08", 2000),
        ("S12", "S11", 12000),
        ("S13", "S12", 9000),
        ("S20", "S13", 14000),
        ("S21", "S20", 7000),
        ("S30", "S21", 2000),
        ("S31", "S30", 6000),
        ("S40", "S31", 3000)
    ],

    # Redirect success with missing docs
    "redirect_success_missing": [
        ("S00", None, 0),
        ("S04", "S00", 2000),
        ("S05", "S04", 3000),
        ("S08", "S05", 5000),
        ("S11", "S08", 2000),
        ("S12", "S11", 14000),
        ("S13", "S12", 11000),
        ("S20", "S13", 16000),
        ("S21", "S20", 8000),
        ("S30", "S21", 2000),
        ("S31", "S30", 7000),
        ("S40", "S31", 3000)
    ],

    # Redirect abandoned
    "redirect_abandoned": [
        ("S00", None, 0),
        ("S04", "S00", 2000),
        ("S05", "S04", 3000),
        ("S08", "S05", 5000),
        ("S10", "S08", 1000),
        ("S20", "S10", 17000),
        ("S43", "S20", 8000)
    ],

    # QR tech error
    "qr_tech_error": [
        ("S00", None, 0),
        ("S06", "S00", 2000),
        ("S07", "S06", 11000),
        ("S08", "S07", 5000),
        ("S10", "S08", 1000),
        ("S20", "S10", 15000),
        ("S21", "S20", 7000),
        ("S30", "S21", 2000),
        ("S31", "S30", 6000),
        ("S41", "S31", 7000)
    ]
}

# Error mappings for specific statuses
ERROR_CODES = {
    "S14": ["issuer_timeout", "issuer_5xx", "network_error", "dv_timeout"],
    "S15": ["issuer_not_found"],
    "S32": ["pin_incorrect", "pin_dismissed"],
    "S41": ["dv_5xx", "network_error", "issuer_timeout", "signing_timeout"],
    "S44": ["issuer_not_found"]
}

ERROR_SOURCES = {
    "issuer_timeout": "issuer",
    "issuer_5xx": "issuer",
    "issuer_not_found": "issuer",
    "network_error": "network",
    "dv_timeout": "dv",
    "dv_5xx": "dv",
    "pin_incorrect": "user_cancel",
    "pin_dismissed": "user_cancel",
    "signing_timeout": "dv"
}

def generate_sharing_requests(num_requests=500):
    """Generate sample sharing request data"""
    requests = []
    base_date = datetime(2025, 11, 1)

    # Distribution weights for journey patterns
    pattern_weights = {
        "notification_success_ready": 25,
        "notification_success_missing": 12,
        "qr_success": 8,
        "qr_success_missing": 5,
        "redirect_success": 10,
        "redirect_success_missing": 7,
        "notification_abandoned": 7,
        "redirect_abandoned": 3,
        "pin_failed": 3,
        "tech_error": 2,
        "qr_tech_error": 2,
        "missing_not_found": 3,
        "missing_tech_error": 2,
        "expired_before_consent": 4,
        "qr_not_scanned": 4,
        "consent_rejected": 3
    }

    for req_num in range(1, num_requests + 1):
        request_id = f"REQ{req_num:06d}"
        sp_id = random.choice(SERVICE_PROVIDERS)

        # Determine pattern first
        pattern = random.choices(
            list(pattern_weights.keys()),
            weights=list(pattern_weights.values())
        )[0]

        # Determine channel based on pattern's journey statuses
        journey = JOURNEY_PATTERNS[pattern]
        if any(s[0] in ["S01", "S02", "S03"] for s in journey):
            channel = "notification"
        elif any(s[0] in ["S06", "S07"] for s in journey):
            channel = "qr"
        elif any(s[0] in ["S04", "S05"] for s in journey):
            channel = "redirect"
        else:
            # If no channel-specific statuses, assign based on pattern name
            if "notification" in pattern:
                channel = "notification"
            elif "qr" in pattern:
                channel = "qr"
            elif "redirect" in pattern:
                channel = "redirect"
            else:
                channel = "notification"  # default

        platform = random.choice(["android", "ios"])
        app_version = random.choice(APP_VERSIONS)
        required_docs = random.choice(DOCUMENT_TYPES)
        required_count = len(required_docs)

        # Random timestamp within November 2025
        days_offset = random.randint(0, 27)
        hours_offset = random.randint(0, 23)
        minutes_offset = random.randint(0, 59)
        base_ts = base_date + timedelta(days=days_offset, hours=hours_offset, minutes=minutes_offset)

        # Generate status events for this request
        journey = JOURNEY_PATTERNS[pattern]
        status_history = []

        for i, (status_code, previous_status, latency_ms) in enumerate(journey):
            event_ts = base_ts + timedelta(milliseconds=sum([j[2] for j in journey[:i+1]]))

            # Determine missing count
            missing_count = 0
            if status_code in ["S11", "S12"]:
                missing_count = random.randint(1, min(2, required_count))

            # Determine error info
            error_code = ""
            error_source = ""
            if status_code in ERROR_CODES:
                error_code = random.choice(ERROR_CODES[status_code])
                error_source = ERROR_SOURCES[error_code]

            status_history.append(status_code)

            event = {
                "request_id": request_id,
                "sp_id": sp_id,
                "channel": channel,
                "platform": platform,
                "app_version": app_version,
                "required_docs": json.dumps(required_docs),
                "required_count": required_count,
                "status_code": status_code,
                "previous_status": previous_status if previous_status else "",
                "status_ts": event_ts.strftime("%Y-%m-%d %H:%M:%S"),
                "step_latency_ms": latency_ms,
                "missing_count": missing_count,
                "error_code": error_code,
                "error_source": error_source,
                "status_history": json.dumps(status_history)
            }

            requests.append(event)

    return requests

def write_csv(data, filename):
    """Write data to CSV file"""
    if not data:
        return

    fieldnames = list(data[0].keys())

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

    print(f"Generated {len(data)} status events")
    print(f"Unique requests: {len(set(row['request_id'] for row in data))}")
    print(f"Saved to: {filename}")

if __name__ == "__main__":
    print("Generating new sample data inspired by csvdata-1.csv...")
    print("=" * 60)

    # Generate 500 sharing requests
    sample_data = generate_sharing_requests(500)

    # Write to CSV
    output_file = "sharing_transactions_new_sample.csv"
    write_csv(sample_data, output_file)

    print("=" * 60)
    print("Sample data generation complete!")
    print("\nNew columns added:")
    print("  - previous_status: Previous status code in the journey")
    print("  - status_history: JSON array of all statuses in order")
    print("\nData characteristics:")
    print("  - Real SP names from csvdata-1.csv")
    print("  - Realistic journey patterns with proper status transitions")
    print("  - Multiple outcome scenarios (success, abandoned, errors, expired)")
    print("  - Channel distribution: notification (~50%), redirect (~25%), qr (~25%)")
