"""동료 거절과 다시 영입"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def go(pg,k):pg.click(f'.map .node[data-a={k}]');choose(pg,'간다');pg.wait_for_function(f"window.__k2.S.loc==='{k}'",timeout=10000);pg.wait_for_timeout(650)
S=lambda pg:pg.evaluate('window.__k2.S')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200);pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("가르침은 건너뛴다")');pg.click('#ov.on .btn.pri')
    pg.evaluate("()=>{const K=window.__k2;K.S.night=3;K.S.tutd=1;K.S.loc='street';K.render();K.SCENE.kirien()}")
    choose(pg,'못 알아들었다고');choose(pg,'말하지 않는다');choose(pg,'혼자 하겠다');assert '초소 앞으로 와' in pg.inner_text('#ov');choose(pg,'고개를 끄덕인다')
    s=S(pg);assert s['dec']['kirien']==1 and s['comps']==[];print('kirien declined')
    pg.click('button[data-c=tab][data-a=quest]');assert '초소 앞에서 만날 수 있다' in pg.inner_text('.M');pg.click('button[data-c=tab][data-a=place]')
    # 오스윈 먼저: 키리엔 없이도 문서고에 간다
    go(pg,'church');assert '문서고 쪽이 소란스럽다' in pg.inner_text('.M');pg.click('button[data-c=archive]');choose(pg,'끼어든다')
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{const G=window.__k2.G;G.fhp=0}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);pg.click('#ov .btn.pri');pg.wait_for_selector('#ov.on h2')
    assert '말 많네' not in pg.inner_text('#ov');choose(pg,'장부에 뭐가');choose(pg,'각자 갈 길을 간다');choose(pg,'돌아선다')
    s=S(pg);assert s['dec']['oswin']==1 and s['comps']==[];assert pg.locator('button[data-c=archive]').count()==0;print('oswin declined')
    # 다시 영입: 오스윈
    pg.click('button[data-c=oswAgain]');choose(pg,'같이 가자');assert '숨어 지내는 것도 지겨웠' in pg.inner_text('#ov');choose(pg,'좋다')
    s=S(pg);assert s['comps']==['oswin'] and s['party']=='oswin' and 'oswin' not in s['dec'];print('oswin re-recruited')
    # 둘이 안 되면 저택 소문 없음
    go(pg,'docks');pg.wait_for_timeout(700);assert not pg.is_visible('#ov.on') and not S(pg).get('manor')
    pg.click('button[data-c=tab][data-a=quest]');assert '거절했던 사람을 다시 찾아가 볼까' in pg.inner_text('.M');pg.click('button[data-c=tab][data-a=place]')
    # 다시 영입: 키리엔 → 둘이 되면 여관에서 저택 소문
    go(pg,'street');pg.click('button[data-c=kirAgain]');choose(pg,'여관으로 보낸다');assert '진작 그럴 것이지' in pg.inner_text('#ov');choose(pg,'좋다')
    s=S(pg);assert s['comps']==['oswin','kirien'] and s['party']=='oswin';print('kirien re-recruited')
    go(pg,'docks');pg.wait_for_selector('#ov.on h2',timeout=5000);assert '오르빌 저택' in pg.inner_text('#ov');print('manor rumor after two ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
