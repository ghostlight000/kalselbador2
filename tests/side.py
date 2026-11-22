"""곁가지 이야기: 돌아오지 않은 피트, 주문을 외는 노인. 새 적, 변두리 길 위 마주침"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def go(pg,k):pg.click(f'.map .node[data-a={k}]');choose(pg,'간다');pg.wait_for_function(f"window.__k2.S.loc==='{k}'",timeout=10000);pg.wait_for_timeout(650)
def win(pg):
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{window.__k2.G.fhp=0}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);t=pg.inner_text('#ov');okpop(pg);return t
E=lambda pg,x:pg.evaluate(x)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200);pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.joinComp('kirien');K.joinComp('oswin');K.S.party='oswin';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.grantPit()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.S.eda=1;K.S.loc='base';K.S.coin=50;K.render()}")
    # 먼 파견에서 피트가 돌아오지 않는다
    pg.click('button[data-c=board]');E(pg,"()=>{const K=window.__k2;K._r=Math.random;Math.random=()=>0.01}");choose(pg,'성벽 바깥 폐허')
    pg.wait_for_selector('#ov.on h2:has-text("돌아오지 않았다")',timeout=15000);E(pg,"()=>{Math.random=window.__k2._r}");okpop(pg)
    s=E(pg,"window.__k2.S");assert s['pq']==1 and s['kids']['pit']['st']=='lost'
    pg.click('button[data-c=tab][data-a=quest]');assert '돌아오지 않은 아이' in pg.inner_text('.M');pg.click('button[data-c=tab][data-a=place]')
    go(pg,'docks');pg.click('button[data-c=pqask]');t=pg.inner_text('#ov');assert '넝마 시장' in t and '가장 역겨운 문장' in t;okpop(pg)
    assert E(pg,"window.__k2.S.outs")==1
    go(pg,'street');go(pg,'outskirts');assert pg.locator('.scw svg').count()==1
    pg.click('button[data-c=pqtent]');choose(pg,'철창으로');assert E(pg,"window.__k2.G.foe")=='ashman';t=win(pg)
    pg.wait_for_selector('#ov.on h2',timeout=5000);assert '나 누구였더라' in pg.inner_text('#ov');choose(pg,'하수구에서 노래하던');t=pg.inner_text('#ov');assert '맞아. 피트' in t and '장부에 한 줄씩' in t;okpop(pg)
    s=E(pg,"window.__k2.S");assert s['pq']==3 and s['kids']['pit']['st']=='hurt';print('pit quest ok')
    # 주문을 외는 노인
    pg.click('button[data-c=hag]');assert '말은 하나도 안 잊었어' in pg.inner_text('#ov');choose(pg,'찾아 주겠다고');assert E(pg,"window.__k2.S.hq")==1
    assert pg.locator('button[data-c=hag]').count()==0
    E(pg,"()=>{const K=window.__k2;K.EXP.outskirts[0].enc=0}");pg.click('button[data-c=explore]');pg.wait_for_selector('#ov.on h2',timeout=10000);assert '하그의 주문책' in pg.inner_text('#ov');okpop(pg)
    assert E(pg,"window.__k2.S.hq")==2 and E(pg,"window.__k2.S.inv.grim")==1
    pg.click('button[data-c=hag]');t=pg.inner_text('#ov');assert '하룻밤에' in t and '기억 속으로요' in t;choose(pg,'책을 돌려준다')
    assert E(pg,"window.__k2.S.hq")==3 and not E(pg,"window.__k2.S.inv.grim");okpop(pg)
    pg.wait_for_timeout(200)
    if pg.is_visible('#ov.on'):okpop(pg)
    pg.click('button[data-c=tab][data-a=quest]');q=pg.inner_text('.M');assert q.count('◆ 끝')>=2;pg.click('button[data-c=tab][data-a=place]');print('hag quest ok')
    # 새 적
    for f,w in [('shade','바닥으로 스며든다'),('lump','엄마를 불렀다'),('mutt','이름표'),('hollow','잊으면 이걸 읽을 것')]:
        E(pg,f"()=>window.__k2.startBattle('fight','{f}')");t=win(pg);assert w in t,(f,t)
    print('new foes ok')
    # 변두리 길 위 마주침
    E(pg,"()=>{const K=window.__k2;K.ENC_ON=true;K._r=Math.random;Math.random=()=>0.01}");go(pg,'street');pg.wait_for_selector('#ov.on h2:has-text("길 위에서")',timeout=5000)
    E(pg,"()=>{Math.random=window.__k2._r;window.__k2.ENC_ON=false}");t=pg.inner_text('#ov');assert '변이한' in t or '텅 빈' in t or '한때 사람이었다' in t or '다리가 하나 더' in t;choose(pg,'돌아서 달아난다')
    print('road ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
