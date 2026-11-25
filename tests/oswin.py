"""v023: 실마리 카드, 임무 탭 막·접기, 오스윈 퀘스트 「지워진 쪽」 → 공장 지대 → 금서고 반전 → 언덕길 → 장부의 끝"""
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
        else:break
E=lambda pg,x:pg.evaluate(x)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    # 실마리 카드: 출처가 붙는다
    t=pg.inner_text('.goalc');assert '모르텐의 말' in t and '“이제 가스등 거리로 가세' in t and '→ 가스등 거리' in t,t
    # 임무 탭: 막 제목, 접기
    pg.click('button[data-c=tab][data-a=quest]');t=pg.inner_text('.M');assert '1막 · 꺼지지 않는 등불' in t and '메인 이야기' not in t
    n0=pg.locator('.M .ms').count();pg.click('.M h2.fold[data-a=a1]');n1=pg.locator('.M .ms').count();assert n1==1 and n0>5,(n0,n1)
    assert '가스등 거리를 순찰한다' in pg.inner_text('.M');pg.click('.M h2.fold[data-a=a1]');assert pg.locator('.M .ms').count()==n0
    pg.click('button[data-c=tab][data-a=place]');print('lead/quest tab ok')
    # 2막: 깨어난 뒤
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('kirien');K.joinComp('oswin');K.S.party='oswin';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.S.pit=1;K.S.manor=1;K.S.mr=3;K.S.ring=1;K.S.dec.ibre=1;K.S.dec.kasimir=1;K.S.dec.barg=1;K.S.dec.eno=1;K.S.eda=1;K.S.acad=1;K.S.vis.academy=1;K.S.mg=1;K.S.mgh='hide';K.S.orx={oswin:1,kirien:1};K.S.loc='docks';K.render()}")
    pg.click('button[data-c=tab][data-a=quest]');t=pg.inner_text('.M');assert '2막 · 장부와 재' in t and '지나온 길' in t;assert t.index('2막')<t.index('1막');pg.click('button[data-c=tab][data-a=place]')
    go(pg,'street');pg.wait_for_selector('#ov.on h2:has-text("오스윈")',timeout=5000);assert '보존실' in pg.inner_text('#ov');choose(pg,'같이 가자')
    t=pg.inner_text('.goalc');assert '공급 검사실' in t and '보존실' not in t,t;pg.click('button[data-c=tab][data-a=quest]');t=pg.inner_text('.M');assert '동료들의 이야기' in t and '보존실의 약' in t,t;pg.click('button[data-c=tab][data-a=place]')
    go(pg,'pres');pg.click('button[data-c=oq1]');choose(pg,'들어간다');assert E(pg,"window.__k2.G.foe")=='clock';win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("보존실")',timeout=5000);choose(pg,'그 상자는 뭐야?');okpop(pg);assert E(pg,"window.__k2.S.oq")==2
    # 오스윈 없이 가면 못 들어간다는 표시
    go(pg,'street');go(pg,'docks');go(pg,'base');pg.click('button[data-c=oq2]');choose(pg,'배정지가 어디야?');assert '하칸골 3번 방직소' in pg.inner_text('#ov');choose(pg,'같이 가자');assert '공장 지대로 가는 길이 열렸다' in pg.inner_text('#ov');okpop(pg)
    assert E(pg,"window.__k2.S.fac")==1 and E(pg,"window.__k2.S.oq")==3
    E(pg,"()=>{const K=window.__k2;K.S.party='kirien';K.render()}");go(pg,'docks');go(pg,'mill')
    assert pg.get_attribute('button[data-c=oq3]','disabled') is not None and '오스윈과 함께' in pg.inner_text('button[data-c=oq3]')
    pg.click('button[data-c=tab][data-a=quest]');assert '오스윈과 함께 다녀야' in pg.inner_text('.M');pg.click('button[data-c=tab][data-a=place]')
    go(pg,'works');pg.click('button[data-c=hboard]');assert '징수 명단' in pg.inner_text('#ov');okpop(pg)
    pg.click('button[data-c=talk]');assert '쇳물 냄새' in pg.inner_text('#ov') or '고개를 안 들어' in pg.inner_text('#ov') or pg.is_visible('#ov.on');pg.keyboard.press('Escape')
    E(pg,"()=>{const K=window.__k2;K.S.party='oswin';K.render()}")
    if pg.is_visible('#ov.on'):pg.click('#ov.on button >> nth=-1')
    go(pg,'mill');pg.click('button[data-c=oq3]');choose(pg,'그 노래 어디서');choose(pg,'오빠라고 말해 준다');t=pg.inner_text('#ov');assert '오빠가 있었으면' in t and '금서고' in t;okpop(pg)
    assert E(pg,"window.__k2.S.oq")==4;print('factory/liese ok')
    # 금서고 반전
    E(pg,"()=>{window.__k2.S.a2=6}");go(pg,'docks');go(pg,'street');go(pg,'vault');pg.click('button[data-c=oq4]');choose(pg,'들어간다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("금서고")',timeout=5000);assert '푸른 재 정제 공정' in pg.inner_text('#ov');choose(pg,'서명을 본다')
    t=pg.inner_text('#ov');nm=E(pg,"window.__k2.S.name");assert nm in t and '편지와 같' in t;choose(pg,'리세를 그렇게 만든 게 나였어?');drain(pg);choose(pg,'금서고를 나선다')
    s=E(pg,"window.__k2.S");assert s['rev']==1 and s['oq']==5 and E(pg,"window.__k2.actN()")==2.5
    t=pg.inner_text('#ov');assert '그 이름' in t;choose(pg,'물러난다');assert pg.locator('button[data-c=revOut]').count()==1
    pg.click('button[data-c=revOut]');choose(pg,'맞선다');assert E(pg,"window.__k2.G.foe")=='purL';win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("언덕길")',timeout=5000);assert '백 년 전부터' in pg.inner_text('#ov');okpop(pg)
    s=E(pg,"window.__k2.S");assert s['revd']==1 and s['hunt']==1
    r=E(pg,"()=>{const K=window.__k2;K.ENC_ON=true;const o=Math.random;Math.random=()=>0.1;const f=K.roadFoe({fr:'docks',to:'street'});Math.random=o;K.ENC_ON=false;return f}");assert r=='hunter',r
    print('reveal ok')
    # 장부의 끝
    go(pg,'street');go(pg,'docks');go(pg,'base');pg.click('button[data-c=tab][data-a=quest]');assert '장부의 끝' in pg.inner_text('.M');pg.click('button[data-c=tab][data-a=place]')
    pg.click('button[data-c=oq5]');choose(pg,'태운다');assert '되돌릴 수 없다' in pg.inner_text('#ov');choose(pg,'다시 생각한다');choose(pg,'이름 하나하나를');choose(pg,'이렇게 하기로');assert '평생 걸리겠군요' in pg.inner_text('#ov');okpop(pg)
    s=E(pg,"window.__k2.S");assert s['oq']==6 and s['oqe']=='return' and s['cq']['oswin']=='done'
    pg.click('button[data-c=tab][data-a=quest]');t=pg.inner_text('.M');assert '장부의 끝' in t and '돌려주고 있다' in t
    pg.click('.M h2.fold[data-a=cq]');assert '장부의 끝' not in pg.inner_text('.M');print('ledger end ok')
    b.close()
assert not errs,errs
print('ALL OK')
