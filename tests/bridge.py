"""v088: 2·3막 다리 「재가 내려앉은 뒤」 · 이데른 「구호소의 노래」"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def win2(pg,tgt):
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{const G=window.__k2.G;G.fhp=0;if(G.pack)G.pack.forEach(p=>p.fhp=0)}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);pg.wait_for_timeout(400)
    for _ in range(4):
        if tgt in pg.inner_text('#ov'):break
        if pg.locator('#ov.on .btn.pri').count():pg.click('#ov.on .btn.pri')
        pg.wait_for_timeout(400)
E=lambda pg,x:pg.evaluate(x)
def go(pg,loc,party='kirien'):E(pg,f"()=>{{const K=window.__k2;K.S.loc='{loc}';K.S.party='{party}';K.EV0=null;K.render()}}")
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;['kirien','oswin','eno','ibre','kasimir'].forEach(c=>K.joinComp(c));K.S.party='kirien';K.grantBase();K.EV0=null}")
    for _ in range(8):
        pg.wait_for_timeout(120)
        if pg.locator('#ov.on .btn.pri').count():pg.click('#ov.on .btn.pri')
        else:break
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{pit:1,manor:1,mr:3,eda:1,acad:1,mg:1,mgh:'hide',rev:1,revd:1,a2:6,h2:3,orx:{kirien:1,oswin:1,eno:1},mgt:{kirien:1,oswin:1,eno:1},rvt:{kirien:1,oswin:1,eno:1},oq0:1});K.S.vis.academy=1;K.render()}")
    # 구호소의 노래: 종지기의 사다리보다 먼저
    go(pg,'church');assert pg.locator('.M button[data-c=h2abel]').count()==0 and pg.locator('.M button[data-c=idM]').count()==1
    assert '구호소의 노래' in pg.inner_text('.goalc')
    pg.click('.M button[data-c=idM]');assert '마르테' in pg.inner_text('#ov');choose(pg,'곁에 앉는다');t=pg.inner_text('#ov');assert '우리 이데른' in t and '모퉁이 뒤' in t,t
    choose(pg,'빵을 나눠 먹는다');okpop(pg);assert E(pg,"window.__k2.S.idM")==1
    go(pg,'church');assert pg.locator('.M button[data-c=h2abel]').count()==1
    # 2막 끝 → 다리
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{h2:6,a3:1,a3h:1,amn:'oswin',taken:null,rqId:null,rq:0,hq:1,hald:0});K.render()}")
    go(pg,'base');assert pg.locator('.M button[data-c=rq0]').count()==0,'잊은 사람은 다리 뒤'
    assert '바뀐 공고' in pg.inner_text('.goalc')
    go(pg,'street');pg.click('.M button[data-c=br1]');assert '돌아오는 형제를 환영함' in pg.inner_text('#ov');choose(pg,'공고를 뗀다');okpop(pg)
    assert E(pg,"window.__k2.S.br")==1 and E(pg,"window.__k2.S.hald")==-1
    assert '(0/3)' in pg.inner_text('.goalc')
    go(pg,'base');pg.click('.M button[data-c=br2]');assert '오스윈께서 잃으신 것' in pg.inner_text('#ov');choose(pg,'차를 낸다');okpop(pg)
    go(pg,'outskirts');pg.click('.M button[data-c=br3]');assert '울릭' in pg.inner_text('#ov');choose(pg,'이마를 보여 준다');okpop(pg)
    go(pg,'docks','eno');pg.click('.M button[data-c=br4]');assert '거꾸로' in pg.inner_text('#ov');choose(pg,'아이들 앞에 선다');win2(pg,'불이 숨 참는 데');choose(pg,'지도를 칭찬한다');okpop(pg)
    s=E(pg,"window.__k2.S");assert s['bf']==1 and s['kmap']==1 and s['hald']==0
    assert '(3/3)' not in pg.inner_text('.goalc') and '빈 의자의 밤' in pg.inner_text('.goalc')
    go(pg,'base');pg.click('.M button[data-c=br5]');t=pg.inner_text('#ov');assert '오스윈의 자리' in t and '이데른' in t,t
    choose(pg,'내일부터 찾으러 가자');okpop(pg);assert E(pg,"window.__k2.S.br")==5
    go(pg,'base');assert pg.locator('.M button[data-c=rq0]').count()==1
    # 옛 저장: 잊은 사람을 지난 기록은 다리를 건너뛴다
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{br:0,rq:3});K.save();K.load();K.render()}")
    assert E(pg,"window.__k2.S.br")==5
    print('bridge ok',errs);assert not errs
    b.close()
