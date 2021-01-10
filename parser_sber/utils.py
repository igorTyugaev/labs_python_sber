import csv
import time
import requests
import logging
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.DEBUG, filename='scrabble.log',
                    format='%(asctime)s %(levelname)s:%(message)s')
logger = logging.getLogger(__name__)

country_dict = {
    'af': 'Afghanistan', 'ax': 'Åland Islands', 'al': 'Albania', 'dz': 'Algeria', 'as': 'American Samoa',
    'ad': 'Andorra',
    'ao': 'Angola', 'ai': 'Anguilla', 'aq': 'Antarctica', 'ag': 'Antigua and Barbuda', 'ar': 'Argentina',
    'am': 'Armenia',
    'aw': 'Aruba', 'au': 'Australia', 'at': 'Austria', 'az': 'Azerbaijan', 'bs': 'Bahamas', 'bh': 'Bahrain',
    'bd': 'Bangladesh', 'bb': 'Barbados', 'by': 'Belarus', 'be': 'Belgium', 'bz': 'Belize', 'bj': 'Benin',
    'bm': 'Bermuda',
    'bt': 'Bhutan', 'bo': 'Bolivia', 'bq': 'Bonaire, Sint Eustatius and Saba', 'ba': 'Bosnia and Herzegovina',
    'bw': 'Botswana', 'bv': 'Bouvet Island', 'br': 'Brazil', 'io': 'British Indian Ocean Territory',
    'vg': 'British Virgin Islands', 'bn': 'Brunei Darussalam', 'bg': 'Bulgaria', 'bf': 'Burkina Faso', 'bumm': 'Burma',
    'bi': 'Burundi', 'kh': 'Cambodia', 'cm': 'Cameroon', 'ca': 'Canada', 'cv': 'Cape Verde', 'ky': 'Cayman Islands',
    'cf': 'Central African Republic', 'td': 'Chad', 'cl': 'Chile', 'cn': 'China', 'cx': 'Christmas Island',
    'cc': 'Cocos (Keeling) Islands', 'co': 'Colombia', 'km': 'Comoros', 'cg': 'Congo', 'ck': 'Cook Islands',
    'cr': 'Costa Rica', 'ci': "Côte d'Ivoire", 'hr': 'Croatia', 'cu': 'Cuba', 'cy': 'Cyprus', 'cz': 'Czech Republic',
    'cshh': 'Czechoslovakia', 'cd': 'Democratic Republic of the Congo', 'dk': 'Denmark', 'dj': 'Djibouti',
    'dm': 'Dominica', 'do': 'Dominican Republic', 'ddde': 'East Germany', 'ec': 'Ecuador', 'eg': 'Egypt',
    'sv': 'El Salvador', 'gq': 'Equatorial Guinea', 'er': 'Eritrea', 'ee': 'Estonia', 'et': 'Ethiopia',
    'fk': 'Falkland Islands', 'fo': 'Faroe Islands', 'yucs': 'Federal Republic of Yugoslavia',
    'fm': 'Federated States of Micronesia', 'fj': 'Fiji', 'fi': 'Finland', 'fr': 'France', 'gf': 'French Guiana',
    'pf': 'French Polynesia', 'tf': 'French Southern Territories', 'ga': 'Gabon', 'gm': 'Gambia', 'ge': 'Georgia',
    'de': 'Germany', 'gh': 'Ghana', 'gi': 'Gibraltar', 'gr': 'Greece', 'gl': 'Greenland', 'gd': 'Grenada',
    'gp': 'Guadeloupe', 'gu': 'Guam', 'gt': 'Guatemala', 'gg': 'Guernsey', 'gn': 'Guinea', 'gw': 'Guinea-Bissau',
    'gy': 'Guyana', 'ht': 'Haiti', 'hm': 'Heard Island and McDonald Islands', 'va': 'Holy See (Vatican City State)',
    'hn': 'Honduras', 'hk': 'Hong Kong', 'hu': 'Hungary', 'is': 'Iceland', 'in': 'India', 'id': 'Indonesia',
    'ir': 'Iran',
    'iq': 'Iraq', 'ie': 'Ireland', 'im': 'Isle of Man', 'il': 'Israel', 'it': 'Italy', 'jm': 'Jamaica', 'jp': 'Japan',
    'je': 'Jersey', 'jo': 'Jordan', 'kz': 'Kazakhstan', 'ke': 'Kenya', 'ki': 'Kiribati', 'xko': 'Korea',
    'xkv': 'Kosovo',
    'kw': 'Kuwait', 'kg': 'Kyrgyzstan', 'la': 'Laos', 'lv': 'Latvia', 'lb': 'Lebanon', 'ls': 'Lesotho', 'lr': 'Liberia',
    'ly': 'Libya', 'li': 'Liechtenstein', 'lt': 'Lithuania', 'lu': 'Luxembourg', 'mo': 'Macao', 'mg': 'Madagascar',
    'mw': 'Malawi', 'my': 'Malaysia', 'mv': 'Maldives', 'ml': 'Mali', 'mt': 'Malta', 'mh': 'Marshall Islands',
    'mq': 'Martinique', 'mr': 'Mauritania', 'mu': 'Mauritius', 'yt': 'Mayotte', 'mx': 'Mexico', 'md': 'Moldova',
    'mc': 'Monaco', 'mn': 'Mongolia', 'me': 'Montenegro', 'ms': 'Montserrat', 'ma': 'Morocco', 'mz': 'Mozambique',
    'mm': 'Myanmar', 'na': 'Namibia', 'nr': 'Nauru', 'np': 'Nepal', 'nl': 'Netherlands', 'an': 'Netherlands Antilles',
    'nc': 'New Caledonia', 'nz': 'New Zealand', 'ni': 'Nicaragua', 'ne': 'Niger', 'ng': 'Nigeria', 'nu': 'Niue',
    'nf': 'Norfolk Island', 'kp': 'North Korea', 'vdvn': 'North Vietnam', 'mp': 'Northern Mariana Islands',
    'no': 'Norway',
    'om': 'Oman', 'pk': 'Pakistan', 'pw': 'Palau', 'xpi': 'Palestine', 'ps': 'Palestinian Territory', 'pa': 'Panama',
    'pg': 'Papua New Guinea', 'py': 'Paraguay', 'pe': 'Peru', 'ph': 'Philippines', 'pl': 'Poland', 'pt': 'Portugal',
    'pn': 'Pitcairn', 'pr': 'Puerto Rico', 'qa': 'Qatar', 'mk': 'Republic of Macedonia', 're': 'Réunion',
    'ro': 'Romania',
    'ru': 'Russia', 'rw': 'Rwanda', 'bl': 'Saint Barthélemy', 'sh': 'Saint Helena', 'kn': 'Saint Kitts and Nevis',
    'lc': 'Saint Lucia', 'mf': 'Saint Martin (French part)', 'pm': 'Saint Pierre and Miquelon',
    'vc': 'Saint Vincent and the Grenadines', 'ws': 'Samoa', 'sm': 'San Marino', 'st': 'Sao Tome and Principe',
    'sa': 'Saudi Arabia', 'sn': 'Senegal', 'rs': 'Serbia', 'csxx': 'Serbia and Montenegro', 'sc': 'Seychelles',
    'xsi': 'Siam', 'sl': 'Sierra Leone', 'sg': 'Singapore', 'sk': 'Slovakia', 'si': 'Slovenia', 'sb': 'Solomon Islands',
    'so': 'Somalia', 'za': 'South Africa', 'gs': 'South Georgia and the South Sandwich Islands', 'kr': 'South Korea',
    'suhh': 'Soviet Union', 'es': 'Spain', 'lk': 'Sri Lanka', 'sd': 'Sudan', 'sr': 'Suriname',
    'sj': 'Svalbard and Jan Mayen', 'sz': 'Swaziland', 'se': 'Sweden', 'ch': 'Switzerland', 'sy': 'Syria',
    'tw': 'Taiwan',
    'tj': 'Tajikistan', 'tz': 'Tanzania', 'th': 'Thailand', 'tl': 'Timor-Leste', 'tg': 'Togo', 'tk': 'Tokelau',
    'to': 'Tonga', 'tt': 'Trinidad and Tobago', 'tn': 'Tunisia', 'tr': 'Turkey', 'tm': 'Turkmenistan',
    'tc': 'Turks and Caicos Islands', 'tv': 'Tuvalu', 'vi': 'U.S. Virgin Islands', 'ug': 'Uganda', 'ua': 'Ukraine',
    'ae': 'United Arab Emirates', 'gb': 'United Kingdom', 'us': 'United States',
    'um': 'United States Minor Outlying Islands', 'uy': 'Uruguay', 'uz': 'Uzbekistan', 'vu': 'Vanuatu',
    've': 'Venezuela',
    'vn': 'Vietnam', 'wf': 'Wallis and Futuna', 'xwg': 'West Germany', 'eh': 'Western Sahara', 'ye': 'Yemen',
    'xyu': 'Yugoslavia', 'zrcd': 'Zaire', 'zm': 'Zambia', 'zw': 'Zimbabwe'
}


