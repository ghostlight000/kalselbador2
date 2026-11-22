import sys,time
from playwright.sync_api import sync_playwright
import pathlib
url=(pathlib.Path(__file__).resolve().parent.parent/'proto'/'index.html').as_uri()
errs=[]
BOT="""(mode)=>{ // mode: parry|dodge|none
 const K=window.__k2;
 window.__bot=setInterval(()=>{
  const G=K.G,t=performance.now();
  if(G.st==='player'){K.act(G.fp>=2?'heavy':'atk');return}
  if(G.st==='qte'&&G.q&&!G.q.done){const p=(t-G.q.t0)/G.q.dur;const mid=(G.q.z[0]+G.q.z[1])/2;if(p>=mid)K.press('qte',t);return}
  if(G.st==='enemy'&&mode!=='none'){for(const b of G.beats){if(!b.res&&t>=b.T-4){K.press(mode,t);break}}}
 },4);}"""
with sync_playwright() as p:
    b=p.chromium.launch()
    for mode,expect in [('parry','점등꾼이 쓰러졌다'),('none','쓰러졌다')]:
        pg=b.new_page(viewport={'width':520,'height':900})
        pg.on('pageerror',lambda e:errs.append(str(e)))
        pg.goto(url); pg.wait_for_timeout(300)
        pg.click('text=싸우기')
        pg.evaluate(BOT,mode)
        pg.wait_for_function("window.__k2.G.st==='end'",timeout=180000)
        h=pg.inner_text('#ov h2'); S=pg.evaluate("window.__k2.G.S"); ph=pg.evaluate("window.__k2.G.ph")
        print(mode,'->',h,'phase',ph,{k:S[k] for k in ['dodge','parry','hit','whiff','full','perf','qte']})
        assert h==expect,(h,expect)
        pg.close()
    # practice mode + settings pause
    pg=b.new_page(viewport={'width':520,'height':900}); pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url); pg.wait_for_timeout(200); pg.click('text=박자 연습')
    pg.evaluate(BOT,'dodge'); pg.wait_for_timeout(6000)
    S=pg.evaluate("window.__k2.G.S"); print('practice',S['dodge'],S['hit']); assert S['dodge']>=2 and S['hit']==0
    pg.evaluate("clearInterval(window.__bot)")
    pg.wait_for_function("window.__k2.G.st==='enemy'"); pg.click('#bset'); pg.wait_for_timeout(200)
    assert pg.evaluate("window.__k2.G.st")=='wait'
    pg.click('text=닫기'); pg.wait_for_function("window.__k2.G.st==='enemy'",timeout=3000); print('pause/resume ok')
    pg.click('#bstop'); pg.wait_for_timeout(200); print('practice end:',pg.inner_text('#ov h2'))
    b.close()
print('errors',errs); assert not errs
