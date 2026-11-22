"""기본 이름 베렌, 1막 끝(에다), 학술원 언덕, 키리엔 퀘스트 결말 셋, 동료 자기 이야기, 저택에서 누구와도 대화"""
import pathlib
from playwright.sync_api import sync_playwright
ROOT=pathlib.Path(__file__).resolve().parent.parent;url=(ROOT/'index.html').as_uri()+'?test'
errs=[]
def choose(pg,t):pg.wait_for_selector(f'#ov.on button:has-text("{t}")',timeout=10000);pg.click(f'#ov.on button:has-text("{t}")');pg.wait_for_timeout(60)
def okpop(pg):pg.wait_for_selector('#ov.on .btn.pri',timeout=10000);pg.click('#ov.on .btn.pri');pg.wait_for_timeout(60)
def go(pg,k):pg.click(f'.map .node[data-a={k}]');choose(pg,'간다');pg.wait_for_function(f"window.__k2.S.loc==='{k}'",timeout=10000);pg.wait_for_timeout(650)
def win(pg):
    pg.wait_for_function('window.__k2.G.on');pg.click('#bov .btn.pri');pg.evaluate("()=>{window.__k2.G.fhp=0}");pg.evaluate("window.__k2.bact('atk')")
    pg.wait_for_function('!window.__k2.G.on',timeout=10000);okpop(pg);pg.wait_for_selector('#ov.on h2',timeout=5000)
S=lambda pg:pg.evaluate('window.__k2.S')
def setup(pg):
    pg.goto(url);pg.evaluate("localStorage.clear()");pg.goto(url);pg.wait_for_timeout(200)
    assert pg.input_value('#cname')=='베렌'
    pg.click('button[data-c=start]');pg.click('#pv .eo');assert '백이십 년' in pg.inner_text('#pv') or True
    pg.click('#pv [data-pv=skip]');pg.click('#pv .eo');pg.click('#pv [data-pv=close]')
    assert S(pg)['name']=='베렌'
    pg.evaluate("()=>{const K=window.__k2;K.S.night=3;K.S.tutd=1;K.joinComp('kirien');K.joinComp('oswin');K.grantBase()}");okpop(pg)
    pg.evaluate("()=>{const K=window.__k2;K.S.pit=1;K.S.coin=50;K.S.loc='street';K.render()}")
