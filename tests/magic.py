"""주문 깨어남: 처음엔 주문을 못 쓴다 → 깨진 돔의 강의실 → 떠오르는 말 → 목격 장면, 브리타·하그·피트, 추적자, 옛 저장 이전"""
import pathlib,json
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def go(pg,k):pg.eval_on_selector(f'.map .node[data-a={k}]',"e=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}))");choose(pg,'간다');pg.wait_for_function(f"window.__k2.S.loc==='{k}'",timeout=10000);pg.wait_for_timeout(650)
E=lambda pg,x:pg.evaluate(x)
def newgame(pg,origin=2):
    pg.goto(url);pg.wait_for_timeout(200);E(pg,"localStorage.clear()");pg.goto(url);pg.wait_for_timeout(200)
    pg.click(f'button[data-c=origin][data-a="{origin}"]');pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    # 영매사로 시작해도 혼불이 없다
    newgame(pg,2)
    s=E(pg,"window.__k2.S");assert s['sk']==['mend'] and not s.get('mg'),s['sk']
    E(pg,"()=>{const K=window.__k2;K.gainXp(400);K.render()}")
    pg.click('button[data-c=tab][data-a=char]');t=pg.inner_text('.M');assert '혼불' not in t and '방전' not in t and '바람막이' not in t;pg.click('button[data-c=tab][data-a=place]')
    assert E(pg,"window.__k2.S.skp")>=3
    # 1막 끝 상태로
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.joinComp('kirien');K.joinComp('oswin');K.S.party='oswin';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.grantPit()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.S.eda=1;K.S.acad=1;K.S.mr=3;K.S.loc='street';K.S.hp=K.S.mhp;K.render()}")
    go(pg,'dome');assert pg.locator('button[data-c=aw1]').count()==1
    assert '깨진 돔의 강의실' in pg.inner_text('.M')
    # 강의실 → 싸움 → 격노에서 떠오르는 말
    pg.click('button[data-c=aw1]');t=pg.inner_text('#ov');assert '분필로 그린 원' in t and '학술원 심부름꾼' in t;choose(pg,'막아선다')
    pg.wait_for_function('window.__k2.G.on');assert E(pg,"window.__k2.G.foe")=='awc';pg.click('#bov .btn.pri')
    pg.wait_for_function("window.__k2.G.st==='player'",timeout=10000)
    E(pg,"()=>{const K=window.__k2;K.G.fhp=Math.floor(K.FOES.awc.hp/2)}");E(pg,"window.__k2.bact('atk')")
    pg.wait_for_selector('.phase',timeout=5000);assert '목 안쪽이 뜨겁다' in pg.inner_text('.phase')
    assert E(pg,"window.__k2.G.awk")==1
    pg.wait_for_function("window.__k2.G.st==='player'||!window.__k2.G.on",timeout=30000)
    if E(pg,"window.__k2.G.st")!='player':
        pg.wait_for_function("window.__k2.G.st==='player'",timeout=30000)
    pg.wait_for_selector('#bacts [data-ba=aw]',timeout=5000)
    E(pg,"()=>{const K=window.__k2;K.G.fhp=10}");pg.click('#bacts [data-ba=aw]')
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);okpop(pg)
    pg.wait_for_selector('#ov.on h2:has-text("처음 듣는 말")',timeout=5000);t=pg.inner_text('#ov');assert '가스등' in t and '정전기가 아닙니다' in t
    choose(pg,'손을 편다');t=pg.inner_text('#ov');assert '솔레' in t;choose(pg,'그래. 주문이다');t=pg.inner_text('#ov');assert '새 주문 — 방전' in t and '교단이 알 겁니다' in t;okpop(pg)
    s=E(pg,"window.__k2.S");assert s['mg']==1 and 'shock' in s['sk'] and s['mgh']=='open' and s['mgs'].get('oswin')
    assert pg.locator('button[data-c=aw1]').count()==0
    # 레벨 기술 고르기에 혼불이 나오고 받은 주문은 나오지 않는다
    pg.click('button[data-c=tab][data-a=char]');t=pg.inner_text('.M');assert '혼불' in t and '바람막이' not in t and '목소리에 실려' in t;pg.click('button[data-c=learn][data-a=spirit]');pg.click('button[data-c=tab][data-a=place]')
    print('awaken ok')
    # 부두 수군거림(드러냈다)
    go(pg,'street');go(pg,'docks');pg.wait_for_selector('#ov.on h2:has-text("운하 부두")',timeout=5000);assert '손끝에서 불이 나는 사람' in pg.inner_text('#ov');okpop(pg)
    # 키리엔이 전투에서 처음 본다
    E(pg,"()=>{const K=window.__k2;K.S.party='kirien';K.S.hp=K.S.mhp;K.render()}")
    E(pg,"window.__k2.startBattle('fight','dog')");pg.click('#bov .btn.pri');pg.wait_for_function("window.__k2.G.st==='player'",timeout=10000)
    E(pg,"()=>{const K=window.__k2;K.G.fp=5;K.G.fhp=1}");E(pg,"window.__k2.useSkill('shock')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);okpop(pg)
    pg.wait_for_selector('#ov.on h2:has-text("키리엔")',timeout=5000);assert '진짜는 처음 봐' in pg.inner_text('#ov');choose(pg,'나도 무섭다');okpop(pg)
    assert E(pg,"window.__k2.S.mgs.kirien")==1;print('witness ok')
    # 추적자
    E(pg,"()=>{const K=window.__k2;K.ENC_ON=true}")
    r=E(pg,"()=>{const K=window.__k2;const o=Math.random;let n=0;Math.random=()=>0.01;const f=K.roadFoe({fr:'street',to:'church'});Math.random=o;K.ENC_ON=false;return f}")
    assert r=='hunter',r
    # 브리타
    go(pg,'street');pg.click('button[data-c=britaM]');t=pg.inner_text('#ov');assert '소문 들었어' in t;choose(pg,'소리 내어 따라');t=pg.inner_text('#ov');assert '할머니 목소리' in t and '새 주문 — 바람막이' in t;okpop(pg)
    assert 'windward' in E(pg,"window.__k2.S.sk")
    # 하그
    E(pg,"()=>{const K=window.__k2;K.S.outs=1;K.S.hq=3;K.render()}");go(pg,'outskirts')
    pg.click('button[data-c=hagM]');choose(pg,'아무것도 안 보인다');okpop(pg);assert E(pg,"window.__k2.S.hm")==2
    pg.click('button[data-c=hagM]');choose(pg,'하얀 쪽을 소리 내어');t=pg.inner_text('#ov');assert '누구냐 너' in t and '새 주문 — 밤새의 노래' in t;okpop(pg)
    # 바람막이·밤새의 노래가 전투에서 돈다
    E(pg,"window.__k2.startBattle('fight','dog')");pg.click('#bov .btn.pri');pg.wait_for_function("window.__k2.G.st==='player'",timeout=10000)
    E(pg,"()=>{const K=window.__k2;K.G.fp=5;K.G.hp=10;K.useSkill('nightsong')}");assert E(pg,"window.__k2.G.hp")>10 and E(pg,"window.__k2.G.forget")==1
    E(pg,"()=>{const K=window.__k2;K.G.fhp=0;K.endBattle('win')}");okpop(pg)
    # 피트
    go(pg,'street');go(pg,'docks');go(pg,'base');pg.click('button[data-c=pitM]');choose(pg,'손끝을 장작에');t=pg.inner_text('#ov');assert '또 해 봐' in t and '부두 애들' in t;okpop(pg)
    assert pg.locator('button[data-c=pitM]').count()==0;print('npc ok')
    # 삼키는 갈래: 아이를 놓치고 분필 원으로 혼자 깨어난다
    newgame(pg,0)
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.joinComp('ibre');K.S.party='ibre';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.S.pit=1;K.S.eda=1;K.S.acad=1;K.S.loc='dome';K.render()}")
    pg.click('button[data-c=aw1]');choose(pg,'막아선다');pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.wait_for_function("window.__k2.G.st==='player'",timeout=10000)
    E(pg,"()=>{const K=window.__k2;K.G.fhp=0}");E(pg,"window.__k2.bact('atk')");pg.wait_for_function('!window.__k2.G.on',timeout=10000);okpop(pg)
    pg.wait_for_selector('#ov.on button:has-text("삼킨다")',timeout=5000);choose(pg,'삼킨다');assert '회색 마차' in pg.inner_text('#ov');okpop(pg)
    s=E(pg,"window.__k2.S");assert s['awl']==1 and not s.get('mg')
    assert '분필 원' in pg.inner_text('button[data-c=aw1]')
    pg.click('button[data-c=aw1]');choose(pg,'말을 뱉는다');t=pg.inner_text('#ov');assert '비늘이 섰습니다' in t;choose(pg,'손을 쥔다');t=pg.inner_text('#ov');assert '본 사람은 없다' in t and '새 주문 — 혼불' in t;okpop(pg)
    s=E(pg,"window.__k2.S");assert s['mg']==1 and s['mgh']=='hide' and 'spirit' in s['sk'];print('swallow branch ok')
    # 옛 저장(v9 영매사, 혼불 보유) 이전
    old=E(pg,"()=>{const K=window.__k2;const o=JSON.parse(JSON.stringify(K.S));o.v=9;o.og=2;o.mg=0;o.sk=['spirit','shock'];o.skp=0;delete o.mgs;return JSON.stringify(o)}")
    E(pg,f"()=>{{localStorage.setItem('kalsel2',{json.dumps(old)})}}");pg.goto(url);pg.wait_for_timeout(400)
    s=E(pg,"window.__k2.S");assert s['v']==11 and s['sk']==['mend'] and s['mgOld']==['spirit'] and s['skp']==1,(s['sk'],s.get('mgOld'),s['skp'])
    print('migrate ok')
    b.close()
assert not errs,errs
print('ALL OK')
