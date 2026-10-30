"""Representative axe-core checks across all 89 topic families."""
from pathlib import Path
import asyncio,json,threading,http.server,functools,collections
from playwright.async_api import async_playwright
from paths import ROOT

async def main():
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self,*args):pass
    server=http.server.ThreadingHTTPServer(('127.0.0.1',0),functools.partial(Handler,directory=str(ROOT)))
    threading.Thread(target=server.serve_forever,daemon=True).start()
    records=[json.loads(line) for line in (ROOT/'manifest.jsonl').read_text().splitlines()]
    sample=[r for r in records if r['variant']==1+(r['topic_id']%8)]
    css=(ROOT/'assets'/'tailwind-2.2.19.min.css').read_bytes()
    axe=(Path(__file__).parent/'axe.min.js').read_text()
    errors=[];incomplete=collections.Counter();results=[]
    async with async_playwright() as p:
        browser=await p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--no-sandbox','--disable-dev-shm-usage'])
        context=await browser.new_context(viewport={'width':1440,'height':1000},reduced_motion='reduce')
        await context.route('https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css',lambda route:route.fulfill(status=200,content_type='text/css',body=css))
        page=await context.new_page()
        for i,r in enumerate(sample):
            await page.goto(f'http://127.0.0.1:{server.server_port}/'+r['html_path'],wait_until='load')
            await page.add_script_tag(content=axe)
            result=await page.evaluate("axe.run(document,{runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21a','wcag21aa']}})")
            violations=[{'id':v['id'],'impact':v['impact'],'description':v['description'],'nodes':[{'target':node['target'],'summary':node.get('failureSummary')} for node in v['nodes']]} for v in result['violations']]
            if violations:errors.append({'file':r['html_path'],'violations':violations})
            for row in result['incomplete']:incomplete[row['id']]+=1
            results.append({'file':r['html_path'],'passes':len(result['passes']),'violations':len(violations)})
            if (i+1)%20==0:print(json.dumps({'accessibility_checked':i+1,'violating_pages':len(errors)}),flush=True)
        await browser.close()
    server.shutdown();server.server_close()
    report={'checker':'axe-core 4.10.3','scope':'One variant of every requested description; all eight shell layouts represented. WCAG 2 A/AA and 2.1 A/AA rule tags. Automated checks are not a full accessibility audit.','pages_checked':len(sample),'pages_without_violations':len(sample)-len(errors),'incomplete_checks':dict(incomplete),'errors':errors,'status':'passed' if not errors else 'failed'}
    (ROOT/'qa_accessibility.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2),flush=True)
    if errors:raise SystemExit(1)
if __name__=='__main__':asyncio.run(main())
