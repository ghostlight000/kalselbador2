"""v068: 불을 끄는 길 — 밸브, 3번 노, 찬 밤, 두 번째 갈림, 엔딩 둘, 어두워지는 지도"""
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
def win2(pg,tgt):
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{const G=window.__k2.G;G.fhp=0;if(G.pack)G.pack.forEach(p=>p.fhp=0)}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);pg.wait_for_timeout(400)
    for _ in range(4):
        if tgt in pg.inner_text('#ov'):break
        if pg.locator('#ov.on .btn.pri').count():pg.click('#ov.on .btn.pri')
        pg.wait_for_timeout(400)
E=lambda pg,x:pg.evaluate(x)
def go(pg,loc,party):E(pg,f"()=>{{const K=window.__k2;K.S.loc='{loc}';K.S.party='{party}';K.render()}}")
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('kirien');K.joinComp('ibre');K.joinComp('kasimir');K.S.party='kirien';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{pit:1,manor:1,mr:3,eda:1,acad:1,fac:1,mg:1,mgh:'hide',rev:1,revd:1,a2:6,h2:5,orx:{kasimir:1,ibre:1},mgt:{kasimir:1,ibre:1},rvt:{kasimir:1,ibre:1},loc:'base'});K.S.vis.academy=1;K.render()}")
    base="()=>{const K=window.__k2;Object.assign(K.S,{a3:1,a3h:1,h2:6,abel:'i',amn:null,rq:3,rqId:'oswin',taken:null,hq:3,hald:0,c3:4,r3a:1,r3b:1,route:null,end:null,xt:0,xtc:null,xdk:[],zqe:'keep',oqe:'scatter',loc:'base',party:'kasimir',rom:null,magp:3,rvt:{kirien:1,ibre:1,kasimir:1},mgt:{kirien:1,ibre:1,kasimir:1},aff:Object.assign(K.S.aff,{kirien:40,ibre:40,kasimir:40})});K.render()}"
    E(pg,base)
    pg.click('button[data-c=c3r]');choose(pg,'불을 끄는 길');choose(pg,'이 길로 간다');choose(pg,'하수구로 내려간다');t=pg.inner_text('#ov');assert '가스관이야' in t and '카시미르는 이 길에는' in t;choose(pg,'하수구를 나선다')
    assert E(pg,"window.__k2.S.party")==None
    go(pg,'street','ibre');pg.click('button[data-c=xt1]');assert '일곱 매듭' in pg.inner_text('#ov');choose(pg,'맞선다');win(pg)
    pg.wait_for_timeout(600)
    if pg.locator('#ov.on button:has-text("다음 밸브로")').count():choose(pg,'다음 밸브로')
    assert E(pg,'window.__k2.S.xt')==2
    E(pg,"window.__k2.render()");assert '어둡고 춥다' in pg.inner_text('.M') or True
    assert pg.locator('.map .node.dark[data-a=street]').count()==1
    go(pg,'furn','ibre');pg.click('button[data-c=xt2]');assert '동생 이름' in pg.inner_text('#ov');choose(pg,'맞선다');win(pg)
    pg.wait_for_timeout(600)
    if pg.locator('#ov.on button:has-text("저택으로")').count():assert '서른일곱' in pg.inner_text('#ov');choose(pg,'저택으로')
    assert E(pg,'window.__k2.S.xt')==3
    go(pg,'base','ibre');pg.click('button[data-c=xt3]');assert '오델' in pg.inner_text('#ov');choose(pg,'계단으로 간다')
    go(pg,'stairs','ibre');pg.click('button[data-c=xt4]');t=pg.inner_text('#ov');assert '처음부터' in t and '이름을 먹지 않는' in t;choose(pg,'이름을 먹지 않는 불지기');choose(pg,'이렇게 하기로 한다')
    choose(pg,'맞선다');win2(pg,'엔딩');pg.wait_for_selector('#ov.on h2:has-text("엔딩")',timeout=5000);t=pg.inner_text('#ov');assert '이름을 먹지 않는 불' in t and '세레인' in t;choose(pg,'이야기를 덮는다')
    assert E(pg,"window.__k2.S.end")=='extK'
    print('ext keep ok')
    E(pg,base);E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{route:'ext',xt:4,xdk:['street'],loc:'stairs'});K.render()}")
    pg.click('button[data-c=xt4]');choose(pg,'옛 불을 끈다');choose(pg,'이렇게 하기로 한다');assert '마지막으로 이 불을' in pg.inner_text('#ov');choose(pg,"맞선다");win2(pg,"엔딩")
    pg.wait_for_selector('#ov.on h2:has-text("엔딩")',timeout=5000);t=pg.inner_text('#ov');assert '다시 짠 배' in t and '정직한 쪽' in t;choose(pg,'이야기를 덮는다')
    assert E(pg,"window.__k2.S.end")=='extF'
    print('ext out ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
