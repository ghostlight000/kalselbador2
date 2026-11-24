"""여관에서 동료 바꾸기, 이동 시간, 길 위 마주침, 저택 손보기·꾸미기·서재·함께 먹기"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on button[data-c=popok]',timeout=10000);pg.click('#ov.on button[data-c=popok]');pg.wait_for_timeout(60)
def go(pg,k):pg.eval_on_selector(f'.map .node[data-a={k}]',"e=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}))");choose(pg,'간다');pg.wait_for_function(f"window.__k2.S.loc==='{k}'",timeout=10000);pg.wait_for_timeout(650);(pg.is_visible('#ov.on h2:has-text("대성당")') and (choose(pg,'고개를 숙인다'),choose(pg,'대성당을 나선다')));(pg.is_visible('#ov.on h2:has-text("문 앞의 상자")') and (choose(pg,'서랍 깊이'),choose(pg,'서랍을 닫는다')))
def waitact(pg):pg.wait_for_function('!window.__k2.S.act',timeout=10000);pg.wait_for_timeout(650)
S=lambda pg:pg.evaluate('window.__k2.S')
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200);pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    # 이동 시간: 1분 이상
    t=pg.evaluate("window.__k2.travelSec('docks','street')");assert 600<=t<=900,t
    assert pg.evaluate("window.__k2.travelSec('docks','base')")>=300;print('travel',t)
    # 키리엔 합류(같이 가자) → 오스윈은 여관으로
    pg.evaluate("()=>{const K=window.__k2;K.S.night=3;K.S.tutd=1;K.render();K.SCENE.kirien()}")
    choose(pg,'못 알아들었다고');choose(pg,'말하지 않는다');choose(pg,'같이 가자');choose(pg,'좋다')
    pg.evaluate("()=>{window.__k2.SCENE.osw2()}");assert pg.locator('#ov button:has-text("같이 가자")').count()==0
    choose(pg,'함께하자');t=pg.inner_text('#ov');assert '신탁 상점의 딸이지요' not in t and '쫓겨난 사람 냄새' in t and '여관 1층에서 기다린다' in t,t;choose(pg,'계속 다닌다')
    s=S(pg);assert s['party']=='kirien' and s['comps']==['kirien','oswin'];print('send to inn ok')
    # 여관에서 바꾸기 (여관 소문 창이 먼저 뜰 수 있다)
    pg.wait_for_timeout(700)
    if pg.is_visible('#ov.on'):choose(pg,'브리타를 찾아가')
    pg.click('button[data-c=rooms]');assert '여관 1층' in pg.inner_text('#ov h2');assert pg.locator('#ov.on button').count()==2;choose(pg,'함께 나갈 동료를 고른다');choose(pg,'오스윈과 나간다');assert S(pg)['party']=='oswin';print('inn swap ok')
    # 길 위 마주침
    pg.evaluate("()=>{const K=window.__k2;K.ENC_ON=true;K._r=Math.random;Math.random=()=>0.01}")
    go(pg,'street');pg.wait_for_selector('#ov.on h2:has-text("길 위에서")',timeout=5000);assert '지름길이' in pg.inner_text('#ov')
    choose(pg,'돌아서 달아난다');pg.evaluate("()=>{Math.random=window.__k2._r;window.__k2.ENC_ON=false}")
    if pg.is_visible('#ov.on button[data-c=popok]'):okpop(pg)
    assert S(pg)['loc']=='street';print('road encounter ok')
    # 저택
    pg.evaluate("()=>{const K=window.__k2;K.grantBase();K.S.coin=100;K.S.inv.scrap=20;K.S.loc='base';K.render()}");choose(pg,'짐을 옮긴다')
    assert pg.locator('button[data-c=deco][disabled]').count()==1 and pg.locator('button[data-c=read]').count()==0
    pg.click('button[data-c=fix]');assert pg.locator('#ov button:has-text("부엌 고치기")').count()==0;choose(pg,'지붕 고치기');waitact(pg);t=pg.inner_text('#ov');assert '새 기와' in t and '문명으로' in t;okpop(pg)
    # 그만두면 돌려받기
    c0=S(pg)['coin'];pg.click('button[data-c=fix]');choose(pg,'마차 창고 고치기');assert S(pg)['coin']==c0-8;pg.click('button[data-c=cancel]');assert S(pg)['coin']==c0 and S(pg)['inv']['scrap']==18;print('refund ok')
    for k in ['벽난로와 거실','부엌','서재','마차 창고']:
        pg.click('button[data-c=fix]');choose(pg,k+' 고치기');waitact(pg);okpop(pg)
    s=S(pg);assert all(s['fix'].get(k) for k in ['roof','hearth','kitchen','study','coach']);assert '고친 곳 5 / 8' in pg.inner_text('.M')
    assert pg.evaluate("window.__k2.travelSec('docks','street')")<t if False else pg.evaluate("window.__k2.travelSec('docks','street')")<=0.6*900;print('all fixed, coach travel',pg.evaluate("window.__k2.travelSec('docks','street')"))
    # 꾸미기
    c0=S(pg)['coin'];pg.click('button[data-c=deco]');choose(pg,'벽지 바꾸기');choose(pg,'짙은 포도주빛');t=pg.inner_text('#ov');assert '잉크 얼룩' in t;choose(pg,'좋다');assert S(pg)['coin']==c0-6
    pg.click('button[data-c=deco]');choose(pg,'벽지 바꾸기');choose(pg,'벗겨진 회벽');choose(pg,'좋다');pg.click('button[data-c=deco]');choose(pg,'벽지 바꾸기');choose(pg,'짙은 포도주빛');choose(pg,'좋다');assert S(pg)['coin']==c0-6;print('deco owned ok')
    pg.click('button[data-c=deco]');choose(pg,'바닥 바꾸기');choose(pg,'잉그라드 직물');choose(pg,'좋다')
    assert '포도주빛 벽지' in pg.inner_text('.place-d') and '잉그라드 직물' in pg.inner_text('.place-d')
    assert pg.evaluate('window.__k2.comfort()')>=8 and pg.evaluate('window.__k2.comfortT()')=='아늑하다';print('comfort',pg.evaluate('window.__k2.comfort()'))
    # 서재
    xp0=S(pg)['xp']+S(pg)['lv']*1000;pg.click('button[data-c=read]');waitact(pg);t=pg.inner_text('#ov');assert '오르빌 상회 장부' in t;okpop(pg);assert S(pg)['read']['0']==1;print('read ok')
    # 함께 먹기: 체력 가득해도 쉴 수 있고, 호감 +2. 바로 다시는 없다
    a0=S(pg)['aff'];pg.click('button[data-c=rest]');waitact(pg);t=pg.inner_text('#ov');assert '수프' in t and '아늑한 거실' in t;okpop(pg)
    a1=S(pg)['aff'];assert a1['kirien']==a0['kirien']+1 and a1['oswin']==a0['oswin']+1,(a0,a1)
    pg.evaluate("()=>{window.__k2.S.meal=Date.now()+1e9;window.__k2.render()}");assert pg.locator('button[data-c=rest][disabled]').count()==1;print('meal ok')
    # 저장 이전: v5 저장에 기본값
    pg.evaluate("()=>{const K=window.__k2;const o=JSON.parse(JSON.stringify(K.S));o.v=5;delete o.fix;delete o.deco;delete o.own;delete o.read;localStorage.setItem('kalsel2',JSON.stringify(o));K.load()}")
    s=S(pg);assert s['v']==12 and s['fix']=={} and s['deco']['mantel']=='face';print('migrate v6 ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
