# Content for the miguel-escobar.com redesign (V47): Mig's copy, verbatim from the site, and its links.
import os

REPO = '/home/claude/miguel-escobar-site'
UL = ('color: inherit; text-decoration-line: underline; text-decoration-color: var(--ul); text-underline-offset: 5px; '
      'text-decoration-thickness: 1px;')


def a(href, text, style=UL, cls='ul', extra=''):
    attrs = f'href="{href}"'
    if href.startswith('http'):
        attrs += ' target="_blank" rel="noopener"'
    if cls:
        attrs += f' class="{cls}"'
    return f'<a {attrs}{extra} style="{style}">{text}</a>'


NAME = ('MIGUEL', 'ESCOBAR')
STATEMENT = 'Editorial instincts and creative acuity for the scale and stakes of tech.'   # V60, Mig's revision
BIO = [
    'I’m a Singapore-based creative communications professional with a deep editorial background. Perpetually curious, plugged into news and culture, and cautiously AI-pilled.',
    'At Esquire magazine, I covered culture, politics, and current affairs, writing, producing, and editing everything from daily articles to investigative features. Over 12 years I’ve moved across editorial, content operations, and strategic communications, working with brands like the NBA, Trust Bank, and Samsung across the Philippines and Singapore. I’ve managed high-volume content projects, enforced editorial standards across several publications, built communications strategies, and produced content and editorial work for brands.',
    'Now I’m learning full-stack programming at the National University of Singapore (NUS) with a view to applying my editorial skills in a more tech-forward context. These days I’m moving toward work on online safety and platform policy.',
]
WORK_TITLE, WORK_SUB = 'Some work', 'I find purpose in work that’s honest, helpful, and human'
FEATURED = [
    ('Online Safety Commission Launch Content', 'https://www.osc.gov.sg/',
     'Web copy, service articles, and explainer videos about online harms for the launch of Singapore’s Online Safety Commission',
     'home-osc', 'A young person absorbed in a phone screen — from the launch of Singapore’s Online Safety Commission.'),
    ('Age Checks Matter', 'https://www.imda.gov.sg/how-we-can-help/age-assurance',
     'A campaign — including outdoor ads, a film, and an explainer video — for Singapore’s IMDA, launching Age Assurance Measures in app stores',
     'home-age-checks', 'A shopkeeper raising her hand to a boy holding beer beneath an “Under 18” sign, from the Age Assurance Measures campaign'),
    ('How to Whitewash a Dictator', 'https://www.esquiremag.ph/politics/opinion/fighting-for-history-on-the-wikipedia-battlefield-a00207-20170817-lfrm2',
     'An investigative feature for Esquire Philippines, on an invisible war for Philippine history waged by Wikipedia editors on hotly contested pages',
     'home-whitewash', 'Ferdinand Marcos collaged over a redacted Wikipedia “Martial law” article, for “How to Whitewash a Dictator”'),
    ('A Pulpit for Pastors of Porn', 'https://www.esquiremag.ph/long-reads/notes-and-essays/the-rise-of-pastor-culture-and-why-it-must-end-a1513-20170629-lfrm',
     'An Esquire Philippines exposé that shed light on a social media subculture of sexual predators in the Philippines, sparking a nationwide reckoning',
     'home-pulpit', 'Halftone hands reaching toward pixelated images inside retro computer windows, for “A Pulpit for Pastors of Porn.”'),
]
MORE = [
    ('More Advertising Work →', 'AdvertisingWork', 'A selection of ads and campaigns I’ve worked on, including for the NBA, Trust Bank, and Alcon',
     'home-advertising', 'A woman laughing, a Trust cashback Visa card held over one eye, as banknotes and confetti rain down.'),
    ('More Editorial Work →', 'EditorialWork', 'A selection of stories I wrote and produced for Esquire Philippines, Tatler Asia, and Smile Magazine',
     'home-editorial', 'A dramatic, low-key editorial portrait of an older man against a black background.'),
]
THOUGHTS_TITLE, THOUGHTS_SUB = 'Thoughts', 'Where I’m at on media, culture, and issues of the day'
ENTRY = ('AUG 2026', 'Nolan’s “Odyssey” is full of sound and fury')

