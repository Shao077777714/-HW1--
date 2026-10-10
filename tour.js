'use strict';
(() => {
 const $ = id => document.getElementById(id);
 const dialog = $('tour-dialog'), card = $('tour-card'), spotlight = $('tour-spotlight');
 const storageKey = 'ginkgo-tour-v1';
 const steps = [
  {target:'#date-inputs',title:'先選一個出發日期',text:'拖動日期滑桿，或直接選擇日期。地圖葉況、推薦景點和見頃時間會一起更新；播放鍵可以看看秋色如何隨日期變化。'},
  {target:'#filter-controls',title:'找到你想去的地方',text:'輸入景點名稱或城市，再依地區、葉況與推薦程度篩選。「只看見頃」能聚焦推估最佳觀賞期；想重新找，就按「清除篩選」。'},
  {target:'#map .ginkgo-marker, #map .ginkgo-cluster',fallback:'#map .leaflet-control-zoom',fallbackText:'目前沒有符合篩選的景點，可先用框起的 ＋／－ 按鈕縮放地圖。清除篩選後，點銀杏標記看照片、特色、交通與來源；數字圓圈可點開放大。',title:'點一片銀杏，打開景點',text:'框起的是可以點開的景點標記。銀杏顏色代表推估葉況，金黃色代表見頃；點標記看照片、特色、交通與來源。數字圓圈可點開放大，地圖也能拖曳探索。'},
  {target:'#recommendation-cards .recommend-card',mobileTarget:'#recommendation-cards .recommend-card .primary',fallback:'#recommendation-cards',title:'從今日推薦開始挑選',text:'推薦卡片會依所選日期與篩選條件更新。看看銀杏特色與參考見頃期，按「查看地圖」就能直接定位、打開景點資訊。'},
  {target:'#timeline-rows .timeline-row',fallback:'.timeline-months',title:'看看哪個時候最適合去',text:'每條時間帶呈現一個景點的轉黃、見頃與落葉階段，黑色直線標示所選日期。這些是規劃推估，出發前可從景點資訊的原始來源確認最新葉況。'},
  {target:'#route-controls',title:'把金黃串成一段散步',text:'選擇路線地區、半日或一日行程，再按「在地圖看路線」查看景點順序。實際步行道路可開啟 Google Maps 確認。準備好，開始找你的秋日散步吧！'}
 ];
 let step = -1, lastFocus, initialScroll = 0, previousOverflow = '', frame;

 function hasVisited() {
  for (const name of ['localStorage','sessionStorage']) {
   try { if (window[name].getItem(storageKey)) return true; } catch (_) { /* Storage may be disabled. */ }
  }
  return false;
 }
 function rememberVisit() {
  for (const name of ['localStorage','sessionStorage']) {
   try { window[name].setItem(storageKey,'seen'); } catch (_) { /* The guide still works without storage. */ }
  }
 }
 function openGuide(welcome) {
  if (dialog.open) return;
  lastFocus = document.activeElement;
  initialScroll = window.scrollY;
  previousOverflow = document.body.style.overflow;
  document.body.style.overflow = 'hidden';
  if (window.GINKGO_APP?.state.playing) $('play').click();
  window.GINKGO_APP?.map?.closePopup();
  step = welcome ? -1 : 0;
  updateCard();
  dialog.showModal();
  if (step >= 0) showStep();
  else positionCard();
  $('tour-next').focus({preventScroll:true});
 }
 function finish() {
  rememberVisit();
  cancelAnimationFrame(frame);
  dialog.close();
  document.body.style.overflow = previousOverflow;
  window.scrollTo({top:initialScroll,behavior:'instant'});
  (lastFocus instanceof HTMLElement && lastFocus !== document.body ? lastFocus : $('tour-open')).focus({preventScroll:true});
 }
 function updateCard() {
  const welcome = step < 0;
  dialog.classList.toggle('tour-welcome',welcome);
  $('tour-welcome-art').hidden = !welcome;
  spotlight.hidden = welcome;
  $('tour-progress').hidden = welcome;
  $('tour-back').hidden = welcome;
  $('tour-back').disabled = step === 0;
  $('tour-eyebrow').textContent = welcome ? '歡迎來到銀杏日和' : `操作導覽 · ${step + 1} / ${steps.length}`;
  $('tour-title').textContent = welcome ? '第一次來到這裡？' : steps[step].title;
  $('tour-description').textContent = welcome ? '需要一段簡短的操作導覽嗎？用 1 分鐘，帶你認識地圖、日期與篩選，找到想去的銀杏景點。' : (steps[step].fallbackText && !document.querySelector(steps[step].target) ? steps[step].fallbackText : steps[step].text);
  $('tour-next').textContent = welcome ? '開始導覽 →' : step === steps.length - 1 ? '開始探索 →' : '下一步 →';
  $('tour-skip').textContent = welcome ? '先自行探索' : '跳過導覽';
  $('tour-footnote').hidden = !welcome;
  $('tour-progress').innerHTML = welcome ? '' : steps.map((_,i)=>`<span class="${i <= step ? 'is-done' : ''}" aria-hidden="true"></span>`).join('');
  $('tour-progress').setAttribute('aria-label',`共 ${steps.length} 步，目前第 ${step + 1} 步`);
 }
 function stepTarget() {
  const item = steps[step];
  return document.querySelector(innerWidth <= 800 && item.mobileTarget ? item.mobileTarget : item.target)
   || document.querySelector(item.fallback);
 }
 function showStep() {
  positionCard();
  $('tour-next').focus({preventScroll:true});
 }
 function positionCard() {
  if (!dialog.open) return;
  const margin = 16, gap = 14, padding = 4, width = Math.min(step < 0 ? 460 : 360,innerWidth - margin * 2);
  card.style.width = `${width}px`;
  const height = card.offsetHeight;
  if (step < 0) {
   card.style.left = `${(innerWidth-width)/2}px`;
   card.style.top = `${Math.max(margin,(innerHeight-height)/2)}px`;
   return;
  }
  const target = stepTarget();
  if (!target) { finish(); return; }
  let r = target.getBoundingClientRect();
  const clamp = (value,max) => Math.max(margin,Math.min(value,max-margin));
  function placement(rect) {
   const x = clamp(rect.left,innerWidth-width), y = clamp(rect.top,innerHeight-height);
   return [
    {x:rect.right+padding+gap,y},
    {x:rect.left-padding-gap-width,y},
    {x,y:rect.bottom+padding+gap},
    {x,y:rect.top-padding-gap-height}
   ].find(p=>p.x>=margin && p.y>=margin && p.x+width<=innerWidth-margin && p.y+height<=innerHeight-margin);
  }
  let position = placement(r);
  if (!position || r.top-padding<margin || r.bottom+padding>innerHeight-margin) {
   // Scroll the document only: scrolling a Leaflet child can shift the map's internal panes.
   window.scrollTo({top:window.scrollY+r.top-margin-padding,behavior:'instant'});
   r = target.getBoundingClientRect();
   position = placement(r);
  }
  position ||= {x:clamp(r.left,innerWidth-width),y:innerHeight-height-margin};
  card.style.left = `${position.x}px`;
  card.style.top = `${Math.max(margin,position.y)}px`;
  // The frame always follows the complete target bounds, independently of the card.
  spotlight.style.left = `${r.left-padding}px`;
  spotlight.style.top = `${r.top-padding}px`;
  spotlight.style.width = `${r.width+padding*2}px`;
  spotlight.style.height = `${r.height+padding*2}px`;
  spotlight.style.borderRadius = target.matches('.ginkgo-marker, .ginkgo-cluster') ? '50%' : '6px';
 }
 $('tour-open').addEventListener('click',()=>openGuide(false));
 $('tour-next').addEventListener('click',()=>{
  if (step === steps.length-1) { finish(); return; }
  if (step < 0) rememberVisit();
  step++;
  updateCard();
  showStep();
 });
 $('tour-back').addEventListener('click',()=>{if(step > 0){step--;updateCard();showStep();}});
 $('tour-skip').addEventListener('click',finish);
 $('tour-close').addEventListener('click',finish);
 dialog.addEventListener('cancel',e=>{e.preventDefault();finish();});
 window.addEventListener('resize',()=>{
  cancelAnimationFrame(frame);
  if(dialog.open) frame=requestAnimationFrame(()=>step < 0 ? positionCard() : showStep());
 });
 if (!hasVisited()) openGuide(true);
})();
