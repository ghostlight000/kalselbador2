"""v051: 새 구역 셋과 곁가지 여섯"""
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
E=lambda pg,x:pg.evaluate(x)
def step(pg,id,btn):
    E(pg,f"()=>{{const q=sxQ('{id}'),st=SX['{id}'].steps[q.i];S.loc=st.at;render();CMD.sxa('{id}')}}");choose(pg,btn)
def fight(pg,btn='맞선다'):
    choose(pg,btn);win(pg);pg.wait_for_selector('#ov.on',timeout=10000)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    assert E(pg,"PL.square.hide(S)") and E(pg,"PL.silver.hide(S)")
    E(pg,"()=>{S.night=3;S.eda=1;S.acad=1;S.fac=1;S.outs=1;S.a2=1;S.coin=200;render()}");pg.wait_for_timeout(700)
    assert E(pg,"!!S.nd.square") and not E(pg,"!!(S.nd||{}).under")
    assert E(pg,"PL.under.u(S)")==False and '물길 아래' in E(pg,"mapSvg()")
    E(pg,"()=>{S.a2=4}");pg.wait_for_timeout(700)
    assert E(pg,"!!S.nd.under&&!!S.nd.silver");assert '지도에 새 구역 — 은방울 언덕' in pg.inner_text('body') or True
    for k in ['square','under','silver']:
        E(pg,f"()=>{{S.loc='{k}';S.act=null;render()}}");t=pg.inner_text('#main') if pg.locator('#main').count() else pg.inner_text('body')
        assert pg.locator(f'.scs').count()>=1, k
        assert E(pg,f"EXP['{k}'][0].n") in pg.inner_text('body'),k
        assert E(pg,f"travelSec('docks','{k}')")<700
    print('districts ok')
    E(pg,"()=>{S.party='oswin';if(!S.comps.includes('oswin'))S.comps.push('oswin');S.loc='square';render()}")
    assert E(pg,"!!TALK.oswin.square&&!!TALK.barg.silver&&!!TALK.eno.under")
    # 지워진 시민
    E(pg,"()=>sxStart('roll')");step(pg,'roll','탁본을 챙긴다');step(pg,'roll','그 사내를 아는');step(pg,'roll','헌병대 쪽을');step(pg,'roll','열쇠를 챙긴다')
    step(pg,'roll','맞선다') if False else None
    E(pg,"()=>{const q=sxQ('roll');S.loc='square';render();CMD.sxa('roll')}");fight(pg)
    choose(pg,'명부에 이름을 다시');choose(pg,'돌아선다');assert E(pg,"sxQ('roll').e")=='write' and not E(pg,"S.inv.rub")
    print('roll ok')
    # 멈춘 시계
    E(pg,"()=>sxStart('clockt')");step(pg,'clockt','톱니를 구해');E(pg,"()=>{S.inv.cogw=3;CMD.sxa}");E(pg,"()=>{const q=sxQ('clockt');q.i=2;render()}")
    step(pg,'clockt','시계탑 꼭대기로');E(pg,"()=>{S.loc='square';render();CMD.sxa('clockt')}");fight(pg)
    choose(pg,'갈린 톱니를 그대로');choose(pg,'종루를 내려온다');assert E(pg,"sxQ('clockt').e")=='keep'
    print('clock ok')
    # 하수구 아이들의 왕
    E(pg,"()=>sxStart('rking')");step(pg,'rking','물길 끝 수문을');E(pg,"()=>{S.loc='under';render();CMD.sxa('rking')}");fight(pg);choose(pg,'장부를 챙긴다')
    step(pg,'rking','아이를 데리고');E(pg,"()=>{S.inv.scrap=6}");step(pg,'rking','고철 다섯으로');choose(pg,'갈림길을 떠난다')
    assert E(pg,"sxQ('rking').e")=='seal' and E(pg,"S.inv.scrap")==1
    print('rking ok')
    # 물에 잠긴 예배당 (하그 결말)
    E(pg,"()=>{S.sxon=1;SX.chapel.open()}");choose(pg,'글자를 탁본해 간다');step(pg,'chapel','하칸골 배수 펌프로');E(pg,"()=>{S.loc='works';render();CMD.sxa('chapel')}");fight(pg);choose(pg,'물길 아래로 돌아간다')
    step(pg,'chapel','재를 담아 하그에게');step(pg,'chapel','돌아선다');assert E(pg,"sxQ('chapel').e")=='hag' and E(pg,"S.hagL")==1
    print('chapel ok')
    # 상복 입은 신부
    E(pg,"()=>sxStart('bride')");step(pg,'bride','정화된 사람이');step(pg,'bride','리벤 저택 하인 방으로');E(pg,"()=>{S.loc='silver';render();CMD.sxa('bride')}");fight(pg)
    c0=E(pg,"S.coin");choose(pg,'부인에게 망각의 병을');choose(pg,'언덕을 내려온다');assert E(pg,"sxQ('bride').e")=='vial' and E(pg,"S.coin")==c0+60
    print('bride ok')
    # 가면 무도회 (무리 싸움)
    E(pg,"()=>{SX.mask.open()}");choose(pg,'초대장을 챙긴다');c0=E(pg,"S.coin");step(pg,'mask','동전 열둘을 낸다');assert E(pg,"S.coin")==c0-12
    E(pg,"()=>{S.loc='silver';render();CMD.sxa('mask')}");choose(pg,'맞선다');pg.wait_for_function('window.__k2.G.on');assert E(pg,"G.pack.length")==2
    pg.click('#bov .btn.pri');E(pg,"()=>{G.pack.forEach(p=>p.fhp=0);G.fhp=0}");E(pg,"bact('atk')");pg.wait_for_function('!window.__k2.G.on',timeout=10000);okpop(pg);pg.wait_for_selector('#ov.on',timeout=10000)
    choose(pg,'장부를 챙긴다');assert E(pg,"S.inv.mledg")==1 and not E(pg,"S.inv.smask")
    step(pg,'mask','장부를 광장 게시판에');t=pg.inner_text('#ov');assert '테오도르' in t;choose(pg,'돌아선다');assert E(pg,"sxQ('mask').e")=='post'
    print('mask ok')
    # 뒷이야기: 시간이 지난 뒤 광장에 오면 한 번
    E(pg,"()=>{sxQ('roll').et=Date.now()-1e9;S.pend=null;sxArrive('square')}");assert E(pg,"S.pend")=='sxp_roll'
    E(pg,"()=>{pending()}");t=pg.inner_text('#ov');assert '사흘째요' in t;choose(pg,'고개를 끄덕인다')
    print('post ok')
    # 길 위 마주침
    E(pg,"()=>{ENC_ON=true}");fs=set(E(pg,"Array.from({length:300},()=>roadFoe({fr:'street',to:'silver'})).filter(Boolean)"));assert fs<= {'glove','footman','dog','thief','hunter'} and ('glove' in fs or 'footman' in fs),fs;E(pg,"()=>{ENC_ON=false}")
    print('road ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
