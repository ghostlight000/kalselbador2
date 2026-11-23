"""종족 설정·종족 능력·재능 (v029): 만들기 화면의 글, 흑금 동전, 레벨 상한, 재능 고르기, 전투 효과, 이야기 재능, 저장 이전"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
E=lambda pg,x:pg.evaluate(x)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def start(pg,race,tr):
    pg.goto(url);pg.wait_for_timeout(200);E(pg,"localStorage.clear()");pg.goto(url);pg.wait_for_timeout(200)
    pg.click(f'button[data-c=race][data-a={race}]');pg.click(f'button[data-c=trait][data-a="{tr}"]');pg.wait_for_timeout(80)
    t=pg.inner_text('.cr');return t
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    # 만들기 화면: 계통 글과 종족 능력
    t=start(pg,'p',1)
    assert '흑금 방계' in t and '금빛 테' in t and '도시에서' in t and '종족 능력 — 비늘' in t and '동전 30' in t, t[:800]
    pg.click('text=파볼릭 이야기');pg.wait_for_timeout(50);assert '칼라쉬' in pg.inner_text('.cr')
    t=start(pg,'i',2);assert '노래하는 바람' in t and '짐승의 감각' in t and '주문 기력 −1' in t
    t=start(pg,'b',4);assert '푸른 눈' in t and '씨족의 맹세' in t and '마력 +1' in t
    # 흑금으로 시작: 동전 35
    start(pg,'p',1);pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]')
    pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');E(pg,"window.__k2.endBattle('tut')");okpop(pg)
    s=E(pg,'window.__k2.S');assert s['coin']==35 and s['tl']==[] and s['v']==11, (s['coin'],s.get('tl'),s['v'])
    E(pg,"()=>{const K=window.__k2;K.S.loc='docks';K.render()}")
    # 레벨 상한과 재능
    E(pg,"()=>{const K=window.__k2;K.gainXp(5000);K.render()}");s=E(pg,'window.__k2.S');assert s['lv']==12 and s['xp']==0, (s['lv'],s['xp'])
    out=E(pg,"window.__k2.gainXp(100)");assert out==[] and E(pg,'window.__k2.S.lv')==12
    assert E(pg,'window.__k2.tlCan()');m0=E(pg,'window.__k2.S.mhp')
    pg.click('button[data-c=tab][data-a=char]');pg.wait_for_timeout(80);t=pg.inner_text('.M');assert '고를 재능' in t and '레벨 상한' in t and '깨어난 목소리' not in t, t[-600:]
    pg.click('button[data-c=tpick][data-a=hide]');pg.wait_for_timeout(50);assert E(pg,'window.__k2.S.mhp')==m0+12
    for k in ['eye','beat','sew']:pg.click(f'button[data-c=tpick][data-a={k}]');pg.wait_for_timeout(30)
    assert not E(pg,'window.__k2.tlCan()') and len(E(pg,'window.__k2.S.tl'))==4
    t=pg.inner_text('.M');assert '고를 수 있는 재능을 모두 골랐다' in t
    # 전투: 비늘이 첫 공격을 절반으로, 붕대 +8
    E(pg,"()=>{const K=window.__k2;K.S.hp=K.S.mhp;K.startBattle('fight','dog')}");pg.wait_for_function('window.__k2.G.on')
    hp=E(pg,'window.__k2.G.hp');E(pg,"window.__k2.hurt(10)");assert E(pg,'window.__k2.G.hp')==hp-5
    E(pg,"window.__k2.hurt(10)");assert E(pg,'window.__k2.G.hp')==hp-15
    w=E(pg,"(()=>{const K=window.__k2;return K.BW()})()");print('BW',w)
    E(pg,"()=>{const K=window.__k2;K.G.fhp=0;K.endBattle('win')}");okpop(pg)
    # 이야기 재능
    E(pg,"()=>{const K=window.__k2;K.S.sx=K.S.sx||{};K.S.sx.cart={e:'truth',i:9,r:9};K.S.aev.barg=8;K.S.tutF=1;K.render()}")
    t=pg.inner_text('.M');assert '이야기 재능' in t and '끝까지 판 사람' in t and '맹세를 받은 자' in t and '모르텐의 가르침' in t and '서 있는 사람' not in t
    # 값 할인 (셈 빠른 손 아님 → 그대로)
    assert E(pg,'window.__k2.px(10)')==10
    # 옛 저장 이전: v10 푸른 눈 → 마력 +1, 흑금 → 동전 +30
    E(pg,"()=>{const K=window.__k2;const o=JSON.parse(JSON.stringify(K.S));o.v=10;o.race='b';o.tr=4;o.st=[5,2,3,5];o.tl=undefined;o.coin=0;localStorage.setItem('kalsel2',JSON.stringify(o))}")
    pg.goto(url);pg.wait_for_timeout(400)
    s=E(pg,'window.__k2.S')
    if s: assert s['st'][1]==3 and s['v']==11 and s['tl']==[], (s['st'],s['v'])
    print('migrate', s and s['st'])
    print('errors',errs);assert not errs
    b.close()
print('ALL OK')
