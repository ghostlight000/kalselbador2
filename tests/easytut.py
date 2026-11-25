"""v069: 쉬움 난이도 적 패턴(두 박자까지, 속임 없음) · 모르텐이 죽은 뒤 박자 되짚기 · 가르침 화면 안내"""
import pathlib
from playwright.sync_api import sync_playwright
url=(pathlib.Path(__file__).resolve().parent.parent/'index.html').as_uri()+'?test'
errs=[]
E=lambda pg,x:pg.evaluate(x)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on')
    t=pg.inner_text('#bov');assert '「회피」' in t and 'F 또는' not in t and pg.locator('#bov svg.tutfig').count()==1
    pg.click('#bov button:has-text("해 보지")');pg.wait_for_timeout(900)
    assert pg.locator('#bacts button[data-p=parry][disabled]').count()==1 and pg.locator('#bacts button.hint[data-p=dodge]').count()==1 and 'kbd' not in pg.inner_html('#bacts')
    E(pg,"window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    # 쉬움: 박자 둘까지, 속임 없음
    E(pg,"()=>{window.__k2.setDiff?window.__k2.setDiff(0):0}")
    E(pg,"()=>{const K=window.__k2;K.CMD&&0}")
    pg.evaluate("()=>{const c=JSON.parse(localStorage.getItem('k2cfg')||'{}');c.diff=0;localStorage.setItem('k2cfg',JSON.stringify(c))}")
    pg.reload();pg.wait_for_timeout(300)
    if pg.locator('button[data-c=cont]').count():pg.click('button[data-c=cont]')
    pg.wait_for_timeout(300)
    mx=E(pg,"()=>{const K=window.__k2;K.G.kind='fight';const r=['four','late','triple'].map(k=>K.easyB(K.MV[k].b));return [K.CFG.diff,Math.max(...r.map(x=>x.length)),r.some(x=>x.some(b=>b.f)),Math.min(...r.filter(x=>x.length>1).map(x=>x[1].t-x[0].t))]}")
    assert mx[0]==0 and mx[1]<=2 and not mx[2] and mx[3]>=520,mx
    print('easy beats',mx)
    # 모르텐이 죽은 뒤
    E(pg,"()=>{const K=window.__k2;K.S.mort=2;K.render()}");E(pg,"window.__k2.CMD.tutor()");pg.wait_for_function('window.__k2.G.on')
    assert '모르텐의 말이 떠오른다' in pg.inner_text('#bov') and '기억 속 모르텐' in pg.inner_text('#bt')
    E(pg,"window.__k2.endBattle('tut')");pg.wait_for_timeout(200);t=pg.inner_text('#ov');assert '박자를 되짚었다' in t and '배웠다' not in t,t;pg.click('#ov.on .btn.pri')
    assert '모르텐이 가르쳐 준 박자를 되짚었다' in pg.inner_text('body')
    print('errors',errs);assert not errs;print('ALL OK')
    b.close()
