
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from models import BrandContext, Product
from scraper.utils import extract_social_handles, extract_contact_details, extract_links, extract_faqs

def fetch_brand_insights(base_url):
    base_url = base_url.strip('/ ')
    if not base_url.startswith('http'):
        base_url = 'https://' + base_url
    insights = BrandContext()
    prod_url = urljoin(base_url, '/products.json')
    try:
        r = requests.get(prod_url, timeout=10)
        if r.status_code == 200 and r.json().get('products'):
            prods = r.json()['products']
            insights.product_catalog = [
                Product(title=p.get('title'), price=(float(p['variants'][0]['price']) if p.get('variants') else None),
                        url=urljoin(base_url, f"/products/{p.get('handle')}") if p.get('handle') else None,
                        image_url=(p['images'][0]['src'] if p.get('images') and p['images'] else None))
                for p in prods
            ]
    except Exception:
        pass
    try:
        home_r = requests.get(base_url, timeout=10)
        if home_r.status_code != 200:
            return None
        soup = BeautifulSoup(home_r.text, 'html.parser')
        if soup.title and soup.title.string:
            insights.brand_name = soup.title.string.strip()
        hero_prods = []
        for a in soup.find_all('a', href=True):
            href = a['href']
            if '/products/' in href:
                title = a.text.strip() or href.split('/')[-1]
                hero_prods.append(Product(title=title, url=urljoin(base_url, href)))
        insights.hero_products = hero_prods[:10]
        about_text = ''
        if soup.find(string=lambda t: t and 'about' in t.lower()):
            abt_sec = soup.find(string=lambda t: t and 'about' in t.lower()).parent
            about_text = abt_sec.get_text(' ', strip=True)
        if about_text:
            insights.about_text = about_text
        all_links = extract_links(soup, base_url)
        insights.important_links = all_links
        for pol_type in ['privacy', 'refund']:
            url = urljoin(base_url, f"/policies/{pol_type}-policy.html")
            r = requests.get(url, timeout=5)
            if r.status_code == 200:
                text = BeautifulSoup(r.text, 'html.parser').get_text(' ', strip=True)[:1000]
                setattr(insights, f'{pol_type}_policy', text)
        insights.social_handles = extract_social_handles(soup)
        insights.contact_details = extract_contact_details(soup)
        insights.faqs = extract_faqs(soup)
    except Exception:
        return None
    return insights.dict()
