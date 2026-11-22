import pathlib,sys
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test';OUT=pathlib.Path(sys.argv[1] if len(sys.argv)>1 else '/tmp/shots');OUT.mkdir(exist_ok=True)
with sync_playwright() as p:
    b=p.chromium.launch()
    for th in ['dark','light']:
        for w,h,tag in [(1280,900,'wide'),(390,844,'phone')]:
            pg=b.new_page(viewport={'width':w,'height':h},color_scheme=th); pg.goto(url); pg.wait_for_timeout(300)
            pg.screenshot(path=str(OUT/f'{th}-{tag}-create.png'),full_page=True)
            pg.fill('#cname','레아'); pg.click('button[data-c=start]'); pg.wait_for_timeout(150)
            pg.screenshot(path=str(OUT/f'{th}-{tag}-intro.png'))
            pg.click('#ov .btn.pri'); pg.evaluate("()=>{const S=window.__k2.S;S.disp.push({id:'lamp',t0:Date.now(),d:600});S.log.unshift('가스등 거리에서 돌아왔다.');window.__k2.render()}")
            pg.wait_for_timeout(150); pg.screenshot(path=str(OUT/f'{th}-{tag}-inn.png'),full_page=True)
            pg.close()
    b.close()
