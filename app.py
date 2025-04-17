import os
import requests
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # ✅ Autorise toutes les origines

API_KEY = os.getenv("APIMO_API_KEY")
PROVIDER_ID = os.getenv("APIMO_PROVIDER_ID")
AGENCY_ID = os.getenv("APIMO_AGENCY_ID")

APIMO_URL = f"https://api.apimo.pro/agency/{AGENCY_ID}/estate?itemsperpage=10"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

@app.route("/listings", methods=["GET"])
def get_listings():
    try:
        response = requests.get(APIMO_URL, headers=headers)
        data = response.json()
        listings = []

        for item in data.get("estates", []):
            listings.append({
                "id": item.get("id"),
                "title": item.get("title", {}).get("fr", "Sans titre"),
                "description": item.get("description", {}).get("fr", "Pas de description"),
                "price": item.get("price"),
                "picture": item.get("pictures", [{}])[0].get("url", "")
            })

        return jsonify(listings)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
