import requests

def safe_get(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
    except HTTPError as err:
        print('None 200 status code: %s', err)
    except Exception as amb_err:
        print('Ambigious error: %s', amb_err)
    else:
        return response
    return None
