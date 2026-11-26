"""호감 단계 이벤트: 4·6·8단계, 길·저택, 2막 전엔 8단계가 열리지 않음, 로맨스 선택, 숫자 숨김"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def go(pg,k):pg.eval_on_selector(f'.map .node[data-a={k}]',"e=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}))");choose(pg,'간다');pg.wait_for_function(f"window.__k2.S.loc==='{k}'",timeout=10000);pg.wait_for_timeout(650);(pg.is_visible('#ov.on h2:has-text("대성당")') and (choose(pg,'고개를 숙인다'),choose(pg,'대성당을 나선다')));(pg.is_visible('#ov.on h2:has-text("문 앞의 상자")') and (choose(pg,'서랍 깊이'),choose(pg,'서랍을 닫는다')))
def drain(pg):
    # 말없이 듣는 줄이 있으면 넘긴다
    for _ in range(8):
        if pg.locator('#ov.on button:has-text("말없이 듣는다")').count():choose(pg,'말없이 듣는다')
        else:break
E=lambda pg,x:pg.evaluate(x)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200);pg.click('button[data-c=sx][data-a=f]') if pg.locator('button[data-c=sx][data-a=f]').count() else None
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.joinComp('kirien');K.joinComp('oswin');K.S.party='kirien';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.S.pit=1;K.S.loc='base';K.S.aff.kirien=30;K.S.orx={kirien:1,oswin:1};K.render()}")
    assert E(pg,"window.__k2.aevFor('kirien')") is None  # 4단계는 길에서
    go(pg,'docks');pg.wait_for_timeout(300);assert not pg.is_visible('#ov.on')  # 저절로 시작하지 않는다
    assert '✦' in pg.inner_text('button[data-c=talk]');(pg.click('button[data-c=talk]') if pg.locator('button[data-c=talk]').count() else (pg.click('button[data-c=rooms]'),pg.click('#ov.on button[data-c=talk][data-a='+pg.evaluate('window.__k2.S.party')+']')));pg.wait_for_selector('#ov.on h2:has-text("처마 밑")',timeout=5000);drain(pg);t=pg.inner_text('#ov');assert '밤을 까먹었어' in t
    choose(pg,'나는 비 오는 날이');drain(pg);choose(pg,'그대로 곁에 머문다');assert '웅덩이' in pg.inner_text('#ov');drain(pg);choose(pg,'같이 들여다본다');drain(pg);okpop(pg)
    s=E(pg,"window.__k2.S");assert s['aev']['kirien']==4 and s['aff']['kirien']==36
    # 숫자 숨김
    pg.click('button[data-c=tab][data-a=char]');t=pg.inner_text('.M');assert '호감' not in t and '촛불' not in t;pg.click('button[data-c=tab][data-a=place]')
    # 쿨다운 동안은 일어나지 않는다
    E(pg,"()=>{const K=window.__k2;K.S.aff.kirien=50;K.S.aevT=Date.now()}");assert E(pg,"window.__k2.aevFor('kirien')") is None
    E(pg,"()=>{window.__k2.S.aevT=0}");go(pg,'base');assert E(pg,"window.__k2.aevFor('kirien')")=='kirien:6'
    # 저택에서 말을 걸면 6단계
    (pg.click('button[data-c=talk]') if pg.locator('button[data-c=talk]').count() else (pg.click('button[data-c=rooms]'),pg.click('#ov.on button[data-c=talk][data-a='+pg.evaluate('window.__k2.S.party')+']')))
    pg.wait_for_selector('#ov.on h2:has-text("지붕 위")',timeout=5000);drain(pg);assert '서른여덟' in pg.inner_text('#ov');choose(pg,'옆에 앉는다');drain(pg);choose(pg,'그대로 곁에 머문다');drain(pg);choose(pg,'내일 밤엔');drain(pg);okpop(pg)
    # 8단계: 1막에는 없다 → 2막에 로맨스 선택(여성 주인공·키리엔)
    E(pg,"()=>{const K=window.__k2;K.S.aff.kirien=72;K.S.aevT=0}");assert E(pg,"window.__k2.aevFor('kirien')") is None
    E(pg,"()=>{const K=window.__k2;K.S.eda=1;K.S.acad=1;K.S.sex='f'}");assert E(pg,"window.__k2.aevFor('kirien')")=='kirien:8'
    go(pg,'docks');pg.click('button[data-c=talk]');pg.wait_for_selector('#ov.on h2:has-text("놋등")',timeout=5000);drain(pg);choose(pg,'반드시 찾는다');drain(pg);choose(pg,'그대로 곁에 머문다');drain(pg);assert '너는 어디에도 안 보내' not in pg.inner_text('#ov');
    if pg.locator('#ov.on .btn.pri').count():okpop(pg)
    E(pg,"()=>{window.__k2.EV0=null}");E(pg,"window.__k2.CMD.talk('kirien')");pg.wait_for_timeout(200);drain(pg);assert '냄새로 먼저 찾아' in pg.inner_text('#ov');choose(pg,'너는 어디에도 안 보내');drain(pg);assert E(pg,"window.__k2.S.rom")=='kirien'
    # 남성 주인공이면 키리엔 로맨스 선택이 없다(오스윈은 있다)
    E(pg,"()=>{const K=window.__k2;K.S.rom=null;K.S.sex='m';K.S.party='oswin';K.S.aff.oswin=72;K.S.aev.oswin=6;K.S.aevT=0}")
    go(pg,'street');pg.click('button[data-c=talk]');pg.wait_for_selector('#ov.on h2:has-text("외워 둔 것")',timeout=5000);drain(pg);choose(pg,'나도 네 이름을');drain(pg);choose(pg,'그대로 곁에 머문다');drain(pg);assert '장부에 적어도 돼' not in pg.inner_text('#ov');
    if pg.locator('#ov.on .btn.pri').count():okpop(pg)
    assert E(pg,"window.__k2.S.rom") is None
    # 개발 버튼 동작
    E(pg,"()=>{const K=window.__k2;K.joinComp('ibre');K.S.party='ibre'}");r=E(pg,"()=>{const K=window.__k2;return Object.keys(K.AEV).map(id=>[4,6,8].every(t=>K.AEV[id][t]&&K.AEV[id][t].p().length>2&&K.AEV[id][t].p2&&K.AEV[id][t].p2().length>2&&K.AEV[id][t].c2.length>=1)).every(x=>x)}");assert r
    print('aev ok');b.close()
assert not errs,errs
print('ALL OK')
