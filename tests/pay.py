"""v077: 갈래별 동료 퀘스트 결실"""
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
        if tgt in pg.inner_text('#ov') or pg.locator('#pv.on').count():break
        if pg.locator('#ov.on .btn.pri').count():pg.click('#ov.on .btn.pri')
        pg.wait_for_timeout(400)
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
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('kirien');K.joinComp('ibre');K.joinComp('kasimir');K.S.party='kirien';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{pit:1,manor:1,mr:3,eda:1,acad:1,fac:1,mg:1,mgh:'hide',rev:1,revd:1,a2:6,h2:5,orx:{kasimir:1,ibre:1},mgt:{kasimir:1,ibre:1},rvt:{kasimir:1,ibre:1},loc:'base'});K.S.vis.academy=1;K.render()}")
    base="()=>{const K=window.__k2;Object.assign(K.S,{a3:1,a3h:1,h2:6,abel:'i',amn:null,rq:3,rqId:'oswin',taken:null,hq:3,hald:0,c3:4,r3a:1,r3b:1,route:null,end:null,xt:0,xtc:null,xdk:[],zqe:'keep',oqe:'scatter',loc:'base',party:'kasimir',rom:null,magp:3,rvt:{kirien:1,ibre:1,kasimir:1},mgt:{kirien:1,ibre:1,kasimir:1},aff:Object.assign(K.S.aff,{kirien:40,ibre:40,kasimir:40})});K.render()}"
    E(pg,base);E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{route:'ext',xt:1,xtK:1,kqe:'new',iqe:'ledger',zqe:'name',kq:6,iq:6,zq:5,cq:Object.assign(K.S.cq||{},{kirien:'done',ibre:'done',kasimir:'done'}),pay:{},aev:{kirien:9,ibre:9,kasimir:9,oswin:9,barg:9,eno:9},romNo:{kirien:1,kasimir:1}});K.render()}")
    assert E(pg,"window.__k2.payDue('ibre')") and E(pg,"window.__k2.payDue('kirien')") and not E(pg,"window.__k2.payDue('oswin')")
    E(pg,"window.__k2.CMD.talk('ibre')");pg.wait_for_timeout(200);listen(pg);t=pg.inner_text('#ov');assert '결투장 장부에 이름을 쓴' in t and '헌병보다 덩치가' in t,t[-400:];choose(pg,'고마워');choose(pg,'곁에 있는다')
    E(pg,"window.__k2.CMD.talk('kirien')");pg.wait_for_timeout(200);listen(pg);t=pg.inner_text('#ov');assert '계단은 안 가르쳤는데' in t,t[-300:];choose(pg,'고마워');choose(pg,'곁에 있는다')
    assert not E(pg,"window.__k2.payDue('ibre')")
    # 마지막 싸움: 거든 동료 둘 → 체력 −10%, 한 줄씩
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{xt:5,xtc:'out',c3:4});K.startBattle('fight','haldF')}");pg.wait_for_timeout(300)
    t=pg.inner_text('#bov');assert '결투장 사람들이 헌병대 길목을' in t and '지도에 없던 밸브' in t,t
    hp=E(pg,"[window.__k2.G.fmax]")[0]
    E(pg,"()=>{const K=window.__k2;K.G.on=false;K.S.pay={};K.startBattle('fight','haldF')}");pg.wait_for_timeout(300)
    hp0=E(pg,"window.__k2.G.fmax");assert abs(hp-hp0*0.9)<=2,(hp,hp0)
    print(errs);assert not errs;print('ALL OK')
    b.close()
