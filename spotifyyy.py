import requests
import base64
import pprint

CLIENT_ID = "f93ae84326014ffcb5bbee3eeecff935"
CLIENT_SECRET = "f742454cfd1049d697a0819376222a93"

auth_url = "https://accounts.spotify.com/api/token"
auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode("ascii")
auth_response = requests.post(auth_url, {
    "grant_type": "client_credentials"
}, headers={
    "Authorization": f"Basic {auth_header}"
})

access_token = auth_response.json()["access_token"]

def search_track_id(query, limit=1):
    """
    Function to search track's id by query.
    Query has to be a **string** format.
    """
    
    url = "https://api.spotify.com/v1/search"
    params = {"q": query, "type": "track", "limit": limit}
    r = requests.get(url, params=params,
                     headers={"Authorization": f"Bearer {access_token}",
                              "Accept": "application/json"},
                     timeout=15)
    items = r.json().get("tracks", {}).get("items", [])
    
    if not items:
        raise ValueError(f"No track found for query: {query}")
    
    return items[0]['id']

def get_track_by_id(track_id):
    """
    Fucntion to search track json by id.
    Item "track_id" has to be a **string** format.
    """
    
    url = f"https://api.spotify.com/v1/tracks/{track_id}"
    r = requests.get(url, headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"}, timeout=15)
    return r

def get_track_by_search(query, limit=1):
    """ 
    Function to search track json by query.
    Query has to be a **string** format.
    """

    url = f"https://api.spotify.com/v1/search"
    params = {"q": query, "type": "track", "limit": limit}
    r = requests.get(url, params=params, headers={"Authorization": f"Bearer {access_token}", "Accept": "application/json"}, timeout=15)
    items = r.json().get("tracks", {}).get("items", [])
    return items

if __name__ == "__main__":
    search_text = input()
    
    res_id = str(search_track_id(search_text))
    res_track = get_track_by_id(res_id)

    pprint.pprint(res_track.json())