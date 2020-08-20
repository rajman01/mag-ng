import requests


def search(page, page_size, query, api_key):
    url = (f'https://newsapi.org/v2/everything?'
           f'q={query}&apiKey={api_key}&'
           f'page={page}&'
           f'pageSize={page_size}')
    response = requests.get(url)
    return response.json()['articles']


def main():
    pass


if __name__ == '__main__':
    main()
