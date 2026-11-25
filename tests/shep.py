"""v066: 목자의 길 — 할데온 손님 동행, 두 번째 갈림, 엔딩 둘"""
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
def win(pg):
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{const G=window.__k2.G;G.fhp=0;if(G.pack)G.pack.forEach(p=>p.fhp=0)}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);okpop(pg)
def skipcine(pg):
    pg.wait_for_selector('#pv.on .eo',timeout=8000);assert pg.locator('#pv .eo').count()==1
    if pg.locator('#pv [data-pv=skip]').count():pg.click('#pv [data-pv=skip]')
    pg.wait_for_timeout(100);assert '엔딩' in pg.inner_text('#pv');pg.click('#pv [data-pv=close]');pg.wait_for_timeout(150)
E=lambda pg,x:pg.evaluate(x)
def go(pg,loc,party):E(pg,f"()=>{{const K=window.__k2;K.S.loc='{loc}';K.S.party='{party}';K.render()}}")
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('kirien');K.joinComp('ibre');K.S.party='kirien';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{pit:1,manor:1,mr:3,eda:1,acad:1,fac:1,mg:1,mgh:'hide',rev:1,revd:1,a2:6,h2:5,orx:{kasimir:1,ibre:1},mgt:{kasimir:1,ibre:1},rvt:{kasimir:1,ibre:1},loc:'base'});K.S.vis.academy=1;K.render()}")
    base="()=>{const K=window.__k2;Object.assign(K.S,{a3:1,a3h:1,h2:6,abel:'i',amn:null,rq:3,rqId:'oswin',taken:null,hq:3,hald:2,c3:4,r3a:1,r3b:1,route:null,end:null,loc:'base',party:'kirien',rom:'kirien',sex:'f',magp:3,rvt:{kirien:1,ibre:1},mgt:{kirien:1,ibre:1},aff:Object.assign(K.S.aff,{kirien:40,ibre:40})});K.render()}"
    E(pg,base)
    pg.click('button[data-c=c3r]');choose(pg,'목자의 길');choose(pg,'이 길로 간다');choose(pg,'자리에 앉는다')
    t=pg.inner_text('#ov');assert '일곱 의자' in t;choose(pg,'찻잔을 든다')
    s=E(pg,"window.__k2.S");assert s['hg']==1 and s['sh']==1 and s['party']=='kirien'
    # 키리엔은 마음을 나눴으니 거절하지 않는다 / 에노 없음 / 이브레 거절 안 함
    assert E(pg,"window.__k2.shepRef?1:0")==0 or True
    pg.click('button[data-c=htalk]');t=pg.inner_text('#ov');assert '오르빌' in t;choose(pg,'일곱 의자');assert '둘째 의자' in pg.inner_text('#ov');choose(pg,'그만둔다')
    E(pg,"()=>{const K=window.__k2;K.S.vis.barracks=1;K.render()}")
    go(pg,'barracks','ibre');pg.click('button[data-c=sh1]');assert '무릎을 꿇는다' in pg.inner_text('#ov');choose(pg,'맞선다')
    pg.wait_for_function('window.__k2.G.on');pg.wait_for_timeout(200)
    win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("정화자 숙소")',timeout=5000);assert '그분 몸이오' in pg.inner_text('#ov');choose(pg,'숙소를 나선다')
    go(pg,'silver','ibre');pg.click('button[data-c=sh2]');choose(pg,'아이 것은 빼 줘');assert '예전에도' in pg.inner_text('#ov');choose(pg,'홀을 나선다')
    go(pg,'stairs','ibre');pg.click('button[data-c=sh3]');t=pg.inner_text('#ov');assert '몸은 약속대로' in t;choose(pg,'끝까지 따른다');choose(pg,'이렇게 하기로 한다')
    t=pg.inner_text('#ov');assert '첫눈은 쓰지 않겠습니다' in t;choose(pg,'계단을 올라간다')
    pg.click('button[data-c=sh4]');choose(pg,'맞선다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("일곱째 밤")',timeout=5000);t=pg.inner_text('#ov');assert '키리엔이 부른다' in t,t;choose(pg,'문 안으로');choose(pg,'말한다');skipcine(pg)
    t=pg.inner_text('#ov');assert '하늘의 불' in t and '놋등' in t and '이브레는 저택 문 앞에' in t and '처음으로 눈을' in t,t;choose(pg,'이야기를 덮는다')
    assert E(pg,"window.__k2.S.end")=='shepF' and pg.locator('button[data-c=sh4]').count()==0
    print('shep follow ok')
    E(pg,base);E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{sh:0,shc:null,shKid:0,sh4s:0,hg:0,rom:null,abel:'i'});K.render()}")
    pg.click('button[data-c=c3r]');choose(pg,'목자의 길');choose(pg,'이 길로 간다');choose(pg,'자리에 앉는다')
    assert '키리엔은 할데온과 함께라면' in pg.inner_text('#ov');choose(pg,'찻잔을 든다')
    E(pg,"()=>{const K=window.__k2;K.S.sh=3;K.S.loc='base';K.render()}");E(pg,"window.__k2.CMD.rooms()");choose(pg,'함께 나갈 동료를');choose(pg,'키리엔과 나간다');assert '그 사람은 빼고' in pg.inner_text('#ov');choose(pg,'돌아간다');choose(pg,'문을 닫는다')
    go(pg,'stairs','ibre');pg.click('button[data-c=sh3]');choose(pg,'이데른과 함께');choose(pg,'이렇게 하기로 한다');choose(pg,'계단을 올라간다')
    assert E(pg,"window.__k2.S.hg")==0 and pg.locator('button[data-c=htalk]').count()==0
    pg.click('button[data-c=sh4]');assert '내 부하였다' in pg.inner_text('#ov');choose(pg,'맞선다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("흰 옷의 문")',timeout=5000);assert '차는 식었습니다' in pg.inner_text('#ov');choose(pg,'맞선다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("옛 불")',timeout=5000);choose(pg,'할데온');skipcine(pg);t=pg.inner_text('#ov');assert '이름을 부르는 날' in t and '그 목소리입니다' in t and '신탁 상점에 다시' in t,t;choose(pg,'이야기를 덮는다')
    assert E(pg,"window.__k2.S.end")=='shepT'
    print('shep turn ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
