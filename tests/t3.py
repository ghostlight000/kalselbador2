import sys
from playwright.sync_api import sync_playwright
import pathlib
url=(pathlib.Path(__file__).resolve().parent.parent/'proto'/'index.html').as_uri()
errs=[]
BOT="""(mode)=>{const K=window.__k2;
 window.__bot=setInterval(()=>{
  const ov=document.querySelector('#ov.on .btn.pri'); if(ov&&!window.__hold){ov.click();return}
  const G=K.G,t=performance.now();
  if(G.st==='player'){K.act(G.fp>=2&&G.tut==null?'heavy':'atk');return}
  if(G.st==='qte'&&G.q&&!G.q.done){const p=(t-G.q.t0)/G.q.dur;if(p>=(G.q.z[0]+G.q.z[1])/2)K.press('qte',t);return}
  if(G.st==='enemy'&&mode!=='none'){
    const b=G.beats.filter(b=>!b.res).sort((x,y)=>x.T-y.T)[0];
    if(b&&t>=b.T-4){let k=mode;if(G.tut!=null)k=K.TS[G.tut].goal==='parry'?'parry':'dodge';K.press(k,t)}}
 },4);}"""
def page(b):
    pg=CTX.new_page(); pg.on('pageerror',lambda e:errs.append(str(e))); pg.goto(url); pg.wait_for_timeout(200); return pg
with sync_playwright() as p:
    b=p.chromium.launch()
    global CTX
    CTX=b.new_context(viewport={'width':520,'height':900})
    # 1. 가르침 전체 → 밤길 → 승리 (받아치기)
    pg=page(b)
    assert pg.is_visible('text=가르침부터')
    pg.click('text=가르침부터'); pg.evaluate(BOT,'parry')
    pg.wait_for_function("localStorage.getItem('k2tut')==='1'",timeout=120000)
    print('tutorial done; flag',pg.evaluate("localStorage.getItem('k2tut')"))
    seen=set()
    pg.wait_for_function("window.__k2.G.st==='end'",timeout=300000)
    print('run end:',pg.inner_text('#ov h2'),pg.evaluate("window.__k2.G.si"),pg.evaluate("window.__k2.G.S.full"))
    assert pg.inner_text('#ov h2')=='점등꾼이 쓰러졌다'
    pg.close()
    # 2. 가르침 완료 뒤 제목 버튼이 바뀌는지
    pg=page(b); assert pg.is_visible('text=가르침 다시 받기'); 
    # 3. 아무것도 안 누르면 첫 적에게 지고 '이 자리에서 다시'
    pg.click('text=밤길 나서기'); pg.evaluate(BOT,'none')
    pg.wait_for_function("window.__k2.G.st==='end'",timeout=300000)
    si=pg.evaluate("window.__k2.G.si"); print('none ->',pg.inner_text('#ov h2'),'stage',si)
    pg.evaluate("clearInterval(window.__bot)"); pg.click('text=이 자리에서 다시'); pg.wait_for_timeout(100)
    assert pg.evaluate("window.__k2.G.si")==si and pg.evaluate("window.__k2.G.hp")==100
    pg.close()
    # 4. 가르침 건너뛰기
    pg=page(b); pg.click('text=가르침 다시 받기'); pg.wait_for_timeout(100); pg.click('text=해 보지'); pg.wait_for_timeout(200)
    pg.click('#bstop'); pg.wait_for_timeout(700); print('skip ->',pg.inner_text('#ov h2')); pg.close()
    # 5. 단계별 판정 넓이 확인
    pg=page(b)
    w=pg.evaluate("""()=>{const K=window.__k2,out=[];K.start('run');const G=K.G;
      for(let i=0;i<3;i++){G.si=i;G.ph=1;out.push(Math.round(K.W().d))} G.ph=2;out.push(Math.round(K.W().d));G.si=0;G.tut=0;out.unshift(Math.round(K.W().d));return out}""")
    print('dodge window by stage (tut,dog,thief,boss,boss2):',w); assert w==sorted(w,reverse=True)
    b.close()
print('errors',errs); assert not errs
