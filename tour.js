'use strict';
(() => {
 const $ = id => document.getElementById(id);
 const dialog = $('tour-dialog'), card = $('tour-card'), spotlight = $('tour-spotlight');
 const storageKey = 'ginkgo-tour-v1';
 const steps = [
  {target:'.date-controls',title:'先選一個出發日期',text:'拖動日期滑桿，或直接選擇日期。地圖葉況、推薦景點和見頃時間會一起更新；播放鍵可以看看秋色如何隨日期變化。'},
  {target:'#filter-controls',title:'找到你想去的地方',text:'輸入景點名稱或城市，再依地區、葉況與推薦程度篩選。「只看見頃」能聚焦推估最佳觀賞期；想重新找，就按「清除篩選」。'},
  {target:'#map',title:'點一片銀杏，打開景點',text:'銀杏標記的顏色代表推估葉況，金黃色代表見頃。點標記看特色、交通與來源；數字圓圈可點開放大，用 ＋／－ 縮放或拖曳地圖探索。'},
  {target:'#recommendation-cards',title:'從今日推薦開始挑選',text:'這裡依所選日期與篩選條件推薦景點。看看銀杏特色與參考見頃期，按「查看地圖」就能直接定位、打開景點資訊。'},
  {target:'.timeline-content',title:'看看哪個時候最適合去',text:'時間帶呈現轉黃、見頃與落葉階段，直線標示你選的日期。這些是規劃推估，出發前可從景點資訊查看原始來源，確認最新葉況。'},
  {target:'#routes .section-intro',title:'把金黃串成一段散步',text:'選擇半日或一日行程，再按「在地圖看路線」查看景點順序。實際步行道路可開啟 Google Maps 確認。準備好，開始找你的秋日散步吧！'}
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
  $('tour-description').textContent = welcome ? '需要一段簡短的操作導覽嗎？用 1 分鐘，帶你認識地圖、日期與篩選，找到想去的銀杏景點。' : steps[step].text;
  $('tour-next').textContent = welcome ? '開始導覽 →' : step === steps.length - 1 ? '開始探索 →' : '下一步 →';
  $('tour-skip').textContent = welcome ? '先自行探索' : '跳過導覽';
  $('tour-footnote').hidden = !welcome;
  $('tour-progress').innerHTML = welcome ? '' : steps.map((_,i)=>`<span class="${i <= step ? 'is-done' : ''}" aria-hidden="true"></span>`).join('');
  $('tour-progress').setAttribute('aria-label',`共 ${steps.length} 步，目前第 ${step + 1} 步`);
 }
 function showStep() {
  const target = document.querySelector(steps[step].target);
  target.scrollIntoView({block:'start',behavior:'instant'});
  // Leave room around the highlighted area, including on narrow screens.
  window.scrollBy({top:-22,behavior:'instant'});
  positionCard();
  $('tour-next').focus({preventScroll:true});
 }
 function positionCard() {
  if (!dialog.open) return;
  const margin = 16, gap = 18, width = Math.min(step < 0 ? 460 : 360,innerWidth - margin * 2);
  card.style.width = `${width}px`;
  const height = card.offsetHeight;
  if (step < 0) {
   card.style.left = `${(innerWidth-width)/2}px`;
   card.style.top = `${Math.max(margin,(innerHeight-height)/2)}px`;
   return;
  }
  const r = document.querySelector(steps[step].target).getBoundingClientRect();
  const left = Math.max(margin,Math.min(r.left,innerWidth-width-margin));
  const top = Math.min(Math.max(margin,r.bottom+gap),Math.max(margin,innerHeight-height-margin));
  card.style.left = `${left}px`;
  card.style.top = `${top}px`;
  // Clip tall sections above the card so its instructions remain readable.
  const x = Math.max(8,r.left-6), y = Math.max(8,r.top-6);
  spotlight.style.left = `${x}px`;
  spotlight.style.top = `${y}px`;
  spotlight.style.width = `${Math.max(0,Math.min(innerWidth-8,r.right+6)-x)}px`;
  spotlight.style.height = `${Math.max(0,Math.min(r.bottom+6,top-10)-y)}px`;
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
