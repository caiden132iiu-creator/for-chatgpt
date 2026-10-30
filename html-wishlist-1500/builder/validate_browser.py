"""Full-corpus browser rendering plus real interactions, without outbound requests."""
import asyncio, json, re, time, sys
import threading, http.server, functools
from pathlib import Path
from playwright.async_api import async_playwright
from data import QUIZZES
from PIL import Image, ImageDraw
from paths import ROOT

SCREEN=ROOT/'previews';SCREEN.mkdir(exist_ok=True)
CSS=(ROOT/'assets'/'tailwind-2.2.19.min.css').read_bytes()
CDN='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'
RECORDS=[json.loads(line) for line in (ROOT/'manifest.jsonl').read_text().splitlines()]
SCREEN_TOPICS={1,3,11,19,28,29,38,41,54,60,63,70,77,78,82,84,85,86,87,89}

async def exercise(page,r):
    t,n=r['topic_id'],r['variant']
    async def text(selector):return (await page.locator(selector).inner_text()).strip()
    if t==46:
        await page.locator('#increment').click();assert await text('#score')=='1'
        await page.locator('#increment').click();assert await text('#score')=='2'
        await page.locator('#reset').click();assert await text('#score')=='0'
    elif t==47:
        assert await page.locator('#task-list li').count()==3
        await page.locator('#new-task').fill('Review the garden plan')
        await page.locator('#todo-form button').click()
        assert await page.locator('#task-list li').count()==4
        await page.locator('#task-list li').last.locator('input').check()
        assert await text('#task-count')=='1 of 4 completed'
        await page.locator('#task-list li').last.locator('button').click()
        assert await text('#task-count')=='0 of 3 completed'
        await page.locator('#new-task').fill('   ');await page.locator('#todo-form button').click()
        assert await page.locator('#task-list li').count()==3
    elif t==48:
        await page.locator('#expand-faq').click();assert await page.locator('details:not([open])').count()==0
        await page.locator('#expand-faq').click();assert await page.locator('details[open]').count()==0
        await page.locator('summary').first.click();assert await page.locator('details[open]').count()==1
    elif t==49:
        await page.locator('#tab-1').click();assert await page.locator('#panel-1').is_visible()
        assert await page.locator('#tab-1').get_attribute('aria-selected')=='true'
        await page.locator('#tab-1').press('ArrowRight');assert await page.locator('#panel-2').is_visible()
        await page.locator('#tab-2').press('Home');assert await page.locator('#panel-0').is_visible()
    elif t==50:
        questions=QUIZZES[(n-1)%len(QUIZZES)][1]
        for i,q in enumerate(questions):await page.locator(f'input[name="question-{i}"][value="{q[2]}"]').check()
        await page.locator('#quiz-form button[type=submit]').click();assert (await text('#quiz-result')).startswith('3 / 3 correct.')
        await page.locator('input[name="question-0"][value="1"]').check()
        await page.locator('#quiz-form button[type=submit]').click();assert (await text('#quiz-result')).startswith('2 / 3 correct.')
        await page.locator('#quiz-form button[type=reset]').click();assert not await page.locator('#quiz-result').is_visible()
    elif t==51:
        await page.locator('#menu-toggle').click();assert await page.locator('#collection-menu').is_visible()
        await page.locator('#menu-toggle').press('Escape');assert not await page.locator('#collection-menu').is_visible()
        await page.locator('#menu-toggle').click();await page.locator('#collection-menu a').first.click()
        assert await page.locator('#menu-toggle').get_attribute('aria-expanded')=='false'
    elif t==52:
        await page.locator('#next-slide').click();assert await text('#slide-position')=='2 / 4'
        await page.locator('#previous-slide').click();assert await text('#slide-position')=='1 / 4'
        await page.locator('#previous-slide').click();assert await text('#slide-position')=='4 / 4'
        assert await page.locator('.slide:visible').count()==1
    elif t==53:
        light=await page.locator('body').evaluate('(el)=>getComputedStyle(el).backgroundColor')
        await page.locator('#theme-toggle').click();assert await page.locator('#theme-toggle').get_attribute('aria-pressed')=='true'
        dark=await page.locator('body').evaluate('(el)=>getComputedStyle(el).backgroundColor');assert dark!=light
        await page.locator('#theme-toggle').click();assert await page.locator('body').evaluate('(el)=>getComputedStyle(el).backgroundColor')==light
    elif t==54:
        for name,value in [('bill','100'),('tip','20'),('people','4')]:await page.locator(f'[name={name}]').fill(value)
        await page.locator('#tip-form button').click()
        assert await text('#tip-value')=='$20.00' and await text('#total-value')=='$120.00' and await text('#person-value')=='$30.00'
        await page.locator('[name=people]').fill('0');assert await text('#person-value')=='—'
        await page.locator('[name=people]').fill('1');assert await text('#person-value')=='$120.00'
    elif t==55:
        assert int(await text('#timer-days'))>0
        await page.evaluate("Date.now=()=>Date.parse(document.getElementById('countdown').dataset.deadline)+1000")
        await page.wait_for_function("document.getElementById('countdown-status').textContent.includes('Launch day')",timeout=3000)
        assert await text('#timer-days')=='00' and await text('#timer-seconds')=='00'
    elif t==56:
        await page.locator('#open-dialog').click();assert await page.locator('#workshop-dialog').is_visible()
        await page.keyboard.press('Escape');assert not await page.locator('#workshop-dialog').is_visible()
        await page.locator('#open-dialog').click();await page.locator('#workshop-dialog button').click();assert not await page.locator('#workshop-dialog').is_visible()
    elif t==57:
        await page.locator('#light-toggle').click();assert await page.locator('#light-toggle').get_attribute('aria-checked')=='true'
        assert await page.locator('#bulb').evaluate("el=>el.classList.contains('on')")
        await page.locator('#light-toggle').click();assert await text('#light-status')=='The light is off'
    elif t==58:
        await page.locator('#start-reaction').click();await page.locator('#reaction-pad').click();assert 'Too soon' in await text('#reaction-result')
        await page.locator('#start-reaction').click();await page.wait_for_selector('#reaction-pad.ready',timeout=4000)
        await page.locator('#reaction-pad').click();assert re.search(r'\d+ ms',await text('#reaction-result'))
    elif t==59:
        await page.evaluate('Math.random=()=>0')
        await page.locator('[data-choice=paper]').click();assert await text('#wins')=='1'
        await page.locator('[data-choice=rock]').click();assert await text('#ties')=='1'
        await page.locator('[data-choice=scissors]').click();assert await text('#losses')=='1'
        await page.locator('#reset-match').click();assert await text('#wins')==await text('#ties')==await text('#losses')=='0'
    elif t==60:
        pairs=await page.locator('.memory-card').evaluate_all('(cards)=>cards.map(c=>c.dataset.pair)')
        a,b=next((i,j) for i in range(8) for j in range(i+1,8) if pairs[i]!=pairs[j])
        await page.locator('.memory-card').nth(a).click();await page.locator('.memory-card').nth(b).click()
        await page.wait_for_function("[...document.querySelectorAll('.memory-card')].every(c=>c.textContent==='?')",timeout=2000)
        await page.locator('#restart-memory').click();pairs=await page.locator('.memory-card').evaluate_all('(cards)=>cards.map(c=>c.dataset.pair)')
        for symbol in dict.fromkeys(pairs):
            for i,value in enumerate(pairs):
                if value==symbol:await page.locator('.memory-card').nth(i).click()
        assert await page.locator('.memory-card:disabled').count()==8 and await text('#memory-moves')=='4'
        assert 'All four pairs found' in await text('#memory-status')
        await page.locator('#restart-memory').click();assert await page.locator('.memory-card:disabled').count()==0
    elif t==61:
        maximum=50 if n%2 else 100;target=1+int(.49*maximum)
        await page.evaluate('Math.random=()=>.49');await page.locator('#new-number').click()
        for value,hint in [(1,'Too low'),(maximum,'Too high'),(maximum,'already tried'),(target,'Found it')]:
            await page.locator('[name=guess]').fill(str(value));await page.locator('#guess-form button').click();assert hint in await text('#guess-hint')
        assert await page.locator('[name=guess]').is_disabled()
        await page.locator('#new-number').click();assert not await page.locator('[name=guess]').is_disabled()
        for value in range(1,8):await page.locator('[name=guess]').fill(str(value));await page.locator('#guess-form button').click()
        assert 'Out of attempts' in await text('#guess-hint')
    elif t==6:
        card=page.locator('[data-order-item]').first;price=int(await card.get_attribute('data-price'))
        await card.locator('[data-change="1"]').click();await card.locator('[data-change="1"]').click()
        assert await card.locator('.quantity').inner_text()=='2'
        assert await text('#basket-total')==f'${price*2/100:.2f}'
        for _ in range(3):await card.locator('[data-change="-1"]').click()
        assert await card.locator('.quantity').inner_text()=='0' and await text('#basket-total')=='$0.00'
    elif t==41:
        task=page.locator('[data-column="0"] .board-task').first
        title=await task.locator('h4').inner_text();await task.locator('button').click()
        assert await page.locator('[data-column="0"] .board-task').count()==2
        assert await page.locator('[data-column="1"] .board-task').count()==4
        assert title in await text('#board-status')
    elif t==43:
        await page.locator('#folder-saved').click();assert await page.locator('#message-list button:visible').count()>0
        await page.locator('#message-search').fill('no-match-qqq');assert await page.locator('#no-messages').is_visible()
        await page.locator('#message-search').fill('');await page.locator('#folder-all').click();assert await page.locator('#message-list button:visible').count()==7
        await page.locator('#message-list button').last.click();assert await text('#message-subject')
    elif t==44:
        first=await text('#track-title');await page.locator('#next-track').click();assert await text('#track-title')!=first
        await page.locator('#previous-track').click();assert await text('#track-title')==first
        await page.locator('#play-track').click();assert await page.locator('#play-track').get_attribute('aria-pressed')=='true'
        await page.locator('#volume').fill('10');await page.locator('#play-track').click();assert await page.locator('#play-track').get_attribute('aria-pressed')=='false'
    elif t==45:
        before=int(await text('#follower-count'));await page.locator('#follow-profile').click();assert int(await text('#follower-count'))==before+1
        await page.locator('#follow-profile').click();assert int(await text('#follower-count'))==before

