from playwright.sync_api import sync_playwright
url='file:///home/claude/kalselbador2/index.html?test'
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]')
    r=pg.evaluate("()=>{const K=window.__k2;K.joinComp('barg');K.joinComp('kirien');K.S.aff.barg=40;K.S.left={barg:1};K.aff('barg',5);const a=K.S.aff.barg;K.S.left.barg=0;K.aff('barg',1);return [a,K.S.aff.barg]}")
    print(r,errs);assert r[0]==40 and r[1]==41 and not errs
    b.close()
