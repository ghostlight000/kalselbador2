"""v048: 장비 칸·헌병대 불하품점·우두머리 전리품·막별 적 강화"""
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
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{S.coin=200;S.loc='street';render()}")
    m0=E(pg,"S.mhp")
    pg.click('button[data-c=shopE]');t=pg.inner_text('#ov');assert '헌병대 사브르' in t and '하칸 강철 칼' not in t and '언덕 너머 일이' in t
    choose(pg,'헌병대 사브르 사기');assert E(pg,"S.eq.wpn")=='sabre';choose(pg,'가게로 돌아간다')
    choose(pg,'누빈 외투 사기');choose(pg,'가게로 돌아간다');choose(pg,'가게를 나선다')
    assert E(pg,"S.eq.body")=='quilt' and E(pg,"S.mhp")==m0+8 and E(pg,"S.coin")==200-E(pg,"px(22)")-E(pg,"px(18)")
    E(pg,"()=>{S.eda=1;render()}");pg.click('button[data-c=shopE]');t=pg.inner_text('#ov');assert '하칸 강철 칼' in t and '맨몸으로' in t;choose(pg,'가게를 나선다')
    print('shop ok')
    # 막별 강화
    E(pg,"()=>{startBattle('fight','dog')}");assert E(pg,"G.fmax")==81;E(pg,"()=>{G.on=false;$('#bt').classList.remove('on')}")
    E(pg,"()=>{S.rev=1}");E(pg,"()=>{startBattle('fight','dog')}");assert E(pg,"G.fmax")==91;E(pg,"()=>{G.on=false;$('#bt').classList.remove('on');S.rev=0}")
    # 장비 효과
    E(pg,"()=>{startBattle('fight','dog')}");E(pg,"()=>{G.fhp=500;G.first=0;G.spell=0}");E(pg,"dmgFoe(100)");assert E(pg,"G.fhp")==390,E(pg,"G.fhp")
    E(pg,"()=>{G.hp=200;G.mhp=200;G.scale=1}");E(pg,"hurt(100)");assert E(pg,"G.hp")==106,E(pg,"G.hp");E(pg,"()=>{G.on=false;$('#bt').classList.remove('on')}")
    print('effects ok')
    # 우두머리 전리품
    E(pg,"()=>{S.night=3;S.mort=2;render();startBattle('fight','lamp')}");pg.click('#bov [data-bo=fgo]');E(pg,"()=>{G.fhp=0}");E(pg,"window.__k2.bact('atk')");pg.wait_for_function('!window.__k2.G.on',timeout=10000)
    t=pg.inner_text('#ov');assert '점등꾼의 놋쇠 갈고리' in t,t;okpop(pg)
    E(pg,"()=>{EV0=null;POP=null;S.pend=null;V='char';render()}");t=pg.inner_text('.M');assert '장비' in t and '헌병대 사브르' in t
    pg.click('button[data-c=eqpick][data-a=trk]');choose(pg,'놋쇠 갈고리 갖추기');assert E(pg,"S.eq.trk")=='hook'
    E(pg,"()=>{EV0=null;startBattle('fight','dog')}");assert E(pg,"G.fp")==3;E(pg,"()=>{G.on=false;$('#bt').classList.remove('on')}")
    print('drop ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