async def exercise_forms(page):
    """Exercise all distinct topic forms with valid and invalid inputs."""
    forms=page.locator('.local-form')
    for j in range(await forms.count()):
        form=forms.nth(j);controls=form.locator('input,select,textarea')
        for i in range(await controls.count()):
            control=controls.nth(i);tag=await control.evaluate('(el)=>el.tagName.toLowerCase()');typ=await control.get_attribute('type') or ''
            name=await control.get_attribute('name') or ''
            if tag=='select':await control.select_option(index=1)
            elif tag=='textarea':await control.fill('Please share the next available date and access information.')
            elif typ=='file':await control.set_input_files({'name':'application.txt','mimeType':'text/plain','buffer':b'Sample applicant. Experience: community workshops and accessible product design.'})
            elif typ=='radio':
                if not await form.locator(f'input[name="{name}"]:checked').count():await control.check()
            elif typ=='checkbox':await control.check()
            elif typ=='email':await control.fill('reader@example.com')
            elif typ=='password':await control.fill('Sample-Only-482!')
            elif typ=='date':await control.fill('2027-06-14' if name=='checkout' else '2027-06-12')
            elif typ=='number':await control.fill('25' if name=='donation-amount-usd' else '2')
            elif name=='card-number':await control.fill('4242 4242 4242 4242')
            elif name=='card-expiry':await control.fill('12/29')
            elif name=='security-code':await control.fill('123')
            else:await control.fill('Robin Taylor' if 'name' in name else '42 Cedar Street')
        await form.locator('button[type=submit]').click()
        assert 'Ready to review' in await form.locator('.form-status').inner_text()
        assert '482!' not in await form.locator('.form-status').inner_text()
        assert '4242 4242' not in await form.locator('.form-status').inner_text()
        start=form.locator('[name=checkin]');end=form.locator('[name=checkout]')
        if await start.count():
            await end.fill('2027-06-11');await form.locator('button[type=submit]').click()
            assert 'after check-in' in await form.locator('.form-status').inner_text()

