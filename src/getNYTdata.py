import requests

def get_data(url: str, cookies: dict) -> str:
    '''Gets text from URL using cookies.'''
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36"}
    response = requests.get(url = url, cookies = cookies, headers = headers).text
    
    return response