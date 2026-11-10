"""Builds the Word Encounter pages, blog pages and sitemap.xml.
Run automatically by GitHub Actions. Do not edit generated files by hand.
Inputs:  devotionals.txt (daily devotionals) and article-*.txt (blog articles).
Entries dated in the future are published automatically on their date."""
import re, os, json, html, datetime, urllib.parse
E = html.escape
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = ROOT
SITE = 'https://obugheni-polyman.com.ng'
TODAY = os.environ.get('BUILD_DATE') or (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)).date().isoformat()  # Nigeria time (BUILD_DATE is for testing)
MON = ['jan','feb','mar','apr','may','jun','jul','aug','sep','oct','nov','dec']
MONF = ['January','February','March','April','May','June','July','August','September','October','November','December']
HEAD = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0A2342">
<meta name="google-adsense-account" content="ca-pub-2239308137644033">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="{ogt}"><meta property="og:site_name" content="Obugheni-Polyman Consulting Services">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-image.jpg"><meta name="twitter:card" content="summary_large_image">
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
gtag('consent','default',{ad_storage:'denied',analytics_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500});</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2239308137644033" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-8JMWCWRPES"></script>
<script>gtag('js',new Date());gtag('config','G-8JMWCWRPES');</script>
{ld}<link rel="stylesheet" href="/site.css"></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="bar"><a class="brand" href="/">Obugheni-Polyman Consulting</a>
<nav aria-label="Primary"><a href="/">Home</a><a href="/about.html">About</a><a href="/services.html">Services</a><a href="/blog.html">Blog</a><a href="/word-encounter.html">Word Encounters</a><a href="/contact.html">Contact</a></nav></div></header>
<main id="main" class="page">
'''
FOOT = '''</main>
<footer class="foot"><div class="cols">
<div><h4>Obugheni-Polyman Consulting</h4><p>CAC registered micro enterprise, BN 9903940<br>Abua/Odual, Rivers State, Nigeria</p></div>
<div><h4>Explore</h4><ul><li><a href="/">Home</a></li><li><a href="/services.html">Services</a></li><li><a href="/blog.html">Blog</a></li><li><a href="/word-encounter.html">Word Encounters</a></li><li><a href="/resources.html">Resources</a></li><li><a href="/research.html">Research</a></li><li><a href="/websites.html">Website Setup</a></li><li><a href="/#training">Training Academy</a></li></ul></div>
<div><h4>Information</h4><ul><li><a href="/about.html">About</a></li><li><a href="/gallery.html">Our Work in Pictures</a></li><li><a href="/sdgs.html">Sustainable Development Goals</a></li><li><a href="/contact.html">Contact</a></li><li><a href="/terms.html">Terms and Refunds</a></li><li><a href="/privacy.html">Privacy</a></li><li><button type="button" id="cookie-settings" class="lnk">Cookie settings</button></li></ul></div>
</div><p class="copy">&copy; 2026 Obugheni-Polyman Consulting Services (BN 9903940). All rights reserved.</p></footer>
<div id="cookie" role="region" aria-label="Cookie notice" hidden><p><b>Cookies.</b> Google cookies for ads and visit counts stay off unless you accept. <a href="/privacy.html">Privacy Notice</a></p>
<div><button type="button" id="cookie-accept" class="btn">Accept</button><button type="button" id="cookie-decline" class="btn alt">Decline</button></div></div>
<script src="/site.js"></script></body></html>
'''

def page(fn, title, desc, body, ogt='website', ld='', wide=False):
    url = SITE + '/' + fn
    h = HEAD
    for k, v in dict(title=E(title), desc=E(desc), url=url, site=SITE, ogt=ogt, ld=ld).items(): h = h.replace('{' + k + '}', v)
    if wide: h = h.replace('class="page"', 'class="page wide"')
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(h + body + FOOT)

def tc(s):
    if s != s.upper(): return s
    s = re.sub(r'(^|\s)([a-z])', lambda m: m.group(1)+m.group(2).upper(), s.lower())
    return re.sub(r'\s(Of|The|In|A|And|To|For|On)(?=\s)', lambda m: m.group(0).lower(), s)

def parse(block):
    L = [re.sub(r'[_*]', '', l).strip() for l in block.split('\n')]
    L = [l for l in L if l]
    if len(L) < 4: return None
    m = re.search(r'(\d{1,2})\s+([A-Za-z]+)\s+(\d{4})', L[0])
    if not m: return None
    mi = MON.index(m.group(2).lower()[:3])
    key = '%s-%02d-%02d' % (m.group(3), mi+1, int(m.group(1)))
    parts = re.split(r'\s+[–—-]\s+', L[2])
    ref = parts[0].strip(); verse = ' – '.join(parts[1:]).strip('“”"\' ')
    body = []; decl = quote = ''
    for l in L[3:]:
        if re.match(r'Prophetic Declaration', l, re.I): decl = re.sub(r'^Prophetic Declaration\s*:?\s*', '', l, flags=re.I); continue
        if 'EMPOWERMENT' in l.upper() and ':' in l: quote = l.split(':', 1)[1].strip().strip('“”"'); continue
        if re.match(r'Be Empowered', l, re.I): break
        if not decl and not quote: body.append(l)
    return dict(key=key, title=tc(L[1]), ref=ref, verse=verse, body=body, decl=decl, quote=quote, mon=MONF[mi], d=int(m.group(1)), y=m.group(3))

raw = open(os.path.join(ROOT, 'devotionals.txt'), encoding='utf-8').read()
ents = [e for e in (parse(b) for b in re.split(r'^\s*={3,}\s*$', raw, flags=re.M)) if e]
ents.sort(key=lambda e: e['key'], reverse=True)
ents = [e for e in ents if e['key'] <= TODAY]
import datetime
for e in ents:
    dt = datetime.date.fromisoformat(e['key'])
    e['date'] = dt.strftime('%A, ') + '%d %s %s' % (dt.day, MONF[dt.month-1], dt.year)
    slug = re.sub(r'[^a-z0-9]+', '-', e['title'].lower().replace("'", '')).strip('-')
    e['file'] = 'word-encounter-%s-%s.html' % (e['key'], slug)

HEAD = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<meta name="theme-color" content="#0A2342">
<meta name="google-adsense-account" content="ca-pub-2239308137644033">
<link rel="canonical" href="{url}">
<link rel="icon" href="/favicon.ico" sizes="any"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta property="og:type" content="{ogt}"><meta property="og:site_name" content="Obugheni-Polyman Consulting Services">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{site}/og-image.jpg"><meta name="twitter:card" content="summary_large_image">
<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}
gtag('consent','default',{ad_storage:'denied',analytics_storage:'denied',ad_user_data:'denied',ad_personalization:'denied',wait_for_update:500});</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2239308137644033" crossorigin="anonymous"></script>
<script async src="https://www.googletagmanager.com/gtag/js?id=G-8JMWCWRPES"></script>
<script>gtag('js',new Date());gtag('config','G-8JMWCWRPES');</script>
{ld}<link rel="stylesheet" href="/site.css"></head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="bar"><a class="brand" href="/">Obugheni-Polyman Consulting</a>
<nav aria-label="Primary"><a href="/">Home</a><a href="/about.html">About</a><a href="/services.html">Services</a><a href="/blog.html">Blog</a><a href="/word-encounter.html">Word Encounters</a><a href="/contact.html">Contact</a></nav></div></header>
<main id="main" class="page">
'''
FOOT = '''</main>
<footer class="foot"><div class="cols">
<div><h4>Obugheni-Polyman Consulting</h4><p>CAC registered micro enterprise, BN 9903940<br>Abua/Odual, Rivers State, Nigeria</p></div>
<div><h4>Explore</h4><ul><li><a href="/">Home</a></li><li><a href="/services.html">Services</a></li><li><a href="/blog.html">Blog</a></li><li><a href="/word-encounter.html">Word Encounters</a></li><li><a href="/resources.html">Resources</a></li><li><a href="/research.html">Research</a></li><li><a href="/websites.html">Website Setup</a></li><li><a href="/#training">Training Academy</a></li></ul></div>
<div><h4>Information</h4><ul><li><a href="/about.html">About</a></li><li><a href="/gallery.html">Our Work in Pictures</a></li><li><a href="/sdgs.html">Sustainable Development Goals</a></li><li><a href="/contact.html">Contact</a></li><li><a href="/terms.html">Terms and Refunds</a></li><li><a href="/privacy.html">Privacy</a></li><li><button type="button" id="cookie-settings" class="lnk">Cookie settings</button></li></ul></div>
</div><p class="copy">&copy; 2026 Obugheni-Polyman Consulting Services (BN 9903940). All rights reserved.</p></footer>
<div id="cookie" role="region" aria-label="Cookie notice" hidden><p><b>Cookies.</b> Google cookies for ads and visit counts stay off unless you accept. <a href="/privacy.html">Privacy Notice</a></p>
<div><button type="button" id="cookie-accept" class="btn">Accept</button><button type="button" id="cookie-decline" class="btn alt">Decline</button></div></div>
<script src="/site.js"></script></body></html>
'''