async def main():
    begun=time.monotonic();queue=asyncio.Queue();results=[];errors=[];functional=0;form_cases=0
    selected=RECORDS
    if '--sample' in sys.argv:selected=[r for r in RECORDS if r['variant']==1 or r['variant']==8]
    delta='--changed-from' in sys.argv
    if delta:
        previous=Path(sys.argv[sys.argv.index('--changed-from')+1])
        previous_hashes={r['id']:r['sha256'] for r in map(json.loads,previous.read_text().splitlines())}
        selected=[r for r in selected if previous_hashes.get(r['id'])!=r['sha256']]
    for r in selected:queue.put_nowait(r)
    mobile_all='--mobile-all' in sys.argv
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    base=f'http://127.0.0.1:{server.server_port}/'
    async with async_playwright() as api:
        browser=await api.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        async def worker(number):
            nonlocal functional,form_cases
            context=await browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
            await context.route(CDN,lambda route:route.fulfill(status=200,content_type='text/css',body=CSS))
            page=await context.new_page();page.set_default_timeout(5000)
            runtime=[];page.on('pageerror',lambda error:runtime.append(str(error)))
            while not queue.empty():
                r=queue.get_nowait();runtime.clear();desktop_ok=False;mobile_ok=False;actions_ok=False
                try:
                    await page.set_viewport_size({'width':1440,'height':1000})
                    await page.goto(base+r['html_path'],wait_until='load',timeout=15000)
                    await page.evaluate("Promise.all([...document.images].map(im=>{im.loading='eager';return im.decode();}))")
                    state=await page.evaluate("({width:innerWidth,scroll:document.documentElement.scrollWidth,h1:parseFloat(getComputedStyle(document.querySelector('h1')).fontSize),images:[...document.images].every(im=>im.complete&&im.naturalWidth>0)})")
                    assert state['scroll']<=state['width']+1, 'Desktop document overflow '+str(state)
                    assert state['h1']>=30 and state['images'],'Missing style or photograph'
                    assert not runtime,'Runtime errors: '+str(runtime)
                    desktop_ok=True
                    if r['variant']==1 and r['topic_id'] in SCREEN_TOPICS:
                        await page.screenshot(path=str(SCREEN/f'{r["topic_id"]:02}-{r["id"]}.png'))
                    if r['topic_id'] in {6,41,43,44,45} or 46<=r['topic_id']<=61:
                        await exercise(page,r);functional+=1;actions_ok=True
                    if r['variant']==1:
                        await exercise_forms(page);form_cases+=await page.locator('.local-form').count()
                    if mobile_all or r['variant'] in [1,8]:
                        await page.set_viewport_size({'width':390,'height':844})
                        await page.evaluate('window.scrollTo(0,0)')
                        state=await page.evaluate("({width:innerWidth,scroll:document.documentElement.scrollWidth})")
                        assert state['scroll']<=state['width']+1,'Mobile document overflow '+str(state)
                        mobile_ok=True
                    assert not runtime,'Interaction runtime errors: '+str(runtime)
                except Exception as exc:
                    errors.append({'file':r['html_path'],'error':str(exc),'runtime':runtime.copy()})
                results.append({'file':r['html_path'],'desktop':desktop_ok,'mobile':mobile_ok,'interaction':actions_ok})
                queue.task_done()
                if len(results)%50==0:print(json.dumps({'checked':len(results),'of':len(selected),'errors':len(errors),'seconds':round(time.monotonic()-begun)}),flush=True)
            await context.close()
        await asyncio.gather(*(worker(i) for i in range(4)))
        await browser.close()
    server.shutdown();server.server_close()
    result={'browser':'Chromium via Playwright','desktop_viewport':'1440 × 1000','mobile_viewport':'390 × 844','pages_loaded':len(results),'desktop_passed':sum(r['desktop'] for r in results),'mobile_passed':sum(r['mobile'] for r in results),'functional_pages_tested':functional,'representative_forms_submitted':form_cases,'tailwind_validation':'Exact pinned 2.2.19 CSS served from a local cache; no outbound requests during browser validation.','elapsed_seconds':round(time.monotonic()-begun,1),'errors':errors,'status':'passed' if not errors else 'failed'}
    report='qa_browser_delta.json' if delta else 'qa_browser_sample.json' if '--sample' in sys.argv else 'qa_browser.json'
    result['validated_html_hashes']={r['id']:r['sha256'] for r in selected}
    (ROOT/report).write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2),flush=True)
    if errors:raise SystemExit(1)

if __name__=='__main__':asyncio.run(main())
