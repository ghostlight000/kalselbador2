"""v064: 3막 ① 잊은 사람 — 할데온의 병 / 전당포 창고"""
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
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{a3:1,a3h:1,br:5,h2:6,abel:'f',amn:'kasimir',taken:null,hq:3,hald:1,loc:'base',party:'ibre',rvt:{kasimir:1,ibre:1},mgt:{kasimir:1,ibre:1}});K.render()}")
    pg.click('button[data-c=rq0]');t=pg.inner_text('#ov');assert '이유는 모름' in t and '전당포' in t;choose(pg,'병을 찾으러 간다')
    assert E(pg,"window.__k2.S.rq")==1 and E(pg,"window.__k2.PL.pawn.hide(window.__k2.S)")==False
    go(pg,'church','ibre');pg.click('button[data-c=rq1a]');assert '약속드린 것입니다' in pg.inner_text('#ov');choose(pg,'고맙다고 말하고')
    s=E(pg,"window.__k2.S");assert s['rq']==2 and s['rqW']=='hald' and s['hald']==2
    go(pg,'base','ibre');a0=E(pg,"window.__k2.S.aff.kasimir");pg.click('button[data-c=rq2]');listen(pg);t=pg.inner_text('#ov');assert '일곱 매듭을 푼다' in t and '촛불이 기울던' in t,t[:300];choose(pg,'곁에 앉는다')
    s=E(pg,"window.__k2.S");assert s['amn'] is None and s['rq']==3 and s['aff']['kasimir']==a0+4
    assert E(pg,"window.__k2.isAmn('kasimir')")==False
    print('path hald ok')
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{amn:'pit',rq:0,br:5,rqId:null,rqW:null,hq:1,loc:'base'});K.render()}")
    pg.click('button[data-c=rq0]');choose(pg,'병을 찾으러 간다')
    go(pg,'church','ibre');assert pg.locator('button[data-c=rq1a]').count()==0
    go(pg,'pawn','ibre');pg.click('button[data-c=rq1b]');choose(pg,'맞선다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("전당포 창고")',timeout=5000);assert '따로 두라' in pg.inner_text('#ov');choose(pg,'병을 챙긴다')
    go(pg,'base','ibre');pg.click('button[data-c=rq2]');t=pg.inner_text('#ov');assert '꼬리표를 뗀다' in t and '갈고리' in t;choose(pg,'머리를 쓰다듬는다')
    s=E(pg,"window.__k2.S");assert s['amn'] is None and s['rqW']=='self'
    print('path self ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
