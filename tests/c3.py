"""v065: 3막 공통 사건 — 마그다의 배신 · 이데른 · 일곱째 문 · 옛 불 · 세 갈래 · 로맨스 상대 이벤트"""
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
E=lambda pg,x:pg.evaluate(x)
def go(pg,loc,party):E(pg,f"()=>{{const K=window.__k2;K.S.loc='{loc}';K.S.party='{party}';K.render()}}")
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('kirien');K.joinComp('ibre');K.S.party='kirien';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{pit:1,manor:1,mr:3,eda:1,acad:1,fac:1,mg:1,mgh:'hide',rev:1,revd:1,a2:6,h2:5,orx:{kasimir:1,ibre:1},mgt:{kasimir:1,ibre:1},rvt:{kasimir:1,ibre:1},loc:'base'});K.S.vis.academy=1;K.render()}")
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{a3:1,a3h:1,h2:6,abel:'f',amn:null,rq:3,n7:7,rqId:'oswin',taken:null,hq:3,hald:2,loc:'base',party:'kirien',rom:'kirien',sex:'f',magp:3,rvt:{kirien:1,ibre:1},mgt:{kirien:1,ibre:1}});K.render()}")
    pg.evaluate("window.__k2.CMD.r3a()");listen(pg);assert '지붕 위' in pg.inner_text('#ov');choose(pg,'다른 사람이 돼도');listen(pg);choose(pg,'곁에 있는다')
    assert E(pg,"window.__k2.S.r3a")==1 and not E(pg,"window.__k2.QTALK(window.__k2.S.rom).length")
    go(pg,'inn','kirien');pg.click('button[data-c=c3a]');assert '오늘은 닫음' in pg.inner_text('#ov');choose(pg,'그 사람 것도');choose(pg,'여관을 나선다')
    assert E(pg,"window.__k2.S.c3")==1
    go(pg,'stairs','kirien');pg.click('button[data-c=c3b]');t=pg.inner_text('#ov');assert '못 하겠어' in t and '감싼 거야' in t;choose(pg,'맞선다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("일곱째 문")',timeout=5000);t=pg.inner_text('#ov');assert '목소리에 열렸다' in t and '고개를 끄덕인다' in t;choose(pg,'문 안으로')
    assert '돌아왔구나, 나' in pg.inner_text('#ov');choose(pg,'너는 누구야');t=pg.inner_text('#ov');assert '오랜만입니다, 베렌' in t and '차를 내던 방' in t;choose(pg,'계단을 뛰어')
    choose(pg,'문을 잠근다');s=E(pg,"window.__k2.S");assert s['c3']==4 and s['mgB']=='h'
    go(pg,'base','kirien');pg.evaluate("window.__k2.CMD.r3b()");listen(pg);choose(pg,'그때는 내 이름을');listen(pg);t=pg.inner_text('#ov');choose(pg,'곁에 있는다')
    pg.click('button[data-c=c3r]');assert pg.locator('#ov.on button:has-text("목자의 길")').count()==1;choose(pg,'목자의 길');choose(pg,'이 길로 간다')
    assert '오래 함께 걷겠습니다' in pg.inner_text('#ov');choose(pg,'자리에 앉는다');choose(pg,'찻잔을 든다');assert E(pg,"window.__k2.S.route")=='shep' and E(pg,"window.__k2.S.hg")==1
    print('hes + shep ok')
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{c3:0,mgB:null,mgK:0,route:null,hg:0,sh:0,r3a:1,r3b:1,hald:0,magp:1,loc:'inn'});K.render()}")
    pg.click('button[data-c=c3a]');choose(pg,'같이 가자');choose(pg,'여관을 나선다')
    go(pg,'stairs','ibre');pg.click('button[data-c=c3b]');assert '돌아보지 않는다' in pg.inner_text('#ov');choose(pg,'맞선다');win(pg)
    pg.wait_for_selector('#ov.on button:has-text("맞선다")',timeout=5000);assert E(pg,"window.__k2.S.c3")==2;choose(pg,'맞선다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("일곱째 문")',timeout=5000);assert '고개를 끄덕인다' not in pg.inner_text('#ov');choose(pg,'문 안으로');choose(pg,'너는 누구야');assert '차를 내던 방' not in pg.inner_text('#ov');choose(pg,'계단을 뛰어');choose(pg,'문을 잠근다')
    go(pg,'base','ibre');pg.click('button[data-c=c3r]');assert pg.locator('#ov.on button:has-text("목자의 길")').count()==0 and '열리지 않았다' in pg.inner_text('#ov');choose(pg,'불을 끄는 길');choose(pg,'이 길로 간다');choose(pg,'하수구로 내려간다');choose(pg,'하수구를 나선다')
    assert E(pg,"window.__k2.S.route")=='ext'
    print('betray + ext ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
