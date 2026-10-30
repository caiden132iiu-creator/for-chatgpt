from core import *
import json

def plans(c,names,prices,features,unit='/ month',target='request'):
    out=f'<div class="{"grid gap-5 md:grid-cols-3" if c.variant!=3 else "space-y-5"}">'
    for i,(name,price,items) in enumerate(zip(names,prices,features)):
        hi=i==1
        out+=f'<article class="panel p-6 md:p-7 {"border-2 accent-border shadow-lg" if hi else ""}" {"style=\"border-color:var(--accent)\"" if hi else ""}>'
        out+=tag('Our most popular choice' if hi else ['An easy beginning','Room to explore','The complete experience'][i])
        out+=f'<h3 class="text-2xl font-bold mt-5">{e(name)}</h3><p class="my-5"><strong class="text-4xl">{money(price)}</strong> <span class="muted text-sm">{e(unit)}</span></p>{ul(items)}<div class="mt-7">{btn("Choose "+name,target,secondary=not hi)}</div></article>'
    return out+'</div>'

def menu(c,items,title,art=None):
    rows=''
    for i,(name,description,price) in enumerate(items):
        rows+=f'<article class="panel p-5"><div class="flex gap-4 justify-between"><h3 class="text-lg font-semibold">{e(name)}</h3><p class="font-bold accent whitespace-nowrap">{money(round(price+(c.n%7)*.2,2))}</p></div>{p(description,"text-sm mt-2")}</article>'
    body=f'<div class="grid gap-4 {"md:grid-cols-2" if c.variant%2==0 else ""}">{rows}</div>'
    return c.section(title,body)

def testimonials(c,title='A few words from the community'):
    quotes=[('The small details made the whole experience feel easy. We knew what to expect, and there was always a clear next step.','A returning customer'),('Warm, thoughtful, and beautifully organized. It felt like someone had considered the questions before we needed to ask.','A neighborhood regular'),('Clear information and a team that actually listens. We have already recommended it to two friends.','A first-time visitor'),('The right mix of care and practical advice. We left with a better plan and the confidence to follow it through.','A community member'),('A lovely reminder that useful things can be made with patience. We will be coming back for the next chapter.','An early supporter')]
    items=pick(quotes,c.n,3)
    body='<div class="grid gap-5 md:grid-cols-3">'
    for i,(quote,role) in enumerate(items):body+=f'<figure class="panel p-6"><blockquote class="leading-relaxed">“{e(quote)}”</blockquote><figcaption class="text-sm mt-5"><strong>{e(c.person_at(i))}</strong><span class="block muted mt-1">{role}</span></figcaption></figure>'
    return c.section(title,body+'</div>',id='reviews')

