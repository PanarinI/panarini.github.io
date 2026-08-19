#!/usr/bin/env python3
"""Готовит страницы к публикации: счётчик на каждой + штамп версии на общих css/js.

    python3 tools/stamp_assets.py

Гонять ПЕРЕД каждым пушем. Два дела в одном файле сознательно: оба обходят те же
страницы, и один вход означает, что забыть про одно из них нельзя.

ШТАМП ВЕРСИИ (08-10). Подключил верхнюю панель, запушил, проверил живой CSS — всё на
месте. А автор увидел голые ссылки без стилей: GitHub Pages отдаёт `cache-control:
max-age=600`, и его браузер десять минут держал предыдущий hub.css, где правил `.topbar`
ещё не было. Проверка «файл на сервере правильный» не равна проверке «человек это увидит».
Лечение: в ссылку дописывается ?v=<хеш содержимого>. Меняется файл — меняется адрес —
браузер обязан взять новый. Касается только страниц хаба: архив живёт на старом css.

СЧЁТЧИК (08-10). GoatCounter, один тег на страницу, без кук и без баннера согласия.
Ставится на ВСЕ страницы сайта, включая архив: ссылка из резюме на hh ведёт именно
в архив, и без счётчика этот приход не виден. Скрипт сам не считает localhost, поэтому
локальные прогоны в статистику не попадают. Свой браузер исключается один раз —
открыть любой адрес сайта с `#toggle-goatcounter` на конце.
Фрагменты без <head> и <body> (вставляются в другие страницы через iframe) пропускаются:
их посещение уже посчитано на странице-хозяине.
"""
import hashlib, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ["assets/hub.css", "assets/hub.js"]
COUNTER_CODE = "panarini"          # поддомен в GoatCounter: <code>.goatcounter.com
COUNTER_TAG = ('<script data-goatcounter="https://%s.goatcounter.com/count"\n'
               '        async src="//gc.zgo.at/count.js"></script>\n' % COUNTER_CODE)


def short(p):
    return hashlib.md5((ROOT / p).read_bytes()).hexdigest()[:8]


# ── страницы ──────────────────────────────────────────────────────────────
hub_pages = list(ROOT.glob("*.html"))
for folder in ("projects", "ru", "ru/projects"):   # ru/ — русский каталог (08-10);
                                                  # ru/projects — русские страницы проектов (08-19):
                                                  # без штампа их css кешировался на десять минут
    hub_pages += list((ROOT / folder).glob("*.html"))
all_pages = sorted(p for p in ROOT.rglob("*.html")
                   if ".git" not in p.parts and "components" not in p.parts)

# ── счётчик на каждой странице ────────────────────────────────────────────
added, skipped = 0, []
for page in all_pages:
    s = page.read_text(encoding="utf-8")
    if "data-goatcounter" in s:
        continue
    if "</head>" in s:
        s = s.replace("</head>", COUNTER_TAG + "</head>", 1)
    elif "</body>" in s:
        s = s.replace("</body>", COUNTER_TAG + "</body>", 1)
    else:
        skipped.append(page.relative_to(ROOT)); continue
    page.write_text(s, encoding="utf-8"); added += 1

# ── штамп версии на общих файлах хаба ─────────────────────────────────────
vers = {a: short(a) for a in ASSETS}
changed = 0
for page in hub_pages:
    s = old = page.read_text(encoding="utf-8")
    for a, v in vers.items():
        s = re.sub(r'(/' + re.escape(a) + r')(\?v=[0-9a-f]+)?\b', r'\1?v=' + v, s)
    if s != old:
        page.write_text(s, encoding="utf-8"); changed += 1


# ── живое число пользователей из листинга CWS ────────────────────────────
# Цифра на сайте устаревает молча: 346 провисели до 08-10, когда их стало 440.
# Тянем из карточки стора и подставляем всюду, где помечено data-cws-users
# или написано «N users» / «N пользователей». Стор недоступен — оставляем как есть.
import urllib.request
CWS = "https://chromewebstore.google.com/detail/aighdeikamhkemngfanhnamdlpoceimo"
users = None
try:
    req = urllib.request.Request(CWS, headers={"User-Agent": "Mozilla/5.0"})
    html = urllib.request.urlopen(req, timeout=15).read().decode("utf-8", "ignore")
    m = re.search(r">([\d,]{2,9}) users<", html)
    if m:
        users = m.group(1)
except Exception as e:
    print(f"счётчик стора недоступен ({e}) — число оставлено прежним")
if users:
    n = 0
    for page in all_pages:
        t = old_t = page.read_text(encoding="utf-8")
        t = re.sub(r"(<b data-cws-users>)[\d,]+(</b>)", r"\g<1>" + users + r"\g<2>", t)
        t = re.sub(r"\b[\d,]{2,9} users\b", users + " users", t)
        t = re.sub(r"\b[\d,]{2,9} пользовател(ей|я)\b", users + r" пользовател\g<1>", t)
        if t != old_t:
            page.write_text(t, encoding="utf-8"); n += 1
    print(f"пользователей в сторе: {users} — обновлено страниц: {n}")

print(f"счётчик: добавлен на {added}, всего страниц с ним "
      f"{sum('data-goatcounter' in p.read_text(encoding='utf-8') for p in all_pages)}"
      f" из {len(all_pages)}")
for p in skipped:
    print(f"  пропущен фрагмент без head/body: {p}")
for a, v in vers.items():
    print(f"{a} → ?v={v}")
print(f"штамп версии: обновлено страниц {changed} из {len(hub_pages)}")
