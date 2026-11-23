"""곁가지 사건: 운하의 신발(조사), 서리이끼(구하기), 불탄 수레(대립), 두 어머니(대립), 이름 없는 종(구하기), 탐사 중 작은 일"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def clear(pg):
    for _ in range(10):
        pg.wait_for_timeout(120)
        if E(pg,"window.__k2.G.on"):win(pg);continue
        if pg.locator('#ov.on').count():
            if pg.locator('#ov.on .btn.pri').count():okpop(pg)
            else:pg.locator('#ov.on button').last.click()
            continue
        break
def go(pg,k):
    clear(pg)
    pg.eval_on_selector(f'.map .node[data-a={k}]',"e=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}))");choose(pg,'간다')
    for _ in range(100):
        if E(pg,f"window.__k2.S.loc==='{k}'&&!window.__k2.S.act"):break
        if E(pg,"window.__k2.G.on"):win(pg)
        pg.wait_for_timeout(100)
    assert E(pg,f"window.__k2.S.loc==='{k}'"),k
    pg.wait_for_timeout(650)
def win(pg):
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{window.__k2.G.fhp=0}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);okpop(pg)
E=lambda pg,x:pg.evaluate(x)
def sxa(pg,id):pg.click(f'button[data-c=sxa][data-a={id}]');pg.wait_for_timeout(80)
def explore(pg):
    pg.click('button[data-c=explore]',timeout=5000)
    for _ in range(80):
        pg.wait_for_timeout(150)
        if E(pg,"window.__k2.G.on"):win(pg);continue
        if pg.locator('#bov.on').count():pg.click('#bov.on .btn.pri');continue
        if pg.locator('#ov.on').count():
            if pg.locator('#ov.on .btn.pri').count():okpop(pg)
            else:pg.locator('#ov.on button').last.click()
            continue
        if not E(pg,"window.__k2.S.act||window.__k2.S.pend"):break
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200);E(pg,"localStorage.clear()");pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('kirien');K.joinComp('oswin');K.S.party='kirien';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.grantPit()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.S.eda=1;K.S.acad=1;K.S.fac=1;K.S.outs=1;K.S.mr=3;K.S.manor=1;K.S.coin=50;K.S.inv.scrap=6;K.S.loc='docks';K.S.hp=K.S.mhp;K.S.sxno={moss:1,cart:1,bottle:1,bell:1,mort:1};K.S.sxon=1;K.render()}")
    # 1) 운하의 신발 — 탐사 중 발견
    E(pg,"()=>{window.__k2.SX.shoe.hook.p=1}")
    pg.click('button[data-c=explore]');pg.wait_for_function('!window.__k2.S.act',timeout=20000)
    if E(pg,"window.__k2.G.on"):win(pg)
    else:okpop(pg)
    pg.wait_for_selector('#ov.on h2:has-text("운하의 신발")',timeout=5000);assert '냄새' in pg.inner_text('#ov');choose(pg,'신발을 챙긴다')
    sxa(pg,'shoe');t=pg.inner_text('#ov');assert '노파' in t and '뱃사공' in t;choose(pg,'계단 가스등')
    pg.click('button[data-c=tab][data-a=quest]');q=pg.inner_text('.M');assert '운하의 신발' in q and '조사' in q and '초소의 근무 일지' in q,q;pg.click('button[data-c=tab][data-a=place]')
    go(pg,'street');sxa(pg,'shoe');assert '학술원 인부' in pg.inner_text('#ov');choose(pg,'마차가 간 곳')
    go(pg,'docks');sxa(pg,'shoe');choose(pg,'맞선다');win(pg);pg.wait_for_selector('#ov.on h2:has-text("계단 밑의 불")',timeout=5000);assert '마르코' in pg.inner_text('#ov');choose(pg,'유리관을 챙긴다')
    go(pg,'works');sxa(pg,'shoe');assert '감독관' in pg.inner_text('#ov');choose(pg,'신발을 신겨 준다');assert '셋까지' in pg.inner_text('#ov');okpop(pg)
    assert E(pg,"window.__k2.S.sx.shoe.e")=='home';print('shoe ok')
    # 2) 서리이끼 — 도착하면 부탁, 묘지 탐사로 모으기
    E(pg,"()=>{const K=window.__k2;delete K.S.sxno.moss}");go(pg,'outskirts');pg.wait_for_selector('#ov.on h2:has-text("천막촌의 열병")',timeout=5000);choose(pg,'이끼를 구해 오겠다')
    go(pg,'church');E(pg,"()=>{const K=window.__k2;K.SX.moss.steps[0].col.p=1}")
    for i in range(3):explore(pg)
    assert E(pg,"window.__k2.S.sx.moss.i")==1,E(pg,"JSON.stringify(window.__k2.S.sx.moss)")
    go(pg,'outskirts');sxa(pg,'moss');assert '회색 장갑' in pg.inner_text('#ov');choose(pg,'마르타에게 준다');okpop(pg);assert E(pg,"window.__k2.S.sx.moss.e")=='kids';print('moss ok')
    # 3) 불탄 수레 — 끝까지 파헤치기
    E(pg,"()=>{const K=window.__k2;delete K.S.sxno.cart}");go(pg,'street');pg.wait_for_selector('#ov.on h2:has-text("불탄 수레")',timeout=5000);choose(pg,'둘을 떼어 놓는다')
    sxa(pg,'cart');choose(pg,'니코를 찾아간다');go(pg,'docks');sxa(pg,'cart');t=pg.inner_text('#ov');assert '보험' in t;choose(pg,'더 살펴보겠다')
    go(pg,'street');sxa(pg,'cart');assert '돈궤' in pg.inner_text('#ov');choose(pg,'보여 준다');okpop(pg);assert E(pg,"window.__k2.S.sx.cart.e")=='truth';print('cart ok')
    # 4) 두 어머니 — 병마개를 연다
    E(pg,"()=>{const K=window.__k2;delete K.S.sxno.bottle}");go(pg,'docks');go(pg,'street');pg.wait_for_selector('#ov.on h2:has-text("두 어머니")',timeout=5000);choose(pg,'내가 알아보겠다')
    go(pg,'outskirts');sxa(pg,'bottle');choose(pg,'클라라를 찾아간다');go(pg,'church');sxa(pg,'bottle');assert '하녀 아이' in pg.inner_text('#ov');choose(pg,'전당포로')
    go(pg,'pawn');sxa(pg,'bottle');choose(pg,'병마개를 열어 본다');assert '요리! 빨리 와' in pg.inner_text('#ov');choose(pg,'둘이 나누게');okpop(pg);assert E(pg,"window.__k2.S.sx.bottle.e")=='both';print('bottle ok')
    # 5) 이름 없는 종 — 넝마 더미 + 고철
    E(pg,"()=>{const K=window.__k2;delete K.S.sxno.bell}");go(pg,'church');pg.wait_for_selector('#ov.on h2:has-text("이름 없는 종")',timeout=5000);choose(pg,'종추를 찾아오겠다')
    go(pg,'outskirts');E(pg,"()=>{const K=window.__k2;K.SX.bell.steps[0].col.p=1}")
    for i in range(2):explore(pg)
    go(pg,'church');E(pg,"()=>{const K=window.__k2;K.S.inv.scrap=6;K.render()}");sxa(pg,'bell');choose(pg,'종을 단다');okpop(pg);assert E(pg,"window.__k2.S.sx.bell.e")=='ring' and E(pg,"window.__k2.S.inv.scrap")==1;print('bell ok')
    pg.click('button[data-c=tab][data-a=quest]');q=pg.inner_text('.M');assert '다시 울린다' in q and '나눠 마셨다' in q;pg.click('button[data-c=tab][data-a=place]')
    # 6) 연계: 모르텐의 열쇠 — 1막에 시작, 깨어나야 2단계, 3막에야 문
    E(pg,"()=>{const K=window.__k2;delete K.S.sxno.mort;K.S.mort=2;K.S.mg=0;K.S.rev=0;K.S.a3=0;K.render()}");go(pg,'docks');go(pg,'street');pg.wait_for_selector('#ov.on h2:has-text("빈 초소")',timeout=5000);assert '일곱째 문' in pg.inner_text('#ov');choose(pg,'수첩과 열쇠를 챙긴다')
    go(pg,'church');sxa(pg,'mort');assert '대정화자' in pg.inner_text('#ov');choose(pg,'열쇠를 다시')
    go(pg,'outskirts');b0=pg.locator('button[data-c=sxa][data-a=mort]');assert b0.is_disabled() and '잠들어' in b0.inner_text()
    E(pg,"()=>{const K=window.__k2;K.S.mg=1;K.S.oq0=1;K.render()}");sxa(pg,'mort');assert '모르야' in pg.inner_text('#ov');choose(pg,'수첩을 덮는다')
    go(pg,'stairs');b0=pg.locator('button[data-c=sxa][data-a=mort]');assert b0.is_disabled() and '경비' in b0.inner_text()
    pg.click('button[data-c=tab][data-a=quest]');q=pg.inner_text('.M');assert '모르텐의 열쇠' in q and '연계' in q and '교단 경비' in q,q;pg.click('button[data-c=tab][data-a=place]')
    E(pg,"()=>{const K=window.__k2;K.S.rev=1;K.S.a3=1;K.render()}");sxa(pg,'mort');choose(pg,'맞선다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("일곱째 문")',timeout=5000);assert '경비대 모르텐' in pg.inner_text('#ov');choose(pg,'병들을 열어');assert '자네는 서 있게' in pg.inner_text('#ov');okpop(pg)
    assert E(pg,"window.__k2.S.sx.mort.e")=='free' and not E(pg,"window.__k2.S.inv.mkey");print('mort ok')
    # 탐사 중 작은 일
    E(pg,"()=>{const K=window.__k2;K.S.pend=null;K.S.xev=0;K.SCENE.xev()}");choose(pg,'뜯어 본다');okpop(pg);print('xev ok')
    b.close()
assert not errs,errs
print('ALL OK')
