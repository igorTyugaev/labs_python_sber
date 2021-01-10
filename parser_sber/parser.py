from utils import *

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'accept': '*/*'}


def get_html(url, params={}):
    try:
        res = requests.get(url, headers=HEADERS, params=params)
        res.raise_for_status()
        return res
    except(res.RequestException, ValueError):
        print('Server error')
        return None


def get_more_info(soup):
    list_more = []
    details_list = []
    box_office_list = []
    technical_specs_list = []

    print('Start scrape more info about film')

    if soup is not None:
        details_soup = soup.find('div', {'class': 'article', "id": "titleDetails"})

        if details_soup is not None:
            children = details_soup.find_all(['h2', 'h3', 'div'])

            key = None
            for child in children:
                if child.get_text() == 'Details':
                    key = 'details'
                elif child.get_text() == 'Box Office':
                    key = 'box_office'
                elif child.get_text() == 'Technical Specs':
                    key = 'technical_specs'
                elif child.get('class') == ['subheading']:
                    key = ''

                if key == 'details' and child.get('class') == ['txt-block']:
                    item_text = child.get_text(strip=True, separator=" ").strip()
                    if item_text.rfind('See ') != -1:
                        item_text = item_text[:item_text.index('See ')]
                    details_list.append(item_text)

                if key == 'box_office' and child.get('class') == ['txt-block']:
                    item_text = child.get_text(strip=True, separator=" ").strip()
                    if item_text.rfind('See ') != -1:
                        item_text = item_text[:item_text.index('See ')]
                    box_office_list.append(item_text)

                if key == 'technical_specs' and child.get('class') == ['txt-block']:
                    item_text = child.get_text(strip=True, separator=" ").strip()
                    if item_text.rfind('See ') != -1:
                        item_text = item_text[:item_text.index('See ')]
                    technical_specs_list.append(item_text)

            list_more.append(details_list)
            list_more.append(box_office_list)
            list_more.append(technical_specs_list)

    return list_more


def get_basic_info(source_url, soup):
    items = soup.find_all('div', class_='lister-item mode-advanced')
    count = 1
    film_list = []
    title = None
    genres = None
    user_rating = None
    top_starts = None
    link_more = None

    for item in items:
        print('Scraping item:', count)

        if item.find('h3', class_='lister-item-header') is not None:
            if item.find('h3', class_='lister-item-header').find('a') is not None:
                title = item \
                    .find('h3', class_='lister-item-header') \
                    .find('a') \
                    .get_text()

            if item.find('h3', class_='lister-item-header').find('a', href=True) is not None:
                link_more = source_url + (item
                    .find('h3', class_='lister-item-header')
                    .find('a', href=True)['href'])

        if item.find('p', class_='text-muted') is not None:
            if item.find('p', class_='text-muted').find('span', class_='genre') is not None:
                genres = item \
                    .find('p', class_='text-muted') \
                    .find('span', class_='genre') \
                    .get_text(strip=True) \
                    .split(',')

        if item.find('div', class_='inline-block ratings-imdb-rating') is not None:
            if item.find('div', class_='inline-block ratings-imdb-rating').find('strong') is not None:
                user_rating = float(item
                                    .find('div', class_='inline-block ratings-imdb-rating')
                                    .find('strong')
                                    .get_text(strip=True))

        if item.find('p', class_='') is not None:
            top_starts = item.find('p', class_='') \
                             .get_text(strip=True)[item.find('p', class_='') \
                                                       .get_text(strip=True).find('Stars:') + len('Stars:'):] \
                .split(',')

        print('Scraping basic info of item end!')

        list_more = scrape_film_page(link_more)
        print(len(list_more))
        print(list_more)
        dict_basic = {
            'title': title,
            'genres': genres,
            'user_rating': user_rating,
            'top_starts': top_starts,
            'details': (list_more[0] if len(list_more) > 0 else ''),
            'box_office': (list_more[1] if len(list_more) > 1 else ''),
            'technical_specs': (list_more[2] if len(list_more) > 2 else '')
        }

        print(dict_basic)

        film_list.append(dict_basic)
        count += 1

    print('Scraping item end!')
    return film_list


def scrape_film_page(seed_url):
    try:
        html = get_html(seed_url)

        if html is not None:
            soup = BeautifulSoup(html.text, 'html.parser')
            list_more = get_more_info(soup)
            return list_more
        else:
            return True

    except Exception as e:
        print("Exception in scrape_film_page", e)
        return e


def scrape_search_page(seed_url, source_url, params={}, max_items=1000):
    film_list = []
    count_page = 1
    start_number = 1

    while True:
        if start_number > max_items:
            print("Превышен лимит чтения! Код: 1000")
            break

        try:
            params['start'] = start_number
            html = get_html(seed_url, params)

            if html is not None:
                soup = BeautifulSoup(html.text, 'html.parser')
            else:
                break

            if soup.find('a', class_='lister-page-next next-page') is not None:
                print('Scraping page number', count_page)
                film_list += get_basic_info(source_url, soup)
                # time.sleep(3)
                start_number += 50
            else:
                print('Scraping last page')
                film_list += get_basic_info(source_url, soup)
                break
        except Exception as e:
            print("Exception in scrape_search_page:", e)
            return e
        count_page += 1
        logger.info(f"Found {len(film_list)} films.")
        logger.info("Parsing in progress...")

    print('Scraping end!')
    print('Result:')
    print(film_list)
    write_to_csv(film_list)
