from parser import *

URL = 'https://www.imdb.com/search/title/'
HOST = 'https://www.imdb.com'
URL_TEST = 'https://www.imdb.com/search/title/?title=+The+Godfather'

# params = {
#     'title': 'Godfather',
#     'title_type': 'tv_movie,tv_miniseries',
#     'release_date': None,
#     'user_rating': None,
#     'genres': None,
#     'countries': None,
#     'start': 1,
#     'ref_': 'adv_nxt'
# }

params = {
    'title': None,
    'title_type': 'tv_movie,tv_miniseries',
    'release_date': None,
    'user_rating': None,
    'genres': 'action',
    'countries': None,
    'start': 1,
    'ref_': 'adv_nxt'
}


def main():
    # get_params()
    scrape_search_page(URL, HOST, params)


if __name__ == "__main__":
    main()
