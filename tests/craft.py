"""v042 채집 장부·자리를 비운 동안·장인 오틸리에·공방·부엌 솥·싸움 중 가방·동료 파견·저장 이전"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
E=lambda pg,x:pg.evaluate(x)
H=3600*0.002*1000  # 테스트 모드의 한 시간(ms)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.grantPit()}");okpop(pg)
    E(pg,"()=>{S.loc='base';S.coin=200;render()}")
    assert E(pg,"S.v")==12 and E(pg,"S.kids.pit.ks.e")==3
    # 채집 장부
    pg.click('button[data-c=ledger]');t=pg.inner_text('#ov');assert '2시간치' in t and '손재주 1' in t and '부두 가장자리' in t
    choose(pg,'피트에게 채집을 맡긴다');choose(pg,'부두 가장자리');assert E(pg,"S.kids.pit.st")=='gath' and E(pg,"S.gl.pit.sp")=='dock'
    choose(pg,'장부를 덮는다');assert '부두 가장자리' in pg.get_attribute('button[data-c=ledger]','title')
    pg.click('button[data-c=board]');assert pg.locator('#ov .drow[disabled]').count()>=6;choose(pg,'닫기')
    E(pg,f"()=>{{S.gl.pit.t0-={H};render()}}");assert '고철 1' in E(pg,"peekTxt('pit')")
    s0=E(pg,"S.inv.scrap||0");pg.click('button[data-c=ledger]');choose(pg,'피트 — 모인 것을 거둬들인다');assert E(pg,"S.inv.scrap||0")==s0+1;choose(pg,'장부로 돌아간다')
    # 단계가 오른다
    E(pg,f"()=>{{S.gsh.dock=2.99;S.gl.pit.t0-={H}}}");choose(pg,'피트 — 모인 것을 거둬들인다');t=pg.inner_text('#ov');assert '2단계' in t and '그물' in t,t;choose(pg,'장부로 돌아간다')
    assert E(pg,"glv('dock')")==2 and E(pg,"grate('dock').fish")==1
    # 한도
    E(pg,f"()=>{{S.gl.pit.t0-={H}*5}}");assert abs(E(pg,"gpeek('pit').h")-2)<.01 and E(pg,"gpeek('pit').full")
    E(pg,"()=>{S.fix.roof=1;S.fix.store=1}");assert abs(E(pg,"gpeek('pit').h")-5)<.05;E(pg,"()=>{S.fix.cellar=1}");assert E(pg,"capH()")==10
    choose(pg,'피트 — 불러들인다');assert E(pg,"S.kids.pit.st")=='ok' and 'pit' not in E(pg,"S.gl");choose(pg,'장부로 돌아간다');choose(pg,'장부를 덮는다')
    print('ledger ok')
    # 자리를 비운 동안
    E(pg,f"()=>{{CMD.gsend('pit','market');EV0=null;S.gl.pit.t0-={H}*3;S.sv=Date.now()-{H}*3;AWAYCK=false;render()}}")
    pg.wait_for_selector('#ov.on h2:has-text("자리를 비운 동안")',timeout=5000);t=pg.inner_text('#ov');assert '피트' in t and '시장 뒷골목' in t and '천 조각' in t,t;okpop(pg)
    assert E(pg,"S.inv.cloth||0")>=4
    E(pg,"()=>{S.sv=Date.now();AWAYCK=false}");pg.wait_for_timeout(700);assert pg.locator('#ov.on').count()==0
    print('away ok')
    # 장인 오틸리에
    E(pg,"()=>{S.loc='docks';render()}");pg.click('button[data-c=smithM]');choose(pg,'공방이 있다고');t=pg.inner_text('#ov');assert '공방부터 고쳐' in t;okpop(pg)
    assert E(pg,"S.smM")==1 and pg.locator('button[data-c=smithM]').count()==0
    E(pg,"()=>{S.loc='base';render()}");pg.click('button[data-c=shop]');assert '공방을 고치면' in pg.inner_text('#ov');okpop(pg)
    E(pg,"()=>{S.fix.shop=1;render()}");pg.click('button[data-c=shop]');assert '내가 해 주면' in pg.inner_text('#ov');choose(pg,'공방을 둘러본다')
    t=pg.inner_text('#ov');assert '아직 배운 것이 없다' in t and '기운 붕대' in t and '불지기' not in t
    c0=E(pg,"S.coin");choose(pg,'기운 붕대 배우기');assert E(pg,"S.rcpL.band")==1 and E(pg,"S.coin")==c0-E(pg,"px(4)");choose(pg,'공방으로 돌아간다')
    b0=E(pg,"S.inv.band||0");cl0=E(pg,"S.inv.cloth");choose(pg,'기운 붕대 만들기');assert E(pg,"S.craft.id")=='band' and E(pg,"S.inv.cloth")==cl0-2;okpop(pg)
    assert '만드는 중' in pg.get_attribute('button[data-c=shop]','title')
    pg.wait_for_selector('#ov.on h2:has-text("기운 붕대을(를) 만들었다")',timeout=8000);okpop(pg);assert E(pg,"S.inv.band")==b0+1 and E(pg,"S.crN")==1
    assert '✦' in pg.inner_text('button[data-c=shop]')
    pg.click('button[data-c=shop]');choose(pg,'오틸리에와 이야기한다');choose(pg,'하칸골에서는');t=pg.inner_text('#ov');assert '서른 해' in t
    E(pg,"()=>{EV0=null;render()}")
    # 부탁
    pg.click('button[data-c=shop]');choose(pg,'무두질한 외투에 대해 묻는다');assert '미지근한 물' in pg.inner_text('#ov');choose(pg,'공방으로 돌아간다')
    choose(pg,'부탁한 것을 건넨다 — 무두질한 외투');assert '모자라다' in pg.inner_text('#ov');choose(pg,'공방으로 돌아간다')
    E(pg,"()=>{add('warm',1)}");choose(pg,'부탁한 것을 건넨다 — 무두질한 외투');assert '무언가가 계속 데우고' in pg.inner_text('#ov') and E(pg,"S.rcpL.coat")==1 and not E(pg,"S.inv.warm||0");choose(pg,'공방으로 돌아간다')
    # 이야기 2장 → 칼날
    E(pg,"()=>{S.crN=4;EV0=null}");E(pg,"CMD.ntalk('otil')");choose(pg,'팔뚝의 흉');assert E(pg,"S.rcpL.blade")==1
    E(pg,"()=>{EV0=null;MATS.forEach(m=>add(m,5));CMD.craftgo('blade')}");okpop(pg);pg.wait_for_selector('#ov.on h2:has-text("재를 먹인 칼날")',timeout=8000);t=pg.inner_text('#ov');assert '낯선 목소리' in t;okpop(pg)
    assert E(pg,"gear('blade')");pg.click('button[data-c=shop]');assert '재를 먹인 칼날' not in pg.inner_text('#ov .m, #ov b') if False else True;assert '<b>재를 먹인 칼날</b>' not in pg.inner_html('#ov') and pg.locator('#ov.on button:has-text("재를 먹인 칼날 만들기")').count()==0;E(pg,"()=>{EV0=null;render()}")
    print('smith ok')
    # 신발
    E(pg,"()=>{S.rcpL.shoe=1;S.craft=null;CMD.craftgo('shoe')}");okpop(pg);pg.wait_for_selector('#ov.on h2:has-text("아이 신발")',timeout=8000);okpop(pg);assert E(pg,"S.kids.pit.shoe")==1 and E(pg,"rcpDone('shoe')")
    # 부엌 솥
    E(pg,"()=>{S.fix.kitchen=1;render()}");pg.click('button[data-c=pot]');assert '아직 만들어 본 요리가 없다' in pg.inner_text('#ov')
    choose(pg,'꿀을(를) 넣는다');choose(pg,'고기을(를) 더 넣는다');assert '겉돈다' in pg.inner_text('#ov');choose(pg,'다른 것을 넣어 본다')
    f0=E(pg,"S.inv.fish");choose(pg,'생선을(를) 넣는다');choose(pg,'들풀을(를) 더 넣는다');assert '생선 수프' in pg.inner_text('#ov') and E(pg,"S.inv.soup")==1 and E(pg,"S.inv.fish")==f0-1;choose(pg,'솥을 내려놓는다')
    E(pg,"()=>{EV0=null;CMD.cook('meat')}");assert E(pg,"S.inv.raw")==1;E(pg,"()=>{EV0=null;render()}")
    print('cook ok')
    # 싸움 중 가방
    E(pg,"()=>{add('salve',2);S.hp=20;startBattle('fight','dog')}");pg.click('#bov [data-bo=fgo]');pg.wait_for_function("window.__k2.G.st==='player'",timeout=15000)
    assert pg.locator('[data-ba=bag]').count()==1;pg.click('[data-ba=bag]');assert pg.locator('[data-ba=bi][data-k=soup]').count()==1
    h0=E(pg,"G.hp");pg.click('[data-ba=bi][data-k=soup]');assert E(pg,"G.hp")==min(h0+35,E(pg,"G.mhp")) and not E(pg,"S.inv.soup||0") and E(pg,"G.bagU")==1
    E(pg,"()=>{G.st='player';G.beats=[];brender()}");pg.click('[data-ba=bag]');pg.click('[data-ba=bi][data-k=salve]');assert E(pg,"G.bagU")==2 and E(pg,"S.inv.salve")==1
    E(pg,"()=>{G.st='player';G.beats=[];brender()}");assert pg.locator('[data-ba=bag][disabled]').count()==1
    # 외투·칼날
    assert E(pg,"S.eq.wpn")=='ablade' and E(pg,"!!S.geq.ablade");E(pg,"()=>{S.eq.body='tcoat';G.hp=200;G.mhp=200;G.scale=1}");E(pg,"(()=>{G.ward=0;G.wall=0;hurt(100)})()");assert E(pg,"G.hp")==110,E(pg,"G.hp")
    E(pg,"()=>{G.first=0;G.spell=0;G.fhp=500}");E(pg,"dmgFoe(100)");assert E(pg,"G.fhp")==385,E(pg,"G.fhp")
    E(pg,"()=>{G.on=false;$('#bt').classList.remove('on');S.hp=S.mhp;render()}")
    print('battle bag ok')
    # 동료를 먼 곳에
    E(pg,"()=>{['kirien','oswin'].forEach(joinComp);S.party='kirien';EV0=null;POP=null;render()}")
    pg.click('button[data-c=board]');pg.click('#ov.on .drow:has-text("성벽 바깥")');t=pg.inner_text('#ov');assert '오스윈 (동료' in t and '키리엔 (동료' not in t;choose(pg,'오스윈 (동료')
    assert E(pg,"S.disp.some(d=>d.comp==='oswin')") and E(pg,"awayC('oswin')")
    pg.wait_for_selector('#ov.on h2:has-text("파견에서 돌아왔다")',timeout=30000);t=pg.inner_text('#ov');assert '오스윈 — “폐허에' in t,t;okpop(pg);assert not E(pg,"awayC('oswin')")
    print('companion dispatch ok')
    # 저장 이전: v11 저장
    E(pg,"()=>{const o=JSON.parse(JSON.stringify(S));o.v=11;delete o.gl;delete o.gsh;delete o.rcpL;delete o.gear;Object.values(o.kids).forEach(k=>{delete k.ks;delete k.kx;k.st='ok'});localStorage.setItem(K,JSON.stringify(o));S=null;load()}")
    assert E(pg,"S.v")==12 and E(pg,"typeof S.gl")=='object' and E(pg,"S.kids.pit.ks.d")==1
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
