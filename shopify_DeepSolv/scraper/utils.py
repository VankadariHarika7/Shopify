
from urllib.parse import urljoin
import re

def extract_social_handles(soup):
    socials = {}
    for a in soup.find_all('a', href=True):
        href = a['href']
        if 'instagram' in href:
            socials['instagram'] = href
        elif 'facebook' in href:
            socials['facebook'] = href
        elif 'tiktok' in href:
            socials['tiktok'] = href
        elif 'twitter' in href:
            socials['twitter'] = href
        elif 'youtube' in href:
            socials['youtube'] = href
    return socials

def extract_contact_details(soup):
    text = soup.get_text(' ', strip=True)
    emails = re.findall(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}', text)
    phones = re.findall(r'\+?\d[\d \-]{7,}\d', text)
    return {
        'emails': emails,
        'phones': phones,
    }

def extract_links(soup, base_url):
    keys = ['order', 'contact', 'blog', 'track']
    links = {}
    for a in soup.find_all('a', href=True):
        txt = a.text.lower()
        for k in keys:
            if k in txt:
                links[k] = urljoin(base_url, a['href'])
    return links

def extract_faqs(soup):
    faqs = []
    for item in soup.find_all(['li', 'div', 'p']):
        text = item.get_text(' ', strip=True)
        if text and text.lower().startswith('q') and '?' in text:
            next_ans = item.find_next(['li', 'div', 'p'])
            ans = next_ans.get_text(' ', strip=True) if next_ans else ''
            faqs.append({'q': text, 'a': ans})
    return faqs
