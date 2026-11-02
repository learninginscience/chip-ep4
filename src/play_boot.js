/* ================= 直接玩版（play.html）的啟動 =================
   build.py 用這段取代 game.src.html 最後的 renderStart();，組出 play.html。
   index.html、teacher.html 不受影響。
   - 打開就直接進第一關：不登記名字、沒有房間、不上傳任何資料。
   - 進度改存 sessionStorage：同一個分頁重新整理會接著玩，關掉分頁就清掉；
     不會寫進 localStorage，所以原本的學生頁不會跳出「要接著走嗎？」。 */
['get', 'set', 'del'].forEach(m => {
  store[m] = {
    get(k, d){ try { const v = sessionStorage.getItem(k); return v == null ? d : JSON.parse(v); } catch(e){ return d; } },
    set(k, v){ try { sessionStorage.setItem(k, JSON.stringify(v)); } catch(e){} },
    del(k){ try { sessionStorage.removeItem(k); } catch(e){} },
  }[m];
});
(() => {
  const saved = store.get(PKEY, null);
  if (saved && saved.P && STEPS[saved.P.step] && STEPS[saved.P.step].t !== 'result'){
    P = saved.P; A = saved.A || {}; extra = saved.extra || { sparksWall:0, skipped:[], parts:[], tries:{} };
    renderStep();
    return;
  }
  P = { cls:'', seat:'', name:'小工程師', step:0, t0:Date.now() };
  A = {}; extra = { sparksWall:0, skipped:[], parts:[], tries:{} };
  go(0);
})();