def pricing(c):
    t,n=c.t,c.n;body=''
    if t==1:
        vertical,unit,intro,features=SAAS[(n-1)%len(SAAS)]
        c.heading=f'A clearer workspace for {vertical}.'
        c.intro=intro+' Compare monthly plans with straightforward limits and no annual commitment.'
        prices=[9+n%9,29+n%13,79+n%17]
        fs=[[f'3 active {unit}s',features[0],features[1],'Email support'],[f'25 active {unit}s',features[0],features[2],features[3],'Priority support'],[f'Unlimited {unit}s',*features[2:],'Dedicated onboarding']]
        body=c.section('A plan for every stage',plans(c,['Seed','Grow','Scale'],prices,fs),id='pricing')
        body+=c.section('Compare the essentials',table(['Monthly plan','Seed','Grow','Scale'],[['Monthly price',*[money(x) for x in prices]],['People included','2','10','Unlimited'],[features[0],'Included','Included','Included'],[features[3],'Not included','Included','Included'],['Workspace history','30 days','1 year','Unlimited']],'Monthly plan comparison'))+c.form('contact')
    elif t==2:
        c.heading=['Find a stronger everyday.','Move well. Feel more like you.','Your next good habit starts here.','Training that fits a real week.','A little stronger, together.'][n%5]
        c.intro='Small classes, welcoming coaches, and room to train at your own pace. Every membership includes a first-week movement check-in.'
        body=c.section('Choose your membership',plans(c,['Open gym','Classes + gym','Complete coaching'],[29+n,59+n,99+n], [['Open gym every day','Locker access','One orientation session'],['Unlimited coached classes','Open gym included','Monthly progress review'],['Everything in Classes + gym','Two private coaching sessions','Personal training plan']]))
        rows=[[day,cls,time] for day,cls,time in pick([('Monday','Strength foundations','6:30 AM'),('Tuesday','Mobility + balance','12:15 PM'),('Wednesday','Cycle intervals','6:00 PM'),('Thursday','Kettlebell basics','7:00 AM'),('Friday','Recovery flow','5:30 PM'),('Saturday','Community circuit','9:00 AM')],n,6)]
        body+=c.section('A week of good movement',table(['Day','Class','Starts'],rows,'Weekly coached classes · 45 minutes each'))+c.form('signup')
    elif t==3:
        c.heading=['Good coffee. An unhurried hour.','Your corner of the morning.','A familiar cup, a fresh start.','Pull up a chair. Stay a little.','Brewed slowly. Shared gladly.'][n%5]
        c.intro='Freshly ground coffee, seasonal drinks, and pastries baked before the doors open. Oat milk is available at no extra charge.'
        c.hero_image=c.image('coffee','A welcoming coffee counter with freshly prepared drinks','w-full h-72 object-cover')
        body=menu(c,pick(DRINKS,n,6),'The coffee counter')+menu(c,pick(PASTRIES,n,4),'From the pastry case')+c.section('A good place to meet',p(f'Find us in {c.city}. Open Monday–Friday, 7 AM–5 PM, and weekends, 8 AM–4 PM. Please tell the team about allergies before ordering.'))
    elif t==4:
        c.heading='Hosting with room to grow.';c.intro='Start with a personal site, expand to a busy storefront, or bring your whole business. Monthly billing keeps the commitment simple.'
        prices=[4+n%4,12+n%5,29+n%8]
        rows=[['Monthly price',*[money(x) for x in prices]],['Websites','1','10','50'],['SSD storage','20 GB','100 GB','300 GB'],['Monthly bandwidth','100 GB','500 GB','2 TB'],['Daily backups','7 days','30 days','90 days'],['TLS certificates','Included','Included','Included'],['Support','Email','24/7 chat','Priority chat + phone']]
        body=c.section('Basic, Pro, or Business',table(['What is included','Basic','Pro · recommended','Business'],rows,'Compare monthly hosting plans'))+c.section('Clear from the first deployment',ul(['No setup fee or annual contract','A staging site for checking changes before launch','A guided migration checklist for your existing site']))+c.form('contact')
    elif t==5:
        c.heading='A fresh start for the road ahead.';c.intro='Careful hand finishing, water-conscious wash bays, and straightforward packages. Most visits take 20–60 minutes.'
        body=c.section('Choose a clean that fits',plans(c,['Quick refresh','Inside + out','Weekend detail'],[12+n%4,26+n%7,68+n%12],[['Exterior hand wash','Wheel rinse','Streak-free dry'],['Exterior wash','Interior vacuum','Glass and dashboard clean'],['Inside + out included','Fabric spot treatment','Protective wax finish']],unit='/ visit'))+c.form('appointment',title='Book your next wash')
    elif t==6:
        c.heading='A cake worth gathering around.';c.intro='Baked to order in small batches. Each 6-inch cake serves 6–8; allow 48 hours before collection.'
        cards=''
        for i,(name,text,price) in enumerate(pick(CAKES,n,4+n%3)):
            cents=(price+n%6)*100
            cards+=f'<article class="panel overflow-hidden" data-order-item data-price="{cents}">{c.art("cake",name,seed=i)}<div class="p-5"><h3 class="text-xl font-bold">{name}</h3>{p(text,"text-sm mt-2")}<p class="font-bold accent my-4">{money(cents/100)}</p><div class="flex gap-3 items-center"><button type="button" class="quantity-button" data-change="-1" aria-label="Remove one {e(name)}">−</button><output class="quantity" aria-live="polite" aria-label="{e(name)} quantity">0</output><button type="button" class="quantity-button" data-change="1" aria-label="Add one {e(name)}">+</button></div></div></article>'
        body=c.section('Choose your celebration',f'<div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">{cards}</div>')+c.section('Your bakery basket','<div class="panel p-6 flex flex-wrap gap-5 justify-between items-center"><div><p class="muted">Cake subtotal · before any local tax</p><output id="basket-total" class="text-3xl font-bold" aria-live="polite">$0.00</output><p class="text-sm muted mt-2">Up to 12 of each cake. Collection details follow below.</p></div>'+btn('Arrange collection','request')+'</div>')+c.form('contact')
        c.scripts.append('''document.querySelectorAll('[data-change]').forEach(button=>button.onclick=()=>{const card=button.closest('[data-order-item]'),qty=card.querySelector('.quantity');qty.textContent=Math.max(0,Math.min(12,Number(qty.textContent)+Number(button.dataset.change)));let total=0;document.querySelectorAll('[data-order-item]').forEach(item=>total+=Number(item.dataset.price)*Number(item.querySelector('.quantity').textContent));document.getElementById('basket-total').textContent=new Intl.NumberFormat('en-US',{style:'currency',currency:'USD'}).format(total/100);});''')
    elif t==7:
        c.heading='Good stories. A plan that suits you.';c.intro='Independent films, thoughtful documentaries, and new discoveries every Friday. All prices are monthly, with cancellation at any time.'
        body=c.section('Find your screen time',plans(c,['Free','Standard','Premium'],[0,8+n%5,16+n%7],[['A rotating film selection','Ad-supported viewing','One screen at a time'],['The complete film library','No advertising','Two simultaneous screens'],['Everything in Standard','Four simultaneous screens','Selected titles in 4K']]))
        body+=c.section('In this week’s collection',c.cards([(a,b,genre,c.art('poster',a,seed=i)) for i,(a,b,genre,mins) in enumerate(pick(MOVIES,n,3))]))+c.form('contact')
    elif t==8:
        c.heading='A little time, just for you.';c.intro='Unhurried appointments, thoughtful consultations, and a style that works beyond the salon chair. Prices include a wash and finish unless noted.'
        groups=[('Cut + shape',[('Signature cut','Consultation, wash, shape, and finish',48+n),('Restyle appointment','Extra time for a considered change',65+n),('Fringe tidy','A short shape-up between full cuts',12+n%4)]),('Color + tone',[('Gloss refresh','A tonal refresh with natural shine',55+n),('Root touch-up','Targeted color and a polished finish',78+n),('Partial highlights','Light and dimension through the top layers',110+n)]),('Care + finish',[('Scalp reset','Gentle cleanse and scalp massage',28+n),('Deep conditioning','A moisture treatment for dry lengths',22+n),('Occasion styling','A lasting finish for an important day',68+n)])]
        for title,items in pick(groups,n,3):body+=menu(c,items,title)
        body+=c.form('appointment',title='Request an appointment')
    elif t==9:
        c.heading='From the oven to your table.';c.intro='Slow-fermented dough, bright tomato sauce, and a rotating selection of seasonal toppings. Small 10-inch, medium 12-inch, large 16-inch.'
        c.hero_image=c.art('pizza','A freshly baked pizza with seasonal toppings','w-full h-72',n)
        rows=[[name,desc,money(base+n%4),money(base+4+n%4),money(base+9+n%4)] for name,desc,base in pick(PIZZAS,n,6)]
        body=c.section('Pick a pizza, choose a size',table(['Pizza','Toppings','Small · 10″','Medium · 12″','Large · 16″'],rows,'Pizzas made to order · prices before tax'))+c.section('A few good extras',ul(['Gluten-free 12-inch base: add $3; shared kitchen','Vegan cheese available: add $2','House chopped salad: $8 · serves two']))+c.form('reservation')
    elif t==10:
        c.heading='Good grooming, gentle hands.';c.intro='A calmer salon visit with one dog per groomer, comfortable handling, and plenty of time to settle. Starting prices apply to dogs under 25 pounds.'
        body=c.section('Three ways to feel fresh',plans(c,['Bath + brush','Tidy + trim','Full groom'],[29+n,45+n,65+n],[['Coat-friendly wash','Gentle blow dry','Full brush-out'],['Bath + brush included','Face, feet, and hygiene trim','Nail trim'],['Tidy + trim included','Full coat styling','Personal coat-care notes']],unit='/ appointment'))+c.section('Before your first visit',p('Bring a current vaccination record and tell us about sensitivities, previous injuries, or handling preferences. Larger dogs and heavily matted coats are quoted after a short consultation.'))+c.form('contact')
    return body

