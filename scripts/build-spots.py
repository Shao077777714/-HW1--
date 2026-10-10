from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
teacher=json.loads((ROOT/'data/teacher-sources.json').read_text(encoding='utf-8'))
cities=json.loads((ROOT/'data/cities.json').read_text(encoding='utf-8'))
rows={r['source_id']:r for r in teacher['rows']}
photos=json.loads((ROOT/'data/spot-photos.json').read_text(encoding='utf-8'))
spots=[]
def add(id,zh,ja,area,lat,lon,source,feature,access,stars=4,period=None,period_url=None,city='東京',region='東京',caveat=None,access_url=None):
    r=rows.get(source)
    spots.append({'id':id,'name':zh,'name_ja':ja,'area':area,'region':region,'city':city,'lat':lat,'lon':lon,'coordinate_note':'園區／街道代表定位點（人工約略定位，非每株銀杏或精確入口）','source_ids':[source] if r else [],'group_id':r['group_id'] if r else source,'teacher_rows':[r['row_number']] if r else [],'url':r['url'] if r else period_url,'feature':feature,'access':access,'access_url':access_url or (r['url'] if r else period_url),'stars':stars,'reason':feature+'；'+('交通便利、適合初次賞杏。' if stars==5 else '適合慢步觀察與安排附近散步。'),'historical_period':period,'period_source':period_url,'period_basis':'官方例年時期' if period else '氣象廳城市標本木平年黃葉日至落葉日，僅為城市參考','current_observation':None,'observation_date':None,'last_checked':'2026-10-08','caveat':caveat or (r['caveat'] if r else '未取得2026景點實測；出發前查官方公告。')})
