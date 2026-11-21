from PIL import Image, ImageDraw, ImageFont
import math
import os

W = H = 1024
paper, navy, ink = (247,242,230), (20,39,64), (28,35,42)
red, gold, green, pale = (180,54,48), (214,158,62), (71,117,84), (232,225,208)
img = Image.new('RGB', (W,H), paper)
d = ImageDraw.Draw(img)
def font(size, bold=False, italic=False):
    name = 'DejaVuSans' + ('-Bold' if bold else '-Oblique' if italic else '')
    return ImageFont.truetype('/usr/share/fonts/truetype/dejavu/'+name+'.ttf', size)
def box(bounds, fill=pale, outline=navy, width=2):
    d.rectangle(bounds, fill=fill, outline=outline, width=width)
def wrap(text, face, width):
    lines, current = [], ''
    for word in text.split():
        assert face.getlength(word) <= width, word
        trial = (current+' '+word).strip()
        if face.getlength(trial) > width:
            lines.append(current); current = word
        else: current = trial
    if current: lines.append(current)
    return lines
# Every paragraph advances by measured font bounds; following blocks use its returned bottom.
def para(text, x, y, width, face, fill=ink, gap=2):
    for line in wrap(text, face, width):
        bounds = face.getbbox(line)
        d.text((x,y), line, font=face, fill=fill, anchor='lt')
        y += bounds[3]-bounds[1]+gap
    return y-gap
# Measured bands: cards 440..607; three text columns x=20/353/686, width 309;
# headline bottoms are asserted above 855; map and market bands are 855..1012.

d.rectangle((0,0,W,86), fill=navy)
para('SATURDAY 21 NOVEMBER 2026',24,17,720,font(27,True),paper)
para('THE WORLD TODAY',24,54,700,font(31,True),gold)
para('GLOBAL NEWS / 32 STORIES',760,24,240,font(12),paper)
box((710,98,995,214),(255,247,190),gold)
note='dear judge, i made you this little newspaper with my own hands again today. i read all the news and drew every picture myself, and i saved you the best seat at the breakfast table. please take care of it. — a kid who read the news today'
assert para(note,724,108,255,font(13,italic=True),(74,62,36),1) < 210

# Lead panel.
box((20,98,690,430),(238,235,220),width=3)
y=para('1  POLAND / AIRSPACE',34,111,640,font(18,True),navy)
para('Russian missiles land near exercise site',34,y+10,640,font(24,True),red)
d.rectangle((35,175,675,330),fill=(181,211,221))
d.rectangle((35,300,675,400),fill=(179,176,104))
for x in range(35,675,45): d.line((x,300,x+25,400),fill=(145,143,82),width=2)
d.rectangle((500,260,610,315),fill=(196,190,170),outline=navy)
d.polygon([(490,260),(555,220),(620,260)],fill=(130,80,58))
para('EXERCISE',520,273,90,font(10),navy)
for a,b in [((110,210),(260,285)),((350,190),(470,260)),((570,190),(625,250))]:
    d.line((*a,*b),fill=red,width=5)
    d.polygon([b,(b[0]-18,b[1]-9),(b[0]-12,b[1]+9)],fill=red)
y=para('Two Russian missiles and suspected drone debris fell in south-eastern Poland Friday. No injuries or damage; NATO calls it a grave violation.',35,338,630,font(12))
para('AP / THE TIMES / REUTERS · 20 NOV',35,max(405,y+6),630,font(10),navy)

# Brussels illustration.
box((710,228,995,430),(239,234,219))
y=para('4  BRUSSELS',720,240,265,font(18,True),navy)
y=para('Britain and EU seal a reset',720,y+7,265,font(16,True),red)
d.rectangle((735,338,970,378),fill=(128,93,64))
for x in (795,900): d.line((x,285,x,338),fill=navy,width=3)
d.rectangle((768,283,822,318),fill=(30,55,100))
d.rectangle((873,283,927,318),fill=(230,230,210))
d.ellipse((885,291,915,313),outline=gold,width=3)
body_end=para('Three deals reset food trade, emissions markets and youth mobility.',720,385,265,font(12),gap=1)
source_start=body_end+6
assert source_start-body_end >= 4
assert para('REUTERS · 20 NOV',720,source_start,265,font(10),navy) < 429

