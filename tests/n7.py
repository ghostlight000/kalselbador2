"""v076: 3막 일곱 의자의 이름"""
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
    E(pg,base);E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{c3:0,n7:0,n7p:{},n7s:0,cogs:{tag:1,warmw:1}});['dome','barracks','furn','square','under'].forEach(k=>K.S.vis[k]=1);K.S.inv.oil=0;K.render()}")
    assert pg.locator('button[data-c=c3a]').count()==0
    pg.click('.M button[data-c=n7a]');assert '「첫째」' in pg.inner_text('#ov');choose(pg,'판을 품에 넣는다')
    go(pg,'inn','kasimir');assert pg.locator('button[data-c=c3a]').count()==0
    go(pg,'outskirts','kasimir');pg.click('.M button[data-c=n7b]');assert '첫 불 자리' in pg.inner_text('#ov');choose(pg,'판을 찾아보겠다')
    go(pg,'dome','kasimir');pg.click('.M button[data-c=n7p]');choose(pg,'맞선다');win2(pg,'오르테아');t=pg.inner_text('#ov');assert '오르테아' in t and '남쪽 바다' in t and '기계의 조각' in t,t;choose(pg,'판을 챙긴다')
    go(pg,'square','kasimir');pg.click('.M button[data-c=n7p]');choose(pg,'판을 뽑는다');assert '이스벤' in pg.inner_text('#ov');choose(pg,'판을 챙긴다')
    go(pg,'under','kasimir');pg.click('.M button[data-c=n7p]');choose(pg,'맞선다');win2(pg,'테살');choose(pg,'판을 챙긴다')
    go(pg,'furn','kasimir');pg.click('.M button[data-c=n7p]');choose(pg,'맞선다');win2(pg,'노르엘');t=pg.inner_text('#ov');assert '판 넷이 다 모였다' in t;choose(pg,'판을 챙긴다')
    assert E(pg,'window.__k2.S.n7')==3
    go(pg,'barracks','kasimir');pg.click('.M button[data-c=n7i]');assert '천이백' in pg.inner_text('#ov');choose(pg,'대성당 아래로');choose(pg,'우물가를 떠난다');assert E(pg,'window.__k2.S.idS')==2
    go(pg,'docks','kasimir');pg.click('.M button[data-c=n7d]');choose(pg,'맞선다');win2(pg,'운반 일지');choose(pg,'한 장을 찢어');choose(pg,'쪽지를 접는다')
    go(pg,'base','kasimir');pg.click('.M button[data-c=n7w]');choose(pg,'내려간다');win2(pg,'수로');choose(pg,'수로 입구에')
    go(pg,'outskirts','kasimir');pg.click('.M button[data-c=n7s]');assert '다시 먹지 못해' in pg.inner_text('#ov');choose(pg,'노래를 청한다');choose(pg,'판을 받는다')
    pg.click('.M button[data-c=n7h]');t=pg.inner_text('#ov');assert '둘째 — 없다' in t and '기계의 조각 2개' in t,t;choose(pg,'판을 챙긴다')
    assert E(pg,'window.__k2.S.n7')==7
    go(pg,'inn','kasimir');assert pg.locator('.M button[data-c=c3a]').count()==1
    # 이미 마지막 잔을 지난 기록은 건너뛴다
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{n7:0,c3:2});K.render()}");assert E(pg,"window.__k2.MS.filter(m=>m[4]===3).every(m=>m[0]==='계단 아래'||m[0]==='옛 불'||m[0]==='세 통의 부름'||m[2](window.__k2.S))")
    print(errs);assert not errs;print('ALL OK')
    b.close()
