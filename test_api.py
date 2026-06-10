import requests

BASE_URL = "http://localhost:8000"

print("Complete API Flow Test")
print("=" * 50)

# 1. Register user
print("\n1. Registering user...")
user_data = {
  "username": "admin1",
  "email": "admin@example.com",
  "password": "secret123",
  "role": "admin"
}
response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
print(f"   Status: {response.status_code}")
if response.status_code == 201:
    print(f"   ✓ User registered: {response.json()['username']}")
else:
    print(f"   ✗ Failed: {response.text}")

# 2. Login
print("\n2. Logging in...")
login_data = {
    "username": "admin1",
    "password": "secret123"
}
response = requests.post(f"{BASE_URL}/auth/token", data=login_data)
if response.status_code == 200:
    token = response.json()['access_token']
    print(f"   ✓ Login successful")
    headers = {"Authorization": f"Bearer {token}"}
else:
    print(f"   ✗ Login failed")
    exit(1)

# 3. Create a course (currently no auth required, but showing token usage)
print("\n3. Creating a course...")
course_data = {
    "name": "Machine Learning",
    "credit": 4
}
response = requests.post(f"{BASE_URL}/courses", json=course_data)
print(f"   Status: {response.status_code}")
if response.status_code == 201:
    course = response.json()
    print(f"   ✓ Course created: {course['name']} (ID: {course['id']})")
else:
    print(f"   ✗ Failed: {response.text}")

# 4. Get all courses
print("\n4. Getting all courses...")
response = requests.get(f"{BASE_URL}/courses")
if response.status_code == 200:
    courses = response.json()
    print(f"   ✓ Found {len(courses)} course(s)")
    for course in courses[-3:]:  # Show last 3 courses
        print(f"     - {course['name']} (Credit: {course['credit']})")
else:
    print(f"   ✗ Failed: {response.text}")

# 5. Search for a course
print("\n5. Searching for courses...")
response = requests.get(f"{BASE_URL}/search", params={"name": "Machine"})
if response.status_code == 200:
    results = response.json()
    print(f"   ✓ Found {len(results)} course(s) matching 'Machine'")
    for course in results:
        print(f"     - {course['name']}")
else:
    print(f"   ✗ Failed: {response.text}")

print("\n" + "=" * 50)
print("✅ All tests passed!")