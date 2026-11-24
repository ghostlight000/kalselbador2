"""바르그·에노: 하수구 안내인 → 에노, 회색 마차의 밤 → 바르그, 거절과 다시 영입, 에다 조건, 동료 전투, 자료 빠짐 검사"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t,_to=10000):
    sel=f'#ov.on button:has-text("{t}")'
    if pg.locator(sel).count()==0 and pg.locator('#ov.on button:has-text("물어보고 싶은 게 있어")').count()>0 and t not in ('물어보고 싶은 게 있어',):
        pg.click('#ov.on button:has-text("물어보고 싶은 게 있어")');pg.wait_for_timeout(60)
    if pg.locator(sel).count()==0 and pg.locator('#ov.on button:has-text("너에 대해 이야기해 줘")').count()>0 and t not in ('너에 대해 이야기해 줘','다른 이야기를 한다','이야기를 그만둔다'):
        pg.click('#ov.on button:has-text("너에 대해 이야기해 줘")');pg.wait_for_timeout(60)
    if pg.locator(sel).count()==0 and t=='다른 이야기를 한다' and pg.locator('#ov.on button:has-text("다른 것도 묻는다")').count()>0:
        sel='#ov.on button:has-text("다른 것도 묻는다")'
    pg.wait_for_selector(sel,timeout=_to);pg.click(sel);pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def go(pg,k):pg.eval_on_selector(f'.map .node[data-a={k}]',"e=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}))");choose(pg,'간다');pg.wait_for_function(f"window.__k2.S.loc==='{k}'",timeout=10000);pg.wait_for_timeout(650);(pg.is_visible('#ov.on h2:has-text("대성당")') and (choose(pg,'고개를 숙인다'),choose(pg,'대성당을 나선다')));(pg.is_visible('#ov.on h2:has-text("문 앞의 상자")') and (choose(pg,'서랍 깊이'),choose(pg,'서랍을 닫는다')))
def win(pg):
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{window.__k2.G.fhp=0}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);okpop(pg)
E=lambda pg,x:pg.evaluate(x)
def start(pg):
    pg.goto(url);pg.wait_for_timeout(200);E(pg,"localStorage.clear()");pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('kirien');K.joinComp('oswin');K.S.party='kirien';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;K.S.loc='docks';K.S.dec.ibre=1;K.S.dec.kasimir=1;K.S.mr=3;K.S.manor=1;K.S.hp=K.S.mhp;K.render()}")
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    # 자료 빠짐 검사
    r=E(pg,"""()=>{pg=null}""") if False else None
    pg.goto(url);pg.wait_for_timeout(200)
    bad=E(pg,"""()=>{const K=window.__k2,out=[];
      for(const id of ['kirien','oswin','ibre','kasimir','barg','eno']){
        if((K.QA[id]||[]).length!==5)out.push(id+' QA');if((K.CH[id]||[]).length!==4)out.push(id+' CH');if(Object.keys(K.CSK[id]||{}).length!==3)out.push(id+' CSK');
        if(!K.AEV[id]||![4,6,8].every(t=>K.AEV[id][t]))out.push(id+' AEV');
        for(const l of ['docks','street','church','base','academy','outskirts'])if(!(K.TALK[id]||{})[l])out.push(id+' TALK '+l);
        for(const o of Object.keys(K.COMP))if(o!==id&&!(K.COMP[id].hello||{})[o])out.push(id+' hello '+o)}
      return out}""")
    assert not bad,bad
    # 하수구 → 에노(거절) → 다시 영입
    start(pg)
    E(pg,"()=>{window.__k2.SCENE.sewer()}");t=pg.inner_text('#ov');assert '물자국이 없다' in t and '목소리가 문장 중간에 바뀐다' in t;choose(pg,'목소리를 따라간다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("피트")',timeout=5000);choose(pg,'이름이 뭐야?');choose(pg,'배고프지 않아?');choose(pg,'저택에서 같이 지내자');choose(pg,'데려간다')
    pg.wait_for_selector('#ov.on h2:has-text("물길 아이")',timeout=5000);choose(pg,'철창에 손을 넣는다');assert '셋까지 세면' in pg.inner_text('#ov');choose(pg,'길을 알려 줘서');t=pg.inner_text('#ov');assert '지도에 구멍' in t and '물소리' in t;choose(pg,'하수구가 더 어울린다');okpop(pg)
    assert E(pg,"window.__k2.S.dec.eno")==1
    pg.click('button[data-c=tab][data-a=quest]');q=pg.inner_text('.M');assert '물길 아이' in q;pg.click('button[data-c=tab][data-a=place]')
    # 에다는 바르그·에노를 만나기 전엔 없다
    pg.click('button[data-c=enoAgain]');choose(pg,'함께하자');t=pg.inner_text('#ov');assert '키리엔과 계속 다닌다' in t and '에노와 다닌다' in t,t;choose(pg,'에노와 다닌다');assert E(pg,"window.__k2.S.party")=='eno' and 'kirien' in E(pg,"window.__k2.S.comps")
    t=pg.inner_text('.goalc');assert '회색 마차의 늑대' in t,t
    # 여관 부엌 → 헌병과 싸운다 → 바르그
    pg.click('button[data-c=bargM]');choose(pg,'자루를 연다');t=pg.inner_text('#ov');assert '이번에도 아니다' in t;assert '탈영병 바르그' in t and '무서운 걸 다 써 버렸대' in t;choose(pg,'늑대 옆에 선다');assert E(pg,"window.__k2.G.foe")=='mp';win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("운하 계단")',timeout=5000);choose(pg,'같이 알아보자');choose(pg,'밤길로 나선다');assert '맹세했다' in pg.inner_text('#ov');choose(pg,'도망친 사람을 넘기기 싫어서');assert '헌병들을 막아섰다' in E(pg,"JSON.stringify(window.__k2.S.jr)");choose(pg,'갈 길을 가라');okpop(pg)
    pg.click('button[data-c=bargAgain]');choose(pg,'저택에서 지내라');choose(pg,'계속 다닌다');assert 'barg' in E(pg,"window.__k2.S.comps")
    go(pg,'street');assert pg.locator('button[data-c=eda]').count()==1;print('meet ok')
    go(pg,'base');E(pg,"()=>{const K=window.__k2;K.S.party='barg';K.S.hp=5;K.render()}");pg.click('button[data-c=rest]');pg.wait_for_function('!window.__k2.S.act',timeout=20000);t=pg.inner_text('#ov');assert '꼬리표' in t,t;okpop(pg)
    # 파견 게시판: 한 줄짜리 목록에서 바로 보낸다
    pg.click('button[data-c=board]');assert pg.locator('#ov.on .drow').count()>=6 and pg.locator('#ov.on .btn').count()==1;pg.locator('#ov.on .drow').first.click();assert len(E(pg,"window.__k2.S.disp"))==1;print('board ok')
    # 메아리: 솔레·리세
    E(pg,"()=>{const K=window.__k2;K.S.disp=[];K.S.kids.pit.st='ok';K.S.sole=1;K.S.acad=1;K.S.eda=1;K.S.mg=1;K.S.oq0=1;K.S.mgh='hide';K.S.oq=6;K.S.oqt=1;K.S.oqe='burn';K.S.party='oswin';K.render()}")
    go(pg,'academy');pg.wait_for_selector('#ov.on h2:has-text("솔레")',timeout=5000);assert '혀를 깨물고' in pg.inner_text('#ov');okpop(pg)
    go(pg,'base');pg.wait_for_selector('#ov.on h2:has-text("리세의 편지")',timeout=5000);t=pg.inner_text('#ov');assert '오빠에게' in t and '붉은 불' in t;okpop(pg);print('echo ok')
    # 바르그·에노 동료 전투
    for cid in ['barg','eno']:
        E(pg,f"()=>{{const K=window.__k2;K.S.party='{cid}';const C=K.S.cl['{cid}'];C.r={{cleave:1,stew:2,back:3,hook:2,read:3,voices:3}};K.S.hp=K.S.mhp-30;K.render()}}")
        E(pg,"window.__k2.startBattle('fight','thief')");pg.click('#bov .btn.pri');pg.wait_for_function("window.__k2.G.st==='player'",timeout=10000)
        f0=E(pg,"window.__k2.G.fhp");E(pg,"window.__k2.bact('guard')");pg.wait_for_timeout(900)
        log=pg.inner_text('#blog');assert ('바르그' if cid=='barg' else '에노') in log,log
        assert E(pg,"window.__k2.G.fhp")<f0
        if cid=='barg':assert '내가 서 있다' in log
        E(pg,"()=>{const K=window.__k2;K.endBattle('win')}");okpop(pg)
    # 출신 반응·종족 질문
    E(pg,"()=>{const K=window.__k2;K.S.party='eno';K.render()}");pg.click('button[data-c=talk]');assert '병사가 하나' in pg.inner_text('#ov');choose(pg,'다른 이야기를 한다')
    choose(pg,'물어보고 싶은 게 있어');choose(pg,'너에 대해 이야기해 줘');assert '지도 좀 보여 줄래?' in pg.inner_text('#ov');choose(pg,'다른 이야기를 한다');choose(pg,'이야기를 그만둔다')
    print('battle/talk ok')
    b.close()
assert not errs,errs
print('ALL OK')
