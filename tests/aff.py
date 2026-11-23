"""v032 호감 하락: 몸짓 한 줄, 날 선 대답, 반감이면 동행 거절, 혐오면 떠남·화해, 카시미르 결투, 바르그가 베렌을 알아보는 갈래"""
import pathlib
from playwright.sync_api import sync_playwright
src=open(pathlib.Path(__file__).resolve().parent/'bargeno.py').read().split('with sync_playwright() as p:')[0]
exec(src)
def win(pg):
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{window.__k2.G.fhp=0}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);okpop(pg)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    start(pg)
    E(pg,"()=>{const K=window.__k2;['ibre','kasimir','barg','eno'].forEach(k=>K.joinComp(k));K.grantBase()}")
    if pg.is_visible('#ov.on'):okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.S.aevT=Date.now();K.S.loc='base';K.S.party='kirien';K.render()}")
    # 날 선 대답이 자기 이야기에 있다
    c=E(pg,"window.__k2.CH.kirien[0].c.map(x=>x[0])");assert '점 같은 걸 믿고 살았어?' in c,c
    # 내려가면 몸짓 한 줄, 0 아래로
    E(pg,"window.__k2.aff('ibre',-40)");assert E(pg,"window.__k2.S.aff.ibre")<0
    # 반감이면 같이 나가지 않는다
    pg.click('button[data-c=rooms]');choose(pg,'함께 나갈 동료를 고른다');choose(pg,'이브레와 나간다');assert '따라가지 않겠습니다' in pg.inner_text('#ov');assert E(pg,"window.__k2.S.party")=='kirien'
    choose(pg,'돌아간다');choose(pg,'문을 닫는다')
    # 혐오면 떠난다 → 결투장에서 화해
    E(pg,"window.__k2.aff('ibre',-20)");pg.wait_for_selector('#ov.on h2:has-text("이브레 — 떠남")',timeout=5000);choose(pg,'붙잡지 않는다')
    assert E(pg,"window.__k2.S.left.ibre")==1;pg.click('button[data-c=rooms]');assert '이브레' not in pg.inner_text('#ov');choose(pg,'문을 닫는다')
    go(pg,'docks');pg.click('button[data-c=recon][data-a=ibre]');choose(pg,'미안하다고 한다');okpop(pg);assert E(pg,"window.__k2.S.left.ibre")==0 and E(pg,"window.__k2.S.aff.ibre")==0
    # 카시미르: 결투
    E(pg,"window.__k2.aff('kasimir',-60)");pg.wait_for_selector('#ov.on h2:has-text("명예 결투")',timeout=5000);choose(pg,'장갑을 줍는다');assert E(pg,"window.__k2.G.foe")=='kasF';win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("명예 결투")',timeout=5000);assert '이백 년 만에 졌군요' in pg.inner_text('#ov');okpop(pg);assert E(pg,"window.__k2.S.left.kasimir")==1
    # 키리엔이 떠나도 퀘스트는 이어진다
    E(pg,"()=>{const K=window.__k2;K.S.acad=1;K.S.kq=0;K.aff('kirien',-60)}");pg.wait_for_selector('#ov.on h2:has-text("키리엔 — 떠남")',timeout=5000);okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.S.loc='sanat';K.render()}");assert pg.locator('button[data-c=kq1]:not([disabled])').count()==1
    # 바르그: 갈래 넷
    def bk(aff,oath,expect,title):
        E(pg,f"()=>{{const K=window.__k2;K.S.left.barg=0;delete K.S.bk;K.S.revd=1;K.S.rev=1;K.S.aff.barg={aff};K.S.aev.barg={8 if oath else 4};K.S.loc='base';K.render()}}")
        E(pg,"window.__k2.CMD.talk('barg')");pg.wait_for_selector(f'#ov.on:has-text("{title}")',timeout=5000)
    bk(70,True,'stay','같은 사람한테 두 번');t=pg.inner_text('#ov');assert '이십 년이다' in t;choose(pg,'그 손을 잡는다');assert E(pg,"window.__k2.S.bk")=='stay'
    bk(20,False,'leave','못 베겠다');okpop(pg);assert E(pg,"window.__k2.S.bk")=='leave' and E(pg,"window.__k2.S.left.barg")==1
    bk(-15,False,'duel','칼을 들어라');choose(pg,'칼을 든다');win(pg);pg.wait_for_selector('#ov.on h2:has-text("결투 뒤")',timeout=5000);okpop(pg);assert E(pg,"window.__k2.S.bk")=='duel'
    bk(-45,False,'turn','진짜 베렌은 불 속에서');okpop(pg);assert E(pg,"window.__k2.S.bk")=='turn'
    print('errors',errs);assert not errs
    b.close()
print('ALL OK')
