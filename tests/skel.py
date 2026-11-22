"""뼈대 전체 경로 테스트: 만들기 → 1편 기록 → 이동 → 파견 → 가르침 → 순찰 3번(밤 끝) → 교단 구역 → 기록 코드 → 새로고침"""
import pathlib,gzip,base64,json
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent
url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
leg=json.dumps({'name':'테오르<script>','race':'p','og':'칼라쉬','tr':'남색 서리비늘','end':'k','pa':'fox','inv':{}},ensure_ascii=False).encode()
LEG='KS1.'+base64.b64encode(gzip.compress(leg)).decode()
BOT="""()=>{const K=window.__k2;window.__bot=setInterval(()=>{const G=K.G,t=performance.now();if(!G.on)return;
  const bo=document.querySelector('#bov.on .btn.pri');if(bo){bo.click();return}
  if(G.st==='player'){K.bact(G.fp>=2&&G.kind!=='tut'?'heavy':'atk');return}
  if(G.st==='qte'&&G.q&&!G.q.done){const p=(t-G.q.t0)/G.q.dur;if(p>=(G.q.z[0]+G.q.z[1])/2)K.press('qte',t);return}
  if(G.st==='enemy'){const b=G.beats.filter(b=>!b.res).sort((x,y)=>x.T-y.T)[0];if(b&&t>=b.T-4){let k='parry';if(G.kind==='tut'&&K.TS[G.tut].goal==='dodge')k='dodge';K.press(k,t)}}},4)}"""
def okpop(pg):
    pg.wait_for_selector('#ov.on .btn',timeout=20000); t=pg.inner_text('#ov h2'); pg.click('#ov.on .btn.pri'); return t
