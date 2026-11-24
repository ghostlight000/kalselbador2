"""v031: 2막 전반 줄기 — 검사실 → 천막촌의 노래 → 장로의 천막 → 고해소 → 정화자 숙소 → 지하 예배실 → 금서고가 열린다. 작은 장소·곁가지·부탁"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def go(pg,k):pg.eval_on_selector(f'.map .node[data-a={k}]',"e=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}))");choose(pg,'간다');pg.wait_for_function(f"window.__k2.S.loc==='{k}'",timeout=10000);pg.wait_for_timeout(650);(pg.is_visible('#ov.on h2:has-text("대성당")') and (choose(pg,'고개를 숙인다'),choose(pg,'대성당을 나선다')))
def win(pg):
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{window.__k2.G.fhp=0}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);okpop(pg)
def drain(pg):
    for _ in range(8):
        if pg.locator('#ov.on button:has-text("말없이 듣는다")').count():choose(pg,'말없이 듣는다')
        else:break
E=lambda pg,x:pg.evaluate(x)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');E(pg,"window.__k2.endBattle('tut')");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;['kirien','oswin','ibre','kasimir','barg','eno'].forEach(k=>K.joinComp(k));K.S.party='barg';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.grantPit();}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.S.eda=1;K.S.acad=1;K.S.vis.academy=1;K.S.mg=1;K.S.mgh='open';K.S.oq=4;K.S.fac=1;K.S.oq0=1;K.S.aevT=Date.now();K.S.loc='works';K.S.hp=K.S.mhp;K.render()}")
    if pg.is_visible('#ov.on'):pg.click('#ov.on button >> nth=-1')
    t=pg.inner_text('.goalc');assert '공급 검사실' in t and '리세의 말' in t,t
    go(pg,'insp');pg.click('button[data-c=a2a]');assert '놋쇠 깔때기' in pg.inner_text('#ov') and '천막에서 본 것' in pg.inner_text('#ov');choose(pg,'장부를 빼앗는다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("징수 명단")',timeout=5000);okpop(pg);s=E(pg,"window.__k2.S");assert s['a2']==1 and s['outs']==1 and s['inv']['roll']==1
    go(pg,'works');go(pg,'docks');go(pg,'street');go(pg,'outskirts');pg.click('button[data-c=a2b]');assert '투리' in pg.inner_text('#ov');choose(pg,'노래를 끝까지 듣는다');okpop(pg)
    go(pg,'elder');pg.click('button[data-c=a2c]');assert '오르마' in pg.inner_text('#ov');choose(pg,'밖으로 나간다');assert E(pg,"window.__k2.G.foe")=='preacher';win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("장로의 천막")',timeout=5000);t=pg.inner_text('#ov');assert '재의 형제단' in t and '등잔 불꽃' in t;okpop(pg)
    go(pg,'outskirts');go(pg,'street');go(pg,'church');go(pg,'confess');pg.click('button[data-c=a2d]');assert '돌아오는 이를 위하여' in pg.inner_text('#ov');choose(pg,'노인을 말린다');okpop(pg);assert E(pg,"window.__k2.S.cfs")=='stop'
    go(pg,'barracks');pg.click('button[data-c=a2e]');assert '울릭 놈 자리' in pg.inner_text('#ov');choose(pg,'맞선다');assert E(pg,"window.__k2.G.foe")=='pilgrim';win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("운반 일지")',timeout=5000);okpop(pg);assert E(pg,"window.__k2.S.vk")==1
    go(pg,'chapel');pg.click('button[data-c=a2f]');assert '돌아오셨다' in pg.inner_text('#ov');choose(pg,'제단 앞으로');assert E(pg,"window.__k2.G.foe")=='penitent';win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("비어 있는 의자")',timeout=5000);okpop(pg);assert E(pg,"window.__k2.S.a2")==6
    t=pg.inner_text('.goalc');assert '금서고' in t and '새 자물쇠' in t,t
    # 이동 시간: 같은 구역 안은 짧다
    assert E(pg,"window.__k2.travelSec('church','chapel')")==90 and E(pg,"window.__k2.travelSec('confess','chapel')")==90 and E(pg,"window.__k2.travelSec('docks','chapel')")>E(pg,"window.__k2.travelSec('docks','church')")
    # 곁가지 정의와 부탁
    sx=E(pg,"Object.keys(window.__k2.SX)");assert all(k in sx for k in ['tag','warmw','dreamk','feast','jobAc','jobWk','jobOt','jobCh']),sx
    pg.click('button[data-c=tab][data-a=quest]');assert '지하 예배실' in pg.inner_text('.M')
    print('errors',errs);assert not errs
    b.close()
print('ALL OK')