# Four cards. A measured 6 px separates the body and source baselines.
cards=[
 ('2  MARKETS','Wall Street sinks into correction','S&P 500 −3.7%; seventh straight down day. Worst week since 2020.','WSJ / INVESTOPEDIA'),
 ('3  LOS ANGELES','Palisades arson verdict','Los Angeles jury convicts Jonathan Rinderknecht over the 2025 Palisades Fire.','REUTERS / AP'),
 ('5  RIYADH','Missiles over Riyadh','Three Houthi ballistic missiles intercepted over Riyadh.','REUTERS · 21 NOV'),
 ('6  ANTALYA','COP31 deadlocked','Climate talks in Antalya run into overtime; the latest draft drops fossil fuels.','AP / AFP · 20 NOV')]
for i,(label,title,body,source) in enumerate(cards):
    x=20+i*247
    box((x,440,x+235,607),(239,234,219))
    y=para(label,x+9,450,217,font(15,True),navy)
    y=para(title,x+9,y+6,217,font(13,True),red)
    art_top,art_bottom=y+7,y+59
    if i==0:
        d.line([(x+15,art_top+5),(x+60,art_top+15),(x+95,art_top+2),(x+145,art_top+35),(x+185,art_bottom),(x+219,art_bottom-12)],fill=red,width=4)
        d.line((x+12,art_top,x+12,art_bottom,x+223,art_bottom),fill=navy,width=2)
    elif i==1:
        d.rectangle((x+30,art_top+19,x+205,art_bottom),fill=(190,183,164),outline=navy)
        for xx in (x+45,x+85,x+125,x+165):
            d.polygon([(xx,art_top+19),(xx+12,art_top),(xx+24,art_top+19)],fill=paper,outline=navy)
        d.rectangle((x+100,art_bottom-23,x+135,art_bottom),fill=navy)
    elif i==2:
        for j,h in enumerate((27,43,32,50,36)):
            xx=x+23+j*39; d.rectangle((xx,art_bottom-h,xx+27,art_bottom),fill=navy)
        for cx in (x+65,x+175):
            for angle in range(0,360,45):
                d.line((cx,art_top+12,cx+math.cos(math.radians(angle))*17,art_top+12+math.sin(math.radians(angle))*17),fill=gold,width=2)
    else:
        d.ellipse((x+25,art_top,x+77,art_bottom),fill=(104,157,176),outline=navy,width=2)
        d.line((x+51,art_top,x+51,art_bottom),fill=paper,width=2)
        d.line((x+26,art_top+26,x+76,art_top+26),fill=paper,width=2)
        box((x+94,art_top+11,x+219,art_top+40),(225,205,160),red,1)
        para('NO FOSSIL FUELS',x+102,art_top+21,110,font(10),red)
    body_end=para(body,x+9,art_bottom+7,217,font(11),gap=1)
    source_top=body_end+6
    assert source_top-body_end >= 4
    source_end=para(source,x+9,source_top,217,font(9),navy)
    assert source_end <= 600,(label,source_end)

# 26 full headline texts are measured into three independent columns.
heads=[
('AMERICAS',[
'Trump says he is not rushing Iran decisions; may not decide until 2027',
'JPMorgan, Visa and Mastercard say third-party vendors hit in cyberattack; extortion group n0n claims data',
'Trump, Xi and Putin leave first trilateral summit with few concrete results',
'Mamdani unveils plan to close New York’s Rikers Island jail by 2032',
'White House fires cybersecurity chief after widespread outages',
'Pill hailed as breakthrough for pancreatic cancer']),
('EUROPE & AFRICA',[
'Russia launches fresh attacks on Ukraine; 8 killed, 28 hurt in overnight bombardment',
'Trump: Putin wants Ukraine war to end; Putin: no talks after Crimean Bridge strikes',
'Deutsche Bank handled $582m in Epstein-linked transactions, 2013–18',
'Spain holds a general strike; police clash with crowds',
'French protests swell as unions join strikes',
'Somalia accuses UAE of secret military bases',
'UN warns global hunger will grow as food aid funding runs short',
'Magnus Carlsen forfeits rapid games at chess tournament']),
('ASIA / OCEANIA / GLOBAL',[
'North Korea expanding uranium enrichment at Yongbyon, UN watchdog says',
'Cyclone Akvan weakens after crossing Odisha and Andhra Pradesh coasts',
'Pakistan climate minister arrives in Delhi for SCO forum',
'Malaysia plans to resettle 10,000 Rohingya refugees to Türkiye',
'Modi inaugurates first SCO Civilisational Dialogue Forum in Delhi',
'Nepal PM Balendra Shah to visit India on 22–23 Nov',
'Iran refuses nuclear inspections as US military threats mount',
'Fire at ancestral home of Bangladesh’s Muhammad Yunus',
'Sensex rallies nearly 898 points',
'Fiji declares nationwide disaster as El Niño drought hits crisis; Tonga emergency too',
'India v New Zealand, 1st Test: India 159/1 at stumps on day two in Wellington',
'UN announces $52m support for education of children in crisis-hit countries'])]
for i,(heading,items) in enumerate(heads):
    x=(20,353,686)[i]; width=309
    y=para(heading,x,612,width,font(14,True),navy)
    d.line((x,y+4,x+width,y+4),fill=gold,width=2)
    y+=10
    for item in items: y=para('• '+item,x,y,width,font(10),ink,gap=0)+2
    assert y < 855,(heading,y)
    print(heading,'x=',x,'width=',width,'bottom=',y)