def page(fn, title, desc, body, ogt='website', ld='', wide=False):
    url = SITE + '/' + fn
    h = HEAD
    for k, v in dict(title=E(title), desc=E(desc), url=url, site=SITE, ogt=ogt, ld=ld).items(): h = h.replace('{' + k + '}', v)
    if wide: h = h.replace('class="page"', 'class="page wide"')
    open(os.path.join(OUT, fn), 'w', encoding='utf-8').write(h + body + FOOT)

# ---- devotional pages ----
for i, e in enumerate(ents):
    first = re.split(r'(?<=[.!?])\s', e['body'][0])[0]
    desc = (e['ref'] + ': ' + first)[:155].rstrip()
    ld = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"Article","headline":e['title'],"datePublished":e['key'],"dateModified":e['key'],"author":{"@type":"Person","name":"Ukwoma Obugheni P."},"publisher":{"@type":"Organization","name":"Obugheni-Polyman Consulting Services","url":SITE+"/"},"mainEntityOfPage":SITE+'/'+e['file']}) + '</script>\n'
    nav = ''
    if i+1 < len(ents): nav += '<a class="pn" href="/%s">&larr; Previous: %s</a>' % (ents[i+1]['file'], E(ents[i+1]['title']))
    if i > 0: nav += '<a class="pn r" href="/%s">Next: %s &rarr;</a>' % (ents[i-1]['file'], E(ents[i-1]['title']))
    paras = ''.join('<p>%s</p>' % E(p) for p in e['body'])
    share = 'https://wa.me/?text=' + __import__('urllib.parse').parse.quote('%s (%s)\n%s/%s' % (e['title'], e['ref'], SITE, e['file']))
    body = '''<article>
<p class="crumb"><a href="/word-encounter.html">Word Encounters</a> &rsaquo; %s</p>
<h1>%s</h1><p class="meta"><time datetime="%s">%s</time> &middot; By Ukwoma Obugheni P.</p>
<blockquote class="verse"><b>%s</b> &ndash; &ldquo;%s&rdquo;</blockquote>
%s
<p class="decl"><b>Prophetic declaration:</b> %s</p>
<p class="emp"><b>Empowerment:</b> &ldquo;%s&rdquo;</p>
<p><a class="btn wa" href="%s" target="_blank" rel="noopener">Share on WhatsApp</a> <a class="btn alt" href="https://wa.me/2347035749180?text=Please%%20add%%20me%%20to%%20the%%20Daily%%20Word%%20Encounter" target="_blank" rel="noopener">Get the Daily Word on WhatsApp</a></p>
</article><div class="pns">%s</div>
<p><a href="/word-encounter.html">See all Word Encounters</a></p>
''' % (E(e['title']), E(e['title']), e['key'], E(e['date']), E(e['ref']), E(e['verse']), paras, E(e['decl']), E(e['quote']), share, nav)
    page(e['file'], e['title'] + ' | Word Encounter | Obugheni-Polyman Consulting', desc, body, 'article', ld)

