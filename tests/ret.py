"""v067: 돌아오는 이의 길 — 기억 태우기, 막아서는 바르그, 두 번째 갈림, 엔딩 둘"""
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
E=lambda pg,x:pg.evaluate(x)
def go(pg,loc,party):E(pg,f"()=>{{const K=window.__k2;K.S.loc='{loc}';K.S.party='{party}';K.render()}}")
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('kirien');K.joinComp('ibre');K.joinComp('barg');K.joinComp('oswin');K.S.party='kirien';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{pit:1,manor:1,mr:3,eda:1,acad:1,fac:1,mg:1,mgh:'hide',rev:1,revd:1,a2:6,h2:5,orx:{kasimir:1,ibre:1},mgt:{kasimir:1,ibre:1},rvt:{kasimir:1,ibre:1},loc:'base'});K.S.vis.academy=1;K.render()}")
    base="()=>{const K=window.__k2;Object.assign(K.S,{a3:1,a3h:1,h2:6,abel:'i',amn:null,rq:3,rqId:'oswin',taken:null,hq:3,hald:0,c3:4,r3a:1,r3b:1,route:null,end:null,rt:0,rtc:null,rburn:[],bqe:'new',loc:'base',party:'kirien',rom:null,magp:3,rvt:{kirien:1,ibre:1,barg:1,oswin:1},mgt:{kirien:1,ibre:1,barg:1,oswin:1},aff:Object.assign(K.S.aff,{kirien:40,ibre:40,barg:40,oswin:40})});K.render()}"
    E(pg,base)
    pg.click('button[data-c=c3r]');choose(pg,'돌아오는 이의 길');choose(pg,'이 길로 간다');choose(pg,'대검 옆을');t=pg.inner_text('#ov');assert '빈 이마' in t and '오스윈은 이 길에는' in t and '바르그는 이 길에는' in t,t;choose(pg,'예배실로 간다')
    E(pg,"()=>{const K=window.__k2;K.S.vis.chapel=1;K.render()}")
    go(pg,'chapel','kirien');pg.click('button[data-c=rt1]');choose(pg,'기억 하나를 고른다');a0=E(pg,"window.__k2.S.aff.ibre");choose(pg,'햇볕 받은 돌');choose(pg,'고개를 든다')
    assert E(pg,"window.__k2.S.rburn")==['ibre'] and E(pg,"window.__k2.S.aff.ibre")==a0-6
    choose(pg,'맞선다');win(pg);pg.wait_for_selector('#ov.on h2:has-text("지하 예배실")',timeout=5000);assert '산 채로' in pg.inner_text('#ov');choose(pg,'예배실을 나선다')
    go(pg,'outskirts','kirien');pg.click('button[data-c=rt2]');choose(pg,'노래를 끊지 않는다');assert '칼을 들어라' in pg.inner_text('#ov');choose(pg,'맞선다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("천막촌")',timeout=5000);assert '내 눈으로 본다' in pg.inner_text('#ov');choose(pg,'계단으로 간다')
    go(pg,'stairs','kirien');pg.click('button[data-c=rt3]');t=pg.inner_text('#ov');assert '할데온의 웃음' in t and '키리엔' in t and '이브레' not in t.split('부른다')[1][:40],t;choose(pg,'지금의 이름으로 선다');choose(pg,'이렇게 하기로 한다')
    choose(pg,'맞선다');win(pg);pg.wait_for_selector('#ov.on h2:has-text("엔딩")',timeout=5000);t=pg.inner_text('#ov');assert '지금의 이름' in t and '이브레와 보낸 밤' in t and '내 이름이다' in t,t;choose(pg,'이야기를 덮는다')
    assert E(pg,"window.__k2.S.end")=='retS'
    print('ret stand ok')
    E(pg,base);E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{route:'ret',rt:3,bqe:'bound',loc:'stairs',aff:Object.assign(K.S.aff,{kirien:10,ibre:10,barg:10,oswin:10})});K.render()}")
    pg.click('button[data-c=rt3]');t=pg.inner_text('#ov');assert '남아 있지 않다' in t and pg.locator('#ov.on button:has-text("지금의 이름으로")').count()==0
    choose(pg,'몸을 넘긴다');choose(pg,'이렇게 하기로 한다');choose(pg,'불 안으로');t=pg.inner_text('#ov');assert '「베렌」' in t and '바르그만은' in t;choose(pg,'이야기를 덮는다')
    assert E(pg,"window.__k2.S.end")=='retG'
    print('ret give ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
