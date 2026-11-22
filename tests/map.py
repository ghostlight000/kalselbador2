"""지도: 확대·축소 버튼, 휠, 끌기, 현재 위치로, 끈 뒤 클릭 막기, 다시 그려도 유지"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    pg.goto(url);pg.wait_for_timeout(200);pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]')
    MW=lambda:pg.evaluate('window.__k2.MW');vb=lambda:pg.get_attribute('.map','viewBox')
    w0=MW()['w'];assert w0==92
    pg.click('button[data-c=mapzoom][data-a="1.3"]');pg.click('button[data-c=mapzoom][data-a="1.3"]');m=MW();print('zoom in',m);assert m['w']<60 and vb()==f"{m['x']} {m['y']} {m['w']} {m['h']}"
    # 다시 그려도 유지
    pg.click('button[data-c=rumor]');pg.click('#ov .btn.pri');assert vb()==f"{m['x']} {m['y']} {m['w']} {m['h']}"
    # 끌기: 장소 위에서 시작해도 끈 뒤에는 장소 창이 열리지 않는다
    box=pg.locator('#mapw').bounding_box();cx,cy=box['x']+box['width']/2,box['y']+box['height']/2
    x0=MW()['x'];pg.mouse.move(cx,cy);pg.mouse.down();pg.mouse.move(cx-120,cy-60,steps=6);pg.mouse.up();pg.wait_for_timeout(50)
    m2=MW();print('drag',m2);assert m2['x']!=x0 and not pg.is_visible('#ov.on')
    # 휠
    w1=MW()['w'];pg.mouse.move(cx,cy);pg.mouse.wheel(0,-300);pg.wait_for_timeout(50);assert MW()['w']<w1;print('wheel ok',MW()['w'])
    # 최대 확대 제한
    for i in range(10):pg.click('button[data-c=mapzoom][data-a="1.3"]')
    assert abs(MW()['w']-92/3.2)<1e-6;print('max zoom ok')
    # 현재 위치로: 운하 부두(22,60)가 가운데
    pg.click('button[data-c=mapcenter]');m=MW();print('center',m);assert abs(m['x']+m['w']/2-22)<0.01 or m['x']==4
    # 확대한 채로 장소 누르기
    pg.click('button[data-c=mapzoom][data-a="0.77"]');pg.click('button[data-c=mapzoom][data-a="0.77"]');pg.click('button[data-c=mapzoom][data-a="0.77"]')
    assert pg.locator('.map .node[data-a=street]').is_visible();pg.click('.map .node[data-a=street]');assert '가스등 거리' in pg.inner_text('#ov h2');pg.click('#ov button:has-text("그만둔다")');print('click while zoomed ok')
    # 끝까지 축소
    for i in range(10):pg.click('button[data-c=mapzoom][data-a="0.77"]')
    m=MW();assert m['w']==92 and m['x']==4 and m['y']==12;print('zoom out full ok')
    # 휴대폰 폭에서도 버튼이 보인다
    pg.set_viewport_size({'width':390,'height':844});pg.wait_for_timeout(100);assert pg.is_visible('button[data-c=mapcenter]')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