# Home: the four-part scroll that replaces About and Some work. Mig's copy, verbatim (one typo fixed:
# "have since work" → "have since worked"). Anchor, headline, body, work link (page key, label).
SCROLL = [
    ('about', 'I’m based in Singapore with regional scope.',
     'I moved here from Manila and have since worked agency-side, on local and APAC-wide campaigns for clients including the NBA, Trust Bank, and the IMDA.',
     None),
    ('editorial', 'My editorial background informs everything I do.',   # V60, Mig's revision
     'In Manila, I was an editor at the local edition of Esquire magazine, covering culture, politics, and current affairs. This formative chapter of my career is a core memory\u00a0— it gave me a journalistic perspective that I’ve since applied in everything I do.',
     ('EditorialWork', 'More Editorial Work')),
    ('branded', 'But the bigger chunk of my career has been in branded content.',
     'Of my 12 years of experience, 10 have been in roles handling advertorials and brand campaigns. My strategic communication senses have been honed and sharpened for over a decade.',
     ('AdvertisingWork', 'More Advertising Work')),
    ('policy', 'Now, I’m learning about content policy and online safety.',
     'I’ve learned programming at NUS and have been plugged into tech news, especially global tech policy, for years. I’m looking to apply my editorial and communications skills towards custodianship of the internet.',
     None),
]


def L(href, text):
    return a(href, text)


