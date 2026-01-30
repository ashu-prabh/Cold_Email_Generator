import requests
import json

url = "http://127.0.0.1:8000/generate_email"
payload = {
    "url": "https://jobs.nike.com/job/R-33460",
    "tone": "Professional",
    "cta": "Book a meeting"
}

try:
    # Health Check
    print(f"Checking health at http://127.0.0.1:8000/...")
    health = requests.get("http://127.0.0.1:8000/")
    print(f"Health Status: {health.status_code}, Response: {health.json()}")

    print(f"Sending request to {url}...")
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        if "emails" in data and len(data["emails"]) > 0:
            print("SUCCESS: Email generated successfully!")
            print("-" * 20)
            print(data["emails"][0][:100] + "...") # Print first 100 chars
        else:
            print("WARNING: Response 200 but no emails found:", data)
    else:
        print("ERROR: Failed verification")
        print(response.text)
except Exception as e:
    print(f"EXCEPTION: {e}")