# ---- list page ----
items = ''.join('<li><a href="/%s"><span class="d">%s</span><strong>%s</strong><span class="r">%s</span></a><p>%s</p></li>' % (e['file'], E(e['date']), E(e['title']), E(e['ref']), E(re.split(r'(?<=[.!?])\s', e['body'][0])[0])) for e in ents)
page('word-encounter.html', 'Word Encounters: Daily Devotionals | Obugheni-Polyman Consulting',
     'Daily Word Encounter devotionals by Ukwoma Obugheni P. Each one has a King James Version Scripture, teaching, a prophetic declaration and an empowerment line.',
     '<h1>Word Encounters</h1><p class="lead">A daily devotional with a King James Version Scripture, a short teaching, a prophetic declaration and an empowerment line. A new Word Encounter is published each day.</p><ul class="list">%s</ul><p><a class="btn wa" href="https://wa.me/2347035749180?text=Please%%20add%%20me%%20to%%20the%%20Daily%%20Word%%20Encounter" target="_blank" rel="noopener">Get the Daily Word on WhatsApp</a></p>' % items)

def inl(t):
    t = E(t)
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    return re.sub(r'\[(.+?)\]\((.+?)\)', r'<a href="\2">\1</a>', t)
def md(txt):
    out = []; mode = None
    def close():
        nonlocal mode
        if mode: out.append('</%s>' % mode); mode = None
    for line in txt.strip().split('\n'):
        l = line.strip()
        if not l: close(); continue
        if l.startswith('### '): close(); out.append('<h3>%s</h3>' % inl(l[4:]))
        elif l.startswith('## '): close(); out.append('<h2>%s</h2>' % inl(l[3:]))
        elif l.startswith('- ') or l.startswith('+ '):
            tag = 'ul' if l[0] == '-' else 'ol'
            if mode != tag: close(); out.append('<%s class="l">' % tag); mode = tag
            out.append('<li>%s</li>' % inl(l[2:]))
        else: close(); out.append('<p>%s</p>' % inl(l))
    close(); return '\n'.join(out)


