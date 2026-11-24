"""v037: 2막 다듬기 — 기계의 조각, 불의 목자의 선물 — 검사실 → 천막촌의 노래 → 장로의 천막 → 고해소 → 정화자 숙소 → 지하 예배실 → 금서고가 열린다. 작은 장소·곁가지·부탁"""
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
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');E(pg,"window.__k2.endBattle('tut')");okpop(pg)
    # 곁가지 끝에 기계의 조각
    E(pg,"()=>{const K=window.__k2;K.sxStart('jobAc');K.sxEnd('jobAc','done',{});K.ev('빵집','<p>끝</p>',[['닫기',null]],1)}")
    t=pg.inner_text('#ov');assert '공급 대기' in t and '교단 위탁' in t,t;assert E(pg,"window.__k2.S.cogs.jobAc")==1
    okpop(pg)
    # 두 번째로는 붙지 않는다
    E(pg,"()=>{const K=window.__k2;K.ev('x','<p>y</p>',[['닫기',null]],1)}");assert '공급 대기' not in pg.inner_text('#ov');okpop(pg)
    # 선물 장면 세 갈래
    for k,want in [('d','가장 따뜻하구나'),('k','서랍'),('b','깜박였다')]:
        E(pg,"()=>{const K=window.__k2;K.S.gift=0;K.SCENE.gift()}");t=pg.inner_text('#ov');assert '매듭이 일곱' in t and '형제여' in t
        choose(pg,{'d':'마신다','k':'서랍 깊이','b':'문턱에'}[k]);assert want in pg.inner_text('#ov');okpop(pg);assert E(pg,"window.__k2.S.gift")==k
    assert E(pg,"window.__k2.S.inv.gvial")==1
    # 2막 셋째 단계 뒤 저택에 돌아오면 뜬다
    E(pg,"()=>{const K=window.__k2;K.S.gift=0;K.S.a2=3;K.S.base=1;K.S.pend=null}")
    # 저택 안은 전체 화면 글 모험, 나오면 보통 창으로
    E(pg,"()=>{const K=window.__k2;K.S.mz={};K.SCENE.manorIn()}");pg.wait_for_selector('#ov.on.ta .taimg svg');choose(pg,'오늘은 돌아간다')
    E(pg,"()=>{window.__k2.ev('x','<p>y</p>',[['닫기',null]],1)}");assert 'ta' not in pg.get_attribute('#ov','class');okpop(pg)
    # 우두머리 둘째 국면: 세 번째마다 결정타, 완전한 받아침으로 힘이 흩어진다
    E(pg,"()=>{const K=window.__k2;K.startBattle('fight','singer')}");pg.wait_for_timeout(300)
    ks=E(pg,"()=>{const K=window.__k2,G=K.G;G.ph=2;G.chg=0;return [K.bpick(),K.bpick(),K.bpick(),G.chg]}");assert ks[2]=='singSig' and ks[3]==0 and ks[0]!='singSig',ks
    v=E(pg,"()=>{const K=window.__k2,G=K.G;G.foe='warden';let n=0;for(let i=0;i<40;i++){G.ph=1;K.bpick();if(G.nbn)n++}G.foe='singer';return n}");assert v>0,v
    E(pg,"window.__k2.endBattle('win')")
    assert errs==[],errs
    print('errors',errs);print('ALL OK')
    b.close()
