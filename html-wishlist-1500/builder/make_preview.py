"""Render a compact contact sheet spanning topics, palettes, and shell layouts."""
import asyncio,threading,http.server,functools,json
from pathlib import Path
from playwright.async_api import async_playwright
from PIL import Image,ImageDraw,ImageFont
from paths import ROOT

async def main():
    picks=[(1,2),(3,3),(11,4),(19,5),(28,6),(29,7),(38,8),(54,1),(63,2),(77,4),(82,5),(86,6)]
    records=[json.loads(line) for line in (ROOT/'manifest.jsonl').read_text().splitlines()]
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    css=(ROOT/'assets'/'tailwind-2.2.19.min.css').read_bytes()
    images=[];previews=ROOT/'previews';previews.mkdir(exist_ok=True)
    async with async_playwright() as api:
        browser=await api.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        page=await browser.new_page(viewport={'width':1440,'height':1100},reduced_motion='reduce')
        await page.route('https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css',lambda route:route.fulfill(status=200,content_type='text/css',body=css))
        for topic,variant in picks:
            r=next(r for r in records if r['topic_id']==topic and r['variant']==variant)
            await page.goto(f'http://127.0.0.1:{server.server_port}/'+r['html_path'],wait_until='load')
            await page.evaluate("Promise.all([...document.images].map(im=>{im.loading='eager';return im.decode();}))")
            path=previews/f'contact-sheet-{topic:02}.png'
            await page.screenshot(path=str(path))
            images.append((path,r))
        await browser.close()
    server.shutdown();server.server_close()
    width,height=440,337;gap=20;labelheight=44
    out=Image.new('RGB',(3*width+4*gap,4*(height+labelheight)+5*gap+80),'#e8edf2')
    draw=ImageDraw.Draw(out)
    try:
        font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',17)
        titlefont=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',27)
    except OSError:font=titlefont=ImageFont.load_default()
    draw.text((gap,22),'1,500 HTML examples / 89 requested topics',fill='#203047',font=titlefont)
    for i,(path,r) in enumerate(images):
        x=gap+(i%3)*(width+gap);y=80+gap+(i//3)*(height+labelheight+gap)
        im=Image.open(path).convert('RGB').resize((width,height),Image.Resampling.LANCZOS)
        out.paste(im,(x,y));draw.rounded_rectangle((x,y+height,x+width,y+height+labelheight),radius=4,fill='white')
        label=r['id'].replace(r['category']+'_','',1).replace('_',' ').title()
        draw.text((x+12,y+height+12),label,fill='#203047',font=font)
    out.save(ROOT/'preview.jpg',quality=88,optimize=True)
    print('Prepared preview.jpg from 12 rendered pages spanning all eight shell layouts.')
if __name__=='__main__':asyncio.run(main())
