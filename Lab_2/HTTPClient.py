import requests

target_endpoint = "https://jsonplaceholder.typicode.com/posts"
post_payload = {
    "userID": 1,
    "title": "Sending POST data via HTTP",
    "body": "Sample content for testing POST functionality."
}

try:
    http_response = requests.post(target_endpoint, json=post_payload)
    print("\nHere's what happened with my POST request:")
    print("Response Status:", http_response.status_code)
    print("Response Headers:", http_response.headers)
    print("Response Content:", http_response.json())
except requests.exceptions.RequestException as error:
    print("Uh oh! Something went wrong with the POST request:", error)

post_result = requests.post(target_endpoint, json=post_payload)
print(post_result.json())

get_endpoint = "https://jsonplaceholder.typicode.com/posts/1"

try:
    get_response = requests.get(get_endpoint)
    print("\nNow let me try a GET request and see what I get:")
    print(get_response.json())
    print("Status Code I received:", get_response.status_code)
    print("Headers I got back:", get_response.headers)
    print("The actual content:", get_response.json())
except requests.exceptions.RequestException as error:
    print("Hmm, the GET request didn't work out:", error)
