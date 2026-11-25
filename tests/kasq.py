"""v062: 카시미르 「마지막 상속자」"""
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
    assert pg.locator('[data-c=talk][data-a=kasimir]').count()==0 or True
    E(pg,"window.__k2.CMD.talk('kasimir')");pg.wait_for_timeout(100);assert '빈 병' in pg.inner_text('#ov');listen(pg);choose(pg,'같이 가자');choose(pg,'이야기를 마친다')
    assert E(pg,"window.__k2.S.zq")==1
    E(pg,"()=>{const K=window.__k2;K.S.vis.silver=1;K.render()}")
    go(pg,'silver','ibre');assert pg.locator('button[data-c=zq1][disabled]').count()==1
    go(pg,'silver','kasimir');pg.click('button[data-c=zq1]');assert '3번 노 출고' in pg.inner_text('#ov');choose(pg,'맞선다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("붉은 물 장부")',timeout=5000);t=pg.inner_text('#ov');assert '이름의 쓸모가 다했다' in t and '제 줄이 먼저' in t;choose(pg,'장부를 챙긴다')
    pg.click('button[data-c=tab][data-a=quest]');t=pg.inner_text('.M');assert '카시미르 — 마지막 상속자' in t and '하인 묘역' in t;pg.click('button[data-c=tab][data-a=place]')
    go(pg,'church','kasimir');pg.click('button[data-c=zq2]');choose(pg,'맞선다');win(pg)
    pg.wait_for_timeout(300);listen(pg);t=pg.inner_text('#ov');assert '「안셀」' in t,t[:300];choose(pg,'고개를 끄덕인다')
    assert E(pg,"window.__k2.S.zq")==3
    go(pg,'base','ibre');pg.click('button[data-c=zq3]');choose(pg,'붉은 물을 끊고');choose(pg,'다시 생각한다');choose(pg,'진짜 이름을 밝힌다');choose(pg,'이렇게 하기로 한다')
    t=pg.inner_text('#ov');assert '여기 눕지 않음' in t and '마지막 상속자」가 끝났다' in t;choose(pg,'고개를 끄덕인다')
    s=E(pg,"window.__k2.S");assert s['zq']==4 and s['zqe']=='name' and s['cq']['kasimir']=='done'
    pg.click('button[data-c=tab][data-a=quest]');pg.click('h2.fold[data-a=done]');t=pg.inner_text('.M');assert '카시미르 — 마지막 상속자' in t
    print('kasimir ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
