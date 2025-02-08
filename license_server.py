from flask import Flask, request, jsonify
from datetime import datetime, timedelta

app = Flask(__name__)

# Sample License Key Database (Replace this with a real database)
LICENSES = {
    "ABC123": {"expiry_date": "2025-03-10", "activated": False, "device_id": None},
    "XYZ789": {"expiry_date": "2025-03-20", "activated": False, "device_id": None}
}

@app.route("/activate", methods=["POST"])
def activate():
    """Activate a license key."""
    data = request.json
    license_key = data.get("license_key")
    device_id = data.get("device_id")

    if license_key in LICENSES:
        license_info = LICENSES[license_key]
        expiry_date = datetime.strptime(license_info["expiry_date"], "%Y-%m-%d")

        if datetime.now() > expiry_date:
            return jsonify({"status": "failed", "message": "License expired"}), 403

        if license_info["activated"] and license_info["device_id"] != device_id:
            return jsonify({"status": "failed", "message": "License already used on another device"}), 403

        LICENSES[license_key]["activated"] = True
        LICENSES[license_key]["device_id"] = device_id

        return jsonify({"status": "success", "expiry_date": license_info["expiry_date"]})
    
    return jsonify({"status": "failed", "message": "Invalid license key"}), 400

@app.route("/check_license", methods=["POST"])
def check_license():
    """Check if a license key is still valid."""
    data = request.json
    license_key = data.get("license_key")

    if license_key in LICENSES:
        license_info = LICENSES[license_key]
        expiry_date = datetime.strptime(license_info["expiry_date"], "%Y-%m-%d")

        if datetime.now() > expiry_date:
            return jsonify({"status": "expired", "message": "License expired"}), 403
        
        return jsonify({"status": "valid", "expiry_date": license_info["expiry_date"]})

    return jsonify({"status": "failed", "message": "Invalid license key"}), 400

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)