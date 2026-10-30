from pathlib import Path
from collections import Counter,defaultdict
import json,re,hashlib,statistics
from lxml import html, etree
from paths import ROOT

CDN='https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css'

def validate():
    records=[json.loads(line) for line in (ROOT/'manifest.jsonl').read_text().splitlines()]
    catalog=json.loads((ROOT/'wishlist_catalog.json').read_text())
    errors=[];stats=Counter();lengths=[];script_lengths=[];structures=set();topic_structures=defaultdict(set);texts=set();unique_desc=set()
    assert len(records)==1500
    assert len(list((ROOT/'pages').rglob('*.html')))==1500
    assert len(list((ROOT/'pages').rglob('*.txt')))==1500
    counts=Counter(r['topic_id'] for r in records)
    assert all(counts[row['topic_id']]==row['requested'] for row in catalog)
    scripts=[]
    for record in records:
        path=ROOT/record['html_path'];source=path.read_text();doc=html.document_fromstring(source);t=record['topic_id'];issues=[]
        def check(condition,message):
            if not condition:issues.append(message)
        check(source.startswith('<!DOCTYPE html>') and source.endswith('</html>\n'),'Incomplete HTML document')
        check(len(doc.xpath('//head'))==1 and len(doc.xpath('//body'))==1,'Head/body structure')
        check(doc.get('lang')=='en','Document language')
        check(len(doc.xpath('//h1'))==1,'Exactly one main heading')
        check(len(doc.xpath('//main'))==1,'Main landmark')
        check(bool(doc.xpath('//meta[@name="viewport"]')),'Responsive viewport')
        check(bool(doc.xpath('//link[@href=$url and @rel="stylesheet"]',url=CDN)),'Required Tailwind line')
        check(not re.search(r'lorem ipsum|your company name|todo:|replace me',source,re.I),'Placeholder text')
        check(not doc.xpath('//script[@src]'),'External JavaScript library')
        ids=doc.xpath('//*[@id]/@id');check(len(ids)==len(set(ids)),'Duplicate DOM IDs')
        idset=set(ids)
        for anchor in doc.xpath('//a'):
            target=anchor.get('href','');check(bool(target) and target!='#','Empty link')
            if target.startswith('#'):check(target[1:] in idset,'Unresolved internal link '+target)
        for im in doc.xpath('//img'):
            check(bool(im.get('alt','').strip()),'Unlabeled image')
            file=(path.parent/im.get('src','')).resolve();check(file.is_file(),'Missing bundled image '+im.get('src',''))
            check(file.is_relative_to(ROOT),'Image outside collection')
        for svg in doc.xpath('//svg'):check(bool(svg.xpath('./title')),'Unlabeled illustration')
        for control in doc.xpath('//input[not(@type="hidden")]|//select|//textarea'):
            ident=control.get('id');labels=doc.xpath('//label[@for=$ident]',ident=ident) if ident else []
            check(bool(labels) or bool(control.xpath('ancestor::label')) or bool(control.get('aria-label')),'Unlabeled form control')
        for button in doc.xpath('//button'):check(bool(''.join(button.itertext()).strip()) or bool(button.get('aria-label')),'Unlabeled button')
        tables=doc.xpath('//table')
        for table in tables:
            check(bool(table.xpath('./caption')),'Table without caption')
            check(bool(table.xpath('./thead/tr/th')),'Table without column headers')
            width=len(table.xpath('./thead/tr/th'))
            check(all(len(row.xpath('./td|./th'))==width for row in table.xpath('./tbody/tr')),'Inconsistent table columns')
            check(bool(table.xpath('./tbody/tr/th[@scope="row"]')),'Table without row headers')
        for section in doc.xpath('//main//section'):check(bool(''.join(section.itertext()).strip()),'Empty section')
        scripts_here=doc.xpath('//script[not(@src)]/text()')
        scripts.extend({'file':record['html_path'],'source':s} for s in scripts_here)
        script_lengths.extend(len(s) for s in scripts_here)
        text=' '.join(doc.xpath('//body//text()[not(ancestor::script) and not(ancestor::style)]'))
        check(len(text.split())>=80,'Insufficient content')
        check(bool((ROOT/record['description_path']).read_text().strip()),'Empty description')
        # Required feature checks cover every requested topic, not just a sample.
        if t<=10 or t in [28,30,35,37,62,65,66,67,68,70,73,75,76,77,78,80,81,84,85,86,87]:check('$' in text,'Missing prices')
        table_topics={1,4,9,11,12,13,14,15,16,17,18,38,40,62,65,69,70,73,74,77,79,82,88}
        if t in table_topics:check(bool(tables),'Required table missing')
        form_topics={1,2,4,5,6,7,8,10,*range(19,28),28,29,30,32,33,35,36,37,55,62,63,64,65,67,68,70,71,72,73,75,76,77,78,79,80,81,82,83,*range(84,90)}
        if t in form_topics:check(bool(doc.xpath('//form')),'Required form missing')
        if t==28:check(6<=len(doc.xpath('//main//section[1]//article'))<=9,'Store needs 6–9 products')
        if t==29:check(len(doc.xpath('//main//figure'))>=6 and 'lg:grid-cols-3' in source,'Three-column photographic gallery')
        if t==30:check('beds' in text and 'baths' in text,'Property bed/bath details')
        if t==31:check('min' in text and len(doc.xpath('//main//article'))>=6,'Recipe time and cards')
        if t==21:check(bool(doc.xpath('//input[@type="file"]')),'Resume upload')
        if t==23:check(len(doc.xpath('//form'))==2 and len(doc.xpath('//input[@type="password"]'))==2,'Paired login/sign-up forms')
        if t==25:check(bool(doc.xpath('//input[@type="radio"]')) and bool(doc.xpath('//input[@type="checkbox"]')) and bool(doc.xpath('//select')),'Survey controls')
        if t in range(38,46):check(bool(doc.xpath('//nav[@aria-label="Workspace sections"]')),'App sidebar')
        if t in range(46,62):check(bool(scripts_here),'Inline interaction script')
        if t==54:check(len(doc.xpath('//input[@type="number"]'))==3,'Tip calculator inputs')
        if t==55:check(bool(doc.xpath('//time[@datetime]')),'Explicit launch date')
        if t==56:check(bool(doc.xpath('//dialog')),'Modal dialog')
        if t==57:check(bool(doc.xpath('//*[@role="switch"]')),'Accessible light switch')
        if t==82:check('dark-theme' in doc.xpath('//body')[0].get('class',''),'Dark theme required')
        if t>=84:
            required={84:{'features','reviews','pricing','faq'},85:{'from-the-seasonal-kitchen','a-look-around-the-table','request'},86:{'rooms','amenities','reviews','request'},87:{'mission','impact','stories','request'},88:{'programs','events','staff','request'},89:{'about','skills','projects','reviews','request'}}[t]
            check(required.issubset(idset) and bool(doc.xpath('//header//nav')) and bool(doc.xpath('//footer')),'Required full-page sections')
        if t==11:
            rows=doc.xpath('//table[1]/tbody/tr');wins=[int(row[2].text_content()) for row in rows];losses=[int(row[3].text_content()) for row in rows];points=[int(row[4].text_content()) for row in rows]
            check(sum(wins)==sum(losses) and all(a+b==10 for a,b in zip(wins,losses)) and points==[a*3 for a in wins],'Standings arithmetic')
        if t==14:
            for row in doc.xpath('//table[1]/tbody/tr'):
                start,end=[row[i].text_content() for i in [3,4]];check(end>start,'Train arrival before departure')
        if t==17:
            scores=[int(row[2].text_content().replace(',','')) for row in doc.xpath('//table[1]/tbody/tr')];check(scores==sorted(scores,reverse=True),'Leaderboard sort')
        lengths.append(len(doc.xpath('//*')));stats['tables']+=len(tables);stats['forms']+=len(doc.xpath('//form'));stats['photos']+=len(doc.xpath('//img'));stats['inline_illustrations']+=len(doc.xpath('//svg'));stats['javascript_pages']+=bool(scripts_here)
        structure=' '.join(str(node.tag)+':'+node.get('class','') for node in doc.iter() if isinstance(node.tag,str))
        signature=hashlib.sha256(structure.encode()).hexdigest();structures.add(signature);topic_structures[t].add(signature)
        texts.add(hashlib.sha256(text.encode()).hexdigest());unique_desc.add(hashlib.sha256((ROOT/record['description_path']).read_bytes()).hexdigest())
        if issues:errors.append({'file':record['html_path'],'issues':issues})
    (Path(__file__).parent/'scripts_for_validation.json').write_text(json.dumps(scripts))
    result={'pages_checked':len(records),'paired_descriptions_checked':len(unique_desc),'requested_counts_matched':True,'unique_html_hashes':len(set(r['sha256'] for r in records)),'unique_visible_text_hashes':len(texts),'distinct_dom_and_class_structures':len(structures),'smallest_structural_variety_within_a_topic':min(len(v) for v in topic_structures.values()),'element_count':{'min':min(lengths),'median':statistics.median(lengths),'max':max(lengths)},'inline_javascript_characters':{'min':min(script_lengths),'median':statistics.median(script_lengths),'max':max(script_lengths)},'features':dict(stats),'errors':errors,'status':'passed' if not errors else 'failed'}
    (ROOT/'qa_static.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
    if errors:raise SystemExit(1)

if __name__=='__main__':validate()
