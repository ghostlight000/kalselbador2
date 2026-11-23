"""동료 전투 참여·기술 갈래, 대화 중 고르는 말(>)"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
E=lambda pg,x:pg.evaluate(x)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200);pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    # 배우지 않은 기술이 흐리게 보인다
    pg.click('button[data-c=tab][data-a=char]');t=pg.inner_text('.M');assert '혼불' not in t and '하나씩 배운다' in t
    pg.click('button[data-c=tab][data-a=place]')
    E(pg,"()=>{const K=window.__k2;K.joinComp('kirien');K.S.loc='docks';K.render()}")
    # 대화: > 줄은 내가 고른다
    pg.evaluate("()=>{window.__k2.S.orx={kirien:1,oswin:1,ibre:1,kasimir:1}}");pg.click('button[data-c=talk]');choose(pg,'이곳은 어때?');t=pg.inner_text('#ov');assert '비린내' in t and '그럼 왜 따라왔어?' in t and '말없이 듣는다' in t
    choose(pg,'그럼 왜 따라왔어?');t=pg.inner_text('#ov');assert '베렌\n“그럼 왜 따라왔어?”' in t and '방향이 같았을 뿐' in t
    choose(pg,'다른 이야기를 한다');choose(pg,'이곳은 어때?');choose(pg,'말없이 듣는다');t=pg.inner_text('#ov');assert '베렌 —' not in t and '방향이 같았을 뿐' in t;choose(pg,'이야기를 그만둔다')
    assert E(pg,"window.__k2.S.aff.kirien")==14;print('talk choice ok')
    # 키리엔 기술 점수: 연속 베기 1단계
    pg.click('button[data-c=tab][data-a=char]');pg.click('button[data-c=cskup][data-a="kirien:flurry"]');assert E(pg,"window.__k2.S.cl.kirien.r.flurry")==1 and E(pg,"window.__k2.S.cl.kirien.cp")==0
    assert pg.locator('button[data-c=cskup]').count()==0 and pg.locator('.ccard').count()>=1 and '여 ·' not in pg.inner_text('.M');pg.click('button[data-c=tab][data-a=place]')
    # 전투: 내 공격 뒤 키리엔이 두 번 벤다(3+1)*2=8
    E(pg,"()=>{window.__k2.startBattle('fight','thief')}");pg.click('#bov .btn.pri');assert pg.is_visible('#bcomp') and '키리엔' in pg.inner_text('#bcompn')
    h0=E(pg,"window.__k2.G.fhp");E(pg,"window.__k2.bact('atk')");pg.wait_for_function("window.__k2.G.st==='enemy'",timeout=5000)
    h1=E(pg,"window.__k2.G.fhp");atk=E(pg,"5+window.__k2.S.st[0]");assert h0-h1==atk+8,(h0,h1,atk);assert '두 번' not in pg.inner_text('#blog') and '2번 벤다' in pg.inner_text('#blog')
    print('companion attacks ok')
    # 공격 끊기: 확률을 억지로 맞춘다
    pg.wait_for_function("window.__k2.G.st==='player'",timeout=10000)
    E(pg,"()=>{const K=window.__k2;K.S.cl.kirien.r.cut=3;K._r=Math.random;K.G.cut=1}")
    E(pg,"window.__k2.bact('guard')");pg.wait_for_function("document.querySelector('#blog').innerText.includes('끼어들어 끊었다')",timeout=5000);E(pg,"()=>{Math.random=window.__k2._r}")
    pg.wait_for_function("window.__k2.G.st==='player'",timeout=5000);print('cut ok')
    # 약점 짚기: 다음 내 공격 +15%
    E(pg,"()=>{const K=window.__k2;K.G.mark=1}");h0=E(pg,"window.__k2.G.fhp");E(pg,"window.__k2.bact('atk')");pg.wait_for_timeout(50);h1=E(pg,"window.__k2.G.fhp")
    assert h0-h1==round(atk*1.15) if False else h0-h1==int(atk*1.15+.5),(h0,h1);print('mark ok')
    # 승리: 동료도 경험
    E(pg,"()=>{const K=window.__k2;K.G.fhp=0}");pg.wait_for_function('!window.__k2.G.on',timeout=8000)
    assert E(pg,"window.__k2.S.cl.kirien.xp")==10;pg.click('#ov .btn.pri')
    # 오스윈: 응급 처치·정전기 막
    E(pg,"()=>{const K=window.__k2;K.joinComp('oswin');K.S.party='oswin';K.S.cl.oswin.r={mend:2,ward:3};K.render();K.startBattle('fight','dog')}");pg.click('#bov .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.G.hp=10;K._r=Math.random;Math.random=()=>0.01}");E(pg,"window.__k2.bact('guard')");pg.wait_for_timeout(300)
    assert E(pg,"window.__k2.G.hp")==26 and E(pg,"window.__k2.G.ward")==1;E(pg,"()=>{Math.random=window.__k2._r}");print('oswin ok')
    pg.click('button[data-c=tab][data-a=char]') if False else None
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