parks=[
('ueno','上野恩賜公園','上野恩賜公園','台東區',35.7147,139.7736,'TKG-002','公園銀杏與博物館散步','JR／地鐵上野站；詳見官網交通案內',5),
('kiba','木場公園','木場公園','江東區',35.6747,139.8074,'TKG-003','寬闊綠地中的銀杏秋色','東京地鐵木場站；詳見官網交通案內',4),
('koganei','小金井公園','小金井公園','小金井市',35.7160,139.5165,'TKG-004','大尺度公園的銀杏散步','由JR武藏小金井站轉巴士；請核對官方交通',4),
('shiba','芝公園','芝公園','港區',35.6554,139.7477,'TKG-005','銀杏與東京鐵塔城市景觀','都營芝公園站；詳見官網交通案內',4),
('johoku','城北中央公園','城北中央公園','板橋區・練馬區',35.7571,139.6775,'TKG-006','運動綠地的銀杏秋色','東武上板橋站或地鐵冰川台站；詳見官網',4),
('zenpukuji','善福寺川綠地','善福寺川緑地','杉並區',35.6899,139.6338,'TKG-007','河岸綠地的銀杏散步','東京地鐵南阿佐谷站；請核對官方交通',4),
('wadabori','和田堀公園','和田堀公園','杉並區',35.6825,139.6429,'TKG-008','河岸公園的緩步行程','京王井之頭線西永福站；請核對官方交通',4),
('toyama','戶山公園','戸山公園','新宿區',35.7050,139.7100,'TKG-009','市區公園銀杏與日常風景','西早稻田站／東新宿站，依園區入口選擇',4),
('hikarigaoka','光丘公園・銀杏並木','光が丘公園・イチョウ並木','練馬區',35.7678,139.6315,'TKG-010','長長銀杏並木的秋日散步','都營大江戶線光丘站；詳見官網交通案內',5),
('hibiya','日比谷公園','日比谷公園','千代田區',35.6734,139.7561,'TKG-011','都心老銀杏與園景','日比谷站／霞關站；施工動線請查官網',4),
('yoyogi','代代木公園','代々木公園','澀谷區',35.6726,139.6947,'TKG-012','草地與銀杏的輕鬆散步','代代木公園站步行約3分鐘（東京官方旅遊指南）',4),
('iwasaki','舊岩崎邸庭園','旧岩崎邸庭園','台東區',35.7098,139.7672,'TKG-013','洋館與銀杏構成的庭園風景','千代田線湯島站1號出口步行約3分鐘',4)]
for p in parks: add(*p)
add('hikari-path','光丘公園・交流小徑','光が丘公園・ふれあいの径','練馬區',35.7666,139.635,'TKG-010','公園小徑上的銀杏觀察','都營大江戶線光丘站；位置為小徑代表點',4,caveat='與銀杏並木分開定位；沒有獨立子地點實測。')
showa_url='https://www.showakinen-koen.jp/flower-information/'
add('showa-canal','昭和記念公園・運河並木','国営昭和記念公園・カナール','立川市',35.7046,139.4061,'TKG-014','運河旁的黃金隧道','JR立川站北口至立川入口約18分鐘（官網）',5,['10-21','11-30'],showa_url,access_url='https://www.showakinen-koen.jp/access/')
add('showa-katarai','昭和記念公園・語らい並木','国営昭和記念公園・かたらいのイチョウ並木','立川市・昭島市',35.7104,139.3963,'TKG-014','林蔭路的銀杏黃金隧道','JR西立川站至西立川入口約2分鐘；入園後步行',5,['10-21','11-30'],showa_url,access_url='https://www.showakinen-koen.jp/access/')
add('shinjuku','新宿御苑','新宿御苑','新宿區',35.6852,139.7100,'TKG-015','庭園裡的銀杏與寬廣草地','新宿御苑前站1號出口步行約5分鐘（GO TOKYO）',5)
add('hachioji-library','八王子・中央圖書館沿道','甲州街道・中央図書館周辺','八王子市',35.6569,139.3100,'TKG-016','甲州街道銀杏並木的沿道散步','JR西八王子站周邊；行走請遵守人行道動線',4,['11-01','11-30'],'https://www.ichou-festa.org/ichounews/',caveat='官方照片日期2026-09-22已確認；未由照片自動判定葉況。祭典日期不是見頃日期。')
add('hachioji-tama','八王子・多摩御陵入口','甲州街道・多摩御陵入口','八王子市',35.6458,139.2912,'TKG-016','沿道不同視角的銀杏觀察','JR高尾站周邊；請在Google Maps確認步行路線',4,['11-01','11-30'],'https://www.ichou-festa.org/ichounews/')
add('east-garden','皇居東御苑・百人番所前','皇居東御苑・百人番所前','千代田區',35.6857,139.7584,'TKG-017','御苑歷史建築旁的銀杏','大手町站至大手門；請先查東御苑開放公告',4)
add('koishikawa','小石川植物園','小石川植物園','文京區',35.7187,139.7435,'TKG-018','植物園中的物種觀察','都營白山站；請先核對官方開園資訊',4)
add('kotokuji','廣德寺','広徳寺','秋留野市',35.7214,139.2271,'TKG-019','古寺與大銀杏的安靜秋景','JR武藏五日市站起程；依觀光協會交通資訊',4)
add('gaien','明治神宮外苑・銀杏並木','明治神宮外苑・いちょう並木','港區・新宿區',35.6745,139.7186,'TKG-023','對稱並木與聖德紀念繪畫館的經典視角','銀座線外苑前站／青山一丁目站（官網）',5,['11-11','12-10'],'https://www.gotokyo.org/jp/story/guide/autumn-leaves-forecast/index.html',access_url='https://www.meijijingugaien.jp/information/access-map.html')
add('ootaguro','大田黑公園','大田黒公園','杉並區',35.6996,139.6257,'TKG-024','入口銀杏並木與日式庭園','JR／丸之內線荻窪站；請查現任管理單位官網',4)
add('ookunitama','大國魂神社・大銀杏','大國魂神社・大銀杏','府中市',35.6679,139.4787,'TKG-025','本殿後方的大銀杏','京王府中站或JR府中本町站；詳見神社官網',4)
add('yasukuni','靖國神社','靖国神社','千代田區',35.6943,139.7431,'TKG-026','境內銀杏參道散步','九段下站；請先查神社境內公告',4,caveat='未取得有拍攝日期的2026銀杏觀測；官方照片頁不是即時鏡頭。')
add('utokyo-hongo','東京大學・本鄉校區','東京大学・本郷キャンパス','文京區',35.7135,139.7607,'TKG-040','正門至安田講堂的銀杏並木','本鄉三丁目站至校區約10分鐘（工學部官網）',5,access_url='https://www.t.u-tokyo.ac.jp/about/info/access',caveat='赤門耐震工程預計至2027年9月；改由開放入口，考試及校方限制日不可入校。')
add('utokyo-komaba','東京大學・駒場Ⅰ校區','東京大学・駒場Ⅰキャンパス','目黑區',35.6604,139.6844,'TKG-040','校區主要通道上的銀杏並木','京王井之頭線駒場東大前站；請先查校方參觀規則',4)
add('kunitachi','國立・大學通','国立・大学通り','國立市',35.6943,139.4467,'TKG-041','學園街道的銀杏慢步','JR中央線國立站南口起程；請確認當日動線',4)
add('hokudai','北海道大學・銀杏並木','北海道大学・イチョウ並木','札幌市',43.0756,141.3451,'HOKUDAI','北13條門一帶的黃金拱廊','札幌市地鐵北12條站；請查大學訪客地圖',5,['10-21','11-10'],'https://www.visit-hokkaido.jp/en/spot/detail_10022.html','札幌','北海道',access_url='https://www.global.hokudai.ac.jp/about/access/')
add('sobue','祖父江銀杏公園','祖父江ぎんなんパーク','稻澤市',35.2551,136.7290,'AICHI','銀杏產地的並木與觀景台','名鐵山崎站下車即達（愛知官方觀光）',5,['11-21','11-30'],'https://www.aichinow.pref.aichi.jp/spots/detail/3587/','名古屋','中部')
add('nishi-honganji','西本願寺・大銀杏','西本願寺・大銀杏','京都市',34.9918,135.7517,'KYOTO','橫向開展的特色大銀杏','JR京都站步行約15分鐘（京都觀光Navi）',4,period_url='https://ja.kyoto.travel/tourism/single01.php?category_id=7&tourism_id=215',city='京都',region='關西')
add('midosuji','御堂筋・銀杏並木','御堂筋・イチョウ並木','大阪市',34.6801,135.5004,'OSAKA','城市大道與銀杏街景','大阪Metro御堂筋線本町站；街道代表定位點',5,period_url='https://www.city.osaka.lg.jp/kensetsu/page/0000242811.html',city='大阪',region='關西')
add('kumamoto','熊本城・大銀杏','熊本城・大イチョウ','熊本市',32.8062,130.7058,'KUMAMOTO','銀杏城名由來的天守前大銀杏','熊本市電至熊本城周邊；請查復舊及公開區域',4,period_url='https://castle.kumamoto-guide.jp/history/',city='熊本',region='九州',access_url='https://castle.kumamoto-guide.jp/access/')
add('tarumizu','垂水千株銀杏樹林','垂水千本イチョウ','垂水市',31.4875,130.7350,'KAGOSHIMA','山坡上的金黃銀杏樹林','垂水港開車約12分鐘、約6.9公里（官方觀光）',5,['11-21','12-10'],'https://www.kagoshima-kankou.com/guide/13192','鹿兒島','九州',caveat='私人土地開放賞景；請尊重園主及當季交通公告。城市氣候使用鹿兒島站，非山坡微氣候。')
for s in spots:
    if s['id'].startswith('showa-') or s['id'].startswith('hachioji-'):
        s['official_yellow_season']=s['historical_period']
        s['historical_period']=['11-08','11-21'] if s['id'].startswith('showa-') else ['11-09','11-22']
        s['period_basis']='本站以官方例年黃葉季中段14天示意推估見頃；不是景點官方預報或實測'
        s['caveat']+=' 官方黃葉季：'+('10月下旬至11月下旬' if s['id'].startswith('showa-') else '11月前後')+'；不能視為整段見頃。'
    if s['id']=='kunitachi': s['species_source']='https://kunimachi.jp/spot/daigakustreet/'
    if s['id'].startswith('utokyo-'): s['species_source']='https://www.u-tokyo.ac.jp/ja/about/campus-guide/1km_of_campus.html' if s['id'].endswith('hongo') else 'https://www.u-tokyo.ac.jp/content/400123561.pdf'
    elif s['id']!='kunitachi': s['species_source']=s['url']
    if s['id']=='shinjuku': s['historical_observation']={'date':'2025-11-28','status':'見頃','url':rows['TKG-015']['evidence_url'],'basis':'老師來源表記錄；歷史實測樣本，不套用2026'}
    if s['id']=='kotokuji': s['historical_observation']={'date':'2025-11-06','status':'轉黃中','url':rows['TKG-019']['evidence_url'],'basis':'老師表保留的照片日期；不是發文日期'}
    if s['id']=='koishikawa': s['historical_observation']={'date':'2025-11-19','status':'黃葉中（未確認見頃）','url':rows['TKG-018']['evidence_url'],'basis':'老師來源表記錄；黃葉不等於見頃'}
    s['photo']=photos[s['id']]
    s['climate_station']=s['city']
    if not s['historical_period']: s['historical_period']=[cities[s['city']]['normal_yellow'],cities[s['city']]['normal_fallen']]
    if not s['period_source']: s['period_source']='https://www.data.jma.go.jp/sakura/data/phn_012.html'
