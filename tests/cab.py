"""삯마차: 어디서든 거처로 15초, 거처에서 떠나온 곳으로 다시. 길에서 마주침 없음. 이동 시간 반(v081)"""
from playwright.sync_api import sync_playwright
url='file:///home/claude/kalselbador2/index.html?test'
E=lambda pg,x:pg.evaluate(x)
def clear(pg):
    for _ in range(6):
        pg.wait_for_timeout(150)
        if pg.locator('#ov.on .btn.pri').count():pg.click('#ov.on .btn.pri')
        elif pg.locator('#ov.on .btn').count():pg.locator('#ov.on .btn').last.click()
        else:break
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    # 동료가 하나뿐이고 저택이 없으면 버튼이 없다
    E(pg,"()=>{const K=window.__k2;K.joinComp('kirien');K.S.loc='docks';K.render()}")
    assert pg.locator('button[data-c=cab]').count()==0
    # 동료 둘, 저택 전 → 여관으로
    E(pg,"()=>{const K=window.__k2;K.joinComp('oswin');K.S.loc='docks';K.EV0=null;K.render()}")
    clear(pg)
    t=pg.inner_text('button[data-c=cab]');assert '녹슨 닻 여관으로' in t,t
    # 저택이 생기면 저택으로
    E(pg,"()=>{const K=window.__k2;K.grantBase();K.S.loc='docks';K.EV0=null;K.render()}")
    clear(pg)
    assert '저택으로' in pg.inner_text('button[data-c=cab]')
    E(pg,"window.__k2.CMD.cab(document.querySelector('button[data-c=cab]').dataset.a)");a=E(pg,"window.__k2.S.act");assert a['cab']==1 and a['to']=='base' and a['fr']=='docks',a
    pg.wait_for_function("window.__k2.S.loc==='base'",timeout=10000);clear(pg)
    assert E(pg,"window.__k2.S.ret")=='docks'
    t=pg.inner_text('button[data-c=cab]');assert '부두' in t and '다시 간다' in t,t
    E(pg,"window.__k2.CMD.cab(document.querySelector('button[data-c=cab]').dataset.a)");pg.wait_for_function("window.__k2.S.loc==='docks'",timeout=10000)
    # 이동 시간 반
    assert E(pg,"window.__k2.travelSec('church','chapel')")==30 and E(pg,"window.__k2.travelSec('docks','street')")<=210
    print('cab ok',errs);assert not errs
    b.close()
