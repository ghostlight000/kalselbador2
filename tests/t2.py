from playwright.sync_api import sync_playwright
import pathlib
url=(pathlib.Path(__file__).resolve().parent.parent/'proto'/'index.html').as_uri()
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url); pg.wait_for_timeout(200)
    # 난이도 고르기 버튼
    pg.click('button[data-s=diff][data-v="2"]'); assert pg.evaluate("window.__k2.CFG.diff")==2
    pg.click('button[data-s=diff][data-v="1"]'); pg.click('text=바로 밤길로'); pg.click('text=맞선다'); pg.wait_for_timeout(100)
    J="""([kind,ofs])=>{const K=window.__k2,G=K.G;G.si=2;G.ph=1;G.st='enemy';G.cur='swing';G.lock=0;G.res={dodge:0,parry:0,hit:0,graze:0};
      const T=performance.now()+5000;G.beats=[{T,a:900,res:null,warned:true},{T:T+99999,a:900,res:null,warned:true}];
      K.press(kind,T+ofs);return G.beats[0].res||'whiff'}"""
    cases=[('dodge',0,'dodge'),('dodge',200,'dodge'),('dodge',-210,'dodge'),('dodge',-300,'graze'),('dodge',-400,'whiff'),('dodge',260,'whiff'),
           ('parry',0,'parry'),('parry',60,'parry'),('parry',100,'hit'),('parry',-200,'hit'),('parry',-300,'whiff')]
    for k,o,exp in cases:
        r=pg.evaluate(J,[k,o]); print(k,o,r); assert r==exp,(k,o,r,exp)
    b.close()
print('errors',errs); assert not errs
