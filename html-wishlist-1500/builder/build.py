"""Build the exact 89-description, 1,500-page wishlist without dependencies."""
from pathlib import Path
import re, json, shutil, hashlib, csv, collections
from core import Page, slug
from paths import ROOT
import render, interactive, dashboards, specials

WISHLIST=ROOT/'original_wishlist.txt'
NAMES=['saas','gym','coffee','hosting','carwash','bakery_order','streaming','salon','pizza','dog_grooming','sports_standings','school_timetable','laptop_comparison','train_schedule','nutrition','office_locations','game_leaderboard','conference_schedule','contact','hotel_booking','job_application','blog_newsletter','login_signup','restaurant_reservation','survey','checkout','event_registration','store','photographer','real_estate','recipes','team','blog','movies','travel','pet_adoption','courses','admin','fitness','finance','project_board','weather','email','music','profile','counter','todo','faq','tabs','quiz','dropdown','slider','dark_mode','tip_calculator','countdown','modal','light_switch','reaction_game','rock_paper_scissors','memory_game','number_guessing','blacksmith','space','robotics','surf_school','lemonade','beekeeping','haunted_house','volcano','dinosaur_museum','cybersecurity','tattoo','board_game_cafe','drone_racing','records','cabins','purple_festival','teal_beach','indigo_conference','pink_sweets','orange_citrus','dark_gaming','yellow_construction','startup','restaurant','hotel','charity','school','portfolio']
def category(t):
    for end,name in [(10,'pricing'),(18,'tables'),(27,'forms'),(37,'grids'),(45,'dashboards'),(61,'interactive'),(76,'unusual'),(83,'colours'),(89,'multisection')]:
        if t<=end:return name
    raise ValueError(t)

def build():
    ROOT.mkdir(exist_ok=True)
    (ROOT/'assets'/'photos').mkdir(parents=True,exist_ok=True)
    photo_source=Path(__file__).parent/'photos'
    if photo_source.is_dir():
        for path in photo_source.glob('*.jpg'):
            target=ROOT/'assets'/'photos'/path.name
            if path.resolve()!=target.resolve():shutil.copyfile(path,target)
        shutil.copyfile(photo_source/'sources.json',ROOT/'assets'/'photo_sources.json')
    assert len(list((ROOT/'assets'/'photos').glob('*.jpg')))==23,'The bundled photo assets are required.'
    source=WISHLIST.read_text()
    entries=re.findall(r'^(.+?)\s*\|\s*X(\d+)\s*$',source,re.M)
    assert len(entries)==89 and sum(int(n) for _,n in entries)==1500
    records=[];catalog=[]
    combined=ROOT/'all_1500_pages.txt'
    with combined.open('w',encoding='utf-8',newline='\n') as out:
        out.write('QUALITY HTML WISHLIST — COMPLETE 1,500-PAGE COLLECTION\n89 requested descriptions. Every page appears below in full.\nEach page also exists separately with a matching description file.\n\n')
        last_category=None
        for t,(description,count) in enumerate(entries,1):
            cat=category(t);count=int(count)
            catalog.append({'topic_id':t,'category':cat,'key':NAMES[t-1],'description':description,'requested':count})
            if cat!=last_category:
                out.write('\n'+'='*88+'\nCATEGORY: '+cat.upper()+'\n'+'='*88+'\n\n')
                last_category=cat
            folder=ROOT/'pages'/cat;folder.mkdir(parents=True,exist_ok=True)
            for n in range(1,count+1):
                c=Page(t,n,description,cat)
                fn=render.pricing if t<=10 else render.tables if t<=18 else render.forms if t<=27 else render.grids if t<=37 else dashboards.render if t<=45 else interactive.render if t<=61 else specials.unusual if t<=76 else specials.colours if t<=83 else specials.multi
                content=fn(c)
                assert content, (t,n)
                html=c.finish(content)
                basename=f'{cat}_{NAMES[t-1]}_{n:02}'
                path=folder/(basename+'.html');path.write_text(html,encoding='utf-8',newline='\n')
                clean_description=description.replace('a event registration','an event registration')
                desc=f'{clean_description[0].upper()+clean_description[1:]}.\nBrand: {c.brand}. Location: {c.city}. Visual direction: {c.palette[0]} palette; '+['a wide opening with a compact masthead','a split introduction with a large image','an editorial introduction with a narrow side column','a framed introduction and generous cards','an accent-colored introductory band','a side introduction with a reading column','a wide photographic or illustrated opening','a compact introduction with a strong vertical accent'][c.layout]+'.'+(' A dark background with light text.' if c.dark else '')+'\n'
                (folder/(basename+'.txt')).write_text(desc,encoding='utf-8')
                rel=path.relative_to(ROOT).as_posix()
                rec={'id':basename,'topic_id':t,'category':cat,'variant':n,'base_description':description,'description':desc.strip(),'html_path':rel,'description_path':str(path.with_suffix('.txt').relative_to(ROOT)),'brand':c.brand,'palette':c.palette[0],'layout':c.layout+1,'component_variant':c.variant+1,'dark':c.dark,'has_javascript':bool(c.scripts),'bytes':len(html.encode()),'sha256':hashlib.sha256(html.encode()).hexdigest(),'split_group':f'topic-{t:02}'}
                records.append(rec)
                out.write('-'*88+'\nFILE: '+rel+'\nDESCRIPTION:\n'+desc+'-'*88+'\n'+html+'\n')
    with (ROOT/'manifest.jsonl').open('w') as f:
        for row in records:f.write(json.dumps(row,ensure_ascii=False)+'\n')
    with (ROOT/'manifest.csv').open('w',newline='') as f:
        fields=['id','topic_id','category','variant','brand','palette','layout','component_variant','dark','has_javascript','bytes','html_path','description_path','split_group','sha256']
        w=csv.DictWriter(f,fields,extrasaction='ignore');w.writeheader();w.writerows(records)
    (ROOT/'wishlist_catalog.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False)+'\n')
    counts=collections.Counter(row['category'] for row in records)
    print(json.dumps({'pages':len(records),'descriptions':len(catalog),'category_counts':dict(counts),'javascript_pages':sum(r['has_javascript'] for r in records),'html_bytes':sum(r['bytes'] for r in records),'combined_bytes':combined.stat().st_size},indent=2))
    browse='# Browse the collection\n\nEach link opens a complete HTML example. All 1,500 pages are listed in manifest.csv and manifest.jsonl.\n\n'
    for cat in counts:
        browse+='## '+cat.title()+'\n\n'
        for row in catalog:
            if row['category']==cat:
                example=next(r for r in records if r['topic_id']==row['topic_id'])
                browse+=f'- [{row["key"].replace("_"," ")}]({example["html_path"]}) — {row["requested"]} variations\n'
        browse+='\n'
    (ROOT/'BROWSE.md').write_text(browse)

if __name__=='__main__':build()
