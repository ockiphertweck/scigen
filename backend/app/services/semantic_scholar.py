import requests


def get_paper_title_search(title, fields):
    # Convert the fields list to a comma-separated string
    fields_param = ",".join(fields)

    # Define the endpoint
    url = "https://api.semanticscholar.org/graph/v1/paper/search/match"

    # Define the parameters
    params = {
        "query": title,
        "fields": fields_param
    }

    # Send the GET request
    response = requests.get(url, params=params)

    # Check the response
    if response.status_code == 200:
        data = response.json()
        if "data" in data and len(data["data"]) > 0:
            return data["data"][0]
        else:
            print("No data found.")
            return None
    else:
        print(f"Request failed with status code {response.status_code}")
        return None