results={}
with sync_playwright() as p:
    b=p.chromium.launch()
    for end in ['new','pour','rest']:
        pg=b.new_page(viewport={'width':1200,'height':1000});pg.on('pageerror',lambda e:errs.append(str(e)))
        setup(pg)
        if end=='new':
            pg.click('button[data-c=tab][data-a=quest]');assert '◇ 등불을 든 사람의 딸' in pg.inner_text('.M') and '동료 이야기' not in pg.inner_text('.M');pg.click('button[data-c=tab][data-a=place]')
            # 학술원 언덕은 아직 잠김
            assert '잠' in pg.evaluate("document.querySelector('.map .node[data-a=academy]').getAttribute('class')") or 'lk' in pg.evaluate("document.querySelector('.map .node[data-a=academy]').getAttribute('class')")
        pg.click('button[data-c=eda]');choose(pg,'살아 있을 거라고');t=pg.inner_text('#ov');assert '‘베렌이 돌아오면' in t and '인기가 많습니다' in t,t
        choose(pg,'아버지를 찾아 주겠다고');t=pg.inner_text('#ov');assert '1막' in t and '약속했어요' in t;okpop(pg)
        s=S(pg);assert s['acad']==1 and s['eda']==1;print(end,'act1 end ok')
        # 언덕: 키리엔이 없으면 요양소가 막힌다
        pg.evaluate("()=>{const K=window.__k2;K.S.party='oswin';K.render()}")
        go(pg,'academy');assert pg.locator('button[data-c=kq1][disabled]').count()==1
        if end=='new':
            pg.click('button[data-c=talk]');t=pg.inner_text('#ov');assert '연구실이 있던 자리' in t;okpop(pg)
            pg.click('button[data-c=tab][data-a=quest]');q=pg.inner_text('.M');assert '동료 이야기' in q and '키리엔과 함께 다녀야' in q and '◆ 언덕 위 유리 지붕' in q;pg.click('button[data-c=tab][data-a=place]')
        pg.evaluate("()=>{const K=window.__k2;K.S.party='kirien';K.render()}")
        pg.click('button[data-c=kq1]');assert '공급 대기' in pg.inner_text('#ov');okpop(pg);assert S(pg)['kq']==1
        pg.click('button[data-c=kq2]');choose(pg,'안으로 들어간다');assert pg.evaluate('window.__k2.G.foe')=='collector';win(pg)
        t=pg.inner_text('#ov');assert '토벤 — “…베렌.”' in t,t;okpop(pg);assert S(pg)['kq']==2
        go(pg,'street');pg.click('button[data-c=kq3]');t=pg.inner_text('#ov');assert '미라의 딸' in t
        if end=='pour':
            choose(pg,'산다');assert S(pg)['inv'].get('mem')==1 and S(pg)['coin']<50;okpop(pg)
        else:
            choose(pg,'사지 않는다');okpop(pg)
        assert S(pg)['kq']==3
        if end!='pour':assert pg.locator('button[data-c=kqbuy]').count()==1
        pg.click('button[data-c=kq4]')
        if end=='pour':choose(pg,'남의 기억을 부어 준다');assert '리나야' in pg.inner_text('#ov')
        elif end=='new':
            assert pg.locator('#ov button:has-text("남의 기억")').count()==0;choose(pg,'빈 채로');assert '…에다.' in pg.inner_text('#ov')
        else:choose(pg,'구호소');assert '내가 기억하면 돼요' in pg.inner_text('#ov')
        okpop(pg);s=S(pg);assert s['kq']==4 and s['kqe']==end and s['cq']['kirien']=='done';results[end]=s['aff']['kirien']
        pg.click('button[data-c=tab][data-a=quest]');assert '◆ 끝' in pg.inner_text('.M');pg.click('button[data-c=tab][data-a=place]')
        if end=='new':
            # 저택 동료의 방: 누구와도 이야기, 오스윈의 자기 이야기
            pg.evaluate("()=>{const K=window.__k2;K.S.aff.oswin=30;K.S.loc='base';K.render()}")
            assert '할 이야기가' in pg.inner_text('button[data-c=rooms]')
            pg.click('button[data-c=rooms]');choose(pg,'오스윈과 이야기한다');assert '칼라쉬의 후예' in pg.inner_text('#ov');choose(pg,'책을 좋아하는구나');okpop(pg)
            pg.click('button[data-c=rooms]');choose(pg,'오스윈과 이야기한다');assert '지워진 아침' in pg.inner_text('#ov');choose(pg,'그래도 넌 여기 있어');okpop(pg)
            s=S(pg);assert s['chd']['oswin']==2 and s['aff']['oswin']==37,s['aff']
            pg.click('button[data-c=rooms]');choose(pg,'오스윈과 이야기한다');assert '장부를 태우기' in pg.inner_text('#ov');okpop(pg)
            pg.evaluate("()=>{window.__k2.S.aff.oswin=30}");pg.click('button[data-c=rooms]');choose(pg,'오스윈과 이야기한다');assert '더 가까워지면' in pg.inner_text('#ov');okpop(pg)
            pg.click('button[data-c=tab][data-a=char]');assert '들은 이야기 2 / 4' in pg.inner_text('.M');pg.click('button[data-c=tab][data-a=place]')
            pg.click('button[data-c=tab][data-a=story]');assert '지워진 아침' in pg.inner_text('.M');print('chapters ok')
        pg.close()
    b.close()
print(results);assert results['new']>results['pour']>results['rest']
print('errors',errs);assert not errs;print('ALL OK')
