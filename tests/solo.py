"""v043: 동료 퀘스트 없이도 메인이 이어진다 — 에다(바르그·에노 안 만남), 공급 검사실(오스윈 퀘스트 없이), 혼자 여는 금서고, 나중에 오스윈에게 설계서 보여 주기"""
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
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    # 에다: 바르그·에노를 만나지 않아도
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('kirien');K.joinComp('oswin');K.S.party='kirien';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.S.pit=1;K.S.manor=1;K.S.mr=3;K.S.ring=1;K.S.dec.ibre=1;K.S.dec.kasimir=1;K.S.loc='docks';K.render()}")
    assert not E(pg,"window.__k2.met(window.__k2.S,'barg')")
    go(pg,'street');assert pg.locator('button[data-c=eda]').count()==1
    t=pg.inner_text('.goalc');assert '물길' not in t and '늑대' not in t,t
    pg.click('button[data-c=tab][data-a=quest]');t=pg.inner_text('.M');assert '아직 만나지 못한 사람' in t and '회색 마차의 늑대' in t,t;pg.click('button[data-c=tab][data-a=place]')
    print('eda ok')
    # 2막: 오스윈 퀘스트 없이 공급 검사실
    E(pg,"()=>{const K=window.__k2;K.S.eda=1;K.S.acad=1;K.S.vis.academy=1;K.S.vis.dome=1;K.S.mg=1;K.S.mgh='hide';K.S.orx={oswin:1,kirien:1};K.S.oq0=1;K.render()}")
    t=pg.inner_text('.goalc');assert '공급 검사실' in t and '회색 마차' in t,t
    go(pg,'docks');go(pg,'works');go(pg,'insp');assert pg.locator('button[data-c=a2a]').count()==1
    print('a2 start ok')
    # 혼자 여는 금서고
    E(pg,"()=>{window.__k2.S.a2=6;window.__k2.render()}");t=pg.inner_text('.goalc');assert '금서고' in t and '운반 일지' in t,t
    go(pg,'works');go(pg,'docks');go(pg,'street');go(pg,'vault');assert pg.locator('button[data-c=oq4]').count()==0;pg.click('button[data-c=vaultS]');choose(pg,'들어간다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("금서고")',timeout=5000);choose(pg,'서명을 본다');t=pg.inner_text('#ov');assert '편지와 같다' in t;choose(pg,'품에 넣는다');choose(pg,'금서고를 나선다')
    s=E(pg,"window.__k2.S");assert s['rev']==1 and s.get('vrev')==1;choose(pg,'맞선다');win(pg);pg.wait_for_selector('#ov.on h2:has-text("언덕길")',timeout=5000);okpop(pg)
    assert E(pg,"window.__k2.S.revd")==1;print('solo vault ok')
    # 오스윈 퀘스트를 나중에: 설계서를 보여 준다
    E(pg,"()=>{const K=window.__k2;K.S.oq=4;K.S.loc='base';K.render()}");pg.click('button[data-c=oq4s]');choose(pg,'서명을 가리킨다');choose(pg,'나는 기억이 없다');drain(pg);choose(pg,'설계서를 덮는다')
    s=E(pg,"window.__k2.S");assert s['oq']==5;pg.wait_for_timeout(300);assert not pg.is_visible('#ov.on h2:has-text("언덕길")')
    print('late oswin ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
