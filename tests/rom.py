"""v072: 로맨스 다시 짜기 — 호감으로 열리는 고백, 나야 쟤야, 정말 끝낼 거야"""
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
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('kirien');K.joinComp('oswin');K.joinComp('barg');K.S.party='kirien';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{pit:1,manor:1,mr:3,eda:1,acad:1,fac:1,mg:1,mgh:'hide',rev:1,revd:1,a2:6,h2:5,orx:{kasimir:1,ibre:1},mgt:{kasimir:1,ibre:1},rvt:{kasimir:1,ibre:1},loc:'base'});K.S.vis.academy=1;K.render()}")
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{a3:1,a3h:1,h2:6,rev:1,sex:'f',rom:null,loc:'base',party:'kirien',rvt:{kirien:1,oswin:1,barg:1},mgt:{kirien:1,oswin:1,barg:1},oq0:1,oq:6,bq:5,aev:{kirien:9,oswin:9,barg:9},chd:{kirien:9,oswin:9,barg:9}});K.S.aff.kirien=65;K.S.aff.oswin=40;K.S.aff.barg=70;K.render()}")
    E(pg,"window.__k2.CMD.talk('kirien')");pg.wait_for_timeout(150);listen(pg);t=pg.inner_text('#ov');assert '냄새로 먼저 찾아' in t,t[:200];choose(pg,'좋아해');listen(pg);choose(pg,'곁에 있는다')
    assert E(pg,"window.__k2.S.rom")=='kirien'
    # 바르그는 75부터
    E(pg,"window.__k2.CMD.talk('barg')");pg.wait_for_timeout(150);assert '등이 춥다' not in pg.inner_text('#ov');E(pg,"()=>{window.__k2.EV0=null;window.__k2.render()}")
    if pg.locator('#ov.on').count():pg.keyboard.press('Escape')
    E(pg,"()=>{const K=window.__k2;K.S.aff.oswin=66;K.render()}")
    E(pg,"window.__k2.CMD.talk('oswin')");pg.wait_for_timeout(150);listen(pg);t=pg.inner_text('#ov');assert '저입니까, 키리엔입니까' in t,t[-300:];choose(pg,'너야.');listen(pg);choose(pg,'곁에 있는다')
    s=E(pg,"window.__k2.S");assert s['rom']=='oswin' and s['romAsk']=='kirien'
    E(pg,"window.__k2.CMD.talk('kirien')");pg.wait_for_timeout(150);listen(pg);t=pg.inner_text('#ov');assert '오스윈 얘기 들었어' in t;choose(pg,'아니. 너야');listen(pg);choose(pg,'곁에 있는다')
    s=E(pg,"window.__k2.S");assert s['rom']=='kirien' and s['romBk']=='oswin' and not s['romAsk']
    a0=s['aff']['oswin'];E(pg,"window.__k2.CMD.talk('oswin')");pg.wait_for_timeout(150);listen(pg);assert '정정' in pg.inner_text('#ov');choose(pg,'자리를 뜬다')
    s=E(pg,"window.__k2.S");assert s['romBk'] is None and s['aff']['oswin']==a0-8 and s['romNo']['oswin']==a0-8
    # 다시 오스윈을 고르고 키리엔과 헤어진다
    E(pg,"()=>{const K=window.__k2;K.S.aff.oswin=K.S.romNo.oswin+15;K.render()}")
    E(pg,"window.__k2.CMD.talk('oswin')");pg.wait_for_timeout(150);listen(pg);choose(pg,'너야.');listen(pg);choose(pg,'곁에 있는다')
    E(pg,"window.__k2.CMD.talk('kirien')");pg.wait_for_timeout(150);listen(pg);choose(pg,'응. 미안해');listen(pg);choose(pg,'자리를 뜬다')
    s=E(pg,"window.__k2.S");assert s['rom']=='oswin' and not s['romAsk'] and s['romX']['kirien']==1
    # 헤어진 키리엔은 호감이 높아도 다시 고백하지 않는다
    E(pg,"()=>{const K=window.__k2;K.S.aff.kirien=95;K.render()}")
    E(pg,"window.__k2.CMD.talk('kirien')");pg.wait_for_timeout(150);listen(pg);t=pg.inner_text('#ov');assert '나야, 오스윈' not in t and '오스윈 말이야' not in t,t[-300:]
    print('rom ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
