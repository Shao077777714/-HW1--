from pathlib import Path
import json, re, urllib.request, concurrent.futures, subprocess, tempfile

ROOT = Path(__file__).resolve().parents[1]
def fetch(url):
    # Windows WebRequest respects the desktop's network proxy configuration.
    if "'" in url: raise ValueError('Invalid URL')
    with tempfile.TemporaryDirectory() as tmp:
        out=Path(tmp)/'download'
        subprocess.run(['powershell','-NoProfile','-Command',f"Invoke-WebRequest -Uri '{url}' -OutFile '{out}' -TimeoutSec 30"],check=True,capture_output=True)
        return out.read_bytes()
def text_cells(row):
    return [re.sub(r'\s+',' ',re.sub('<[^>]+>','',x)).strip() for x in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', row,re.S)]
stations={'東京':[44,47662,'11-23','12-03','11-26'],'札幌':[14,47412,'11-04','11-11','11-03'],'名古屋':[51,47636,'11-18','12-03','11-17'],'京都':[61,47759,'11-24','12-04','11-27'],'大阪':[62,47772,'11-22','12-04','11-24'],'熊本':[86,47819,'11-27','12-08',None],'鹿兒島':[88,47827,'11-25','12-06','11-27']}
def climate(item):
    city, (prec,block,yellow,fallen,forecast)=item
    url=f'https://www.data.jma.go.jp/stats/etrn/view/nml_sfc_ym.php?prec_no={prec}&block_no={block}'
    html=fetch(url).decode('utf-8','replace')
    months={}
    for row in re.findall(r'<tr[^>]*>(.*?)</tr>',html,re.S):
        cells=text_cells(row)
        if cells and re.fullmatch(r'\d+月',cells[0]) and len(cells)>6:
            months[cells[0].removesuffix('月')]={'mean':float(cells[4]),'max':float(cells[5]),'min':float(cells[6])}
    if len(months)!=12: raise ValueError(f'climate table parse failed: {city}')
    return city,{'climate':months,'climate_source':url,'normal_yellow':yellow,'normal_fallen':fallen,'forecast_yellow':forecast,'forecast_published':'2026-10-01','scale':'城市標本木；不是各景點實測'}

teacher=json.loads((ROOT/'data/teacher-sources.json').read_text(encoding='utf-8'))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: cities=dict(pool.map(climate,stations.items()))
(ROOT/'data/cities.json').write_text(json.dumps(cities,ensure_ascii=False,indent=2),encoding='utf-8')
vendor={'leaflet.js':'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js','leaflet.css':'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css','leaflet.markercluster.js':'https://unpkg.com/leaflet.markercluster@1.5.3/dist/leaflet.markercluster.js','MarkerCluster.css':'https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.css','MarkerCluster.Default.css':'https://unpkg.com/leaflet.markercluster@1.5.3/dist/MarkerCluster.Default.css'}
(ROOT/'vendor').mkdir(exist_ok=True)
for name,url in vendor.items(): (ROOT/'vendor'/name).write_bytes(fetch(url))
print('Read climate normals for',list(cities),'and saved Leaflet + MarkerCluster locally.')
