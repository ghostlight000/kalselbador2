"""개발자 창: 보이는 조건과 각 버튼"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;base=(ROOT/'index.html').as_uri()
errs=[]
with sync_playwright() as p:
    b=p.chromium.launch();ctx=b.new_context(viewport={'width':1200,'height':900});pg=ctx.new_page()
    pg.on('pageerror',lambda e:errs.append(str(e)))
    # 1. 그냥 열면 보이지 않는다
    pg.goto(base);pg.wait_for_timeout(300);assert pg.is_hidden('#devb') and not pg.evaluate('window.__k2.DEV');print('plain: hidden')
    # 2. #dev로 열면 보인다(내 컴퓨터 파일)
    pg.goto(base+'#dev');pg.reload();pg.wait_for_timeout(300);assert pg.is_visible('#devb');print('#dev: visible')
    pg.goto(base+'?test');pg.wait_for_timeout(300)
    pg.click('button[data-c=start]');pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]')
    pg.click('#devb');assert pg.is_visible('#dov .dev')
    pg.click('#dov [data-dv=coin]');pg.click('#dov [data-dv=band]');S=pg.evaluate('window.__k2.S');assert S['coin']==55 and S['inv']['band']==7
    pg.click('#dov [data-dv=leg]');assert pg.evaluate('window.__k2.S.legacy.end')=='k'
    pg.click('#dov [data-dv=night][data-a="3"]');pg.click('#dov [data-dv=comp]');pg.click('#dov [data-dv=close]');pg.wait_for_timeout(800)
    assert not pg.is_visible('#ov.on') and not pg.evaluate('window.__k2.S.base')
    pg.click('#devb');pg.click('#dov [data-dv=comp]');pg.click('#dov [data-dv=close]');pg.wait_for_timeout(800)
    assert pg.inner_text('#ov h2')=='잿빛 사슴 여관';assert '여우 모양 문진' in pg.inner_text('#ov');pg.click('#ov .btn.pri');print('2 companions → base ok')
    # 즉시 완료: ?test에서는 이미 빠르니 끄고 켜는 표시만 확인
    pg.click('#devb');t=pg.inner_text('#dov [data-dv=fast]');print('fast btn:',t);pg.click('#dov [data-dv=close]')
    # 격노 직전 점등꾼 → 공격 한 번이면 격노 → 즉시 승리
    pg.click('#devb');pg.click('#dov [data-dv=fight][data-a=lamp2]');pg.wait_for_timeout(200)
    assert pg.is_visible('#bdev');pg.click('#bov .btn.pri');pg.evaluate("window.__k2.bact('heavy')")
    pg.wait_for_function("window.__k2.G.st==='qte'");pg.wait_for_timeout(500);pg.keyboard.press('Space')
    pg.wait_for_function("window.__k2.G.ph===2",timeout=5000);print('phase 2 reached')
    pg.wait_for_timeout(2600);pg.click('#bdev [data-bdev=win]');pg.wait_for_function('!window.__k2.G.on',timeout=5000)
    h=pg.inner_text('#ov h2');print('win ->',h);assert '점등꾼' in h;pg.click('#ov .btn.pri')
    # 즉시 패배
    pg.click('#devb');pg.click('#dov [data-dv=fight][data-a=dog]');pg.click('#bov .btn.pri');pg.click('#bdev [data-bdev=lose]');pg.wait_for_function('!window.__k2.G.on',timeout=5000)
    assert pg.inner_text('#ov h2')=='쓰러졌다';pg.click('#ov .btn.pri')
    # 진행 중인 일 끝내기(빠른 모드 끄고)
    pg.evaluate("()=>{window.__k2.TEST}")
    pg.click('#devb');pg.click('#dov [data-dv=state]');assert '"night": 3' in pg.input_value('#dvs');pg.click('#dov [data-dv=close]')
    # 시작 연출 다시
    pg.click('#devb');pg.click('#dov [data-dv=pro]');assert pg.is_visible('#pv .eo');print('prologue replay ok')
    b.close()
print('errors',errs);assert not errs;print('ALL OK')
