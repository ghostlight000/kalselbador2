"""v084 연인 장면(이야기하기 ✦) · 마지막 밤 · 로맨스 상대와의 밤"""
from playwright.sync_api import sync_playwright
url='file:///home/claude/kalselbador2/index.html?test'
E=lambda pg,x:pg.evaluate(x)
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def listen(pg):
    for _ in range(6):
        b=pg.locator('#ov.on button:has-text("말없이 듣는다")')
        if b.count():b.first.click();pg.wait_for_timeout(60)
        else:break
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page();errs=[];pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    E(pg,"()=>{const K=window.__k2;['kirien','oswin','barg','ibre'].forEach(c=>K.joinComp(c));K.grantBase();K.EV0=null}")
    for _ in range(8):
        pg.wait_for_timeout(120)
        if pg.locator('#ov.on .btn.pri').count():pg.click('#ov.on .btn.pri')
        else:break
    # 연인 장면: 마음을 나눈 뒤 시간이 지나면 이야기하기 첫 화면에
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{rom:'kirien',loc:'base',party:'kirien',orx:{kirien:1,oswin:1,barg:1,ibre:1}});K.S.romAtId='kirien';K.S.romAt=0;K.render()}")
    assert E(pg,"window.__k2.romxDue('kirien')")==1
    E(pg,"window.__k2.CMD.talk('kirien')");choose(pg,'연인의 시간 — 다음 날 아침');listen(pg);choose(pg,'좋아해. 어제도 오늘도');choose(pg,'곁에 머문다')
    assert E(pg,"window.__k2.romxDue('kirien')")==0
    E(pg,"()=>{window.__k2.S.romx.kirien[1]=1}");assert E(pg,"window.__k2.romxDue('kirien')")==2
    E(pg,"window.__k2.CMD.talk('kirien')");choose(pg,'안 잃어버릴 사람 목록');listen(pg);choose(pg,'키리엔의 엄마 이름을');assert '미라' in pg.inner_text('#ov');choose(pg,'곁에 머문다')
    # 마지막 밤: 불을 끄는 길 마지막 단계 앞
    E(pg,"()=>{const K=window.__k2;Object.assign(K.S,{a3:1,c3:4,route:'ext',xt:5,xtc:'out',xtO1:1,xtO2:1,xtK:1,xtCu:1,xtO:1,xtD:1,xtA:1,xtCo:1,xtSv:1,pit:1});K.render()}")
    assert E(pg,"window.__k2.lnDue()") and pg.locator('button[data-c=lastN]').count()==1
    E(pg,"()=>{const K=window.__k2;K.S.loc='stairs';K.render()}");assert pg.locator('button[data-c=xt4]').is_disabled()
    E(pg,"()=>{const K=window.__k2;K.S.loc='base';K.render()}");pg.click('button[data-c=lastN]')
    t=pg.inner_text('#ov');assert '점은 사양하겠다' in t and '문틀은 다 높였습니다' in t,t
    choose(pg,'내일 내 이름을 불러 줘');assert '피트' in pg.inner_text('#ov');choose(pg,'곁에 남는다');listen(pg);choose(pg,'약속할게');choose(pg,'새벽을 맞는다')
    assert E(pg,"window.__k2.S.lastN")==1 and E(pg,"window.__k2.S.romF")=='kirien'
    E(pg,"()=>{const K=window.__k2;K.S.loc='stairs';K.render()}");assert not pg.locator('button[data-c=xt4]').is_disabled()
    print('lastn ok',errs);assert not errs
    b.close()
