"""v046: 2막 후반 「쫓기는 이름」 — 수배서·여관 추격, 설계서, 대연소로(노 지기), 아벨, 형제단(울릭), 일곱째 문·배신·대성당 추격, 아벨 후일"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def go(pg,k):pg.eval_on_selector(f'.map .node[data-a={k}]',"e=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}))");choose(pg,'간다');pg.wait_for_function(f"window.__k2.S.loc==='{k}'",timeout=10000);pg.wait_for_timeout(650);(pg.is_visible('#ov.on h2:has-text("대성당")') and (choose(pg,'고개를 숙인다'),choose(pg,'대성당을 나선다')));(pg.is_visible('#ov.on h2:has-text("문 앞의 상자")') and (choose(pg,'서랍 깊이'),choose(pg,'서랍을 닫는다')))
def win(pg):
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{window.__k2.G.fhp=0}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);okpop(pg)
def drain(pg):
    for _ in range(8):
        if pg.locator('#ov.on button:has-text("말없이 듣는다")').count():choose(pg,'말없이 듣는다')
E=lambda pg,x:pg.evaluate(x)
def good(pg):
    return E(pg,"(()=>{const N=CHASES[CHS.id].nodes[CHS.i];return N.o.findIndex(o=>o[2]>0)})()")
def runchase(pg,ok=True):
    while E(pg,"!!CHS"):
        if E(pg,"!!CHASES[CHS.id].nodes[CHS.i].q"):
            E(pg,"(()=>{const t=CHS.tok;EV0=null;CHS.q0=Date.now()-1200;chQ(t)})()" if ok else "(()=>{const t=CHS.tok;EV0=null;chQ(t,1)})()")
        else:
            i=good(pg) if ok else (1-good(pg) if len(E(pg,"CHASES[CHS.id].nodes[CHS.i].o"))==2 else (0 if good(pg)!=0 else 1))
            E(pg,"(()=>{const t=CHS.tok;EV0=null;chPick(t,IDX)})()".replace('IDX',str(i)))
        if E(pg,"!!CHS"):choose(pg,'계속 달린다')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('kirien');K.joinComp('oswin');K.joinComp('barg');K.S.party='kirien';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{pit:1,manor:1,mr:3,ring:1,eda:1,acad:1,mg:1,a2:6,rev:1,revd:1,hunt:1,h2:0,gift:'k'});K.S.inv.gvial=1;K.S.dec.ibre=1;K.S.dec.kasimir=1;K.S.vis.academy=1;K.S.vis.works=1;K.S.loc='inn';K.render()}")
    t=pg.inner_text('.goalc');assert '얼굴 없는 수배서' in t,t
    pg.click('button[data-c=h2wanted]');t=pg.inner_text('#ov');assert '촛불이 기우는 자' in t;choose(pg,'2층 끝방');choose(pg,'뒷계단')
    assert E(pg,"document.querySelector('#ov').classList.contains('ta')") and E(pg,"CHS.id")=='inn'
    runchase(pg,True);pg.wait_for_selector('#ov.on h2:has-text("오르빌 저택")');okpop(pg)
    s=E(pg,"window.__k2.S");assert s['h2']==1 and s['loc']=='base';print('wanted ok')
    pg.click('button[data-c=h2plan]');assert '죽은 이의 것만' in pg.inner_text('#ov');choose(pg,'3번 노를 찾아간다');assert E(pg,"window.__k2.S.h2")==2
    E(pg,"()=>{window.__k2.S.loc='furn';window.__k2.render()}");pg.click('button[data-c=h2furn]');choose(pg,'막아선다');assert E(pg,"G.foe")=='pourer' and E(pg,"G.fmax")==round(180*1.45);win(pg)
    choose(pg,'맞선다');assert E(pg,"G.foe")=='keeper';win(pg);pg.wait_for_selector('#ov.on h2:has-text("시험 연소 기록")',timeout=5000);t=pg.inner_text('#ov');assert '할데온' in t and '흉내' in t;okpop(pg);assert E(pg,"window.__k2.S.h2")==3;print('furnace ok')
    E(pg,"()=>{window.__k2.S.loc='church';window.__k2.render()}");pg.click('button[data-c=h2abel]');t=pg.inner_text('#ov');assert '거짓말' in t;choose(pg,'어머니는');assert '목소리를 바쳤어' in pg.inner_text('#ov');okpop(pg)
    s=E(pg,"window.__k2.S");assert s['h2']==4 and s['abelN']==1
    E(pg,"()=>{const S=window.__k2.S;S.party='barg';S.loc='outskirts';window.__k2.render()}");pg.click('button[data-c=h2broth]');t=pg.inner_text('#ov');assert '울릭' in t and '…울릭.' in t and '바르그' in t;choose(pg,'맞선다');assert E(pg,"G.foe")=='ulrik';win(pg);pg.wait_for_selector('#ov.on h2:has-text("천막촌 끝")',timeout=5000);assert '겨울 아침' in pg.inner_text('#ov');okpop(pg)
    assert E(pg,"window.__k2.S.h2")==5;print('abel/brotherhood ok')
    E(pg,"()=>{const S=window.__k2.S;S.party='kirien';S.loc='stairs';window.__k2.render()}");pg.click('button[data-c=h2door]');t=pg.inner_text('#ov');assert '당신 목소리에만' in t and '유리병' in t;choose(pg,'유리병을 마신다');assert '일곱 개의 손' in pg.inner_text('#ov');okpop(pg)
    t=pg.inner_text('#ov');assert '여관도 내가 알려 줬어' in t and '냄새가 달랐어' in t;choose(pg,'계단 아래 어둠')
    runchase(pg,False);choose(pg,'맞선다');assert E(pg,"G.foe")=='squad';win(pg);pg.wait_for_selector('#ov.on h2:has-text("운하")',timeout=5000);t=pg.inner_text('#ov');assert '분대를 쓰러뜨리고' in t;choose(pg,'저택으로');okpop(pg)
    s=E(pg,"window.__k2.S");assert s['h2']==6 and s['a3']==1 and s.get('gvU')==1 and not s['inv'].get('gvial');print('door ok')
    t=pg.inner_text('.goalc');assert '3막' in t,t
    E(pg,"()=>{window.__k2.S.loc='church';window.__k2.render()}");pg.click('button[data-c=h2abelA]');choose(pg,'용서한다');okpop(pg);assert E(pg,"window.__k2.S.abel")=='f'
    print('abel after ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
