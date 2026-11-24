"""지도(v019, 1편 방식): 고정 높이 창, 확대·축소 버튼, 휠, 끌기, 현재 위치로, 끈 뒤 클릭 막기, 다시 그려도 유지, 이동하면 새 위치로"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200);pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]');pg.click('#ov.on button:has-text("막대를 쥔 노인을 따라간다")');pg.click('#ov.on button:has-text("막대 앞에 선다")');pg.wait_for_function('window.__k2.G.on');pg.evaluate("window.__k2.endBattle('tut')");pg.click('#ov.on .btn.pri')
    MP=lambda:pg.evaluate('({...window.__k2.MW})');tf=lambda:pg.evaluate("document.querySelector('.map').style.transform")
    pg.locator('#mapw').scroll_into_view_if_needed()
    box=pg.locator('#mapw').bounding_box();assert 400<=box['height']<=440,box
    m=MP();assert m['s']==1
    # 처음엔 현재 위치(운하 부두)가 창 가운데
    nb=pg.locator('.map .node[data-a=inn] rect').bounding_box();assert box['x']<nb['x']<box['x']+box['width'] and box['y']<nb['y']<box['y']+box['height'],(nb,box)
    pg.click('button[data-c=mapzoom][data-a="1.3"]');pg.click('button[data-c=mapzoom][data-a="1.3"]');m=MP();assert m['s']>1.6 and abs(float(tf().split('scale(')[1].rstrip(')'))-MP()['s'])<1e-3
    # 다시 그려도 유지
    pg.click('button[data-c=rumor]');pg.click('#ov button:has-text("이야기를 그만둔다")');assert abs(float(tf().split('scale(')[1].rstrip(')'))-MP()['s'])<1e-3 and MP()['x']==m['x']
    # 끌기: 장소 위에서 시작해도 끈 뒤에는 장소 창이 열리지 않는다
    cx,cy=box['x']+box['width']/2,box['y']+box['height']/2
    x0=MP()['x'];pg.mouse.move(cx,cy);pg.mouse.down();pg.mouse.move(cx-120,cy-60,steps=6);pg.mouse.up();pg.wait_for_timeout(50)
    m2=MP();assert abs(m2['x']-(x0-120))<1 and not pg.is_visible('#ov.on'),m2;print('drag ok')
    # 휠: 커서 아래 지점이 고정
    s1=MP()['s'];pg.mouse.move(cx,cy);pg.mouse.wheel(0,300);pg.wait_for_timeout(50);assert MP()['s']<s1;print('wheel ok')
    for i in range(12):pg.click('button[data-c=mapzoom][data-a="1.3"]')
    assert abs(MP()['s']-2.2)<1e-9
    for i in range(14):pg.click('button[data-c=mapzoom][data-a="0.77"]')
    smin=MP()['s'];assert smin<0.7;print('zoom range ok',smin)
    # 축소한 채로 장소 누르기
    pg.click('.map .node[data-a=street]');assert '가스등 거리' in pg.inner_text('#ov h2');pg.click('#ov button:has-text("간다")')
    pg.wait_for_function("window.__k2.S.loc==='street'",timeout=10000);pg.wait_for_timeout(700)
    # 도착하면 새 위치가 가운데
    nb=pg.locator('.map .node[data-a=street] rect').bounding_box();box=pg.locator('#mapw').bounding_box()
    assert abs(nb['x']+nb['width']/2-(box['x']+box['width']/2))<6,(nb,box);print('recenter ok')
    # 현재 위치로
    pg.mouse.move(cx,cy);pg.mouse.down();pg.mouse.move(cx+150,cy,steps=5);pg.mouse.up();pg.click('button[data-c=mapcenter]')
    nb=pg.locator('.map .node[data-a=street] rect').bounding_box();assert abs(nb['x']+nb['width']/2-(box['x']+box['width']/2))<6
    # 휴대폰 폭
    pg.set_viewport_size({'width':390,'height':844});pg.wait_for_timeout(100);assert pg.is_visible('button[data-c=mapcenter]') and pg.locator('#mapw').bounding_box()['height']<=345
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
