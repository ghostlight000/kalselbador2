"""v073: 요리 조합·배우기·장, 재료 출처, 우두머리 전리품 제작"""
import pathlib
from playwright.sync_api import sync_playwright
url=(pathlib.Path(__file__).resolve().parent.parent/'index.html').as_uri()+'?test'
errs=[]
E=lambda pg,x:pg.evaluate(x)
def choose(pg,t):pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def go(pg,l):E(pg,f"()=>{{const K=window.__k2;K.S.loc='{l}';K.S.vis['{l}']=1;K.render()}}")
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.coin=200;K.grantBase();}");pg.click('#ov.on .btn.pri')
    go(pg,'docks');pg.click('.M button[data-c=mkt]');assert '부두 아침 장' in pg.inner_text('#ov');choose(pg,'생선 사기');choose(pg,'꿀 사기');choose(pg,'자리를 뜬다')
    assert E(pg,"window.__k2.S.inv.fish")>=1 and E(pg,"window.__k2.S.inv.honey")>=1
    pg.click('.M button[data-c=dlearn]');choose(pg,'꿀 절임 생선 배우기');assert E(pg,"window.__k2.S.dishL.pickle")==1;choose(pg,'고맙다고 한다')
    go(pg,'works');pg.click('.M button[data-c=mkt]');choose(pg,'미지근한 물 사기');choose(pg,'자리를 뜬다')
    E(pg,"()=>{const K=window.__k2;K.S.fix.kitchen=1;K.S.loc='base';K.render()}")
    E(pg,"window.__k2.CMD.pot()");t=pg.inner_text('#ov');assert '꿀 절임 생선' in t and '재료 구하는 곳' in t;choose(pg,'생선을(를) 넣는다');choose(pg,'꿀을(를) 더 넣는다')
    assert '꿀 절임 생선' in pg.inner_text('#ov') and E(pg,"window.__k2.S.inv.pickle")==1;choose(pg,'솥을 내려놓는다')
    # 전리품 → 제작법
    E(pg,"()=>{const K=window.__k2;K.startBattle('fight','clock')}");pg.wait_for_function('window.__k2.G.on')
    E(pg,"()=>{const G=window.__k2.G;G.fhp=0}");E(pg,"window.__k2.endBattle('win')");pg.wait_for_timeout(200)
    assert E(pg,"window.__k2.S.inv.spring")==1 and E(pg,"window.__k2.S.rcpL.spblade")==1;assert '태엽 칼' in pg.inner_text('#ov')
    print('errors',errs);assert not errs;print('ALL OK')
    b.close()