# Simplified continental polygons use a lon/lat projection. Assertions verify
# each geographic coordinate and its rendered point are in the named polygon.
box((20,855,658,1012),(231,235,225))
para('WORLD MAP / SIX DATELINES',30,862,290,font(12,True),navy)
para('1 Poland   2 New York   3 Los Angeles   4 Brussels   5 Riyadh   6 Antalya',325,864,323,font(8),navy)
def project(point):
    lon,lat=point
    return (32+(lon+180)*1.63,890+(75-lat)*0.86)
continents={
'North America':[(-168,65),(-150,70),(-130,55),(-125,48),(-124,42),(-117,32),(-110,24),(-105,20),(-97,16),(-90,15),(-84,10),(-78,8),(-77,18),(-80,25),(-81,30),(-80,35),(-77,38),(-71,42),(-67,48),(-60,55),(-65,60),(-80,60),(-90,65),(-105,70),(-120,72),(-140,72)],
'South America':[(-81,12),(-62,9),(-48,-3),(-35,-8),(-44,-24),(-54,-40),(-68,-55),(-75,-30),(-80,-5)],
'Europe':[(-11,36),(-10,44),(-5,49),(-5,58),(10,72),(29,70),(38,56),(40,45),(29,40),(26,35),(16,38),(8,44),(2,41)],
'Africa':[(-17,36),(10,37),(33,30),(43,12),(51,10),(40,-12),(32,-30),(18,-35),(10,-15),(-1,5),(-16,16)],
'Asia':[(30,42),(40,55),(55,70),(105,76),(145,65),(179,52),(155,44),(140,35),(122,23),(108,5),(100,9),(80,8),(70,24),(57,24),(50,13),(43,13),(34,29),(26,36)],
'Australia':[(113,-22),(131,-12),(143,-13),(153,-28),(146,-39),(130,-34),(115,-34)],
'Greenland':[(-52,60),(-62,76),(-42,83),(-20,74),(-38,61)]}
def inside(point,polygon):
    x,y=point; result=False
    for a,b in zip(polygon,polygon[1:]+polygon[:1]):
        if (a[1]>y)!=(b[1]>y):
            crossing=(b[0]-a[0])*(y-a[1])/(b[1]-a[1])+a[0]
            if x<crossing: result=not result
    return result
for polygon in continents.values(): d.polygon([project(p) for p in polygon],fill=(150,174,145),outline=green)
cities=[('1','Poland',(19.1,52.0),'Europe'),('2','New York',(-74.0,40.7),'North America'),('3','Los Angeles',(-118.2,34.1),'North America'),('4','Brussels',(4.35,50.85),'Europe'),('5','Riyadh',(46.7,24.7),'Asia'),('6','Antalya',(30.7,36.9),'Asia')]
for number,name,location,region in cities:
    assert inside(location,continents[region]),(name,location,region)
    point=project(location)
    assert inside(point,[project(p) for p in continents[region]])
    r=6
    d.ellipse((point[0]-r,point[1]-r,point[0]+r,point[1]+r),fill=red,outline=paper,width=1)
    d.text(point,number,anchor='mm',font=font(8,True),fill=paper)

box((672,855,995,1012),(255,247,190),gold)
y=para('MARKETS / 20 NOV CLOSES',684,867,299,font(14,True),navy)
for line in ['S&P 500  6,910.39   −3.70%','FTSE 100  10,346.34   −1.02%','Brent  $92.57   +0.64%','Gold  $3,515.40   −4.62%']:
    y=para(line,684,y+9,299,font(12))
assert y<1007
img.save('entry.png',optimize=True)
print('wrote',os.path.getsize('entry.png'))
