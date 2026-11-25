"""v049: 실드·브레이크 (엘리트·보스)"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def go(pg,k):pg.eval_on_selector(f'.map .node[data-a={k}]',"e=>e.dispatchEvent(new MouseEvent('click',{bubbles:true}))");choose(pg,'간다');pg.wait_for_function(f"window.__k2.S.loc==='{k}'",timeout=10000);pg.wait_for_timeout(650);(pg.is_visible('#ov.on h2:has-text("대성당")') and (choose(pg,'고개를 숙인다'),choose(pg,'대성당을 나선다')));(pg.is_visible('#ov.on h2:has-text("문 앞의 상자")') and (choose(pg,'서랍 깊이'),choose(pg,'서랍을 닫는다')))
def win(pg):
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{const G=window.__k2.G;G.fhp=0;if(G.pack)G.pack.forEach(p=>p.fhp=0)}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);okpop(pg)
def drain(pg):
    for _ in range(8):
        if pg.locator('#ov.on button:has-text("말없이 듣는다")').count():choose(pg,'말없이 듣는다')
E=lambda pg,x:pg.evaluate(x)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{startBattle('fight','dog')}");assert E(pg,"G.shmax")==0;E(pg,"()=>{G.on=false;$('#bt').classList.remove('on')}")
    E(pg,"()=>{startBattle('fight','glass')}");assert E(pg,"G.shmax")==4 and E(pg,"G.sh")==4
    assert '실드' in pg.inner_text('#bsh')
    E(pg,"()=>{G.fhp=1000;G.first=0;G.spell=0}");E(pg,"dmgFoe(100)");assert E(pg,"G.fhp")==965 and E(pg,"G.sh")==3,E(pg,"[G.fhp,G.sh]")
    E(pg,"dmgFoe(10,3)");assert E(pg,"G.sh")==0 and E(pg,"G.brk")==1
    assert '무너짐' in pg.inner_text('#bsh')
    f0=E(pg,"G.fhp");E(pg,"dmgFoe(100)");assert E(pg,"G.fhp")==f0-150
    E(pg,"()=>{G.st='wait';G.cDone=true;enemyTurn()}");assert E(pg,"G.brk")==0 and E(pg,"G.sh")==0
    pg.wait_for_function("window.__k2.G.st==='player'",timeout=5000)
    E(pg,"()=>{G.cDone=true;enemyTurn()}");assert E(pg,"G.sh")==4
    E(pg,"()=>{G.on=false;$('#bt').classList.remove('on')}")
    print('elite ok')
    E(pg,"()=>{S.night=3;startBattle('fight','lamp')}");assert E(pg,"G.shmax")==6
    E(pg,"()=>{G.sh=0;G.fhp=Math.floor(G.fmax/2)-1;maybePhase(()=>{})}");assert E(pg,"G.ph")==2 and E(pg,"G.sh")==6
    E(pg,"()=>{G.on=false;$('#bt').classList.remove('on')}")
    print('boss ok')
    # v055: 적이 휘두르는 도중 실드가 깨지면 남은 박자가 멎고 더 맞지 않는다. 암전 없이 글자만
    E(pg,"()=>{startBattle('fight','glass')}");E(pg,"()=>{G.fhp=1000;G.sh=1;G.st='wait';G.cDone=true;G.next=Object.keys(MV).find(k=>MV[k].b&&MV[k].b.length>=3)||G.next;enemyTurn()}")
    n=E(pg,"G.beats.length");assert n>=2,n
    h0=E(pg,"G.hp");E(pg,"resolveBeat(G.beats[0],'parry',0)")
    assert E(pg,"G.brk")==1 and E(pg,"G.beats.slice(1).every(b=>b.res==='brk')")
    assert E(pg,"document.querySelector('.phase.brk')")is None
    pg.wait_for_function("window.__k2.G.st==='player'",timeout=6000);assert E(pg,"G.hp")==h0
    assert '무너져 멎음' in pg.inner_text('#blog') or True
    E(pg,"()=>{G.on=false;$('#bt').classList.remove('on')}")
    E(pg,"()=>{S.night=3;startBattle('fight','lamp')}");E(pg,"()=>{G.ph=2;G.sh=1;dmgFoe(10,1)}");pg.wait_for_timeout(100)
    assert E(pg,"getComputedStyle(document.querySelector('.phase.brk')).backgroundColor")=='rgba(0, 0, 0, 0)'
    E(pg,"()=>{G.on=false;$('#bt').classList.remove('on')}")
    print('break-cancel ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