def tables(c):
    t,n=c.t,c.n;body=''
    if t==11:
        c.heading='Every match moves the table.';c.intro='Follow the community season, compare results, and see who is setting the pace. A win earns three points; every team plays ten matches.'
        teams=[f'{PREFIXES[(n+i)%40]} {x}' for i,x in enumerate(pick(['Falcons','Rovers','United','Foxes','Athletic','Wolves','Sparks','Ravens'],n,6))];wins=[0]*6
        for a in range(6):
            for b in range(a+1,6):
                for repeat in range(2):wins[c.r.choice([a,b])]+=1
        order=sorted(range(6),key=lambda i:(-wins[i],teams[i]))
        rows=[[str(k+1),teams[i],wins[i],10-wins[i],wins[i]*3] for k,i in enumerate(order)]
        body=c.section('Season standings',table(['Rank','Team','Wins','Losses','Points'],rows,f'{c.brand} · completed regular season'))+c.section('The next round',p(f'{teams[order[0]]} and {teams[order[1]]} meet in the final on Saturday, June {12+n%12}, at 4 PM. Gates open one hour before kickoff.'))
    elif t==12:
        c.heading='A week with room to learn.';c.intro=f'Grade {5+n%5} · A balanced week of focused lessons, creative work, movement, and time to recharge.'
        subjects=pick(['Mathematics','Language arts','Biology','World history','Geography','Design + technology','Creative writing','Art studio','Music','Physical education'],n,10)
        rows=[]
        for r,time in enumerate(['8:30–9:20','9:30–10:20','10:35–11:25','11:25–12:10','12:10–1:00','1:10–2:00']):rows.append([time]+(['Lunch + outdoor break']*5 if r==3 else [subjects[(r*3+d)%10] for d in range(5)]))
        body=c.section('Monday through Friday',table(['Time','Monday','Tuesday','Wednesday','Thursday','Friday'],rows,'Weekly learning timetable · local time'))+c.section('Ready for the week',ul(['Bring a notebook, refillable water bottle, and your reading book each day.','Art materials stay in the studio; sports shoes are needed for physical education.','Office hours with teachers: Tuesday and Thursday, 2:15–3 PM.']))
    elif t==13:
        c.heading='Three laptops. One clearer choice.';c.intro='Compare fictional configurations side by side, from a light everyday notebook to a mobile creative workstation. Prices are for the configurations listed.'
        names=[f'{PREFIXES[(n+i)%40]} {x}' for i,x in enumerate(['Air 13','Studio 14','Pro 16'])]
        rows=[['Price',money(699+n*10),money(1099+n*10),money(1699+n*10)],['Display','13.3″ · 1920 × 1200','14″ · 2560 × 1600','16″ · 3200 × 2000'],['Processor','6-core efficiency CPU','10-core balanced CPU','14-core performance CPU'],['Memory','8 GB','16 GB','32 GB'],['SSD storage','256 GB','512 GB','1 TB'],['Weight','2.4 lb','3.1 lb','4.5 lb'],['Typical battery estimate','Up to 14 hours','Up to 12 hours','Up to 9 hours'],['Best for','Notes and everyday tasks','Code and design','Video and large projects']]
        body=c.section('The details that matter',table(['Specification',*names],rows,'Laptop configuration comparison'))+c.section('Match the tool to the work',c.cards([(names[i],text,['Everyday','Balanced','Performance'][i],c.art('device',names[i],seed=i)) for i,text in enumerate(['Light enough for a daily commute and capable of everyday writing, browsing, and calls.','A sharp screen and extra memory for a mixed workload of code, design, and collaboration.','A larger working area and more memory for demanding creative applications.'])]))
    elif t==14:
        c.heading='A better way between places.';c.intro='A sample regional timetable with direct services, local departure times, and clearly marked arrival times. Check the platform board before boarding.'
        stations=pick(['Harbor Central','Pine Junction','Mill Street','Lakeside','Northgate','Oak Crossing','Market Square','River End'],n,5)
        rows=[]
        for i in range(8):
            start=6*60+25+i*70+n%5*5;duration=38+(i%4)*12
            fmt=lambda m:f'{m//60:02}:{m%60:02}'
            rows.append([f'R{210+n*8+i}',stations[i%4],stations[(i%4)+1],fmt(start),fmt(start+duration),f'{duration} min',str(i%4+1)])
        body=c.section('Today’s regional services',table(['Service','From','To','Departs','Arrives','Travel time','Platform'],rows,'Weekday train schedule · all times local'))+c.section('Travel with a little breathing room',ul(['Arrive 10 minutes before departure.','Bicycles travel in the marked carriage, subject to space.','Step-free boarding assistance can be arranged at the station desk.']))
    elif t==15:
        c.heading='Everyday foods, clearly compared.';c.intro='A practical reference for familiar ingredients. Values are approximate for the edible portion shown and vary by preparation and brand.'
        foods=[('Rolled oats, dry',389,16.9,66.3),('Brown rice, cooked',123,2.7,25.6),('Chickpeas, cooked',164,8.9,27.4),('Apple, raw with skin',52,.3,13.8),('Banana, raw',89,1.1,22.8),('Broccoli, steamed',35,2.4,7.2),('Plain Greek yogurt',59,10.3,3.6),('Almonds, raw',579,21.2,21.6),('Lentils, cooked',116,9,20.1),('Sweet potato, baked',90,2,20.7),('Egg, hard-boiled',155,12.6,1.1),('Avocado, raw',160,2,8.5)]
        grams=[80,100,125][n%3]
        rows=[[name,f'{grams} g',round(kcal*grams/100),f'{prot*grams/100:.1f} g',f'{carb*grams/100:.1f} g'] for name,kcal,prot,carb in pick(foods,n,8)]
        body=c.section('Nutrition at a glance',table(['Food','Portion','Calories · kcal','Protein','Carbohydrate'],rows,'Approximate nutrition per listed portion'))+c.section('Use the table thoughtfully',p('Cooked and dry weights are not interchangeable. For a packaged food, use its label; for recipe calculations, weigh ingredients in the state listed. These reference values are not individualized dietary advice.'))
    elif t==16:
        c.heading='Find your nearest friendly desk.';c.intro='Local teams, clear opening hours, and one place to find the contact information you need.'
        rows=[]
        for i,city in enumerate(pick(CITIES,n,6)):rows.append([city,f'{120+n*3+i*11} {pick(["Market Street","Cedar Avenue","River Road","Union Lane","Oak Street","Mill Way"],n,6)[i]}',f'(207) 555-{100+(n*6+i)%100:04}','Mon–Fri · 9 AM–5 PM' if i%2==0 else 'Tue–Sat · 10 AM–6 PM'])
        body=c.section('Our office locations',table(['Office','Address','Telephone','Hours'],rows,'Sample office directory · local opening hours'))+c.section('Plan a visit',p('Walk-ins are welcome during office hours. For a detailed consultation or an accessibility request, use the inquiry form so the right person is available.'))+c.form('contact')
    elif t==17:
        c.heading='The climb, one good run at a time.';c.intro='A fictional season ladder for the community arena. Scores reset each season; ties are ordered by fewer matches played.'
        handles=pick(['MintComet','PixelHeron','OrbitFox','QuietNova','CopperQuest','MossByte','SolarWren','TidalEcho','VelvetRook','EmberGlitch','LunarFinch','CobaltDrift'],n,10)
        data=sorted([(h,c.r.randrange(1200,9800),c.r.randrange(15,66)) for h in handles],key=lambda row:(-row[1],row[2]))
        body=c.section('Season leaderboard',table(['Rank','Player','Score','Matches','Division'],[[i+1,h,f'{score:,}',matches,'Diamond' if i<3 else 'Platinum' if i<7 else 'Gold'] for i,(h,score,matches) in enumerate(data)],'Community ladder · end-of-week standings'))+c.section('Fair play comes first',ul(['Play on a single account for this season.','Report suspected exploits to the moderation team.','Every skill level is welcome in the unranked practice room.']))
    elif t==18:
        c.heading='A day of useful ideas.';c.intro='Practical talks, thoughtful conversations, and enough time between sessions to meet someone new. All sessions take place on the ground floor.'
        topics=pick(['Designing a calmer inbox','Accessible forms in practice','Building a useful data notebook','What a small team can automate','The craft of good documentation','Mapping a service journey','Interfaces that work offline','Making research easier to share'],n,6)
        rows=[[time,topic,c.person_at(i),['Cedar Hall','The Workshop','River Room'][i%3]] for i,(time,topic) in enumerate(zip(['9:30–10:15','10:30–11:15','11:30–12:15','1:15–2:00','2:15–3:00','3:15–4:00'],topics))]
        body=c.section('Your conference schedule',table(['Time','Talk','Speaker','Room'],rows,'One-day program · local time'))+c.section('Between the sessions',ul(['Registration and coffee: 8:45–9:25 AM.','Lunch in the courtyard: 12:15–1:15 PM.','Community questions and closing notes: 4:10–4:40 PM.']))+c.form('event')
    return body

