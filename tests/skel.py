"""전체 경로 테스트
만들기(성별·1편 기록) → 시작 연출 → 여관·탐사 → 지도로 이동 → 가르침 → 첫 번째 밤 →
키리엔 → 교단 문서고(정화자) → 오스윈 → 저택 소문 → 노래하는 옛 주인 → 본거지 →
하수구 쥐 떼 → 피트 → 파견 → 동료의 방·대화·호감도 → 기록 코드 → 저장 이전 → 패배 → 처음부터"""
import pathlib,gzip,base64,json
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent
url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
leg=json.dumps({'name':'테오르<script>','race':'p','og':'칼라쉬','tr':'남색 서리비늘','end':'k','pa':'fox','inv':{}},ensure_ascii=False).encode()
LEG='KS1.'+base64.b64encode(gzip.compress(leg)).decode()
BOT="""()=>{const K=window.__k2;clearInterval(window.__bot);window.__bot=setInterval(()=>{const G=K.G,t=performance.now();if(!G.on)return;
  const bo=document.querySelector('#bov.on .btn.pri');if(bo){bo.click();return}
  if(G.st==='player'){K.bact(G.kind==='tut'||G.fp>=2?'heavy':'atk');return}
  if(G.st==='qte'&&G.q&&!G.q.done){const p=(t-G.q.t0)/G.q.dur;if(p>=(G.q.z[0]+G.q.z[1])/2)K.press('qte',t);return}
  if(G.st==='enemy'){const b=G.beats.filter(b=>!b.res).sort((x,y)=>x.T-y.T)[0];if(b&&t>=b.T-4){let k='parry';if(G.kind==='tut'&&K.TS[G.tut].goal==='dodge')k='dodge';K.press(k,t)}}},4)}"""
def okpop(pg):
    pg.wait_for_selector('#ov.on .btn',timeout=20000); t=pg.inner_text('#ov h2'); pg.click('#ov.on .btn.pri'); return t
def choose(pg,text):
    sel=f'#ov.on button:has-text("{text}")'
    if pg.locator(sel).count()==0 and pg.locator('#ov.on button:has-text("물어보고 싶은 게 있어")').count()>0 and text!='물어보고 싶은 게 있어':
        pg.click('#ov.on button:has-text("물어보고 싶은 게 있어")');pg.wait_for_timeout(60)
    if pg.locator(sel).count()==0 and pg.locator('#ov.on button:has-text("너에 대해 이야기해 줘")').count()>0 and text not in ('너에 대해 이야기해 줘','다른 이야기를 한다','이야기를 그만둔다'):
        pg.click('#ov.on button:has-text("너에 대해 이야기해 줘")');pg.wait_for_timeout(60)
    if pg.locator(sel).count()==0 and text=='다른 이야기를 한다' and pg.locator('#ov.on button:has-text("다른 것도 묻는다")').count()>0:
        sel='#ov.on button:has-text("다른 것도 묻는다")'
    pg.wait_for_selector(sel,timeout=20000); pg.click(sel); pg.wait_for_timeout(60)
def go(pg,k):
    pg.eval_on_selector(f'.map .node[data-a={k}]',"e=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}))"); choose(pg,'간다'); pg.wait_for_function(f"window.__k2.S.loc==='{k}'",timeout=10000); pg.wait_for_timeout(650)
def fight(pg):
    pg.wait_for_function('window.__k2.G.on',timeout=10000); pg.evaluate("()=>{const S=window.__k2.S;S.hp=S.mhp}"); pg.evaluate(BOT)
    pg.wait_for_function('!window.__k2.G.on',timeout=240000); h=okpop(pg); assert h!='쓰러졌다',h; return h
