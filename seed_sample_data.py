"""Add sample Chennai restaurants + reviews through the app's real HTML forms.

Usage: python seed_sample_data.py http://localhost:8000
       python seed_sample_data.py https://<your-app>.onrender.com
Each POST carries the CSRF token from the form, exactly like a browser would.
"""
import http.cookiejar
import re
import sys
import urllib.parse
import urllib.request

BASE = sys.argv[1].rstrip('/')

RESTAURANTS = [
    ("Murugan Idli Shop", "G.N. Chetty Road, T. Nagar, Chennai", "Soft idlis with podi and four chutneys",
     [("Arun", 5, "Best idli in T. Nagar, super soft."), ("Priya", 4, "Quick service, a bit crowded at night.")]),
    ("Ratna Cafe", "Triplicane High Road, Triplicane, Chennai", "Classic cafe famous for sambar idli",
     [("Karthik", 5, "The sambar is legendary."), ("Divya", 4, "Old-school place, great filter coffee.")]),
    ("Buhari Hotel", "Anna Salai, Mount Road, Chennai", "Historic restaurant, home of Chicken 65",
     [("Rahul", 4, "Must try the Chicken 65."), ("Meena", 3, "Good food, service could be faster.")]),
]

opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


def csrf_token(path):
    html = opener.open(BASE + path, timeout=120).read().decode()
    return re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)


def post(path, data, token_page):
    data = dict(data, csrf_token=csrf_token(token_page))
    # Over HTTPS Flask-WTF also checks the Referer header (browsers send it automatically)
    req = urllib.request.Request(BASE + path, urllib.parse.urlencode(data).encode(),
                                 headers={'Referer': BASE + token_page})
    resp = opener.open(req, timeout=120)
    return resp.geturl()


for name, addr, desc, reviews in RESTAURANTS:
    url = post('/add', {'restaurant_name': name, 'street_address': addr, 'description': desc}, '/create')
    rid = int(url.rstrip('/').rsplit('/', 1)[1])
    for user, rating, text in reviews:
        post(f'/review/{rid}', {'user_name': user, 'rating': rating, 'review_text': text}, f'/{rid}')
    print(f'Added {name} (id {rid}) with {len(reviews)} reviews -> {url}')