# ---- blog articles ----
TOPICS = {
 'ls': ('Learning support', 'Helping children who struggle, at home and in school.'),
 'ie': ('Inclusive education', 'Making classrooms work for every learner.'),
 'se': ('IEPs and special education', 'Planning and measuring support for learners with needs.'),
 'sc': ('School improvement', 'Checking and strengthening how a school works.'),
 'rw': ('Research and writing', 'Projects, dissertations and evidence for decisions.'),
 'fc': ('Faith and counseling', 'Pastoral care, culture and church practice.'),
 'gm': ('Green mobility', 'EV charging, batteries and clean transport.'),
}
arts = []
for fn in sorted(os.listdir(ROOT)):
    if not (fn.startswith('article-') and fn.endswith('.txt')): continue
    raw_a = open(os.path.join(ROOT, fn), encoding='utf-8').read()
    meta_txt, _, body_a = raw_a.partition('\n---\n')
    meta = dict(l.split(':', 1) for l in meta_txt.strip().split('\n') if ':' in l)
    meta = {k.strip(): v.strip() for k, v in meta.items()}
    stem = fn[len('article-'):-4]
    arts.append(dict(stem=stem, file='blog-%s.html' % stem, title=meta['title'], date=meta['date'], topic=meta['topic'], mins=int(meta.get('minutes', 6)),
                     desc=meta['description'], audience=meta.get('audience', ''), cta=meta.get('cta', ''), related=[r.strip() for r in meta.get('related', '').split(',') if r.strip()], body=body_a))