mapping=[]
for r in teacher['rows']:
    ids=[s['id'] for s in spots if r['source_id'] in s['source_ids']]
    role='景點直接來源' if ids else ('失效／舊管理排除' if r['grade']=='X' else '補充索引／候選待證' if r['source_id'] in ['TKG-030','TKG-031','TKG-032'] else '整合／歷史／預報參考')
    mapping.append({'source_id':r['source_id'],'group_id':r['group_id'],'row_number':r['row_number'],'spot_ids':ids,'mapping_role':role,'note':r['caveat']})
data={'as_of':'2026-10-08','teacher':teacher,'source_mapping':mapping,'cities':cities,'spots':spots,'forecast_source':'https://n-kishou.com/corp/news-contents/autumn/','yellow_source':'https://www.data.jma.go.jp/sakura/data/phn_012.html','fallen_source':'https://www.data.jma.go.jp/sakura/data/phn_013.html','method':'所有2026景點實測未取得。歷年平均模式：以官網例年範圍或JMA城市平年標本木黃葉日到落葉日為參考，並以黃葉前14日、期末後7日展示轉黃/落葉階段，為本站示意推估而非實測。城市預報模式：若有2026城市預報，使用城市預報日與JMA平年黃葉日的差平移歷年範圍；並非景點官方預報。沒有城市預報則維持歷年參考。推薦星等為本站編輯評分。步行時間使用代表點直線距離乘1.4／時速4.5公里估算；Google Maps另行查詢實際路線。'}
(ROOT/'data/spots.json').write_text(json.dumps(spots,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'data/source-mapping.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2),encoding='utf-8')
(ROOT/'data/site-data.js').write_text('window.GINKGO_DATA = '+json.dumps(data,ensure_ascii=False,indent=2)+';\n',encoding='utf-8')
print(f'{len(spots)} destination/subpoints; {len(mapping)} source mappings; data.js supports file:// without fetch.')
