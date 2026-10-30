from pathlib import Path
from html import escape
import random, base64, re
from data import *

HERE = Path(__file__).parent
TAILWIND = '<link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">'
def e(value): return escape(str(value), quote=True)
def money(value): return f'${value:,.2f}' if value % 1 else f'${value:,.0f}'
def slug(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
def pick(seq,n,count): return [seq[(n+i)%len(seq)] for i in range(count)]
def p(text, cls=''): return f'<p class="leading-relaxed muted {cls}">{e(text)}</p>'
def ul(items): return '<ul class="space-y-3">'+''.join(f'<li class="flex items-start gap-3"><span class="checkmark accent" aria-hidden="true"></span><span>{e(s)}</span></li>' for s in items)+'</ul>'
def btn(text, target=None, attrs='', secondary=False):
    cl='btn btn-secondary' if secondary else 'btn'
    if target: return f'<a class="{cl}" href="#{e(target)}" {attrs}>{e(text)}<span class="link-arrow" aria-hidden="true"></span></a>'
    return f'<button type="button" class="{cl}" {attrs}>{e(text)}</button>'
def metric(label,value,note=''): return f'<div class="panel p-5"><p class="text-sm muted">{e(label)}</p><p class="text-3xl font-bold mt-2">{e(value)}</p><p class="text-xs muted mt-2">{e(note)}</p></div>'
def table(headers,rows,caption,numbered=False):
    out=f'<div class="panel overflow-x-auto"><table class="w-full text-sm text-left"><caption class="text-left p-5 font-semibold">{e(caption)}</caption><thead><tr>'
    out+=''.join(f'<th scope="col" class="px-5 py-3 whitespace-nowrap">{e(h)}</th>' for h in headers)+'</tr></thead><tbody>'
    for row in rows:
        out+='<tr>'+''.join(f'<{("th scope=\"row\"" if j==0 else "td")} class="px-5 py-4">{e(v)}</{("th" if j==0 else "td")}>' for j,v in enumerate(row))+'</tr>'
    return out+'</tbody></table></div>'
def tag(t):return f'<span class="tag text-xs font-semibold px-3 py-1 rounded-full">{e(t)}</span>'

class Page:
    def __init__(self,topic,n,desc,category):
        self.t,self.n,self.desc,self.category=topic,n,desc,category
        self.r=random.Random(topic*10007+n*71)
        self.layout=(n-1)%8
        self.variant=((n-1)//8)%5
        self.palette=PALETTES[(n*3+topic)%len(PALETTES)]
        forced={77:'purple',78:'teal',79:'indigo',80:'pink',81:'orange',83:'mustard'}
        if topic in forced:self.palette=next(p for p in PALETTES if p[0]==forced[topic])
        self.dark=topic==82 or (topic in [17,34,43,44,59,68,77] and n%4==0)
        self.brand=f'{PREFIXES[(n-1)%len(PREFIXES)]} {SUFFIXES[topic-1]}'
        self.city=CITIES[(topic+n)%len(CITIES)]
        self.person=PEOPLE[(topic+n)%len(PEOPLE)]
        self.sections=[];self.scripts=[];self.serial=0
        self.heading=self.brand
        self.intro='Thoughtful details, clear choices, and a friendly place to begin.'
        self.eyebrow=self.city
        self.hero_image=None
    def person_at(self,i):return PEOPLE[(self.n+self.t+i)%len(PEOPLE)]
    def image(self,key,alt,cls='w-full h-48 object-cover',crop=0):
        return f'<img src="../../assets/photos/{key}.jpg" alt="{e(alt)}" class="{cls}" width="360" height="240" style="object-position:{40+crop%25}% center" loading="lazy">'
    def art(self,kind,label,cls='w-full h-48',seed=0):
        self.serial+=1
        rr=random.Random(self.t*511+self.n*37+seed*107)
        a,b=self.palette[1:3]; gid=f'art-{self.serial}'
        bg=rr.choice([b,'#e4e6eb','#eee9df','#dfebed'])
        pre=f'<svg xmlns="http://www.w3.org/2000/svg" class="{cls}" viewBox="0 0 480 300" role="img" aria-labelledby="{gid}"><title id="{gid}">{e(label)}</title><rect width="480" height="300" fill="{bg}"/>'
        if kind in ['landscape','house','surf','volcano']:
            art=f'<circle cx="{rr.randrange(65,400)}" cy="65" r="36" fill="#f4c569"/><path d="M0 230L110 90L225 226L342 70L480 225V300H0Z" fill="{a}" opacity=".42"/><path d="M0 266Q120 190 240 255T480 232V300H0Z" fill="{a}"/>'
            if kind=='house':art+='<path d="M145 155L242 89L339 155Z" fill="#533d35"/><rect x="163" y="154" width="158" height="111" rx="3" fill="#f8f0df"/><rect x="223" y="204" width="34" height="61" fill="#74533e"/><path d="M180 176H208V202H180ZM274 176H302V202H274Z" fill="#90bbc3"/>'
            if kind=='surf':art+='<path d="M0 228Q100 178 193 235T390 225T540 233V300H0Z" fill="#2b94a4"/><path d="M0 245Q100 206 193 250T390 241" fill="none" stroke="#e4ffff" stroke-width="7"/>'
            if kind=='volcano':art+='<path d="M185 145L235 74L275 144L253 130L232 151L217 132Z" fill="#e46c3c"/><path d="M234 75Q192 36 230 14M250 63Q282 29 262 4" fill="none" stroke="#9b9b9b" stroke-width="14" opacity=".6"/>'
        elif kind in ['food','cake','pizza','lemon','honey']:
            art='<ellipse cx="240" cy="247" rx="140" ry="18" fill="#263238" opacity=".12"/>'
            if kind=='cake':art+=f'<path d="M135 230V130Q240 98 345 130V230Q240 260 135 230Z" fill="{a}"/><ellipse cx="240" cy="130" rx="105" ry="30" fill="#fff3da"/><path d="M135 174Q240 205 345 174M135 206Q240 234 345 206" stroke="#fff3da" stroke-width="12" fill="none"/><circle cx="235" cy="115" r="15" fill="#c35158"/><circle cx="262" cy="120" r="13" fill="#df7371"/>'
            elif kind=='honey':art+='<rect x="169" y="82" width="142" height="167" rx="26" fill="#e5a62e"/><rect x="176" y="63" width="128" height="31" rx="7" fill="#564d38"/><rect x="180" y="134" width="120" height="71" rx="5" fill="#fff6d8"/><path d="M220 169L233 148H258L271 169L258 191H233Z" stroke="#a5731f" stroke-width="4" fill="none"/>'
            elif kind=='lemon':art+='<ellipse cx="226" cy="165" rx="92" ry="67" fill="#f1c53b" transform="rotate(-20 226 165)"/><path d="M287 117Q295 57 352 69Q346 115 287 117Z" fill="#4c8e58"/><circle cx="160" cy="211" r="43" fill="#fff3aa"/><circle cx="160" cy="211" r="34" stroke="#edc33f" stroke-width="6" fill="none"/>'
            else:
                art+='<circle cx="240" cy="155" r="104" fill="#fffaf0"/><circle cx="240" cy="155" r="84" fill="'+('#deaf69' if kind=='pizza' else '#d4a76c')+'"/>'
                for j in range(10):
                    x,y=rr.randrange(180,300),rr.randrange(100,214)
                    art+=f'<circle cx="{x}" cy="{y}" r="{rr.randrange(7,14)}" fill="{rr.choice(["#9f453c","#538452","#e5ce86"])}"/>'
        elif kind in ['person','pet']:
            art=f'<path d="M112 300Q116 202 240 196Q364 202 368 300Z" fill="{a}"/><ellipse cx="240" cy="143" rx="64" ry="73" fill="{rr.choice(["#d29f79","#b27e5b","#e6bc98","#865a46"])}"/>'
            if kind=='person':art+='<path d="M176 135Q156 55 229 56Q319 42 307 135L283 102Q228 126 194 103Z" fill="#463831"/>'
            elif 'rabbit' in label.lower():art+='<ellipse cx="205" cy="66" rx="18" ry="60" fill="#b79a7e"/><ellipse cx="275" cy="66" rx="18" ry="60" fill="#b79a7e"/><ellipse cx="205" cy="66" rx="7" ry="42" fill="#e4b8ad"/><ellipse cx="275" cy="66" rx="7" ry="42" fill="#e4b8ad"/>'
            elif 'dog' in label.lower():art+='<path d="M186 97Q136 81 156 181L180 183L205 112M291 97Q344 81 324 181L300 183L275 112" fill="#76584a"/>'
            else:art+='<path d="M179 117L155 48L216 80M263 80L325 48L300 125" fill="#76584a"/>'
            art+='<circle cx="218" cy="144" r="5" fill="#263238"/><circle cx="264" cy="144" r="5" fill="#263238"/><path d="M225 176Q240 187 255 176" stroke="#543c34" stroke-width="4" fill="none"/>'
        elif kind=='sports':
            art=f'<rect x="60" y="45" width="360" height="210" rx="12" fill="{a}"/><path d="M80 65H400V235H80ZM240 65V235M80 115H130V185H80M400 115H350V185H400" stroke="#fff" stroke-width="4" fill="none" opacity=".8"/><circle cx="240" cy="150" r="48" fill="none" stroke="#fff" stroke-width="4"/><circle cx="240" cy="150" r="8" fill="#fff"/>'
        elif kind=='car':
            art=f'<path d="M92 182L143 164L177 109H307L348 164L389 182V228H92Z" fill="{a}"/><path d="M183 122H238V162H158ZM251 122H297L326 162H251Z" fill="#d8eef2"/><circle cx="159" cy="228" r="30" fill="#303a45"/><circle cx="323" cy="228" r="30" fill="#303a45"/><circle cx="159" cy="228" r="13" fill="#d1dbe2"/><circle cx="323" cy="228" r="13" fill="#d1dbe2"/><path d="M92 192H121M360 192H389" stroke="#f7e6b9" stroke-width="12"/>'
        elif kind=='train':
            art=f'<path d="M105 230H380M130 260H355" stroke="#586575" stroke-width="8"/><rect x="150" y="47" width="180" height="190" rx="35" fill="{a}"/><rect x="169" y="75" width="142" height="72" rx="12" fill="#d1eaf0"/><path d="M240 75V147" stroke="{a}" stroke-width="10"/><circle cx="190" cy="193" r="14" fill="#fff0ba"/><circle cx="290" cy="193" r="14" fill="#fff0ba"/><path d="M195 238L172 270M285 238L308 270" stroke="#303a45" stroke-width="10"/>'
        elif kind=='weather':
            art='<circle cx="220" cy="122" r="55" fill="#edbc45"/><path d="M220 41V19M220 223V201M139 122H117M323 122H301M163 65L147 49M293 195L277 179M277 65L293 49M147 195L163 179" stroke="#d29c31" stroke-width="10"/>'
            if any(w in label.lower() for w in ['cloud','rain','overcast']):art+='<path d="M180 222Q126 216 147 174Q163 151 191 165Q204 119 248 133Q282 132 294 167Q345 158 349 197Q348 225 315 227H180Z" fill="#f5fafc" stroke="#8398a8" stroke-width="5"/>'
            if 'rain' in label.lower():art+='<path d="M205 243L194 267M249 243L238 267M293 243L282 267" stroke="#4384a4" stroke-width="7"/>'
        elif kind=='lamp':
            art=f'<path d="M174 76H306L343 177H137Z" fill="{a}"/><path d="M240 177V251M184 255H296" stroke="#4a535a" stroke-width="12"/><path d="M166 188L146 226M314 188L334 226M240 188V218" stroke="#e1b146" stroke-width="7"/>'
        elif kind=='boardgame':
            art=f'<rect x="84" y="55" width="230" height="190" rx="10" fill="#f5e4b9"/><path d="M100 75H294V225H100ZM100 125H294M100 175H294M165 75V225M230 75V225" fill="none" stroke="{a}" stroke-width="4"/><rect x="316" y="151" width="83" height="83" rx="14" fill="{a}"/><g fill="#fff">'+''.join(f'<circle cx="{x}" cy="{y}" r="7"/>' for x,y in [(335,170),(380,170),(358,192),(335,215),(380,215)])+'</g><circle cx="132" cy="102" r="16" fill="#c66548"/><circle cx="262" cy="202" r="16" fill="#52846b"/>'
        elif kind=='room':
            art='<rect x="38" y="40" width="142" height="132" rx="4" fill="#a5d2e3"/><path d="M109 40V172M38 106H180" stroke="#f8fafc" stroke-width="7"/><rect x="205" y="112" width="215" height="110" rx="14" fill="'+a+'"/><rect x="192" y="171" width="239" height="79" rx="9" fill="#f4f0e6"/><rect x="219" y="141" width="74" height="43" rx="7" fill="#fffbf2"/><rect x="319" y="141" width="74" height="43" rx="7" fill="#fffbf2"/><path d="M192 210H431V249H192Z" fill="'+a+'" opacity=".7"/><path d="M208 249V273M413 249V273" stroke="#654d3d" stroke-width="8"/>'
        elif kind in ['rocket','robot','drone','sword','dinosaur','device']:
            if kind=='rocket':art='<path d="M219 215L232 267L247 232L260 267L273 213" fill="#e99a41"/><path d="M195 211V142Q195 84 240 38Q285 84 285 142V211Z" fill="#f9fafb"/><path d="M195 164L153 222H195M285 164L327 222H285" fill="'+a+'"/><circle cx="240" cy="128" r="28" fill="#82c7db" stroke="'+a+'" stroke-width="9"/>'
            elif kind=='sword':art='<path d="M224 198L224 57L241 29L258 57V198Z" fill="#e9edf2" stroke="#73808c" stroke-width="4"/><path d="M187 201H295" stroke="#b5944e" stroke-width="14"/><path d="M240 211V265" stroke="#614331" stroke-width="19"/><circle cx="240" cy="271" r="14" fill="#b5944e"/>'
            elif kind=='dinosaur':art='<path d="M103 217Q155 163 191 168Q240 92 294 117L302 74L356 70L368 103L327 124L311 204L301 258H275L266 212H211L201 258H173L170 212Q130 236 103 217Z" fill="'+a+'"/><circle cx="339" cy="86" r="5" fill="#fff"/>'
            elif kind=='drone':art='<path d="M175 103L308 222M308 103L175 222" stroke="#515b66" stroke-width="17"/><rect x="207" y="132" width="68" height="56" rx="19" fill="'+a+'"/>'+''.join(f'<ellipse cx="{x}" cy="{y}" rx="49" ry="14" fill="#b6c6cd" stroke="#48525c" stroke-width="3"/>' for x,y in [(175,103),(308,222),(308,103),(175,222)])
            elif kind=='robot':art='<rect x="170" y="77" width="140" height="107" rx="23" fill="'+a+'"/><rect x="187" y="99" width="106" height="60" rx="14" fill="#e6f8f4"/><circle cx="216" cy="128" r="9" fill="#263238"/><circle cx="267" cy="128" r="9" fill="#263238"/><path d="M240 77V46M170 206L133 236M310 206L347 236" stroke="'+a+'" stroke-width="12"/><rect x="185" y="192" width="110" height="60" rx="14" fill="'+a+'"/><circle cx="240" cy="42" r="9" fill="#e5b84f"/>'
            else:art='<rect x="116" y="64" width="249" height="158" rx="12" fill="#35404c"/><rect x="128" y="77" width="225" height="131" rx="4" fill="'+a+'"/><path d="M93 232H388L367 250H117Z" fill="#8396a4"/><path d="M155 113H260M155 136H317M155 159H282M155 183H218" stroke="'+b+'" stroke-width="9" opacity=".8"/>'
        elif kind=='cup' and any(word in label.lower() for word in ['board','basket','notebook','tote','candle','vase','throw','tray','kettle','apron','carafe','towel','pen rest']):
            name=label.lower()
            art='<ellipse cx="240" cy="258" rx="145" ry="17" fill="#263238" opacity=".12"/>'
            if 'board' in name or 'pen rest' in name:art+='<rect x="120" y="105" width="240" height="126" rx="25" fill="#997044"/><rect x="217" y="68" width="46" height="68" rx="18" fill="#997044"/><circle cx="240" cy="88" r="8" fill="'+bg+'"/><path d="M145 133Q240 153 338 131M145 166Q240 190 338 164M145 201Q240 218 338 199" stroke="#b4895d" stroke-width="4" fill="none"/>'
            elif 'notebook' in name:art+='<rect x="154" y="64" width="174" height="192" rx="9" fill="'+a+'"/><path d="M170 64V256" stroke="#f8eddb" stroke-width="7"/><rect x="205" y="112" width="88" height="55" rx="3" fill="#f8eddb"/><path d="M217 130H280M217 145H265" stroke="'+a+'" stroke-width="4"/>'
            elif 'tote' in name:art+='<path d="M155 127H325L342 252H138Z" fill="#ece1c9" stroke="#b29e7b" stroke-width="4"/><path d="M193 130V96Q240 34 287 96V130" stroke="'+a+'" stroke-width="14" fill="none"/><path d="M201 177H280V222H201Z" fill="'+a+'" opacity=".7"/>'
            elif 'basket' in name:art+='<path d="M120 134H360L328 250H152Z" fill="#c4a36d"/><ellipse cx="240" cy="132" rx="120" ry="27" fill="#9b7c4f"/><path d="M133 165H348M142 190H341M147 220H335M175 148L185 247M215 153L220 250M260 153L257 250M303 147L293 250" stroke="#ead1a0" stroke-width="7"/>'
            elif 'candle' in name:art+='<rect x="168" y="125" width="144" height="128" rx="20" fill="'+a+'"/><ellipse cx="240" cy="125" rx="72" ry="18" fill="#f8edd7"/><path d="M240 122Q213 100 239 65Q266 104 240 122Z" fill="#efa63c"/><rect x="198" y="162" width="84" height="53" rx="4" fill="#f8edd7"/>'
            elif 'vase' in name or 'carafe' in name:art+='<path d="M215 55H265V122Q331 160 303 247Q240 265 177 247Q149 160 215 122Z" fill="'+a+'" opacity=".8"/><ellipse cx="240" cy="56" rx="25" ry="7" fill="#fff6df"/><path d="M240 65V159M240 98Q202 80 189 51M240 124Q276 102 296 83" stroke="#4c7650" stroke-width="7" fill="none"/>' if 'vase' in name else '<path d="M214 55H266V125L304 169V247H176V169L214 125Z" fill="#97c4cb" opacity=".75" stroke="#467d8a" stroke-width="4"/>'
            elif 'tray' in name:art+='<path d="M105 128L293 83L383 181L181 237Z" fill="#c5a55e"/><path d="M132 138L286 104L350 176L187 215Z" fill="#e9d49a"/><path d="M105 128V153L181 260L383 204V181" stroke="#90743d" stroke-width="6" fill="none"/>'
            elif 'apron' in name:art+='<path d="M209 61H271L286 108L334 143L312 258H168L146 143L194 108Z" fill="'+a+'"/><path d="M209 61Q240 32 271 61" stroke="#d9c8a8" stroke-width="10" fill="none"/><rect x="199" y="167" width="82" height="52" rx="6" fill="#e9e0cf"/>'
            elif 'kettle' in name:art+='<path d="M165 162Q165 116 240 116Q315 116 315 162V237H165Z" fill="'+a+'"/><path d="M180 123V98Q240 42 300 98V123" stroke="#4b4440" stroke-width="14" fill="none"/><path d="M308 172L352 124L366 137L315 211" fill="'+a+'"/><rect x="221" y="99" width="40" height="19" rx="7" fill="#4b4440"/>'
            else:art+='<path d="M125 116L309 82L359 221L172 255Z" fill="'+a+'"/><path d="M143 147L320 115M152 177L334 149M163 211L346 183" stroke="#fff1d8" stroke-width="10" opacity=".7"/>'
        else:
            art=f'<circle cx="240" cy="152" r="108" fill="{a}"/>'
            if kind=='record':art+='<circle cx="240" cy="152" r="81" fill="#202b36"/><circle cx="240" cy="152" r="29" fill="'+bg+'"/><circle cx="240" cy="152" r="7" fill="#202b36"/>'
            elif kind=='poster':
                art=f'<rect x="110" y="20" width="260" height="260" rx="8" fill="{a}"/><circle cx="{rr.randrange(190,290)}" cy="108" r="51" fill="{b}"/><path d="M110 216L161 142L211 188L271 132L370 225V280H110Z" fill="#26364c"/><path d="M137 245H344M137 260H285" stroke="{b}" stroke-width="6" opacity=".8"/>'
            else:art+='<path d="M190 108H270Q286 108 286 126V213H190Z" fill="#fff5e0"/><path d="M286 130H301Q329 156 301 181H286" fill="none" stroke="#fff5e0" stroke-width="13"/><path d="M214 83Q203 61 221 44M249 83Q239 63 257 43" fill="none" stroke="#fff5e0" stroke-width="6" opacity=".7"/>'
        return pre+art+'</svg>'
    def section(self,title,body,id=None,kicker=None):
        ident=id or slug(title)
        self.sections.append((ident,title))
        self.serial+=1
        sub=f'<p class="eyebrow accent mb-2">{e(kicker)}</p>' if kicker else ''
        return f'<section id="{ident}" class="section-block py-8 md:py-10">{sub}<div class="section-heading mb-6 flex items-center justify-between gap-4"><h2 class="text-2xl md:text-3xl font-bold tracking-tight">{e(title)}</h2><span aria-hidden="true" class="accent text-sm section-number">{len(self.sections):02}</span></div>{body}</section>'
    def cards(self,items,cols=3):
        variants=[f'grid gap-5 sm:grid-cols-2 lg:grid-cols-{cols}','grid gap-6 md:grid-cols-2','grid gap-4 md:grid-cols-3','space-y-5',f'grid gap-6 md:grid-cols-{cols}']
        out=f'<div class="{variants[self.variant]}">'
        for i, item in enumerate(items):
            title,text,extra,image=item
            side=self.variant==3
            out+=f'<article class="panel overflow-hidden {"md:flex md:items-center" if side else "flex flex-col"}">'
            if image:out+=f'<div class="{"md:w-1/3 flex-shrink-0" if side else ""}">{image}</div>'
            out+=f'<div class="p-5 md:p-6 flex flex-col flex-1">{tag(extra) if extra else ""}<h3 class="text-xl font-semibold mt-3 mb-2">{e(title)}</h3>{p(text)}'
            out+='</div></article>'
        return out+'</div>'
    def faq(self,title='A few helpful answers',items=None):
        items=items or pick(FAQS,self.n+self.t,4+(self.n%2))
        body='<div class="space-y-3">'+''.join(f'<details class="panel p-5"><summary class="font-semibold cursor-pointer">{e(q)}</summary><p class="muted leading-relaxed mt-4">{e(a)}</p></details>' for q,a in items)+'</div>'
        return self.section(title,body,id='faq')
    def field(self,label,type='text',name=None,options=None,required=True,attrs=''):
        self.serial+=1;name=name or slug(label);ident=f'f-{self.serial}-{name}'
        req='required' if required else ''
        base=f'id="{ident}" name="{name}" class="field w-full rounded-lg px-3 py-3 mt-2" {req} {attrs}'
        if type=='textarea':control=f'<textarea {base} rows="4" minlength="8"></textarea>'
        elif type=='select':control=f'<select {base}><option value="">Choose an option</option>'+''.join(f'<option value="{e(o)}">{e(o)}</option>' for o in options or [])+'</select>'
        else:control=f'<input type="{type}" {base}>'
        return f'<div><label for="{ident}" class="font-medium text-sm">{e(label)}{" <span class=muted>(optional)</span>" if not required else ""}</label>{control}</div>'
    def form(self,kind='contact',title=None):
        configs={
          'contact':('Let’s talk',['name','email','subject','message'],'Prepare message'),
          'booking':('Plan your stay',['name','email','checkin','checkout','guests','room'],'Review stay request'),
          'reservation':('Save a place at the table',['name','email','date','time','party','note'],'Review reservation'),
          'signup':('Find your next session',['name','email','plan','date'],'Review membership'),
          'newsletter':('A good read, once a month',['email'],'Preview subscription'),
          'job':('Make your next move',['name','email','role','file','message'],'Review application'),
          'event':('Meet us there',['name','email','ticket','guests'],'Review registration'),
          'donate':('Keep good work moving',['name','email','amount','frequency'],'Review donation'),
          'tattoo':('Tell us about your next piece',['name','email','artist','date','message'],'Review consultation')}
        configs['appointment']=('A time set aside for you',['name','email','date','time','service'],'Review appointment')
        title,fields,submit=configs.get(kind,configs['contact']) if title is None else (title,configs[kind][1],configs[kind][2])
        parts=[]
        for f in fields:
            if f=='name':parts.append(self.field('Full name',attrs='autocomplete="name"'))
            elif f=='email':parts.append(self.field('Email address','email',attrs='autocomplete="email"'))
            elif f=='subject':parts.append(self.field('What can we help with?','select',options=['A new project','An existing request','Partnerships','Something else']))
            elif f in ['message','note']:parts.append(self.field('Project details' if kind in ['job','tattoo'] else ('Message' if f=='message' else 'Dietary or access requests'),'textarea',required=f!='note'))
            elif f in ['checkin','checkout','date']:parts.append(self.field({'checkin':'Check-in date','checkout':'Check-out date','date':'Preferred date'}[f],'date',name=f))
            elif f=='guests':parts.append(self.field('Number of guests','number',attrs='min="1" max="12" value="2"'))
            elif f=='party':parts.append(self.field('Party size','select',options=[f'{n} guests' for n in range(1,9)]))
            elif f=='time':parts.append(self.field('Arrival time','select',options=['12:00 PM','1:30 PM','5:30 PM','6:30 PM','7:30 PM','8:30 PM']))
            elif f=='room':parts.append(self.field('Room type','select',options=getattr(self,'room_options',['Garden queen · $149 / night','Corner king · $189 / night','Terrace suite · $249 / night'])))
            elif f=='plan':parts.append(self.field('Membership','select',options=['Open gym','Classes + gym','Complete coaching']))
            elif f=='role':parts.append(self.field('Role','select',options=['Product designer','Front-end engineer','Community coordinator','Operations associate']))
            elif f=='file':parts.append(self.field('Resume · PDF or document','file',attrs='accept=".pdf,.doc,.docx,.txt"'))
            elif f=='ticket':parts.append(self.field('Ticket type','select',options=getattr(self,'ticket_options',['Community pass · $35','Full-day pass · $85','Workshop bundle · $125'])))
            elif f=='service':parts.append(self.field('Service','select',options=['Quick refresh','Inside + out','Weekend detail'] if self.t==5 else ['Signature cut','Restyle appointment','Color consultation','Care + finish']))
            elif f=='amount':parts.append(self.field('Donation amount · USD','number',attrs='min="1" max="50000" step="1" value="25"'))
            elif f=='frequency':parts.append(self.field('Frequency','select',options=['One time','Monthly']))
            elif f=='artist':parts.append(self.field('Preferred artist','select',options=[self.person_at(i) for i in range(3)]))
        self.scripts.append(FORM_JS)
        return self.section(title,f'<div class="grid gap-7 md:grid-cols-3"><aside class="panel p-6"><h3 class="text-xl font-semibold mb-3">{e(self.brand)}</h3>{p("Tell us a little about what you have in mind. Review the details on this page before taking the next step.") }<p class="text-sm mt-5">{e(self.city)}<br>Tuesday–Saturday · 9 AM–5 PM</p>{p("Required fields have a visible label. Personal details stay in this page; this is a working interface sample.","text-xs mt-5")}</aside><form class="panel p-6 md:col-span-2 local-form"><div class="grid gap-5 sm:grid-cols-2">'+''.join(parts)+f'</div><button class="btn mt-6" type="submit">{e(submit)}</button><div role="status" aria-live="polite" class="form-status mt-4 text-sm"></div></form></div>',id='request')
    def finish(self,body):
        layout_names=['wide masthead','split introduction','editorial column','framed canvas','accent band','side masthead','gallery lead','compact app shell']
        links=''.join(f'<a class="nav-link text-sm font-medium" href="#{ident}">{e(title)}</a>' for ident,title in self.sections[:3])
        emblem=f'<span class="brand-mark flex-shrink-0" aria-hidden="true">{e(self.brand[0])}</span>'
        brand=f'<a href="#top" class="flex items-center gap-3 font-bold tracking-tight">{emblem}<span>{e(self.brand)}</span></a>'
        nav=f'<header class="site-header"><div class="max-w-6xl mx-auto px-5 md:px-8 py-5 flex flex-wrap gap-5 items-center justify-between">{brand}<nav aria-label="Main navigation" class="flex flex-wrap gap-x-6 gap-y-3">{links}</nav></div></header>'
        hero_kinds={1:'device',2:'person',4:'device',5:'car',6:'cake',7:'poster',8:'person',10:'pet',11:'sports',12:'device',13:'device',14:'train',15:'food',16:'house',17:'device',18:'device',19:'device',20:'room',21:'person',22:'landscape',23:'device',24:'food',25:'device',26:'cup',27:'device',28:'cup',30:'house',31:'food',34:'poster',36:'pet',37:'device',38:'device',39:'person',40:'device',41:'device',42:'weather',43:'device',44:'record',46:'device',47:'device',48:'device',49:'device',50:'device',51:'landscape',54:'food',55:'rocket',57:'lamp',58:'device',59:'boardgame',60:'landscape',61:'device',64:'robot',67:'honey',68:'house',70:'dinosaur',71:'device',72:'person',73:'boardgame',75:'record',79:'device',82:'device',83:'house',88:'house'}
        hero_photos={29:('ocean','Photographic study of light on the ocean'),32:('person1','A representative studio team portrait'),33:('forest','A landscape from the field journal'),35:('mountain','A mountain landscape for an unhurried journey'),45:('person2','A representative member portrait'),52:('valley','A view from the photographic field story'),53:('forest','A quiet landscape for an unhurried read'),56:('still6','Hand tools ready for a practical workshop'),87:('cafe','A welcoming place for a community meal')}
        if self.hero_image:hero_img=self.hero_image
        elif self.t in hero_photos:
            key,alt=hero_photos[self.t];hero_img=self.image(key,alt,'w-full h-64 md:h-80 object-cover')
        else:hero_img=self.art(hero_kinds.get(self.t,'landscape'),self.brand+' '+('dog grooming illustration' if self.t==10 else 'original illustration'),'w-full h-64 md:h-80',self.n)
        label=f'<p class="eyebrow accent mb-5">{e(self.eyebrow)}</p>'
        words=f'{label}<h1 class="text-4xl md:text-5xl font-bold leading-tight tracking-tight">{e(self.heading)}</h1><p class="muted text-lg leading-relaxed mt-5 max-w-2xl">{e(self.intro)}</p>'
        if self.sections:words+=f'<div class="mt-7 flex flex-wrap gap-3">{btn(self.sections[0][1],self.sections[0][0])}{tag("Thoughtfully local" if self.t not in range(38,46) else "Workspace overview")}</div>'
        hero_variants=[
            f'<div class="max-w-3xl py-10 md:py-16">{words}</div>',
            f'<div class="grid gap-8 md:grid-cols-2 items-center py-10"><div>{words}</div><div class="panel overflow-hidden">{hero_img}</div></div>',
            f'<div class="grid gap-6 md:grid-cols-3 py-12 border-b divider"><div>{label}<p class="text-sm muted">Independent by design.<br>Open to what comes next.</p></div><div class="md:col-span-2">{words.replace(label, "")}</div></div>',
            f'<div class="panel p-6 md:p-10 my-9"><div class="grid gap-7 md:grid-cols-2 items-center"><div>{words}</div><div class="overflow-hidden rounded-xl">{hero_img}</div></div></div>',
            f'<div class="hero-band p-7 md:p-12 my-8 rounded-2xl">{words}</div>',
            f'<div class="grid gap-7 md:grid-cols-3 py-10"><aside class="panel p-6 flex flex-col justify-between"><p class="eyebrow accent">{e(self.palette[0])} edition</p><p class="text-sm muted mt-6">A considered collection from<br>{e(self.city)}.</p></aside><div class="md:col-span-2 py-3">{words}</div></div>',
            f'<div class="py-8"><div class="panel overflow-hidden mb-7">{hero_img}</div><div class="grid gap-6 md:grid-cols-3"><div class="md:col-span-2">{words}</div><aside class="self-end"><p class="eyebrow accent">Explore at your pace</p><p class="muted mt-2">Useful details. Clear choices.<br>A place to start.</p></aside></div></div>',
            f'<div class="panel my-8 p-6 md:p-9 border-l-8 accent-border"><div class="flex flex-wrap gap-5 justify-between items-start"><div class="max-w-3xl">{words}</div><span class="link-arrow accent" style="width:1.4rem;height:1.4rem" aria-hidden="true"></span></div></div>']
        foot=f'<footer class="mt-12 border-t divider"><div class="max-w-6xl mx-auto px-5 md:px-8 py-9 flex flex-wrap gap-6 justify-between"><div><p class="font-bold">{e(self.brand)}</p><p class="text-sm muted mt-2">Made with care in {e(self.city.split(",")[0])}.</p></div><a class="text-sm font-semibold accent" href="#top">Back to top</a></div></footer>'
        a,b,bg,ink=self.palette[1:]
        css=CSS.replace('ACCENT',a).replace('TINT',b).replace('CANVAS',bg).replace('INK',ink)
        font='Georgia, ui-serif, serif' if self.layout in [2,5] or (self.t in [3,6,28,29,62,75,85,86] and self.n%3==0) else 'ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif'
        css+='\nh1,h2{font-family:'+font+'}\n'
        scripts='\n'.join(dict.fromkeys(self.scripts))
        return f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>{e(self.brand)} — {e(self.heading)}</title>\n<meta name="description" content="{e(self.intro)}">\n{TAILWIND}\n<style>\n{css}\n</style>\n</head>\n<body id="top" class="{"dark-theme" if self.dark else ""} antialiased">\n<a href="#main" class="skip-link">Skip to content</a>\n{nav}\n<main id="main" class="max-w-6xl mx-auto px-5 md:px-8 pb-8">\n{hero_variants[self.layout]}\n{body}\n</main>\n{foot}\n'+(f'<script>\n"use strict";\n{scripts}\n</script>\n' if scripts else '')+'</body>\n</html>\n'

FORM_JS='''document.querySelectorAll('.local-form').forEach(form=>form.addEventListener('submit',event=>{
  event.preventDefault();
  const status=form.querySelector('.form-status');
  const start=form.querySelector('[name="checkin"]'),end=form.querySelector('[name="checkout"]');
  if(start&&end&&end.value<=start.value){status.textContent='Choose a check-out date after check-in.';return;}
  if(!form.reportValidity())return;
  const data=new FormData(form),lines=[];
  data.forEach((value,key)=>{if(key.toLowerCase().includes('password')||key.includes('card')||key.includes('security'))return;if(value instanceof File){if(value.name)lines.push('Resume: '+value.name);}else if(value)lines.push(key.replaceAll('-',' ')+': '+value);});
  status.textContent='Ready to review — '+lines.join(' · ')+'. No information has been sent or charged.';
}));'''

CSS='''
.link-arrow{display:inline-block;width:.55rem;height:.55rem;border-top:2px solid currentColor;border-right:2px solid currentColor;flex-shrink:0;margin-left:.35rem}.checkmark{display:inline-block;width:.45rem;height:.8rem;border-bottom:2px solid currentColor;border-right:2px solid currentColor;transform:rotate(40deg);flex-shrink:0;margin:.2rem .15rem 0}.memory-card{font-size:1.2rem!important}
:root{--accent:ACCENT;--tint:TINT;--canvas:CANVAS;--ink:INK;--surface:#fff;--muted:#52616c;--line:#d6dfe3;color-scheme:light}
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--canvas);color:var(--ink);font-family:ui-sans-serif,system-ui,sans-serif}h1,h2,h3,p{overflow-wrap:break-word}button,input,select,textarea{font:inherit}button,a,input,select,textarea,summary{-webkit-tap-highlight-color:transparent}button:disabled{opacity:.5;cursor:not-allowed}a,button,summary,input,select,textarea{outline-offset:4px}a:focus-visible,button:focus-visible,summary:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:3px solid var(--accent)}img,svg{max-width:100%;display:block}svg text{font-family:system-ui,sans-serif}button{cursor:pointer}a{text-decoration:none;color:inherit}[hidden]{display:none!important}.muted{color:var(--muted)}.accent{color:var(--accent)}.panel{background:var(--surface);border:1px solid var(--line);border-radius:1rem;min-width:0}.site-header{background:var(--surface);border-bottom:1px solid var(--line)}.brand-mark{display:inline-flex;align-items:center;justify-content:center;width:2.4rem;height:2.4rem;border-radius:.8rem;background:var(--accent);color:#fff;font-size:1.15rem}.eyebrow{font-size:.72rem;letter-spacing:.14em;font-weight:700;text-transform:uppercase}.tag{display:inline-block;align-self:flex-start;background:var(--tint);color:var(--accent)}.btn{display:inline-flex;align-items:center;justify-content:center;gap:.5rem;border:1px solid transparent;border-radius:.6rem;background:var(--accent);color:#fff;font-weight:650;padding:.8rem 1.1rem;text-align:center;line-height:1.35}.btn:hover{filter:brightness(.93)}.btn-secondary{background:var(--surface);color:var(--accent);border-color:var(--line)}.field{background:var(--surface);color:var(--ink);border:1px solid var(--line);min-width:0}.field:focus{border-color:var(--accent)}input[type=checkbox],input[type=radio]{accent-color:var(--accent)}.divider{border-color:var(--line)}table{border-collapse:collapse;min-width:32rem}thead{background:var(--tint);color:var(--accent)}tbody tr+tr{border-top:1px solid var(--line)}tbody tr:nth-child(even){background:color-mix(in srgb,var(--canvas) 55%,var(--surface))}tbody th{font-weight:600}.hero-band{background:var(--tint)}.accent-border{border-left-color:var(--accent)}.nav-link:hover{text-decoration:underline;text-underline-offset:.3rem}.skip-link{position:absolute;top:-100px;left:1rem;z-index:100;background:var(--surface);padding:1rem;border:2px solid var(--accent)}.skip-link:focus{top:1rem}.dark-theme{--canvas:#111722;--surface:#1c2533;--ink:#f2f5fa;--muted:#bac6d3;--line:#3b495d;--tint:#29364b;--accent:#b6caff;color-scheme:dark}.dark-theme .btn{background:#b6caff;color:#17223c}.dark-theme .btn-secondary{background:var(--surface);color:#b6caff}.dark-theme .brand-mark{background:#b6caff;color:#17223c}.progress-track{height:.55rem;background:var(--tint);border-radius:1rem;overflow:hidden}.progress-fill{height:100%;background:var(--accent);border-radius:1rem}.interactive-stage{min-height:15rem}.game-choice[aria-pressed=true],.tab-button[aria-selected=true]{background:var(--accent);color:var(--surface)}.modal-backdrop{position:fixed;inset:0;background:rgba(10,18,28,.65);z-index:50;display:flex;align-items:center;justify-content:center;padding:1.25rem}.modal-card{max-height:90vh;overflow:auto;max-width:32rem;width:100%}.poster-caption{background:var(--ink);color:var(--surface)}.memory-grid{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:.6rem}.memory-card{aspect-ratio:1;font-size:1.7rem;border:1px solid var(--line);background:var(--tint);border-radius:.7rem;color:var(--ink)}.memory-card.matched{background:var(--accent);color:var(--surface)}.reaction-pad{width:100%;min-height:12rem;border-radius:1rem;background:var(--tint);color:var(--ink);padding:1.5rem;border:2px solid var(--accent);font-size:1.3rem;font-weight:700}.reaction-pad.ready{background:#166534;color:white;border-color:#166534}.light-bulb{transition:background .2s,box-shadow .2s}.light-bulb.on{background:#ffdb69;box-shadow:0 0 70px #ffdb6988}.order-line{display:flex;gap:.8rem;align-items:center;justify-content:space-between}.quantity-button{border:1px solid var(--line);border-radius:.5rem;width:2.2rem;height:2.2rem;background:var(--surface);font-weight:bold}.app-nav a[aria-current=page]{background:var(--tint);color:var(--accent)}.app-nav a{display:block;padding:.7rem .8rem;border-radius:.5rem}.stat-delta{font-size:.75rem;color:var(--accent)}.board-column{background:var(--tint);border-radius:1rem;padding:1rem;min-width:0}.min-w-0{min-width:0}
@media(max-width:640px){h1{font-size:2.3rem!important}.section-number{display:none}.site-header nav{font-size:.8rem}.section-block{scroll-margin-top:1rem}.memory-card{font-size:1.25rem}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}*,*:before,*:after{animation:none!important;transition:none!important}}
'''
