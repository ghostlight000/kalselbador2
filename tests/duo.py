"""v061: 저택의 동료들 — 엿듣기 · 말다툼 편들기 · 질투"""
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
E=lambda pg,x:pg.evaluate(x)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('oswin');K.joinComp('kasimir');K.S.party='oswin';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{loc:'base'});K.S.aff.oswin=10;K.S.aff.kasimir=10;K.render()}")
    assert pg.locator('button[data-c=duo]').count()==1
    pg.click('button[data-c=duo]');t=pg.inner_text('#ov');assert '붉은 물' in t and '남의 병을' in t and '카시미르' in t,t[:400]
    a0=E(pg,"window.__k2.S.aff.oswin");k0=E(pg,"window.__k2.S.aff.kasimir")
    choose(pg,'오스윈 말이 맞다');t=pg.inner_text('#ov');assert '걱정이었지요' in t;choose(pg,'자리를 뜬다')
    assert E(pg,"window.__k2.S.aff.oswin")>a0 and E(pg,"window.__k2.S.aff.kasimir")<k0
    # 쿨다운: 바로는 다음 장면 없음
    assert pg.locator('button[data-c=duo]').count()==0
    print('argue ok')
    # 질투: 카시미르 55, 오스윈 70 → 카시미르가 질투
    E(pg,"()=>{const K=window.__k2;K.S.duoT=0;K.S.aff.kasimir=55;K.S.aff.oswin=70;K.render()}")
    pg.click('button[data-c=duo]');listen(pg);t=pg.inner_text('#ov');assert '질투' in t and '오스윈' in t,t[:300];choose(pg,'너도 소중해');listen(pg);choose(pg,'이야기를 마친다')
    assert E(pg,"window.__k2.S.jeal.kasimir")==1
    print('jealous ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
