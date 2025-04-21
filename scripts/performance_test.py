import urllib
import time
import re
import secrets
import http.cookiejar


BASE_URL = "http://localhost:5000"

USERNAME = "user" + secrets.token_hex(5)
PASSWORD = "Password"  # noqa: S105

cookie_jar = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie_jar))


def send_request(url: str, data=None, method="GET"):  # noqa: ANN001
    request = urllib.request.Request(url, data=data, method=method)
    response = opener.open(request)
    return response.read().decode("utf-8")


def measure_step(step_name: str, url: str, data=None, method="GET"):  # noqa: ANN001
    start_time = time.time()
    response_data = send_request(url, data, method)

    duration = time.time() - start_time
    print(f"{step_name} took {duration:.3f} seconds")
    return response_data


signup_data = urllib.parse.urlencode(
    {"username": USERNAME, "password": PASSWORD}
).encode("utf-8")
measure_step("POST /api/signup", f"{BASE_URL}/api/signup", signup_data, "POST")

measure_step("GET /", f"{BASE_URL}/")


measure_step("GET /note/1", f"{BASE_URL}/note/1")


encoded_user_url = urllib.parse.quote("/user/User1")
measure_step("GET /user/User1", f"{BASE_URL}{encoded_user_url}")


note_data = urllib.parse.urlencode(
    {"title": "Test Note", "tags": "tag1, tag2", "content": "This is a test note."}
).encode("utf-8")
response_data = measure_step(
    "POST /api/note/new", f"{BASE_URL}/api/note/new", note_data, "POST"
)


match = re.search(r"/note/(\d+)", response_data)
if match:
    last_index = match.group(1)
else:
    msg = "Could not extract the last index from the response data"
    raise ValueError(msg)


update_data = urllib.parse.urlencode(
    {
        "title": "Updated Test Note",
        "tags": "tag1, tag2, tag3",
        "content": "This is an updated test note.",
    }
).encode("utf-8")
measure_step(
    f"POST /api/note/{last_index}/update",
    f"{BASE_URL}/api/note/{last_index}/update",
    update_data,
    "POST",
)


measure_step(
    f"POST /api/note/{last_index}/delete",
    f"{BASE_URL}/api/note/{last_index}/delete",
    method="POST",
)

measure_step("GET /search?query=a", f"{BASE_URL}/search?query=a")


measure_step("GET /signout", f"{BASE_URL}/signout")


signin_data = urllib.parse.urlencode(
    {
        "username": USERNAME,
        "password": PASSWORD,
    },
).encode("utf-8")
measure_step("POST /api/signin", f"{BASE_URL}/api/signin", signin_data, "POST")
