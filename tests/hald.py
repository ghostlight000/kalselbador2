"""v063: 할데온과의 만남 — 대성당 회랑 세 번, 숨은 신뢰 S.hald"""
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
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('kasimir');K.joinComp('ibre');K.S.party='kasimir';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{pit:1,manor:1,mr:3,eda:1,acad:1,fac:1,mg:1,mgh:'hide',rev:1,revd:1,a2:6,h2:5,orx:{kasimir:1,ibre:1},mgt:{kasimir:1,ibre:1},rvt:{kasimir:1,ibre:1},loc:'base'});K.S.vis.academy=1;K.render()}")
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{archM:1,rev:0,revd:0,a2:2,h2:0,loc:'church',party:'kirien'});K.joinComp('kirien');K.S.party='kirien';K.render()}")
    assert pg.locator('button[data-c=hald]').count()==1
    pg.click('button[data-c=hald]');t=pg.inner_text('#ov');assert '겨울 시대' in t and '키리엔' in t;oil=E(pg,"window.__k2.S.inv.oil||0")
    a0=E(pg,"window.__k2.S.aff.kirien");choose(pg,'불은 있어야 해');assert '기름 두 병' in pg.inner_text('#ov');choose(pg,'회랑을 나선다')
    s=E(pg,"window.__k2.S");assert s['hq']==1 and s['hald']==1 and s['inv']['oil']==oil+2 and s['aff']['kirien']==a0-1
    assert pg.locator('button[data-c=hald]').count()==0
    E(pg,"()=>{const K=window.__k2;K.S.a2=4;K.render()}");pg.click('button[data-c=hald]');assert '먼저 등을 돌렸습니다' in pg.inner_text('#ov');choose(pg,'그 벗이 누군데');choose(pg,'회랑을 나선다')
    assert E(pg,"window.__k2.S.hq")==2 and E(pg,"window.__k2.S.hald")==1
    assert pg.locator('button[data-c=hald]').count()==0
    E(pg,"()=>{const K=window.__k2;K.S.h2=3;K.S.amn='oswin';K.render()}");pg.click('button[data-c=hald]');t=pg.inner_text('#ov');assert '오스윈 일은 미안합니다' in t and '병에 담아' in t;choose(pg,'믿어 볼게');choose(pg,'회랑을 나선다')
    s=E(pg,"window.__k2.S");assert s['hq']==3 and s['hald']==2;assert pg.locator('button[data-c=hald]').count()==0
    print('hald ok')
    E(pg,"()=>{const K=window.__k2;K.joinComp('kasimir');Object.assign(K.S,{loc:'base',party:'kirien',amn:'kasimir',rev:1,rvt:{kirien:1,ibre:1},mgt:{kirien:1,ibre:1},aev:{kirien:99,ibre:99},chd:{kirien:9,ibre:9},iq:5});K.S.aff.kasimir=90;K.S.aff.kirien=0;K.render()}")
    assert E(pg,"window.__k2.talkSub?window.__k2.talkSub('kasimir'):'x'") in ('이야기를 나눈다','x')
    print(E(pg,"(()=>{const K=window.__k2;return K.S.comps.map(id=>id+':'+[K.talkNew&&K.talkNew(id),K.chNext&&!!K.chNext(id),K.aevFor&&!!K.aevFor(id)].join(','))})()"))
    E(pg,"window.__k2.CMD.rooms()");pg.wait_for_timeout(100);t=pg.inner_text('#ov');assert '동료와 이야기한다 ✦' not in t,t
    choose(pg,'문을 닫는다');E(pg,"()=>{window.__k2.S.amn=null}");E(pg,"window.__k2.CMD.rooms()");pg.wait_for_timeout(100);assert '동료와 이야기한다 ✦' in pg.inner_text('#ov')
    print('amn mark ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
