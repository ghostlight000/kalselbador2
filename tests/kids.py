"""파견 가까운/먼 곳, 다친 아이 간호·구호소, 아이 고용, 초상 고르기와 사진 거르기"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
E=lambda pg,x:pg.evaluate(x)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200);pg.click('button[data-c=cav][data-a=i2]')
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    assert E(pg,"window.__k2.S.av")=='i2' and pg.locator('.L .av').count()==1
    # 나쁜 사진 주소는 그리지 않는다
    E(pg,"()=>{const K=window.__k2;K.S.av='data:image/png;base64,AAA\" onerror=\"alert(1)';K.render()}");assert pg.locator('.L img.av').count()==0
    E(pg,"()=>{const K=window.__k2;K.S.av='i2';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.grantPit()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.S.loc='base';K.S.coin=100;K.S.inv.band=3;K.render()}")
    assert pg.locator('.scw svg, .scw img').count()==1
    assert E(pg,"window.__k2.DSP.wall.d")>=7200 and E(pg,"window.__k2.DSP.dock.d")>=1200
    pg.click('button[data-c=board]');t=pg.inner_text('#ov');assert '가까운 곳' in t and '먼 곳' in t;pg.click('#ov.on .drow:has-text("시장 심부름")')
    assert E(pg,"window.__k2.S.kids.pit.st")=='out';pg.click('button[data-c=board]');assert pg.locator('#ov .drow[disabled]').count()>=6;choose(pg,'닫기')
    pg.wait_for_selector('#ov.on h2:has-text("파견에서 돌아왔다")',timeout=40000);okpop(pg);assert E(pg,"window.__k2.S.kids.pit.st")=='ok'
    # 다친 아이: 간호
    E(pg,"()=>{const K=window.__k2;K.S.kids.pit.st='hurt';K.render()}");assert '다친 아이' in pg.inner_text('button[data-c=kids]')
    pg.click('button[data-c=board]');assert pg.locator("#ov .drow[disabled]").count()>=6;choose(pg,'닫기')
    pg.click('button[data-c=kids]');assert '돌봐 줘야' in pg.inner_text('#ov');assert '일을 찾아올' in pg.inner_text('#ov');choose(pg,'피트 간호하기');okpop(pg)
    assert E(pg,"window.__k2.S.kids.pit.st")=='care' and E(pg,"window.__k2.S.inv.band")==3
    pg.wait_for_function("window.__k2.S.kids.pit.st==='ok'",timeout=15000);print('care ok')
    # 구호소
    E(pg,"()=>{const K=window.__k2;K.S.kids.pit.st='hurt';K.render()}");c0=E(pg,"window.__k2.S.coin");pg.click('button[data-c=kids]');choose(pg,'구호소에 보내기');okpop(pg)
    assert E(pg,"window.__k2.S.kids.pit.st")=='hosp' and E(pg,"window.__k2.S.coin")==c0-8;pg.wait_for_function("window.__k2.S.kids.pit.st==='ok'",timeout=15000);print('hospital ok')
    # 1막이 끝나면 고용
    E(pg,"()=>{const K=window.__k2;K.S.eda=1;K.render()}");pg.click('button[data-c=kids]');c0=E(pg,"window.__k2.S.coin");choose(pg,'넬 고용하기');okpop(pg);assert E(pg,"window.__k2.S.kids.nell.st")=='ok' and E(pg,"window.__k2.S.coin")==c0-15
    pg.click('button[data-c=board]');pg.click('#ov.on .drow:has-text("부두 잡동사니")');choose(pg,'넬');assert E(pg,"window.__k2.S.kids.nell.st")=='out' and E(pg,"window.__k2.S.kids.pit.st")=='ok'
    print('hire ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
