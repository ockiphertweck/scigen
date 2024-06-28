import httpx


BASE_URL = "https://api.semanticscholar.org"


def _send_request(endpoint, params=None):
    """
    Sends a GET request to the given endpoint with the provided parameters.

    Args:
        endpoint (str): The API endpoint to send the request to.
        params (dict): A dictionary of query parameters to include in the request.

    Returns:
        dict or None: The JSON response as a dictionary if the request is successful, None otherwise.
    """
    url = f"{BASE_URL}{endpoint}"
    response = httpx.get(url, params=params)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Request failed with status code {response.status_code}")
        return None


def get_paper_title_search(title, fields):
    """
    Retrieves the first paper that matches the given title from the Semantic Scholar API.

    Args:
        title (str): The title of the paper to search for.
        fields (list): A list of fields to include in the response.

    Returns:
        dict or None: A dictionary containing the data of the first matching paper, or None if no data is found.
    """
    fields_param = ",".join(fields)
    params = {"query": title, "fields": fields_param}
    data = _send_request("/graph/v1/paper/search/match", params)

    if data and "data" in data and len(data["data"]) > 0:
        return data["data"][0]
    else:
        print("No data found.")
        return None


def get_recommend_papers(paper_id):
    """
    Retrieves a list of recommended papers for a given paper ID.

    Args:
        paper_id (str): The ID of the paper for which recommendations are requested.

    Returns:
        list or None: A list of recommended papers if recommendations are found, None otherwise.
    """
    print("Paper ID:", paper_id)
    endpoint = f"/recommendations/v1/papers/forpaper/{paper_id}"
    data = _send_request(endpoint)
    print("Recom:", data)
    if data and "recommendedPapers" in data and len(data["recommendedPapers"]) > 0:
        return data["recommendedPapers"]
    else:
        print("No recommendations found.")
        return None
