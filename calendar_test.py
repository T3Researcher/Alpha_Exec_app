import requests

CANVAS_API_BASE_URL = "https://ufl.instructure.com"
CANVAS_ACCESS_TOKEN = "1016~AIFzMnnhEA3EdCcNadYdx1awlrtoDYNseiftZUSAmX69me27F3gNVfXvMNKetm1n"

# Set the Authorization header with your API key
headers = {"Authorization": f"Bearer {CANVAS_ACCESS_TOKEN}"}

# Make a request to the Canvas API to retrieve the user's profile
response = requests.get(f"{CANVAS_API_BASE_URL}/api/v1/users/self/profile", headers=headers)

# Extract the user ID from the response
user_id = response.json()["id"]

# Make a request to the Canvas API to retrieve the user's calendar events
response = requests.get(f"{CANVAS_API_BASE_URL}/api/v1/users/{user_id}/calendar_events", headers=headers)

# Extract the calendar events from the response
calendar_events = response.json()

# Print out the calendar events
for event in calendar_events:
    print(event["title"])
    print(event["description"])
    print(event["start_at"])
    print(event["end_at"])
    print(event["type"])
user_id