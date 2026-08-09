/* hub.js — общий скрипт хаба. До 2026-08-10 лайтбокс был скопирован на каждой
   странице проекта, и правка расходилась по трём файлам. */
(function () {
  'use strict';

  /* ── Хронология открывается на СЕГОДНЯ ────────────────────────────────
     Решение автора 08-10: самое актуальное — в правом кадре, а лента уходит
     в прошлое влево. Разметка остаётся хронологической (старое → новое), это
     честный порядок для чтения и для доступности; сдвигаем только начальный
     взгляд, чтобы человек сперва видел, чем проект стал, а не с чего начинал. */
  document.querySelectorAll('.timeline').forEach(function (t) {
    t.scrollLeft = t.scrollWidth;
  });

  /* ── Лупа ──────────────────────────────────────────────────────────── */
  var lb = document.getElementById('lb');
  if (!lb) return;
  var im = lb.querySelector('img'), last = null;

  document.querySelectorAll('[data-zoom]').forEach(function (el) {
    el.addEventListener('click', function () {
      last = el;
      im.src = el.getAttribute('data-zoom');
      im.alt = (el.querySelector('img') || {}).alt || '';
      lb.classList.add('on');
      lb.focus();
    });
    el.addEventListener('keydown', function (e) {      // с клавиатуры тоже
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); el.click(); }
    });
  });

  function close() {
    lb.classList.remove('on');
    im.src = '';
    if (last) last.focus();
  }
  lb.addEventListener('click', close);
  document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
})();