def forms(c):
    t,n=c.t,c.n
    heads={19:('A good conversation starts here.','Tell us what you are working on, what feels unclear, and where a little help would make a difference.'),20:('A quieter place to come back to.','Choose dates, the number of guests, and a room that gives your trip a little breathing space.'),21:('Bring your curiosity to work.','We are building a thoughtful team. Tell us how you work, what you care about, and what you would like to make better.'),22:('Notes for a more considered week.','Independent stories about places, people, and practical ideas. Stay for a good read; return when you have a moment.'),23:('A place for your next chapter.','Check a sign-in or sign-up form in a clear, accessible member portal. This sample does not create an account.'),24:('The table is only the beginning.','Seasonal food, an easy welcome, and time to enjoy both. Request a table for lunch or an unhurried evening.'),25:('Help shape what comes next.','A short community survey about the spaces, sessions, and small details that would make your neighborhood more welcoming.'),26:('Useful things, carefully chosen.','Review your basket and try a complete checkout form. This demonstration does not process a payment or place an order.'),27:('Come for the ideas. Stay for the people.','An independent gathering for curious designers, makers, and community builders. Choose a pass and prepare your registration.')}
    c.heading,c.intro=heads[t]
    if t in [19,20,21,24,27]:
        kind={19:'contact',20:'booking',21:'job',24:'reservation',27:'event'}[t]
        if t==20:return c.section('Three ways to settle in',c.cards([('Garden queen','A restful room overlooking the courtyard.','From $149 / night',c.art('house','Garden-view lodge room',seed=1)),('Corner king','A generous corner room with a reading nook.','From $189 / night',c.art('house','Corner lodge suite',seed=2)),('Terrace suite','A private terrace and room for a longer stay.','From $249 / night',c.image('valley','Open valley views near the lodge'))]))+c.form(kind)
        if t==21:return c.section('Work with care, grow with purpose',ul(['Transparent salary bands published with each role','Flexible hours with four shared collaboration hours','An annual learning budget and regular peer feedback']))+c.form(kind)
        return c.form(kind)
    if t==22:return c.section('Fresh from the journal',c.cards([(a,text,cat,c.image(['forest','cafe','ocean'][i%3],a,crop=n+i)) for i,(a,cat,text) in enumerate(pick(ARTICLES,n,6))]))+c.form('newsletter')
    if t==23:
        signin=c.field('Email address','email',name='email',attrs='autocomplete="username"')+c.field('Password','password',name='password',attrs='autocomplete="current-password" minlength="8"')
        signup=c.field('Full name',attrs='autocomplete="name"')+c.field('Email address','email',name='email',attrs='autocomplete="email"')+c.field('Choose a password','password',name='new-password',attrs='autocomplete="new-password" minlength="8"')
        sign='<div class="grid gap-6 md:grid-cols-2">'
        for title,fields,action in [('Welcome back',signin,'Check sign-in details'),('Make a new start',signup,'Check sign-up details')]:sign+=f'<form class="local-form panel p-6 md:p-8 space-y-5"><h3 class="text-2xl font-bold">{title}</h3>{fields}<button class="btn" type="submit">{action}</button><p class="form-status text-sm muted" role="status"></p></form>'
        c.scripts.append(FORM_JS)
        return c.section('Your member space',sign+'</div>')+c.section('A clear starting point',p('Use at least eight characters in the password field. These forms validate details in this page only; they do not authenticate you, save a password, or create an account.'))
    if t==25:
        survey=f'<form class="local-form panel p-6 md:p-8 max-w-3xl mx-auto space-y-7"><fieldset><legend class="font-bold mb-3">How often do you visit the community space?</legend>'+''.join(f'<label class="flex gap-3 items-center my-3"><input type="radio" name="visit-frequency" value="{value}" required> {value}</label>' for value in ['Every week','A few times a month','A few times a year','Not yet'])+'</fieldset><fieldset><legend class="font-bold mb-3">Which sessions would you enjoy? Choose any.</legend>'+''.join(f'<label class="flex gap-3 items-center my-3"><input type="checkbox" name="interests" value="{value}"> {value}</label>' for value in pick(['Repair workshops','Community cooking','Quiet reading hours','Local history walks','Creative writing','Gardening sessions','Beginner photography'],n,5))+'</fieldset>'+c.field('Best time to take part','select',options=['Weekday mornings','Weekday evenings','Saturday afternoons','Sunday mornings'])+c.field('One thing we could improve','textarea',required=False)+'<button class="btn" type="submit">Review my answers</button><div class="form-status text-sm" role="status"></div></form>'
        c.scripts.append(FORM_JS)
        return c.section('Your neighborhood, your voice',survey)
    if t==26:
        products=pick(PRODUCTS,n,2);subtotal=products[0][2]+products[1][2];shipping=6;tax=round(subtotal*.06,2);total=subtotal+shipping+tax
        fields=c.field('Full name',attrs='autocomplete="shipping name"')+c.field('Email address','email',attrs='autocomplete="email"')+c.field('Street address',attrs='autocomplete="shipping street-address"')+c.field('City',attrs='autocomplete="shipping address-level2"')+c.field('State or region',attrs='autocomplete="shipping address-level1"')+c.field('Postal code',attrs='autocomplete="shipping postal-code"')+c.field('Country','select',options=['United States'])
        payment=c.field('Cardholder name',name='cardholder',attrs='autocomplete="cc-name"')+c.field('Card number · demo only',name='card-number',attrs='inputmode="numeric" autocomplete="off" pattern="[0-9 ]{12,23}" maxlength="23"')+c.field('Expiry · MM/YY',name='card-expiry',attrs='autocomplete="off" pattern="(0[1-9]|1[0-2])/[0-9]{2}" maxlength="5"')+c.field('Security code',name='security-code',attrs='inputmode="numeric" autocomplete="off" pattern="[0-9]{3,4}" maxlength="4"')
        order=''.join(f'<div class="order-line py-3"><span>{e(name)} × 1</span><strong>{money(price)}</strong></div>' for name,text,price in products)+''.join(f'<div class="order-line py-2"><span>{label}</span><span>{money(val)}</span></div>' for label,val in [('Subtotal',subtotal),('Standard shipping',shipping),('Estimated tax · 6%',tax),('Total',total)])
        c.scripts.append(FORM_JS)
        return c.section('Your order, step by step',f'<div class="grid gap-6 md:grid-cols-3"><form class="local-form panel p-6 md:col-span-2"><fieldset><legend class="text-xl font-bold mb-5">Shipping details</legend><div class="grid gap-5 sm:grid-cols-2">{fields}</div></fieldset><fieldset class="mt-8"><legend class="text-xl font-bold mb-5">Payment details</legend><p class="muted text-sm mb-4">Use demonstration details, not a real card. No payment will be taken.</p><div class="grid gap-5 sm:grid-cols-2">{payment}</div></fieldset><button class="btn mt-6" type="submit">Review demo order</button><div class="form-status text-sm mt-4" role="status"></div></form><aside class="panel p-6 self-start"><h3 class="text-xl font-bold mb-4">Order summary</h3>{order}<p class="text-xs muted mt-4">Standard delivery: 3–5 business days. Returns accepted within 30 days for unused items.</p></aside></div>')

