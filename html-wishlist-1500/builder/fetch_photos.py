"""Fetch documented photographic sources; embed small derivatives in each HTML."""
from pathlib import Path
from urllib.request import urlopen, Request
from PIL import Image, ImageOps
import io, json, concurrent.futures

ROOT = Path(__file__).parent / 'photos'
ROOT.mkdir(exist_ok=True)
SOURCES = {}
def add(key, repo, file):
    SOURCES[key] = f'https://raw.githubusercontent.com/StartBootstrap/{repo}/master/src/assets/img/{file}'
for i in range(1, 4):
    add(f'person{i}', 'startbootstrap-agency', f'team/{i}.jpg')
    add(f'person{i+3}', 'startbootstrap-landing-page', f'testimonials-{i}.jpg')
for i in range(1, 7):
    add(f'still{i}', 'startbootstrap-creative', f'portfolio/thumbnails/{i}.jpg')
for key, file in [('coffee','intro.jpg'),('drinks','products-01.jpg'),('pastry','products-02.jpg'),('beans','products-03.jpg'),('cafe','about.jpg')]:
    add(key, 'startbootstrap-business-casual', file)
for key, file in [('mountain','bg-masthead.jpg'),('forest','demo-image-01.jpg'),('valley','demo-image-02.jpg')]:
    add(key, 'startbootstrap-grayscale', file)
add('ocean', 'startbootstrap-landing-page', 'bg-masthead.jpg')
add('code', 'startbootstrap-landing-page', 'bg-showcase-2.jpg')
add('festival', 'startbootstrap-agency', 'header-bg.jpg')

def fetch(item):
    key, url = item
    path = ROOT / (key + '.jpg')
    if not path.exists():
        raw = urlopen(Request(url, headers={'User-Agent':'HTML-Wishlist-Builder/1.0'}), timeout=30).read()
        im = Image.open(io.BytesIO(raw)).convert('RGB')
        size = (200, 200) if key.startswith('person') else (360, 240)
        im = ImageOps.fit(im, size, method=Image.Resampling.LANCZOS)
        im.save(path, quality=62, optimize=True)
    return {'key':key,'source_url':url,'bytes':path.stat().st_size}

if __name__ == '__main__':
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(fetch, SOURCES.items()))
    (ROOT / 'sources.json').write_text(json.dumps(results, indent=2)+'\n')
    print(f'Prepared {len(results)} local photographs; {sum(r["bytes"] for r in results):,} bytes.')