with sync_playwright() as p:
    b=p.chromium.launch(); ctx=b.new_context(viewport={'width':1200,'height':900}); pg=ctx.new_page()
    pg.on('pageerror',lambda e:errs.append(str(e))); pg.on('console',lambda m:m.type=='error' and 'ERR_TUNNEL' not in m.text and 'fonts.g' not in m.text and errs.append(m.text))
    pg.goto(url); pg.wait_for_timeout(300)
    assert pg.evaluate('window.__k2.TEST')
    # 만들기
    pg.fill('#cname','레아'); pg.click('button[data-c=race][data-a=b]'); pg.click('button[data-c=trait][data-a="1"]'); pg.click('button[data-c=origin][data-a="1"]')
    pg.click('text=1편의 기록이 있다면'); pg.fill('#legt',LEG); pg.click('button[data-c=legread]'); pg.wait_for_timeout(200)
    t=pg.inner_text('.cr'); assert '불을 이어받은 자' in t and '<script>' not in t, t[-300:]
    pg.click('button[data-c=start]'); pg.wait_for_timeout(150)
    # 시작 연출: 네 장 + 제목. 처음 누르면 줄이 다 뜨고, 다시 누르면 넘어간다
    assert pg.is_visible('#pv .eo'); first=pg.inner_text('#pv')
    for i in range(4):
        pg.click('#pv .eo'); pg.click('#pv .eo'); pg.wait_for_timeout(50)
        t=pg.inner_text('#pv')
        if i==1: assert '레아는' in t and '용 사냥꾼' in t, t   # 출신 1 = 용 사냥꾼 일족의 후예
        if i==2: assert '불지기' in t, t                     # 1편 엔딩 k의 소문
    pg.click('#pv .eo'); pg.click('#pv [data-pv=close]'); pg.wait_for_timeout(100)
    S=pg.evaluate('window.__k2.S'); print('made',S['name'],S['race'],S['og'],S['st'],S['loc'],S['pro']); assert S['pro']==99 and S['loc']=='street' and not S['base']
    # 본거지 전: 여관·파견이 보이지 않는다
    assert pg.locator('button[data-c=go][data-a=inn]').count()==0 and pg.locator('button[data-c=board]').count()==0
    assert pg.is_disabled('button[data-c=go][data-a=church]')
    # 순찰 → 가르침 권유 → 가르침
    pg.click('button[data-c=patrol]'); pg.click('#ov button:has-text("가르침을 받는다")'); pg.wait_for_function('window.__k2.G.on')
    pg.evaluate(BOT)
    pg.wait_for_function('!window.__k2.G.on',timeout=120000); print('tut:',okpop(pg)); assert pg.evaluate('window.__k2.S.tutd')==1
    for i in range(3):
        pg.wait_for_timeout(300)
        if pg.evaluate('window.__k2.S.hp')<pg.evaluate('window.__k2.S.mhp')*0.6:
            pg.click('button[data-c=rest]'); okpop(pg)
        pg.click('button[data-c=patrol]')
        pg.wait_for_function('window.__k2.G.on',timeout=10000); foe=pg.evaluate('window.__k2.G.foe')
        pg.wait_for_function('!window.__k2.G.on',timeout=200000); h=okpop(pg)
        S=pg.evaluate('window.__k2.S'); print(foe,'->',h,'hp',S['hp'],'night',S['night'])
        if h=='쓰러졌다': raise SystemExit('lost to '+foe)
    # 첫 번째 밤 → 본거지 장면
    pg.wait_for_selector('#ov.on h2'); assert pg.inner_text('#ov h2')=='잿빛 사슴 여관'; assert '여우 모양 문진' in pg.inner_text('#ov'); okpop(pg)
    S=pg.evaluate('window.__k2.S'); assert S['base']==1 and S['inv'].get('relic')==1 and S['night']==3 and S['inv'].get('wick')==1
    pg.click('button[data-c=go][data-a=inn]'); pg.wait_for_function("window.__k2.S.loc==='inn'",timeout=10000); pg.wait_for_timeout(600)
    # 파견
    pg.click('button[data-c=board]'); pg.click('#ov button:has-text("시장 심부름")'); pg.wait_for_timeout(100)
    pg.wait_for_function("document.querySelector('#ov.on h2')&&document.querySelector('#ov.on h2').textContent==='파견에서 돌아왔다'",timeout=10000)
    b0=S['inv'].get('band',0); okpop(pg); S=pg.evaluate('window.__k2.S'); print('dispatch ->',S['inv'],S['coin']); assert S['inv']['band']==b0+1
    pg.click('button[data-c=go][data-a=church]'); pg.wait_for_function("window.__k2.S.loc==='church'",timeout=10000); pg.wait_for_timeout(600)
    pg.click('button[data-c=tab][data-a=quest]'); q=pg.inner_text('.M'); print('quest now:',[l for l in q.split('\n') if '◇' in l]); assert '뼈대는 여기까지' in q
    pg.click('button[data-c=tab][data-a=story]'); assert '테오르' in pg.inner_text('.M')
    pg.click('button[data-c=tab][data-a=char]'); assert '용 사냥꾼 일족의 후예' in pg.inner_text('.M')
    # 기록 코드 왕복
    code=pg.evaluate('window.__k2.scode()'); assert code.startswith('KS2.')
    o=pg.evaluate('c=>window.__k2.sdecode(c)',code); assert o['night']==3 and o['name']=='레아'
    # 새로고침 뒤 이어 하기
    pg.reload(); pg.wait_for_timeout(300); assert pg.evaluate('window.__k2.S.loc')=='church'
    # 옛 저장 이전: 체력 이상값
    pg.evaluate("()=>{const s=JSON.parse(localStorage.getItem('kalsel2'));s.hp=99999;delete s.vis;localStorage.setItem('kalsel2',JSON.stringify(s))}"); pg.reload(); pg.wait_for_timeout(300)
    S=pg.evaluate('window.__k2.S'); assert S['hp']==S['mhp'] and S['vis']
    pg.evaluate("()=>{const s=JSON.parse(localStorage.getItem('kalsel2'));s.v=1;delete s.base;delete s.pro;s.loc='inn';s.og=2;localStorage.setItem('kalsel2',JSON.stringify(s))}"); pg.reload(); pg.wait_for_timeout(300)
    S=pg.evaluate('window.__k2.S'); assert S['v']==2 and S['base']==1 and S['pro']==99 and S['loc']=='inn' and not pg.is_visible('#pv .eo'); print('v1 migrate ok')
    # 처음부터 다시
    pg.click('button[data-c=settings]'); pg.click('#sov >> text=처음부터 다시'); pg.click('#sov >> text=지우고 처음부터'); pg.wait_for_timeout(200)
    assert pg.evaluate('window.__k2.S') is None and pg.is_visible('#cname')
    # 지는 경우: 아무것도 누르지 않고 점등꾼과 싸우면 여관에서 눈을 뜬다
    pg.evaluate("()=>{const K=window.__k2;K.S=null}")
    pg.fill('#cname','패배'); pg.click('button[data-c=start]'); pg.wait_for_timeout(100); pg.click('#pv [data-pv=skip]'); pg.click('#pv .eo'); pg.click('#pv [data-pv=close]')
    pg.evaluate("()=>{const K=window.__k2;K.S.loc='street';K.S.night=2;K.S.tutd=1;K.startBattle('fight','lamp')}")
    pg.evaluate("""()=>{const K=window.__k2;window.__b2=setInterval(()=>{const G=K.G;if(!G.on)return;const bo=document.querySelector('#bov.on .btn.pri');if(bo){bo.click();return}if(G.st==='player')K.bact('guard')},20)}""")
    pg.wait_for_function('!window.__k2.G.on',timeout=200000); h=okpop(pg); S=pg.evaluate('window.__k2.S'); print('lose ->',h,S['loc'],S['hp'],S['mhp'])
    assert h=='쓰러졌다' and S['loc']=='street' and S['hp']==-(-S['mhp']*3//10)
    b.close()
print('errors',errs); assert not errs; print('ALL OK')