def grids(c):
    t,n=c.t,c.n;items=[];body=''
    if t==28:
        c.heading=['Useful objects. Lasting pleasure.','A little better, every day.','Made to be reached for.','Find something worth keeping.','Thoughtful things for familiar places.'][n%5]
        c.intro='A considered collection of home, work, and travel essentials. Honest materials, useful details, and prices you can see at a glance.'
        for i,(name,text,price) in enumerate(pick(PRODUCTS,n,6+n%4)):items.append((name,text,money(price+n%5),c.art('cup',name,seed=i)))
        body=c.section('The everyday collection',c.cards(items))+c.section('Buy with a little breathing room',p('Free standard shipping over $100. Returns within 30 days for unused items. Need help choosing a size or material? Send us a note.'))+c.form('contact')
    elif t==29:
        c.heading='The ordinary, seen a little longer.';c.intro=f'A field portfolio by {c.person}. Quiet landscapes, changing light, and the small details that make a place its own.'
        photos=pick([('ocean','Water, before the wind'),('forest','A path through the green'),('mountain','Where the clouds settle'),('valley','The valley at rest'),('cafe','A gathering place'),('still3','Objects with a story'),('beans','Texture, close to hand'),('pastry','The work of a morning'),('coffee','A familiar ritual')],n,9)
        gallery='<div class="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">'
        for i,(key,title) in enumerate(photos):gallery+=f'<figure class="panel overflow-hidden">{c.image(key,title,"w-full object-cover "+("h-64" if n%2 else "h-48"),n+i)}<figcaption class="p-4"><span class="text-xs accent">Study {n:02}.{i+1:02}</span><h3 class="font-semibold mt-1">{title}</h3></figcaption></figure>'
        body=c.section('Selected photographs',gallery+'</div>')+c.form('contact')
    elif t==30:
        c.heading='A place that feels like your next chapter.';c.intro=f'Explore a sample collection of homes around {c.city}. Clear prices, useful room details, and a little space to picture the everyday.'
        for i in range(6+n%3):
            beds=2+(n+i)%4;baths=1+(n+i)%3;price=235000+beds*53000+(n*7+i*13)*1000
            name=f'{118+n*3+i*17} {pick(["Cedar Lane","Orchard Way","River Street","Alder Court","Meadow Drive","Willow Avenue","Birch Terrace","Laurel Road"],n,8)[i%8]}'
            items.append((name,f'{beds} beds · {baths} baths · {900+beds*320+i*45:,} sq ft. '+['A bright kitchen and a sheltered garden.','Easy access to local shops and the riverside path.','A flexible study and a generous living area.'][i%3],money(price),c.art('house',name,seed=i)))
        body=c.section('Homes with a little more possibility',c.cards(items))+c.form('contact')
    elif t==31:
        c.heading='Good food for a real week.';c.intro='Straightforward recipes, seasonal ingredients, and room for your own small changes. Find something you want to cook tonight.'
        for i,(title,time,level,text) in enumerate(pick(RECIPES,n,6+n%3)):items.append((title,text,f'{time} · {level}',c.art('food',title,seed=i)))
        body=c.section('From the recipe notebook',c.cards(items))+c.section('A well-stocked beginning',ul(['Keep olive oil, beans, rice, and a few favorite spices in the cupboard.','Taste before seasoning again; a little lemon can be as useful as salt.','Read the whole recipe before you start, and make room on the worktop.']))
    elif t==32:
        c.heading='Good work starts with good people.';c.intro='A small, curious team with different skills and a shared habit: listening carefully before making something new.'
        for i in range(4+n%3):items.append((c.person_at(i),TEAM_BIOS[(n+i)%len(TEAM_BIOS)],TEAM_ROLES[(n+i)%len(TEAM_ROLES)],c.image(f'person{i%6+1}',f'Portrait representing {c.person_at(i)}',crop=n+i)))
        body=c.section('Meet the people behind the work',c.cards(items))+c.section('How we work together',ul(['Share what you know and ask when something is unclear.','Make useful progress in small, reviewable steps.','Give time to craft, feedback, and the people affected by our decisions.']))+c.form('contact')
    elif t==33:
        c.heading='A journal for the quietly curious.';c.intro='Stories from independent makers, patient travelers, and people finding a more thoughtful way through ordinary days.'
        for i,(title,cat,text) in enumerate(pick(ARTICLES,n,6+n%3)):items.append((title,text,cat,c.image(['forest','cafe','ocean','still6','coffee','valley'][i%6],title,crop=n+i)))
        body=c.section('The latest dispatches',c.cards(items))+c.form('newsletter')
    elif t==34:
        c.heading='Make tonight a good story.';c.intro='An independent cinema shelf for the evenings when you want to find something a little different. All titles and synopses are original fictional selections.'
        for row,title in enumerate(['Tonight’s discoveries','A second look']):
            posters=''
            for i,(name,text,genre,minutes) in enumerate(pick(MOVIES,n+row*5,5)):
                posters+=f'<article class="panel overflow-hidden">{c.art("poster",name,cls="w-full h-56",seed=row*10+i)}<div class="p-4">{tag(genre)}<h3 class="font-bold text-lg mt-3">{name}</h3><p class="text-xs muted mt-1">{minutes} min · Independent cinema</p>{p(text,"text-sm mt-3")}</div></article>'
            body+=c.section(title,f'<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">{posters}</div>')
    elif t==35:
        c.heading='Take the slower road somewhere new.';c.intro='Small-group journeys built around local knowledge, time outdoors, and a comfortable base. Starting prices are per person for three nights, excluding flights.'
        for i,(place,text,price,key) in enumerate(pick(DESTINATIONS,n,6)):items.append((place,text+' · Three nights, local guide, and breakfast included.',f'From {money(price+n*5)}',c.image(key,place+' landscape',crop=n+i)))
        body=c.section('Your next good horizon',c.cards(items))+c.form('contact')
    elif t==36:
        c.heading='A good home changes everything.';c.intro='Meet a few of the animals waiting for patient, caring homes. Our team helps match energy levels, routines, and the people already in your household.'
        for i,(name,species,age,text) in enumerate(pick(PETS,n,6)):items.append((name,text,f'{species} · {age}',c.art('pet',f'Illustrated portrait of {name}, a {species.lower()}',seed=i)))
        body=c.section('Someone lovely is waiting',c.cards(items))+c.section('An adoption with support',ul(['Begin with a conversation about your home and routine.','Meet your potential companion in a calm, supervised setting.','Leave with care notes and a follow-up contact for settling in.']))+c.form('contact')
    elif t==37:
        c.heading='Learn something you can put to use.';c.intro='Focused courses with practical exercises, clear levels, and room to learn in your own time. One-time prices include the lesson materials.'
        for i,(title,level,price,lessons,text) in enumerate(pick(COURSES,n,6+n%3)):items.append((title,text,f'{level} · {lessons} · {money(price+n%5)}',c.art('device' if i%2 else 'landscape',title,seed=i)))
        body=c.section('Find your next course',c.cards(items))+c.section('Learn at a manageable pace',p('Each lesson ends with a small, useful exercise. Suggested study time is two hours per week; you can pause and return whenever your schedule allows.'))+c.form('contact')
    return body