def S(pg): return pg.evaluate('window.__k2.S')
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1200,'height':900}); pg=ctx.new_page()
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and 'ERR_TUNNEL' not in m.text and 'fonts.g' not in m.text and errs.append(m.text))
    pg.goto(url); pg.wait_for_timeout(300); assert pg.evaluate('window.__k2.TEST')
    # ---- 만들기 ----
    pg.fill('#cname','레아'); pg.click('button[data-c=sex][data-a=f]'); pg.click('button[data-c=race][data-a=b]'); pg.click('button[data-c=trait][data-a="1"]'); pg.click('button[data-c=origin][data-a="1"]')
    pg.click('text=1편의 기록이 있다면'); pg.fill('#legt',LEG); pg.click('button[data-c=legread]'); pg.wait_for_timeout(200)
    t=pg.inner_text('.cr'); assert '불을 이어받은 자' in t and '<script>' not in t
    pg.click('button[data-c=start]'); pg.wait_for_timeout(150)
    assert '손끝이 푸른 사람은 데려간다' in pg.inner_text('#pv')
    for i in range(5):
        pg.click('#pv .eo'); pg.click('#pv .eo'); pg.wait_for_timeout(50); t=pg.inner_text('#pv')
        if i==0: assert '레아는' in t and '용 사냥꾼' in t and '푸르다' in t, t
        if i==1: assert '레아의 것' in t and '아버지의 마지막 말' in t and '서두르지 않으면' in t, t
        if i==3: assert '문을 거칠게' in t and '불지기' in t and pg.evaluate('window.__k2.PV.kt.length')==1, t
    pg.click('#pv .eo'); pg.click('#pv [data-pv=close]'); pg.wait_for_timeout(100)
    assert '모르텐' in pg.inner_text('#ov') and '손끝이 푸르군' in pg.inner_text('#ov'); choose(pg,'막대를 쥔 노인을 따라간다'); choose(pg,'막대 앞에 선다'); pg.wait_for_function('window.__k2.G.on'); pg.evaluate(BOT)
    pg.wait_for_function('!window.__k2.G.on',timeout=120000); okpop(pg); assert S(pg)['tutd']==1 and S(pg)['mort']==1
    assert '모르텐' in pg.inner_text('.Rr'); pg.click('button[data-c=mtalk]'); choose(pg,'거리 끝의 그건 누구야?'); choose(pg,'그런데 왜 싸워?'); assert '레아\n“그런데 왜 싸워?”' in pg.inner_text('#ov') and '친구니까' in pg.inner_text('#ov'); choose(pg,'이야기를 그만둔다')
    s=S(pg); print('made',s['name'],s['sex'],s['race'],s['og'],s['loc']); assert s['sex']=='f' and s['loc']=='docks' and not s['base'] and s['inv'].get('letter')==1
    assert pg.locator('button[data-c=board]').count()==0 and pg.locator('.map .node[data-a=base]').count()==0
    pg.click('button[data-c=rumor]'); assert '쉴 곳을 묻는다' not in pg.inner_text('#ov'); choose(pg,'근처의 소문'); assert '마그다' in pg.inner_text('#ov'); choose(pg,'이야기를 그만둔다')
    pg.evaluate("window.__k2.EXP.docks[0].enc=0"); pg.click('button[data-c=explore][data-a="0"]')
    pg.wait_for_function("document.querySelector('#ov.on h2')&&document.querySelector('#ov.on h2').textContent==='부두 창고 뒤지기'",timeout=10000); okpop(pg)
    pg.eval_on_selector('.map .node[data-a=church]',"e=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}))"); assert '첫 번째 밤' in pg.inner_text('#ov'); okpop(pg)
    # ---- 첫 번째 밤 ----
    go(pg,'street')
    for i in range(3):
        pg.wait_for_timeout(300); pg.click('button[data-c=patrol]'); h=fight(pg); print(S(pg)['night'],h)
    # ---- 키리엔 ----
    pg.wait_for_selector('#ov.on h2',timeout=5000); assert pg.inner_text('#ov h2')=='모르텐' and '박자가' in pg.inner_text('#ov'); choose(pg,'그의 눈을 감겨 준다'); assert '공급 하나' in pg.inner_text('#ov'); choose(pg,'막대를 줍는다')
    assert S(pg)['mort']==2 and S(pg)['inv'].get('mstaff')==1 and '모르텐이 나를 밀쳐' in pg.evaluate("JSON.stringify(window.__k2.S.jr||window.__k2.S.journal||'')")+pg.evaluate("JSON.stringify(window.__k2.S)")
    pg.wait_for_selector('#ov.on h2',timeout=5000); assert pg.inner_text('#ov h2')=='여우 머리의 여자' and '죽은 사람 냄새' in pg.inner_text('#ov')
    choose(pg,'누구냐고 묻는다'); choose(pg,'편지를 보여 준다'); assert '하나도 안 웃긴데' in pg.inner_text('#ov'); assert pg.locator('#ov button:has-text("혼자 하겠다")').count()==1; choose(pg,'같이 가자'); choose(pg,'좋다')
    s=S(pg); assert s['comps']==['kirien'] and s['party']=='kirien' and s['aff']['kirien']==18, s['aff']; print('kirien joined, aff',s['aff'])
    assert pg.evaluate("window.__k2.romOK('kirien')") and not pg.evaluate("window.__k2.romOK('kasimir')")
    # 대화(이곳에 대해) → 호감 +4 한 번만
    pg.click('button[data-c=talk]'); assert '없는 걸 쫓는' in pg.inner_text('#ov'); choose(pg,'다른 이야기를 한다'); assert '여우 머리' in pg.inner_text('#ov'); assert pg.locator('#ov.on button').count()<=6; choose(pg,'이곳은 어때?'); assert '이름을 붙인대' in pg.inner_text('#ov'); choose(pg,'다른 이야기를 한다'); assert '이곳은 어때?' in pg.inner_text('#ov')
    choose(pg,'너에 대해 이야기해 줘'); choose(pg,'지난 이야기를 들려줘'); assert '점쟁이의 딸' in pg.inner_text('#ov'); choose(pg,'점은 안 믿어'); t=pg.inner_text('#ov'); assert '틀린 적이 없었어' in t and '/ 4' not in t; choose(pg,'다른 이야기를 한다')
    choose(pg,'사람 찾는 일은 힘들지 않아?'); choose(pg,'이야기를 그만둔다'); assert S(pg)['aff']['kirien']==27 and S(pg)['chd']['kirien']==1, S(pg)['aff']
    assert pg.evaluate("window.__k2.affTier('kirien')")==3 and '성냥불' not in pg.inner_text('body')
    # ---- 교단 문서고 → 오스윈 ----
    go(pg,'church'); pg.click('button[data-c=archive]'); choose(pg,'끼어든다'); h=fight(pg); assert '정화자' in h
    pg.wait_for_selector('#ov.on h2',timeout=5000); assert pg.inner_text('#ov h2')=='오스윈'; assert '말 많네' in pg.inner_text('#ov')
    choose(pg,'장부에 뭐가 있느냐고 묻는다'); assert pg.locator('#ov button:has-text("각자 갈 길을 간다")').count()==1; choose(pg,'함께하자'); assert '여관 1층에서 기다린다' in pg.inner_text('#ov') and '털 날리는' not in pg.inner_text('#ov'); choose(pg,'계속 다닌다'); s=S(pg); assert s['comps']==['kirien','oswin'] and s['party']=='kirien'; print('oswin joined')
    assert '여관 1층에서 기다린다' in pg.inner_text('.Rr')
    # ---- 여관 주인 소문 → 저택 ----
    go(pg,'docks'); pg.wait_for_selector('#ov.on h2',timeout=5000); assert '판돈꾼' in pg.inner_text('#ov'); choose(pg,'결투장으로 가 보기로 한다')
    assert 'goal' in pg.get_attribute('button[data-c=ibreM]','class'); pg.click('button[data-c=ibreM]'); assert '무색 3번이 또 이겼다' in pg.inner_text('#ov') and '오르빌 저택 이야기도' in pg.inner_text('#ov'); choose(pg,'도전한다'); h=fight(pg); assert '무색 3번' in h
    pg.wait_for_selector('#ov.on h2',timeout=5000); assert '브리타' in pg.inner_text('#ov'); choose(pg,'이름이 뭐야?'); assert '그 이름을 물은 사람은 처음' in pg.inner_text('#ov'); choose(pg,'함께하자'); choose(pg,'계속 다닌다'); assert 'ibre' in S(pg)['comps']; print('ibre joined')
    assert pg.locator('.map .node[data-a=base]').count()==0
    go(pg,'street'); pg.click('button[data-c=brita]'); assert '한 줄도 말이 안 돼' in pg.inner_text('#ov'); choose(pg,'주문이 사라졌다는 거야?'); assert '겨울 시대 노인들' in pg.inner_text('#ov'); choose(pg,'묘지로 가 보기로 한다')
    go(pg,'church'); pg.click('button[data-c=tomb]'); t=pg.inner_text('#ov'); assert '불을 거둔 이' in t; choose(pg,'열쇠를 챙긴다'); print('pre-manor story ok')
    assert pg.locator('.map .node[data-a=base]').count()==1
    t=pg.inner_text('#ov'); assert '어디서 뵌 것 같군요' in t; choose(pg,'누구냐고 묻는다'); assert '육십 년 전에 대가 끊겼는데요' in pg.inner_text('#ov') or '피 냄새' in pg.inner_text('#ov'); choose(pg,'함께하자'); choose(pg,'계속 다닌다'); assert 'kasimir' in S(pg)['comps']; print('kasimir joined')
    go(pg,'base'); pg.click('button[data-c=manorIn]'); assert '노래 들려?' in pg.inner_text('#ov'); choose(pg,'안으로 들어선다')
    choose(pg,'계단 위의 문'); assert '잠겼다' in pg.inner_text('#ov'); choose(pg,'내려간다')
    choose(pg,'서재 (잠겨 있다)'); choose(pg,'다른 곳을 본다')
    choose(pg,'응접실'); choose(pg,'악보받침'); assert '솔 · 미 · 레 · 도' in pg.inner_text('#ov'); choose(pg,'다른 곳을 본다')
    choose(pg,'응접실'); choose(pg,'건반을 누른다')
    for n in ['솔','미','레','도']: choose(pg,n)
    assert '어긋난다' in pg.inner_text('#ov'); choose(pg,'처음부터 다시')
    for n in ['도','레','미','솔']: pg.click(f'#ov.on button:text-is("{n}")'); pg.wait_for_timeout(50)
    assert '서재' in pg.inner_text('#ov') and S(pg)['mz']['key']==1; choose(pg,'열쇠를 챙긴다')
    choose(pg,'부엌'); choose(pg,'찬장을 뒤진다'); assert '세 시 십오 분' in pg.inner_text('#ov'); choose(pg,'다른 곳을 본다')
    choose(pg,'서재'); choose(pg,'금고 바늘을'); pg.click('#ov.on button:text-is("4시")'); choose(pg,'15분'); choose(pg,'다시 맞춘다')
    pg.click('#ov.on button:text-is("3시")'); choose(pg,'15분'); assert '대신 노래해 둘게' in pg.inner_text('#ov'); choose(pg,'열쇠를 챙긴다')
    choose(pg,'계단 위의 문'); choose(pg,'문을 연다'); h=fight(pg); assert '노래하는 옛 주인' in h
    pg.wait_for_selector('#ov.on h2',timeout=5000); t=pg.inner_text('#ov'); assert '여관비는 아끼겠네' in t and '여우 모양 문진' in t; choose(pg,'짐을 옮긴다')
    s=S(pg); assert s['base']==1 and s['inv'].get('relic')==1 and not s['pit']; print('base ok')
    assert pg.locator('button[data-c=board]').count()==0
    # 동료의 방: 데려갈 동료 바꾸기
    pg.click('button[data-c=rooms]'); assert pg.locator('#ov.on button').count()==3; choose(pg,'함께 나갈 동료를 고른다'); choose(pg,'오스윈과 나간다'); assert S(pg)['party']=='oswin'; assert '본거지에서 지낸다' in pg.inner_text('.Rr')
    # ---- 하수구의 아이 → 피트 ----
    go(pg,'docks'); pg.click('button[data-c=explore][data-a="0"]')
    pg.wait_for_function("document.querySelector('#ov.on h2')&&document.querySelector('#ov.on h2').textContent==='부두 창고 뒤지기'",timeout=10000); okpop(pg)
    pg.wait_for_selector('#ov.on h2',timeout=5000); assert pg.inner_text('#ov h2')=='하수구 입구'; choose(pg,'안내인을 따라간다'); h=fight(pg); assert '쥐 떼' in h
    pg.wait_for_selector('#ov.on h2',timeout=5000); t=pg.inner_text('#ov'); assert pg.inner_text('#ov h2')=='피트'; choose(pg,'이름이 뭐야?'); choose(pg,'배고프지 않아?'); assert '지붕은 있습니다' in pg.inner_text('#ov'); choose(pg,'저택에서 같이 지내자'); assert '글은 읽을 줄 압니까' in pg.inner_text('#ov'); choose(pg,'데려간다')
    assert S(pg)['pit']==1; print('pit ok')
    pg.wait_for_selector('#ov.on h2:has-text("물길의 안내인")',timeout=5000); choose(pg,'네가 해 봐'); choose(pg,'그걸 왜 마셔?'); assert '할머니 목소리' in pg.inner_text('#ov'); choose(pg,'함께하자'); choose(pg,'계속 다닌다')
    assert 'eno' in S(pg)['comps']
    if S(pg)['loc']!='docks': go(pg,'docks')
    assert 'goal' in pg.get_attribute('button[data-c=bargM]','class'); pg.click('button[data-c=bargM]'); choose(pg,'누구냐고 묻는다'); assert '잿빛 송곳니' in pg.inner_text('#ov'); choose(pg,'둘러댄다'); choose(pg,'운하 계단으로'); choose(pg,'구호소로'); choose(pg,'밤길로'); choose(pg,'자루를 여는'); choose(pg,'저택에서 지내라'); choose(pg,'계속 다닌다')
    assert 'barg' in S(pg)['comps']; print('barg/eno ok')
    # ---- 파견 ----
    go(pg,'base'); pg.click('button[data-c=board]'); pg.click('#ov.on .drow:has-text("시장 심부름")')
    pg.wait_for_function("document.querySelector('#ov.on h2')&&document.querySelector('#ov.on h2').textContent==='파견에서 돌아왔다'",timeout=10000); okpop(pg); print('dispatch ok')
    # ---- 레벨·능력치·기술 ----
    s=S(pg); print('level',s['lv'],'xp',s['xp'],'sp',s['sp'],'skp',s['skp'],'sk',s['sk']); assert s['lv']>=3 and s['sp']>=2 and s['skp']>=1 and s['sk']==['hamstring']
    pg.click('button[data-c=tab][data-a=char]'); assert '✦' in pg.inner_text('.top')
    st0=s['st'][1]; m0=s['mhp']; pg.click('button[data-c=statup][data-a="1"]'); pg.click('button[data-c=statup][data-a="0"]'); s=S(pg); assert s['st'][1]==st0+1 and s['mhp']==m0+4
    assert pg.locator('button[data-c=learn][data-a=spirit]').count()==0; pg.evaluate("()=>{window.__k2.S.mg=1;window.__k2.render()}"); pg.click('button[data-c=learn][data-a=spirit]'); s=S(pg); assert 'spirit' in s['sk']; print('stats/skills ok',s['st'],s['sk'])
    # 기술을 실전에서: 혼불·발목 긋기
    pg.click('button[data-c=tab][data-a=place]'); pg.evaluate("clearInterval(window.__bot)"); pg.evaluate("window.__k2.startBattle('fight','dog')"); pg.click('#bov .btn.pri'); pg.wait_for_function("window.__k2.G.st==='player'")
    pg.evaluate("window.__k2.G.fp=5"); pg.click('#bacts [data-ba=skill]'); assert pg.locator('#bacts [data-k=spirit]').count()==1
    f0=pg.evaluate('window.__k2.G.fhp'); pg.click('#bacts [data-k=spirit]'); pg.wait_for_timeout(50); f1=pg.evaluate('window.__k2.G.fhp'); assert f0-f1==round(10+2.4*S(pg)['st'][1]) or f0-f1==int(10+2.4*S(pg)['st'][1]+.5), (f0,f1)
    pg.wait_for_function("window.__k2.G.st==='enemy'",timeout=5000); pg.evaluate(BOT); pg.wait_for_function('!window.__k2.G.on',timeout=120000); okpop(pg); pg.wait_for_selector('#ov.on .btns button',timeout=5000); pg.click('#ov.on .btns button >> nth=0'); okpop(pg); print('skill in battle ok')
    pg.click('button[data-c=tab][data-a=quest]'); q=pg.inner_text('.M'); assert '◇ 등불을 든 사람의 딸' in q
    pg.click('button[data-c=tab][data-a=char]'); c=pg.inner_text('.M'); assert '키리엔' in c and '오스윈' in c and '여' in c
    pg.click('button[data-c=tab][data-a=story]'); assert '테오르' in pg.inner_text('.M') and '오르빌 저택' in pg.inner_text('.M')
    pg.click('button[data-c=tab][data-a=place]')
    # ---- 기록 코드 · 새로고침 · 저장 이전 ----
    code=pg.evaluate('window.__k2.scode()'); o=pg.evaluate('c=>window.__k2.sdecode(c)',code); assert o['base']==1 and o['comps']==['kirien','oswin','ibre','kasimir','eno','barg']
    pg.reload(); pg.wait_for_timeout(300); assert S(pg)['loc']=='base' and S(pg)['party']=='oswin'
    pg.evaluate("()=>{const s=JSON.parse(localStorage.getItem('kalsel2'));s.hp=99999;delete s.vis;delete s.sex;delete s.aff;s.comps.push('임시 동료 1');localStorage.setItem('kalsel2',JSON.stringify(s))}"); pg.reload(); pg.wait_for_timeout(300)
    s=S(pg); assert s['hp']==s['mhp'] and s['vis'] and s['sex']=='x' and s['aff']=={} and s['comps']==['kirien','oswin','ibre','kasimir','eno','barg']
    pg.evaluate("()=>{const s=JSON.parse(localStorage.getItem('kalsel2'));s.v=1;delete s.base;delete s.pro;s.loc='inn';localStorage.setItem('kalsel2',JSON.stringify(s))}"); pg.reload(); pg.wait_for_timeout(300)
    s=S(pg); assert s['v']==11 and s['base']==1 and s['pro']==99 and s['loc']=='base' and s['pit']==1 and not pg.is_visible('#pv .eo'); print('migrate ok')
    # ---- 패배: 본거지 없으면 여관에서 ----
    pg.evaluate("()=>{const K=window.__k2;K.S=null}"); pg.evaluate("window.__k2.render()")
    pg.fill('#cname','카인'); pg.click('button[data-c=start]'); pg.wait_for_timeout(100); pg.click('#pv [data-pv=skip]'); pg.click('#pv .eo'); pg.click('#pv [data-pv=close]')
    pg.evaluate("()=>{const K=window.__k2;K.S.loc='street';K.S.night=2;K.S.tutd=1;K.startBattle('fight','lamp')}")
    pg.evaluate("""()=>{const K=window.__k2;window.__b2=setInterval(()=>{const G=K.G;if(!G.on)return;const bo=document.querySelector('#bov.on .btn.pri');if(bo){bo.click();return}if(G.st==='player')K.bact('guard')},20)}""")
    pg.wait_for_function('!window.__k2.G.on',timeout=240000); h=okpop(pg); s=S(pg); print('lose ->',h,s['loc'])
    assert h=='쓰러졌다' and s['loc']=='docks' and s['sex']=='x' and not pg.evaluate("window.__k2.romOK('kirien')") and pg.evaluate("window.__k2.romOK('oswin')")
    # ---- 처음부터 ----
    pg.click('button[data-c=settings]'); pg.click('#sov >> text=처음부터 다시'); pg.click('#sov >> text=지우고 처음부터'); pg.wait_for_timeout(200)
    assert pg.evaluate('window.__k2.S') is None and pg.is_visible('#cname')
    b.close()
print('errors',errs); assert not errs; print('ALL OK')
