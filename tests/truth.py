from playwright.sync_api import sync_playwright
url='file:///home/claude/kalselbador2/index.html?test'
errs=[]
def choose(pg,t):pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(120)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]')
    E=lambda x:pg.evaluate(x)
    E("()=>{const K=window.__k2;['kirien','ibre','kasimir','eno','oswin'].forEach(c=>K.joinComp(c));Object.assign(K.S,{orx:{kirien:1,ibre:1,kasimir:1,eno:1,oswin:1},mgt:{kirien:1,ibre:1,kasimir:1,eno:1,oswin:1},rev:1,rvt:{kirien:1,ibre:1,kasimir:1,eno:1},oq:6,oq0:1,cq:{kasimir:'done',ibre:'done'},zq:4,iq:5,nq:1,kq:1,zqe:'age',iqe:'ledger',route:'ext',c3:4,loc:'silver',party:'kasimir',romNo:{kirien:1,oswin:1,kasimir:1}});K.render()}")
    # 요즘 어때 — 진실 대사 풀에서만
    pool=E("()=>JSON.stringify(window.__k2.MOODT?1:0)")
    for _ in range(6):
        E("()=>{window.__k2.CMD.talk('kasimir')}");pg.wait_for_timeout(150)
        if pg.locator('#ov.on button:has-text("물어보고 싶은")').count():choose(pg,'물어보고 싶은')
        choose(pg,'요즘 어때');t=pg.inner_text('#ov')
        assert any(k in t for k in ['촛불','흰 머리카락','붉은 물','별이 보입니다','표정']),t
        pg.keyboard.press('Escape');E("()=>{const K=window.__k2;K.S.act=null;document.querySelector('#ov').classList.remove('on')}")
    E("()=>{window.__k2.CMD.talk('kasimir')}");pg.wait_for_timeout(150)
    if pg.locator('#ov.on button:has-text("물어보고 싶은")').count():choose(pg,'물어보고 싶은')
    choose(pg,'이곳은 어때');t=pg.inner_text('#ov');assert '줄 하나치고는' in t,t
    E("()=>{document.querySelector('#ov').classList.remove('on');const K=window.__k2;K.S.loc='square';K.S.party='ibre';K.render();K.CMD.talk('ibre')}");pg.wait_for_timeout(150)
    if pg.locator('#ov.on button:has-text("물어보고 싶은")').count():choose(pg,'물어보고 싶은')
    choose(pg,'이곳은 어때');t=pg.inner_text('#ov');assert '결투장 장부에 있습니다' in t,t
    r=E("()=>{const K=window.__k2;return [K.S.bk,JSON.stringify(K.moodT?1:0)]}")
    print(errs);assert not errs;print('ALL OK')
    b.close()
