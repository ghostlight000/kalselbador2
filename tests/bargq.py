"""v059: 바르그 퀘스트 「맹세의 끝」"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def listen(pg):
    for _ in range(12):
        if pg.locator('#ov.on button:has-text("말없이 듣는다")').count():choose(pg,'말없이 듣는다')
        else:break
def win(pg):
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{const G=window.__k2.G;G.fhp=0;if(G.pack)G.pack.forEach(p=>p.fhp=0)}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);okpop(pg)
E=lambda pg,x:pg.evaluate(x)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('barg');K.S.party='barg';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{pit:1,manor:1,mr:3,eda:1,acad:1,mg:1,mgh:'hide',rev:1,revd:1,a2:6,h2:4,bk:'stay',orx:{barg:1},mgt:{barg:1},loc:'base'});K.S.vis.academy=1;K.render()}")
    # 시작: 말을 걸면 꼬리표
    E(pg,"window.__k2.CMD.talk('barg')");pg.wait_for_timeout(100);assert '꼬리표' in pg.inner_text('#ov');listen(pg);choose(pg,'같이 가자');choose(pg,'이야기를 마친다')
    assert E(pg,"window.__k2.S.bq")==1
    pg.click('button[data-c=tab][data-a=quest]');t=pg.inner_text('.M');assert '바르그 — 맹세의 끝' in t and '천막의 기록' in t,t;pg.click('button[data-c=tab][data-a=place]')
    # 1 보존실
    E(pg,"()=>{const K=window.__k2;K.S.loc='pres';K.render()}");assert pg.locator('button[data-c=bq1]').count()==1
    pg.click('button[data-c=bq1]');choose(pg,'맞선다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("3번 천막의 장부")',timeout=5000);t=pg.inner_text('#ov');assert '그들의 맹세는 내가 거둔다' in t;choose(pg,'장부를 챙긴다')
    assert E(pg,"window.__k2.S.bq")==2
    # 2 천막촌 끝: 형제단의 밤 전에는 막힘
    E(pg,"()=>{const K=window.__k2;K.S.loc='outskirts';K.render()}");assert pg.locator('button[data-c=bq2][disabled]').count()==1
    E(pg,"()=>{const K=window.__k2;K.S.h2=5;K.render()}");pg.click('button[data-c=bq2]');choose(pg,'맞선다');win(pg)
    pg.wait_for_selector('#ov.on h2:has-text("겨울 아침")',timeout=5000);t=pg.inner_text('#ov');assert '끝내 못 풀고 갔다' in t;choose(pg,'이마의 재를 닦아 준다');choose(pg,'원을 떠난다')
    # v082 울릭 이야기: 질문 넷
    listen(pg);pg.wait_for_selector('#ov.on:has-text("울릭 이야기")',timeout=5000)
    for q in ['울릭은 어떤 사람이었어','맹세하던 날은 어땠어','교단 쪽에 섰어','다시 나란히 설 수 있을까']:
        choose(pg,q);listen(pg)
    t=pg.inner_text('#ov');assert '제 발로 걸었다' in t,t;choose(pg,'저택으로 돌아간다');listen(pg);choose(pg,'고개를 끄덕인다')
    assert len(E(pg,"window.__k2.S.bqUq"))==4
    s=E(pg,"window.__k2.S");assert s['bq']==3 and s['bqU']=='wipe'
    # 3 부두 지붕
    E(pg,"()=>{const K=window.__k2;K.S.loc='docks';K.render()}");pg.click('button[data-c=bq3]');listen(pg);choose(pg,'기다려 줘서 고마워');listen(pg);choose(pg,'지붕을 내려간다')
    assert E(pg,"window.__k2.S.bq")==4
    # 4 푸른 끈
    E(pg,"()=>{const K=window.__k2;K.S.loc='base';K.render()}");assert pg.locator('button[data-c=bq4]').count()==0;E(pg,"window.__k2.CMD.talk('barg')");listen(pg);choose(pg,'푸른 끈');listen(pg);choose(pg,'끈을 풀고 새 맹세를 받는다');choose(pg,'다시 생각한다');listen(pg);choose(pg,'끈을 풀고 새 맹세를 받는다');choose(pg,'이렇게 하기로 한다');listen(pg)
    t=pg.inner_text('#ov');assert '맹세의 끝」이 끝났다' in t;choose(pg,'고개를 끄덕인다')
    s=E(pg,"window.__k2.S");assert s['bq']==5 and s['bqe']=='new' and s['cq']['barg']=='done'
    pg.click('button[data-c=tab][data-a=quest]');t=pg.inner_text('.M');assert '끝낸 일' in t and '천막의 기록' not in t;pg.click('button[data-c=tab][data-a=place]')
    print('quest ok')
    # v082 끈 질문이 결말에 따라 바뀐다 · 다시 벼린 대검
    lab=lambda i:E(pg,f"(()=>{{const q=window.__k2.dlg().QA.barg[{i}][0];return typeof q==='function'?q(window.__k2.S):q}})()")
    assert lab(1)=='내 손목에 감아 준 끈 말이야.' and lab(0)=='그 대검은 어쩌다 부러졌어?'
    E(pg,"()=>{const K=window.__k2;K.S.loc='base';K.render()}");assert E(pg,"window.__k2.QTALK('barg').map(x=>x[1]).join()")=='bsw'
    pg.evaluate("window.__k2.CMD.bsw()");listen(pg);choose(pg,'하칸골에 같이 가기로 한다');assert E(pg,"window.__k2.S.bsw")==1
    E(pg,"()=>{const K=window.__k2;K.S.loc='works';K.S.party='barg';K.render()}");pg.click('button[data-c=bswF]')
    pg.wait_for_selector('#ov.on:has-text("다시 벼리는 날")',timeout=5000);assert '늙은 대장장이' in pg.inner_text('#ov')
    choose(pg,'지금 내 이름을 새긴다');listen(pg)
    for k in range(3):
        assert f'망치질 {k+1}/3' in pg.inner_text('#ov')
        if k==0:
            pos=lambda:E(pg,"(()=>{const b=document.getElementById('fgb').getBoundingClientRect(),m=document.getElementById('fgm').getBoundingClientRect();return (m.left+m.width/2-b.left)/b.width})()")
            x1=pos();pg.wait_for_timeout(250);x2=pos();assert 0<=x1<=1 and 0<=x2<=1 and abs(x1-x2)>0.02,(x1,x2)
        if k==1:E(pg,"()=>{window.__fgMiss=1}")
        choose(pg,'망치를 내리친다');E(pg,"()=>{window.__fgMiss=0}")
    assert E(pg,"window.__k2.S.bswH")==2;listen(pg);choose(pg,'날이 식기를 기다린다');listen(pg);assert '내 이름이 작게' in pg.inner_text('#ov')
    choose(pg,'새 칼을 축하한다');listen(pg);assert '20%' in pg.inner_text('#ov');choose(pg,'공방을 나선다')
    assert E(pg,"window.__k2.S.bsw")==2 and lab(0)=='검을 다시 벼리니까 어때?'
    print('bsw ok')
    # 떠나는 결말
    E(pg,"()=>{const K=window.__k2;K.S.bq=4;K.S.cq.barg=null;K.S.loc='base';K.render()}");pg.evaluate("window.__k2.CMD.bq4()");listen(pg);choose(pg,'끈을 풀어 그의 손에');choose(pg,'이렇게 하기로 한다');listen(pg);choose(pg,'떠나는 등을 본다')
    s=E(pg,"window.__k2.S");assert s['bqe']=='free' and s['left']['barg'] and s['party']!='barg'
    print('free ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
# v059 이야기 사건: 재의 서명 · 여덟 번째 종
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;K.S.night=3;K.S.mort=2;K.joinComp('ibre');K.joinComp('eno');K.S.party='ibre';K.grantBase()}");okpop(pg)
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{pit:1,manor:1,mr:3,eda:1,acad:1,mg:1,mgh:'hide',rev:1,revd:1,a2:6,orx:{ibre:1,eno:1},mgt:{ibre:1,eno:1},loc:'base'});K.render()}")
    E(pg,"window.__k2.CMD.talk('ibre')");pg.wait_for_timeout(100);assert '재의 서명' in pg.inner_text('#ov');listen(pg);choose(pg,'동생을 찾자');listen(pg);choose(pg,'이야기를 잇는다')
    assert E(pg,"window.__k2.S.rvt.ibre")==1
    E(pg,"()=>{document.querySelectorAll('#ov.on').forEach(e=>e.classList.remove('on'))}")
    E(pg,"()=>{const K=window.__k2;K.S.a3=1;K.S.loc='docks';K.render()}")
    pg.evaluate("()=>{const K=window.__k2;K.S.pend='a3Hearth';K.render()}");pg.wait_for_timeout(100)
    E(pg,"()=>window.__k2.SCENE.a3Hearth()");pg.wait_for_timeout(100);t=pg.inner_text('#ov');assert '여덟 번째 종' in t and '문을 지켰습니다' in t and '물이 조용해요' in t,t
    choose(pg,'나는 누구였을까');choose(pg,'불을 끈다');assert E(pg,"window.__k2.S.a3h")==1
    b.close()
print('events ok', errs);assert not errs