arts = [a for a in arts if a['date'] <= TODAY]
arts.sort(key=lambda a: (a['date'], a['stem']), reverse=True)
by_stem = {a['stem']: a for a in arts}
for a in arts:
    rel_list = [by_stem[r] for r in a['related'] if r in by_stem] or [x for x in arts if x is not a][:2]
    rel = ''.join('<li><a href="/%s">%s</a></li>' % (r['file'], E(r['title'])) for r in rel_list)
    ld = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"Article","headline":a['title'],"datePublished":a['date'],"dateModified":a['date'],"author":{"@type":"Organization","name":"Obugheni-Polyman Consulting Services"},"publisher":{"@type":"Organization","name":"Obugheni-Polyman Consulting Services","url":SITE+"/"},"mainEntityOfPage":SITE+'/'+a['file']}) + '</script>\n'
    body = '<article><p class="crumb"><a href="/blog.html">Blog</a> &rsaquo; %s</p><h1>%s</h1><p class="meta">By Obugheni-Polyman Consulting Services &middot; Abua/Odual, Rivers State &middot; %s &middot; %d-minute read</p>%s<div class="cta"><h2>Need help?</h2><p>%s</p><p><a class="btn" href="/contact.html">Contact us</a> <a class="btn alt" href="/services.html">See our services</a></p></div><h2>Related articles</h2><ul class="l">%s</ul></article><p><a href="/blog.html">Back to the blog</a></p>' % (E(a['title']), E(a['title']), E(a['audience']), a['mins'], md(a['body']), E(a['cta']), rel)
    page(a['file'], a['title'] + ' | Obugheni-Polyman Consulting', a['desc'], body, 'article', ld)

used = []
for a in arts:
    if a['topic'] not in used: used.append(a['topic'])
cards = ''
for k, a in enumerate(arts):
    start = '<span class="tag start">Latest</span>' if k == 0 else ''
    cards += '<li class="bc" data-t="%s"><a href="/%s"><span class="tags"><span class="tag">%s</span>%s</span><strong>%s</strong><span class="d">%s &middot; %d-minute read</span></a><p>%s</p><p><a class="more" href="/%s">Read the article &rarr;</a></p></li>' % (a['topic'], a['file'], TOPICS[a['topic']][0], start, E(a['title']), E(a['audience']), a['mins'], E(a['desc']), a['file'])
