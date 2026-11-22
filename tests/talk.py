"""v018: 처음 가르침은 꼭, 박자 연습 없음, 지금 할 일, 모르텐 질문이 깊어짐, 동료 질문 묶음, 출신·종족 반응"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def go(pg,k):pg.click(f'.map .node[data-a={k}]');choose(pg,'간다');pg.wait_for_function(f"window.__k2.S.loc==='{k}'",timeout=10000);pg.wait_for_timeout(650)
E=lambda pg,x:pg.evaluate(x)
def btns(pg):return [b.inner_text().split('\n')[0] for b in pg.locator('#ov.on button').all()]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=origin][data-a="4"]');pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]')
    assert btns(pg)==['막대를 쥔 노인을 따라간다'];choose(pg,'막대를 쥔 노인을 따라간다');assert '박자부터' in pg.inner_text('#ov');choose(pg,'막대 앞에 선다')
    pg.wait_for_function('window.__k2.G.on');assert not pg.is_visible('#bstop')
    E(pg,"window.__k2.endBattle('tut')");t=pg.inner_text('#ov');assert '가스등 거리로 가세' in t;okpop(pg)
    # 지금 할 일 + 지도 표식
    t=pg.inner_text('.goalc');assert '가스등 거리를 순찰한다' in t and '가스등 거리로' in t,t
    assert pg.locator('.map .node.goal[data-a=street]').count()==1
    go(pg,'street');assert pg.locator('button[data-c=practice]').count()==0
    assert 'goal' in pg.get_attribute('button[data-c=patrol]','class') and '지도에서' not in pg.inner_text('.goalc')
    print('tutorial/goal ok')
    # 모르텐: 처음엔 셋, 물을수록 깊어진다
    pg.click('button[data-c=mtalk]');q=btns(pg);assert q[:3]==['거리 끝의 그건 누구야?','왜 아직 경비를 서?','이 도시는 어떤 곳이야?'] and len(q)==4,q
    choose(pg,'이 도시는 어떤 곳이야?');choose(pg,'다른 이야기를 한다');q=btns(pg);assert '푸른 재가 뭐야?' in q and len(q)==4,q
    for _ in range(12):
        q=[x for x in btns(pg) if x!='이야기를 그만둔다']
        if not q or '들었던 이야기' in pg.inner_text('#ov'):break
        choose(pg,q[0])
        if pg.locator('#ov.on button:has-text("말없이 듣는다")').count():choose(pg,'말없이 듣는다')
        choose(pg,'다른 이야기를 한다')
    assert '들었던 이야기를 다시' in pg.inner_text('#ov') and len(E(pg,"Object.keys(window.__k2.S.masked)"))==12;choose(pg,'이야기를 그만둔다')
    print('morten q ok')
    # 동료: 출신 반응(재의 정화자) → 질문 묶음
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('oswin');K.S.party='oswin';K.render()}")
    pg.click('button[data-c=talk]');t=pg.inner_text('#ov');assert '제 이름도 그렇게 지워졌습니다' in t;choose(pg,'다른 이야기를 한다')
    q=btns(pg);assert len(q)<=5 and '물어보고 싶은 게 있어' in q,q
    choose(pg,'물어보고 싶은 게 있어');q=[x for x in btns(pg) if x!='다른 이야기를 한다'];assert 2<=len(q)<=3,q
    first=q[0];choose(pg,first)
    if pg.locator('#ov.on button:has-text("말없이 듣는다")').count():choose(pg,'말없이 듣는다')
    choose(pg,'다른 것도 묻는다');q=[x for x in btns(pg) if x!='다른 이야기를 한다'];assert first not in q and len(q)>=1,q
    E(pg,"()=>{window.__k2.S.aff.oswin=25}");choose(pg,'다른 이야기를 한다');choose(pg,'물어보고 싶은 게 있어');q=btns(pg);assert '내가 어떻게 보여?' in q,q
    choose(pg,'내가 어떻게 보여?');t=pg.inner_text('#ov');race=E(pg,"window.__k2.S.race");assert {'p':'같은 파볼릭','i':'잉그라드시군요','b':'벨데인이시군요'}[race] in t,t
    print('companion q ok')
    b.close()
assert not errs,errs
print('ALL OK')
