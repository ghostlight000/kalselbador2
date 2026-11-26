"""v078: 3·4막 소문·장소 글·갈래별 곁가지"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def listen(pg):
    for _ in range(12):
        if pg.locator('#ov.on button:has-text("말없이 듣는다")').count():choose(pg,'말없이 듣는다')
        else:break
def win(pg):
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{const G=window.__k2.G;G.fhp=0;if(G.pack)G.pack.forEach(p=>p.fhp=0)}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);okpop(pg)
def win2(pg,tgt):
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{const G=window.__k2.G;G.fhp=0;if(G.pack)G.pack.forEach(p=>p.fhp=0)}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);pg.wait_for_timeout(400)
    for _ in range(4):
        if tgt in pg.inner_text('#ov') or pg.locator('#pv.on').count():break
        if pg.locator('#ov.on .btn.pri').count():pg.click('#ov.on .btn.pri')
        pg.wait_for_timeout(400)
def skipcine(pg):
    pg.wait_for_selector('#pv.on .eo',timeout=8000);assert pg.locator('#pv .eo').count()==1
    if pg.locator('#pv [data-pv=skip]').count():pg.click('#pv [data-pv=skip]')
    pg.wait_for_timeout(100);assert '엔딩' in pg.inner_text('#pv');pg.click('#pv [data-pv=close]');pg.wait_for_timeout(150)
E=lambda pg,x:pg.evaluate(x)
def go(pg,loc,party):E(pg,f"()=>{{const K=window.__k2;K.S.loc='{loc}';K.S.party='{party}';K.render()}}")
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('kirien');K.joinComp('ibre');K.joinComp('kasimir');K.S.party='kirien';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{pit:1,manor:1,mr:3,eda:1,acad:1,fac:1,mg:1,mgh:'hide',rev:1,revd:1,a2:6,h2:5,orx:{kasimir:1,ibre:1},mgt:{kasimir:1,ibre:1},rvt:{kasimir:1,ibre:1},loc:'base'});K.S.vis.academy=1;K.render()}")
    base="()=>{const K=window.__k2;Object.assign(K.S,{a3:1,a3h:1,h2:6,abel:'i',amn:null,rq:3,rqId:'oswin',taken:null,hq:3,hald:0,c3:4,r3a:1,r3b:1,route:null,end:null,xt:0,xtc:null,xdk:[],zqe:'keep',oqe:'scatter',loc:'base',party:'kasimir',rom:null,magp:3,rvt:{kirien:1,ibre:1,kasimir:1},mgt:{kirien:1,ibre:1,kasimir:1},aff:Object.assign(K.S.aff,{kirien:40,ibre:40,kasimir:40})});K.render()}"
    E(pg,"()=>{const K=window.__k2;['barracks','confess','square','silver'].forEach(k=>K.S.vis[k]=1)}")
    def run(route,flags,steps):
        E(pg,base);E(pg,f"()=>{{const K=window.__k2;Object.assign(K.S,{{route:'{route}',r4:{{}},pay:{{kirien:'{route}',ibre:'{route}',kasimir:'{route}'}},coin:200}},{flags});K.render()}}")
        for loc,key,pick,want in steps:
            go(pg,loc,'kasimir');pg.click(f'.M button[data-c=r4x][data-a={key}]');pg.wait_for_timeout(100)
            if pick=='맞선다':choose(pg,'맞선다');win2(pg,want);pick2='이름을 묻는다';t=pg.inner_text('#ov');choose(pg,pick2)
            else:choose(pg,pick)
            t=pg.inner_text('#ov');assert want in t,(key,t[-300:]);choose(pg,'자리를 뜬다')
        r4=E(pg,'window.__k2.S.r4');assert len(r4)==5,r4
    run('shep',"{shW:1,shC:1,shI:1,shWk:1,shA:1}",[('church','choir','원래는','할데온'),('barracks','deser','성벽 밖','접힌 회색 옷'),('silver','hconf','서명한 이름을','이름을'),('church','garden','씨앗을','꼬투리'),('church','hcup','금 간 잔','이백 년')])
    go(pg,'church','kasimir');assert '형제라 부른다' in pg.inner_text('.M')
    run('ret',"{rt:2,rtM:1,rtT:1,rtL:1,rtR:1,rtS:1}",[('street','bkid','이마를 닦아','이름 부르던'),('outskirts','oldl','곁에 앉아','아내 이야기'),('confess','rconf','병을 돌려놓게','이름을 지어'),('outskirts','ulbro','맞선다','토르'),('base','fletter','벽난로에','「같」')])
    run('ext',"{xt:3,xtK:1,xtCu:1,xtD:1,xtO:1,xtSv:1,xtCo:1,xdk:['street']}",[('street','candle','몽땅 사서','처마마다'),('docks','confd','곁에 있어','이름을'),('square','mpdoubt','투구를','스무 살'),('silver','hkid','별 이름을','모르텐'),('street','relit','같이 이름을','촛불 아래서도')])
    E(pg,"()=>{window.__k2.CMD.tab('quest')}");pg.wait_for_timeout(200);E(pg,"()=>{window.__k2.CMD.tab('place')}")
    print(errs);assert not errs;print('ALL OK')
    b.close()