filters = '<button type="button" data-t="all" aria-pressed="true">All</button>' + ''.join('<button type="button" data-t="%s" aria-pressed="false">%s</button>' % (t, TOPICS[t][0]) for t in used)
boxes = ''.join('<a href="#articles"><b>%s</b><span>%s</span></a>' % TOPICS[t] for t in used) + '<a href="/services.html"><b>Consulting and training</b><span>How schools and organizations put ideas into practice.</span></a><a href="/word-encounter.html"><b>Faith and personal growth</b><span>The daily Word Encounter devotional.</span></a>'
ldb = '<script type="application/ld+json">' + json.dumps({"@context":"https://schema.org","@type":"CollectionPage","name":"Blog | Obugheni-Polyman Consulting","url":SITE+"/blog.html","description":"Practical guides on learning support, inclusive education, research and community growth.","hasPart":[{"@type":"Article","headline":a['title'],"url":SITE+'/'+a['file']} for a in arts]}) + '</script>\n'
BLOGCSS = '<style>.tf{display:flex;flex-wrap:wrap;gap:8px;margin:6px 0 18px}.tf button{border:1px solid #cfd6e3;background:#fff;color:#0A2342;padding:8px 16px;border-radius:999px;font:600 .9rem inherit;cursor:pointer}.tf button[aria-pressed=true]{background:#0A2342;color:#fff;border-color:#0A2342}.tags{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:4px}.tag{background:#e3eefb;color:#174a8b;border-radius:999px;padding:2px 12px;font-size:.78rem;font-weight:700}.tag.start{background:#fbefc9;color:#7a5c00}.topics{display:grid;grid-template-columns:repeat(auto-fit,minmax(210px,1fr));gap:12px;margin:10px 0 22px}.topics a{display:block;border:1px solid #e1e6ef;border-radius:12px;padding:12px 14px;text-decoration:none;background:#fafcff}.topics b{display:block;color:#0A2342}.topics span{font-size:.88rem;color:#555}.more{font-weight:700}.note2{font-size:.88rem;color:#555}</style>'
BLOGJS = "<script>(function(){var b=document.querySelectorAll('.tf button'),c=document.querySelectorAll('.bc');b.forEach(function(x){x.addEventListener('click',function(){b.forEach(function(y){y.setAttribute('aria-pressed',String(y===x))});c.forEach(function(el){el.hidden=!(x.dataset.t==='all'||el.dataset.t===x.dataset.t)})})})})();</script>"
blogbody = BLOGCSS + '<h1>Blog</h1><p class="lead">Practical guides on learning support, inclusive education, research and community development for parents, teachers, school leaders and students across Nigeria and beyond.</p><h2>What we write about</h2><div class="topics">' + boxes + '</div><h2 id="articles">Latest articles</h2><div class="tf" role="group" aria-label="Filter articles by topic">' + filters + '</div><ul class="list">' + cards + """</ul>
<div class="cta"><h2>Suggest a topic</h2><p>Is there a question you would like us to answer? Tell us, and we will consider it for a future article. You can also ask to be told when a new article is published.</p>
<p><a class="btn wa" href="https://wa.me/2347035749180?text=I%20would%20like%20to%20suggest%20a%20blog%20topic%3A%20" target="_blank" rel="noopener">Suggest a topic on WhatsApp</a> <a class="btn alt" href="https://wa.me/2347035749180?text=Please%20tell%20me%20when%20new%20blog%20articles%20are%20published" target="_blank" rel="noopener">Get new articles</a> <a class="btn alt" href="/contact.html">Contact us</a></p></div>
<p class="note2">Our articles are written by the team at Obugheni-Polyman Consulting Services (CAC BN 9903940) and give general information only. They are not medical, legal or other professional advice. For help with your own situation, <a href="/contact.html">get in touch</a>.</p>""" + BLOGJS
page('blog.html', 'Blog: Guides on Learning, Inclusive Education, Research and Community Growth | Obugheni-Polyman Consulting', 'Practical guides on learning support, inclusive education, research and community growth for parents, teachers, school leaders and students across Nigeria.', blogbody, 'website', ldb)

# ---- sitemap and robots ----
STATIC = ['/', '/services.html', '/about.html', '/training.html', '/safety-training.html', '/inclusive-classroom-iep-training.html', '/research.html', '/resources.html', '/websites.html', '/gallery.html', '/sdgs.html', '/contact.html', '/terms.html', '/privacy.html']
rows = [('/', None, '1.0'), ('/word-encounter.html', TODAY, '0.9'), ('/blog.html', TODAY, '0.9')]
rows += [(u, None, '0.8') for u in STATIC[1:6]] + [(u, None, '0.6') for u in STATIC[6:11]] + [(u, None, '0.5') for u in STATIC[11:]]
rows += [('/' + e['file'], e['key'], '0.8') for e in ents] + [('/' + a['file'], a['date'], '0.8') for a in arts]
def row(u, d, p): return '<url><loc>%s%s</loc>%s<priority>%s</priority></url>\n' % (SITE, u, ('<lastmod>%s</lastmod>' % d) if d else '', p)
open(os.path.join(OUT, 'sitemap.xml'), 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(row(*r) for r in rows) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write('User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n' % SITE)
print('Built', len(ents), 'devotional pages,', len(arts), 'articles. Today (Nigeria):', TODAY)
