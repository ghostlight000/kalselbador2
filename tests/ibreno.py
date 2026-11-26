"""v060: 이브레 「색 없는 이름」 · 에노 「물길 아래의 노래」"""
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
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('ibre');K.joinComp('eno');K.S.party='ibre';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{pit:1,manor:1,mr:3,eda:1,acad:1,fac:1,mg:1,mgh:'hide',rev:1,revd:1,a2:6,h2:5,orx:{ibre:1,eno:1},mgt:{ibre:1,eno:1},rvt:{ibre:1,eno:1},loc:'base'});K.S.vis.academy=1;K.render()}")
    # 이브레
    E(pg,"window.__k2.CMD.talk('ibre')");pg.wait_for_timeout(100);assert '무색 4번' in pg.inner_text('#ov');listen(pg);choose(pg,'같이 싸우자');choose(pg,'이야기를 마친다')
    assert E(pg,"window.__k2.S.iq")==1
    go(pg,'works','eno');assert pg.locator('button[data-c=iq1][disabled]').count()==1
    go(pg,'works','ibre');pg.click('button[data-c=iq1]');choose(pg,'모래 위에 선다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("무색 징수 명단")',timeout=5000);assert '표본실 이관' in pg.inner_text('#ov');choose(pg,'명단을 챙긴다')
    go(pg,'sanat','ibre');pg.click('button[data-c=iq2]');choose(pg,'맞선다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("무색 4번")',timeout=5000);assert '허물 관찰' in pg.inner_text('#ov');choose(pg,'저택으로 데려간다')
    go(pg,'base','ibre');pg.evaluate("window.__k2.CMD.iq3()");listen(pg);choose(pg,'네가 지어 줘');listen(pg);choose(pg,'고개를 끄덕인다')
    assert E(pg,"window.__k2.S.iqN")=='sun' and E(pg,"window.__k2.S.iq")==4
    pg.click('button[data-c=tab][data-a=quest]');t=pg.inner_text('.M');assert '이브레 — 색 없는 이름' in t and '명부 앞에서' in t;pg.click('button[data-c=tab][data-a=place]')
    go(pg,'square','ibre');pg.click('button[data-c=iq4]');choose(pg,'무색들의 장부를');choose(pg,'이렇게 하기로 한다')
    t=pg.inner_text('#ov');assert '「볕」' in t and '색 없는 이름」이 끝났다' in t;choose(pg,'고개를 끄덕인다')
    s=E(pg,"window.__k2.S");assert s['iq']==5 and s['iqe']=='ledger' and s['cq']['ibre']=='done'
    print('ibre ok')
    # 에노
    go(pg,'base','eno');E(pg,"window.__k2.CMD.talk('eno')");pg.wait_for_timeout(100);assert '막힌 물길' in pg.inner_text('#ov');listen(pg);choose(pg,'같이 내려가자');choose(pg,'이야기를 마친다')
    E(pg,"()=>{const K=window.__k2;K.S.inv.scrap=2;K.render()}");assert pg.locator('button[data-c=nq1][disabled]').count()==1
    E(pg,"()=>{const K=window.__k2;K.S.inv.scrap=6;K.render()}");pg.click('button[data-c=nq1]');choose(pg,'맞선다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("저택 지하")',timeout=5000);choose(pg,'살문을 닫는다');assert E(pg,"window.__k2.S.inv.scrap")==1 and E(pg,"window.__k2.S.nq")==2
    go(pg,'under','eno');pg.click('button[data-c=nq2]');choose(pg,'맞선다');win(pg)
    pg.wait_for_timeout(300);listen(pg);t=pg.inner_text('#ov');assert '너도 나처럼 여럿이구나' in t,t[:300];choose(pg,'이 조각을 어떻게');choose(pg,'나에게 돌려보낸다');choose(pg,'이렇게 하기로 한다');listen(pg)
    t=pg.inner_text('#ov');assert '물길 아래의 노래」가 끝났다' in t;choose(pg,'고개를 끄덕인다')
    s=E(pg,"window.__k2.S");assert s['nq']==4 and s['nqe']=='return' and s['cq']['eno']=='done'
    pg.click('button[data-c=tab][data-a=quest]');pg.click('h2.fold[data-a=done]');t=pg.inner_text('.M');assert '에노 — 물길 아래의 노래' in t and '이브레 — 색 없는 이름' in t;pg.click('button[data-c=tab][data-a=place]')
    print('eno ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
