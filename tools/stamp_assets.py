#!/usr/bin/env python3
"""Штампует версию на общие css/js, чтобы браузер не показывал старое.

    python3 tools/stamp_assets.py

Зачем (08-10). Подключил верхнюю панель, запушил, проверил живой CSS — всё на месте.
А автор увидел голые ссылки без стилей: GitHub Pages отдаёт `cache-control: max-age=600`,
и его браузер десять минут держал предыдущий hub.css, в котором правила `.topbar` ещё не было.
Проверка «файл на сервере правильный» не равна проверке «человек видит правильное».

Лечение: в ссылку на файл дописывается ?v=<хеш содержимого>. Меняется файл — меняется
адрес — браузер обязан взять новый. Гонять ПЕРЕД каждым пушем, где тронуты assets/.
"""
import hashlib, pathlib, re

ROOT = pathlib.Path(__file__).resolve().parent.parent
ASSETS = ["assets/hub.css", "assets/hub.js"]

def short(p):
    return hashlib.md5((ROOT / p).read_bytes()).hexdigest()[:8]

vers = {a: short(a) for a in ASSETS}
pages = list(ROOT.glob("*.html"))
for folder in ("projects", "ru"):          # ru/ — русский каталог, добавлен 08-10
    pages += list((ROOT / folder).glob("*.html"))
changed = 0
for page in pages:
    s = old = page.read_text(encoding="utf-8")
    for a, v in vers.items():
        s = re.sub(r'(/' + re.escape(a) + r')(\?v=[0-9a-f]+)?\b', r'\1?v=' + v, s)
    if s != old:
        page.write_text(s, encoding="utf-8"); changed += 1

for a, v in vers.items():
    print(f"{a} → ?v={v}")
print(f"страниц обновлено: {changed} из {len(pages)}")