def isDigit(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def get_params():
    print('- - - Title - - -')
    title = input(" | Enter title (e.g. The Godfather): \n |-> ")
    while not title:
        print(' | It seems you entered an empty line')
        print(' | Please, try again!')
        title = input(" | Enter title (e.g. The Godfather): \n |-> ")
    print()

    print('- - - Title Type - - -')
    print(' | 1. Feature Film	 2. TV Movie	 3. TV Series	 4. TV Episode')
    print(' | 5. TV Special	 6. Mini-Series	 7. Documentary	 8. Video Game')
    print(' | 9. Short Film	 10. Video	 11. TV Short')

    title_type = input(" | Enter title Type (e.g. 1, 2, 8) without space!: \n |-> ").strip().split(',')
    while not (all((num.isdigit() and int(num) >= 1 and int(num) <= 11) for num in title_type)):
        print(' | Invalid data type!')
        print(' | Please, try again!')
        title_type = input(" | Enter title Type (e.g. 1,2,8) without space!: \n |-> ").strip().split(',')
    title_type = map(int, title_type)
    print()

    print('- - - Release Date - - -')
    print('* Format: YYYY-MM-DD, YYYY-MM, or YYYY')
    release_date_from = input(" | Enter date from: \n |-> ")
    release_date_to = input(" | Enter date to: \n |-> ")
    print()

    print('- - - User Rating - - -')
    print('* Valid values are number in the range 1.0 - 10')

    user_rating_from = input(" | Enter user rating from: \n |-> ")

    while not (isDigit(user_rating_from) and float(user_rating_from) >= 1 and float(user_rating_from) <= 10):
        print(' | * Valid values are number in the range 1.0 - 10')
        print(' | Please, try again!')
        user_rating_from = input(" | Enter user rating from: \n |-> ")

    user_rating_to = input(" | Enter user rating to: \n |-> ")
    while not (isDigit(user_rating_to) and float(user_rating_to) >= 1 and float(user_rating_to) <= 10):
        print(' | * Valid values are number in the range 1.0 - 10')
        print(' | Please, try again!')
        user_rating_to = input(" | Enter user rating to: \n |-> ")

    user_rating_from = float(user_rating_from)
    user_rating_to = float(user_rating_to)

    print(' | User Rating:', user_rating_from, 'to', user_rating_to)
    print()

    print('- - - Genres - - -')
    print(' | 1. Action	 2. Adventure	 3. Animation	 4. Biography')
    print(' | 5. Comedy	 6. Crime	 7. Documentary	 8. Drama')
    print(' | 9. Family	 10. Fantasy	 11. Film-Noir	 12. Game-Show')
    print(' | 13. History	 14. Horror	 15. Music	 16. Musical')
    print(' | 17. Mystery	 18. News	 19. Reality-TV	 20. Romance')
    print(' | 21. Sci-Fi	 22. Sport	 23. Talk-Show	 24. Thriller')
    print(' | 25. War	 26. Western')

    genres = input(" | Enter genres (e.g. 1,2,8) without space!: \n |-> ").strip().split(',')
    while not (all((num.isdigit() and int(num) >= 1 and int(num) <= 26) for num in genres)):
        print(' | Invalid data type!')
        print(' | Please, try again!')
        genres = input(" | Enter genres (e.g. 1,2,8) without space!: \n |-> ").strip().split(',')
    genres = map(int, genres)
    print()

    print('- - - Country - - -')
    first_characters_country = input(
        ' | Enter the first one or two characters of the country name (e.g. "Ru"): \n |-> ')
    print(' | Perhaps you were referring to one of these countries: ')
    print(' | - - - - - - - - - - - -')
    print(' | {:>6} |  {}'.format('Code', 'Name country'))
    print(' | - - - - - - - - - - - -')
    for dict_inner in country_dict.items():
        if dict_inner[1].startswith(first_characters_country.capitalize()):
            print(' | {:>6} |  {}'.format(str(dict_inner[0]), str(dict_inner[1])))

    print(' | - - - - - - - - - - - -')
    code_country = input(" | Enter only code country: \n |-> ").lower()
    while not (code_country in country_dict.keys()):
        print(' | The specified code is missing!')
        print(' | Please, try again!')
        code_country = input(" | Enter only code country: \n |-> ").lower()
    print()

    params = {
        'title': title,  # title = God
        'title_type': title_type,  # title_type=tv_special,tv_miniseries
        'release_date': str(release_date_from) + ', ' + str(release_date_to),
        # release_date = 1960 - 01 - 01, 2010 - 12 - 31
        'user_rating': str(user_rating_from) + ', ' + str(user_rating_to),  # user_rating = 2.8, 10.0
        'genres': genres,  # genres = family, film - noir, romance
        'countries': code_country  # countries = us
    }

    return True


def write_to_csv(film_list):
    try:
        keys = film_list[0].keys()
        with open('allFilms.csv', 'w', newline='') as output_file:
            dict_writer = csv.DictWriter(output_file, keys)
            dict_writer.writeheader()
            dict_writer.writerows(film_list)
            logging.info('Films list wrote on csv.')
    except:
        return False
    logger.info("Finish scrabble!")
