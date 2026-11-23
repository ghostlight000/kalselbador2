"""v030 대화: NPC 주제별 대화(브리타·하그·오델·아벨), 동료의 '다른 사람들 이야기', 대화 창 머리와 말 줄 정리"""
import pathlib
from playwright.sync_api import sync_playwright
src=open(pathlib.Path(__file__).resolve().parent/'bargeno.py').read().split('with sync_playwright() as p:')[0]
exec(src)
with sync_playwright() as p:
    b=p.chromium.launch();pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
    start(pg)
    E(pg,"()=>{const K=window.__k2;K.S.aevT=Date.now();K.S.orx={kirien:1,oswin:1};K.S.mr=3;K.S.loc='street';K.S.night=3;K.render()}")
    # 브리타
    pg.click('button[data-c=ntalk][data-a=brita]');t=pg.inner_text('#ov');assert '점등 장대' in t and '늙은 점등꾼' in t and pg.locator('#ov .tkh').count()==1,t
    choose(pg,'토벤을 알아?');t=pg.inner_text('#ov');assert '내 뒤를 이은 점등꾼' in t and pg.locator('#ov .tkb b').count()==0,t
    choose(pg,'다른 것도 묻는다');t=pg.inner_text('#ov');assert '점등 장대' not in t
    choose(pg,'이야기를 그만둔다')
    # 동료: 다른 사람들 이야기
    E(pg,"window.__k2.CMD.talk('kirien')");choose(pg,'다른 사람들 이야기');t=pg.inner_text('#ov');assert '오스윈' in t and '마그다' not in t and 'pit' not in t and '바르그' not in t,t
    choose(pg,'오스윈은 어때?');t=pg.inner_text('#ov');assert '끝까지 들으면' in t and '오스윈 이야기' in t,t
    choose(pg,'이야기를 그만둔다')
    # 하그·오델·아벨: 만난 뒤에만
    E(pg,"()=>{const K=window.__k2;K.S.loc='outskirts';K.S.outs=1;K.S.hq=0;K.render()}");assert pg.locator('button[data-c=ntalk][data-a=hag]').count()==0
    E(pg,"()=>{const K=window.__k2;K.S.hq=3;K.S.hm=1;K.render()}");pg.click('button[data-c=ntalk][data-a=hag]');assert '부엉이 머리' in pg.inner_text('#ov');choose(pg,'겨울 시대는 어땠어?');assert '노래가 있었어' in pg.inner_text('#ov');choose(pg,'이야기를 그만둔다')
    E(pg,"()=>{const K=window.__k2;K.S.loc='pawn';K.S.kq=3;K.render()}");pg.click('button[data-c=ntalk][data-a=odel]');choose(pg,'미라를 기억해?');assert '여우 귀' in pg.inner_text('#ov');choose(pg,'이야기를 그만둔다')
    E(pg,"()=>{const K=window.__k2;K.S.loc='church';K.S.sx.bell={i:1,r:1};K.render()}");pg.click('button[data-c=ntalk][data-a=abel]');t=pg.inner_text('#ov');assert '종지기' in t and '일곱째 문' not in t;choose(pg,'이야기를 그만둔다')
    # 일반 장면 말 줄 정리: 이름표
    h=E(pg,"window.__k2.sayFmt('<p>오델 — “하나.”</p><p>오델 — “둘.”</p><p class=\"m\">쉼</p><p>오델 — “셋.”</p>')");assert h.count('<b>오델</b>')==2,h
    print('errors',errs);assert not errs
    b.close()
print('ALL OK')