EDITORIAL = [
    ('Politics in Esquire', [
        'In my time with Esquire, I produced and published features on politicians and politically controversial figures. These include former presidential spokesperson '
        + L('https://www.esquiremag.ph/long-reads/esqa/salvador-panelo-a1513-a1521-20160919-lfrm3', 'Salvador Panelo') + ', former senator '
        + L('https://www.esquiremag.ph/long-reads/what-ive-learned/richard-gordon-what-i-ve-learned-a00207-20170717-lfrm', 'Dick Gordon') + ', and political influencer '
        + L('https://www.esquiremag.ph/long-reads/profiles/mocha-uson-full-text-a1521-20161202-lfrm4', 'Mocha Uson')
        + '. I also worked on Esquire’s blockbuster December 2016 issue, featuring '
        + L('https://www.esquiremag.ph/long-reads/profiles/her-excellency-full-text-a1506-20180402-lfrm3', 'Vice President Leni Robredo') + ' on the cover.',
        'With Esquire, I was on the frontlines of online culture wars, just as social media’s era of political rancour and polarisation began in the Philippines. So through my work, I learned firsthand about the roles and responsibilities of media in a democracy.',
    ], 'editorial-politics', 'Portrait of former Philippine Vice President Leni Robredo in a red top against a dark background, from Esquire Philippines.'),
    ('Culture in Esquire', [
        'Politics and current events were just among many areas we covered at Esquire. I also got to write and produce features in style and entertainment, including '
        + L('https://www.esquiremag.ph/life/women/anne-curtis-smith-is-a-woman-we-love-a00207-20171111', 'big celebrity interviews') + ', '
        + L('https://www.esquiremag.ph/culture/movies-and-tv/goyo-cinematographer-pong-ignacio-frame-epic-a00203-20180910-lfrm', 'film and cinema stories') + ', and '
        + L('https://www.esquiremag.ph/style/fashion/local-denimheads-have-produced-the-first-filipino-made-raw-selvedge-jeans-a00207-20171024-lfrm2', 'fashion features') + '.',
        'I wrote and produced one of Esquire’s biggest-ever stories: '
        + L('https://www.esquiremag.ph/long-reads/what-ive-learned/eddie-garcia-what-ive-learned-a1513-20181015-lfrm', 'an interview with Eddie Garcia')
        + ', a legendary actor and icon of Filipino cinema. '
        + L('https://www.youtube.com/watch?v=yY4LLYrMHt8', 'The full interview') + ' is still the publication’s most-viewed video on Facebook and YouTube.',
    ], 'editorial-culture', 'A dramatic, low-key editorial close-up portrait of actor Eddie Garcia in a pinstriped suit against a dark background, from a feature in Esquire Philippines.'),
    ('Tatler Asia’s Most Influential', [
        'Asia’s Most Influential is one of Tatler Asia’s signature editorial products. Every year, Tatler publishes a list of profiles of over 500 influential people from various fields. In 2021 '
        + L('https://www.tatlerasia.com/power-purpose/ideas-education/art-influence-and-the-purveyors-responsibility-according-to-top-auctioneer-jonathan-crockett', 'I contributed')
        + ' over 100 of those profiles, including honourees in Singapore and the Philippines. It was, for me, a writing exercise that demanded quick writing and fast-turnaround fact-checking.',
    ], 'editorial-tatler', 'Tatler’s “Asia’s Most Influential” series title, set in white and gold serif lettering on black.'),
    ('Smile Magazine Cover Story', [
        'I wrote the cover story for '
        + L('https://smile.ink-live.com/html5/reader/production/default.aspx?pubname=&amp;edid=029443cb-cf76-46cf-a91b-5360ee2806f0', 'the February 2020 issue')
        + ' of Cebu Pacific Air’s in-flight magazine, Smile. It was a feature on Barotac Nuevo, Iloilo, the one and only town in the entire Philippines that loves football more than basketball.',
    ], 'editorial-smile', 'A football match on the town plaza pitch in front of the historic Barotac Nuevo church in Iloilo, for the Smile magazine cover story.'),
]
ADVERTISING = [
    ('Trust Bank Singapore', [
        'Since the 2022 launch of Trust Bank, a digital bank in Singapore, I’ve worked on its campaigns and always-on social. That includes creative leadership for the award-winning 2024 '
        + L('https://www.marketing-interactive.com/trust-bank-million-dollars-campaign', 'launch of its cashback card')
        + ' — an above-the-line campaign involving ' + L('https://www.youtube.com/watch?v=nhxvOzenBR4', 'a film') + ' and islandwide out-of-home.',
    ], 'ads-trust', 'A woman laughing as Singapore dollar notes and gold confetti rain around her, holding up a Trust Bank cashback card.'),
    ('NBA Asia-Pacific Newsletters', [
        'I write copy for the weekly newsletters and direct mailers of the NBA in key Asia-Pacific territories: Australia, New Zealand, Japan, and the Philippines. Day-to-day work for this involves the application of cultural fluency and market-specific strategies to drive click-through.',
    ], 'ads-nba', 'A dramatic NBA promotional collage of San Antonio Spurs and New York Knicks players over city skylines, with a golden basketball.'),
    ('Alcon Asia-Pacific Campaigns', [
        'I worked on the regional launch campaigns of Precision1 and Total — contact lens brands by the global pharmaceutical and eye care company Alcon. These involved productions in South Korea and Vietnam, for materials that would be used across Asia and beyond.',
    ], 'ads-alcon', 'A woman working at a laptop in a warm-lit, elegant dark-blue office with abstract art behind her, from an Alcon campaign.'),
    ('GoTyme Bank Philippines', [
        'I worked on copy and concept for the 2023 launch campaign of GoTyme Bank, a digital bank in the Philippines. Its unique proposition is the human quality of its customer service, so the campaign reflected that, mainly through its '
        + L('https://www.youtube.com/watch?v=MCDe-yLaxYE', 'campaign film') + ' and a trio of ' + L('https://www.youtube.com/watch?v=yBnokrkGRbM', 'shorts') + '.',
    ], 'ads-gotyme', 'A grinning presenter in a suit points to a framed portrait of a man held up before a seated audience, from the GoTyme Bank campaign film.'),
]
md = open(os.path.join(REPO, 'src/content/thoughts/the-odyssey-review.md'), encoding='utf-8').read()
POST_PARAS = [p.strip().replace('\n', ' ') for p in md.split('---', 2)[2].strip().split('\n\n') if p.strip()]
POST_TITLE = '“The Odyssey” is magnificent, but far too amenable'
HANG = ' text-indent: -0.3em;' if POST_TITLE.startswith('“') else ''   # the quote's width at the title's tracking
POST_DECK = 'What are movies even for these days, especially when they’re this big?'
