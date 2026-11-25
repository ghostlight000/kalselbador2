from playwright.sync_api import sync_playwright
url='file:///home/claude/kalselbador2/index.html?test'
errs=[]
def choose(pg,t):pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(120)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E=lambda x:pg.evaluate(x)
    E("()=>{const K=window.__k2;K.joinComp('barg');K.joinComp('kirien');Object.assign(K.S,{bk:'leave',left:{barg:1},loc:'docks',party:'kirien'});K.S.aff.barg=20;K.render()}")
    for _ in range(4):
        if pg.locator('#ov.on').count():pg.locator('#ov.on button').last.click();pg.wait_for_timeout(150)
    print(pg.locator('#ov.on').count(),pg.locator('button[data-c=recon]').count(),pg.evaluate('window.__k2.S.loc'),pg.evaluate('JSON.stringify(window.__k2.S.left)'))
    pg.click('button[data-c=recon]');choose(pg,'돌아와 줘');assert '할 말을 들고' in pg.inner_text('#ov');choose(pg,'지붕을 내려간다')
    assert E("window.__k2.S.left.barg")==1
    pg.click('button[data-c=recon]');choose(pg,'베렌이 왜');choose(pg,'조금 떠오르는');assert '거짓말 냄새' in pg.inner_text('#ov');choose(pg,'지붕을 내려간다')
    pg.click('button[data-c=recon]');choose(pg,'베렌이 왜');choose(pg,'아무것도 떠오르지');choose(pg,'옆에');assert '내일 아침에 간다' in pg.inner_text('#ov');choose(pg,'지붕을 내려간다')
    assert E("window.__k2.S.left.barg")==1 and pg.locator('button[data-c=recon]').count()==0
    E("()=>{const K=window.__k2;K.S.brRet=Date.now()-1e9;K.S.loc='street';K.render()}")
    E("()=>{const K=window.__k2;K.CMD.go('base')}");pg.wait_for_timeout(1500)
    pg.wait_for_selector('#ov.on h2:has-text("현관")',timeout=8000);assert '옆자리는' in pg.inner_text('#ov');choose(pg,'들어와')
    assert E("window.__k2.S.left.barg")==0 and E("window.__k2.S.aff.barg")>=16
    print(errs);assert not errs;print('ALL OK')
    b.close()
