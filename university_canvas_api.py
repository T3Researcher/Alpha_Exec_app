from wsgiref import headers

from canvasapi import Canvas
import requests

# Define your Canvas instance and access token
CANVAS_API_BASE_URL = "https://ufl.instructure.com"
CANVAS_ACCESS_TOKEN = "1016~AIFzMnnhEA3EdCcNadYdx1awlrtoDYNseiftZUSAmX69me27F3gNVfXvMNKetm1n"
headers = {
    "Authorization": "Bearer 1016~AIFzMnnhEA3EdCcNadYdx1awlrtoDYNseiftZUSAmX69me27F3gNVfXvMNKetm1n"
}

# Create a Canvas object
canvas = Canvas(CANVAS_API_BASE_URL, CANVAS_ACCESS_TOKEN)


# Get courses for the authenticated user
def get_canvas_courses():
    user = canvas.get_current_user()
    courses = user.get_courses()
    return courses


# Get assignments for a specific course
def get_canvas_assignments(course_id):
    course = canvas.get_course(course_id)
    assignments = course.get_assignments()
    return assignments


def get_canvas_modules(course_id):
    course = canvas.get_course(course_id)
    modules = course.get_modules()

    # Print modules for debugging purposes
    print("Modules:", modules)

    if modules:
        return modules
    else:
        print("Error: Unable to fetch modules.")
        return None


def get_account_calendars():
    url = f"{CANVAS_API_BASE_URL}/api/v1/account_calendars"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: API call failed with status code {response.status_code}")
        print(response.text)
        return None

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error: Unable to parse JSON response - {e}")
        print(response.text)
        return None


def get_account_calendar(account_id):
    url = f"{CANVAS_API_BASE_URL}/api/v1/account_calendars/{account_id}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: API call failed with status code {response.status_code}")
        print(response.text)
        return None

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error: Unable to parse JSON response - {e}")
        print(response.text)
        return None


def update_calendar_visibility(account_id, visible):
    url = f"{CANVAS_API_BASE_URL}/api/v1/account_calendars/{account_id}"
    data = {"visible": visible}
    response = requests.put(url, headers=headers, data=data)

    if response.status_code != 200:
        print(f"Error: API call failed with status code {response.status_code}")
        print(response.text)
        return None

    try:
        return response.json()
    except requests.exceptions.JSONDecodeError as e:
        print(f"Error: Unable to parse JSON response - {e}")
        print(response.text)
        return None
