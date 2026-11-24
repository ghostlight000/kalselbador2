"""v050: 동시에 나오는 여러 적"""
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
    E(pg,"()=>{S.night=3;S.mort=2;CFG.auto=true;startBattle('fight','dog',['dog','thief'])}");pg.click('#bov [data-bo=fgo]');pg.wait_for_function("window.__k2.G.st==='player'",timeout=15000)
    assert E(pg,"G.pack.length")==3 and pg.locator('#bpack .pkc').count()==3
    pg.click('#bpack .pkc[data-pk="2"]');assert E(pg,"G.foe")=='thief' and E(pg,"G.ti")==2
    E(pg,"()=>{G.fhp=1}");pg.click('[data-ba=atk]')
    pg.wait_for_function("window.__k2.G.st==='player'&&window.__k2.G.turn>=2",timeout=30000)
    assert E(pg,"G.pack[2].fhp")<=0 and E(pg,"G.foe")=='dog' and E(pg,"G.on")
    assert pg.locator('#bpack .pkc.dead').count()==1
    print('target switch ok')
    E(pg,"()=>{G.fhp=1}");pg.click('[data-ba=atk]');pg.wait_for_function("window.__k2.G.st==='player'&&window.__k2.G.turn>=3",timeout=30000)
    assert len(E(pg,"pkAlive()"))==1
    E(pg,"()=>{G.fhp=1}");pg.click('[data-ba=atk]');pg.wait_for_function('!window.__k2.G.on',timeout=15000)
    t=pg.inner_text('#ov');assert '굶주린 골목개 · 굶주린 골목개 · 가스등 도둑' in t and '모두 쓰러졌다' in t,t;okpop(pg)
    print('pack win ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
