"""호감 단계 이벤트: 4·6·8단계, 길·저택, 2막 전엔 8단계가 열리지 않음, 로맨스 선택, 숫자 숨김"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def go(pg,k):pg.click(f'.map .node[data-a={k}]');choose(pg,'간다');pg.wait_for_function(f"window.__k2.S.loc==='{k}'",timeout=10000);pg.wait_for_timeout(650)
def drain(pg):
    # 말없이 듣는 줄이 있으면 넘긴다
    for _ in range(8):
        if pg.locator('#ov.on button:has-text("말없이 듣는다")').count():choose(pg,'말없이 듣는다')
        else:break
E=lambda pg,x:pg.evaluate(x)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200);pg.click('button[data-c=sx][data-a=f]') if pg.locator('button[data-c=sx][data-a=f]').count() else None
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("가르침은 건너뛴다")');pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.joinComp('kirien');K.joinComp('oswin');K.S.party='kirien';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.S.pit=1;K.S.loc='base';K.S.aff.kirien=30;K.render()}")
    assert E(pg,"window.__k2.aevNext('base')") is None  # 4단계는 길에서
    assert E(pg,"window.__k2.aevNext('road')")=='kirien:4'
    go(pg,'docks');pg.wait_for_selector('#ov.on h2:has-text("처마 밑")',timeout=5000);drain(pg);t=pg.inner_text('#ov');assert '여우가 비' in t
    choose(pg,'나는 비 오는 날이');drain(pg);okpop(pg)
    s=E(pg,"window.__k2.S");assert s['aev']['kirien']==4 and s['aff']['kirien']==33
    # 숫자 숨김
    pg.click('button[data-c=tab][data-a=char]');t=pg.inner_text('.M');assert '호감' not in t and '촛불' not in t;pg.click('button[data-c=tab][data-a=place]')
    # 쿨다운 동안은 일어나지 않는다
    E(pg,"()=>{const K=window.__k2;K.S.aff.kirien=50;K.S.aevT=Date.now()}");assert E(pg,"window.__k2.aevNext('base')") is None
    E(pg,"()=>{window.__k2.S.aevT=0}");assert E(pg,"window.__k2.aevNext('base')")=='kirien:6'
    # 저택에서 쉬면 6단계
    go(pg,'base')
    pg.wait_for_selector('#ov.on h2:has-text("지붕 위")',timeout=5000);drain(pg);assert '서른여덟' in pg.inner_text('#ov');choose(pg,'옆에 앉는다');drain(pg);okpop(pg)
    # 8단계: 1막에는 없다 → 2막에 로맨스 선택(여성 주인공·키리엔)
    E(pg,"()=>{const K=window.__k2;K.S.aff.kirien=72;K.S.aevT=0}");assert E(pg,"window.__k2.aevNext('road')") is None
    E(pg,"()=>{const K=window.__k2;K.S.eda=1;K.S.acad=1;K.S.sex='f'}");assert E(pg,"window.__k2.aevNext('road')")=='kirien:8'
    go(pg,'docks');pg.wait_for_selector('#ov.on h2:has-text("놋등")',timeout=5000);drain(pg);assert '사라지게 두지 않는다' in pg.inner_text('#ov')
    choose(pg,'사라지게 두지 않는다');drain(pg);okpop(pg);assert E(pg,"window.__k2.S.rom")=='kirien'
    # 남성 주인공이면 키리엔 로맨스 선택이 없다(오스윈은 있다)
    E(pg,"()=>{const K=window.__k2;K.S.rom=null;K.S.sex='m';K.S.party='oswin';K.S.aff.oswin=72;K.S.aev.oswin=6;K.S.aevT=0}")
    go(pg,'street');pg.wait_for_selector('#ov.on h2:has-text("외워 둔 것")',timeout=5000);drain(pg);assert '평생 외워' in pg.inner_text('#ov');choose(pg,'나도 네 이름을');drain(pg);okpop(pg)
    assert E(pg,"window.__k2.S.rom") is None
    # 개발 버튼 동작
    E(pg,"()=>{const K=window.__k2;K.joinComp('ibre');K.S.party='ibre'}");r=E(pg,"()=>{const K=window.__k2;return Object.keys(K.AEV).map(id=>[4,6,8].every(t=>K.AEV[id][t]&&K.AEV[id][t].p().length>2)).every(x=>x)}");assert r
    print('aev ok');b.close()
assert not errs,errs
print('ALL OK')
