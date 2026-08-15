#!/usr/bin/env python3
"""Подсвечивает места, где текст страницы звучит собранным, а не сказанным.

    python3 tools/text_lint.py            # все страницы хаба
    python3 tools/text_lint.py projects/exportgpt.html

Не правит — показывает. Правит человек.

Зачем. Автор раз за разом ловит в моих текстах одно и то же: фраза построена так,
чтобы «щёлкнуть», а не чтобы её сказали вслух. Машина не отличит складное от живого,
но признаки складности формальны, и их немного. Список растёт от разборов автора —
он ведётся в `mosty/vitrina/kak-pisat.md`, сюда уезжает то, что проверяемо.
"""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent

# ── проверки ──────────────────────────────────────────────────────────────
LONG_SENTENCE = 26          # слов; длиннее — фразу строили, а не говорили
LONG_CAPTION  = 18          # слов в подписи под кадром

MARKERS = [
    (r"\bnot\s+\w+[^.]{0,40}\bbut\b",            "пара «не X, а Y» — риторическая фигура"),
    (r"\brather than\b",                          "«rather than» — та же пара, другим словом"),
    (r"\bprecisely\b|\bexactly what\b",           "усилитель, который ничего не добавляет"),
    (r"\bthat is why\b|\bwhich is why\b",         "вывод-связка: проверь, есть ли посылка выше"),
    (r"\bthe old\b|\bthe former\b|\bpreviously\b","опора на прошлое, которого читатель не видел"),
    (r"\bnot a paid\b|\binstead of a paid\b",     "определение через отрицание неизвестного"),
    (r"—[^—.]{0,60}:",                            "тире и двоеточие в одной фразе — три такта"),
    (r"\bit is not just\b|\bnot only\b[^.]{0,60}\bbut also\b", "нарастание «не только… но и»"),
]

def sentences(text):
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]

def strip_tags(html):
    html = re.sub(r"<(script|style|svg)[^>]*>.*?</\1>", " ", html, flags=re.S)
    return re.sub(r"<[^>]+>", " ", html)

def check(page: pathlib.Path):
    html = page.read_text(encoding="utf-8")
    hits = []

    for m in re.finditer(r"<figcaption>(.*?)</figcaption>", html, re.S):
        words = strip_tags(m.group(1)).split()
        if len(words) > LONG_CAPTION:
            hits.append((f"подпись из {len(words)} слов", " ".join(words)[:90]))

    body = strip_tags(html)
    body = re.sub(r"\s+", " ", body)
    for s in sentences(body):
        n = len(s.split())
        if n > LONG_SENTENCE:
            hits.append((f"предложение из {n} слов", s[:110]))
        for pattern, why in MARKERS:
            if re.search(pattern, s, re.I):
                hits.append((why, s[:110]))
    return hits

targets = [pathlib.Path(a) for a in sys.argv[1:]] or \
          sorted(list(ROOT.glob("*.html")) + list((ROOT / "projects").glob("*.html")) +
                 list((ROOT / "ru").glob("*.html")))

total = 0
for page in targets:
    p = page if page.is_absolute() else ROOT / page
    hits = check(p)
    if not hits:
        continue
    print(f"\n=== {p.relative_to(ROOT)}")
    for why, frag in hits:
        print(f"  · {why}\n      {frag}")
    total += len(hits)
print(f"\nвсего мест к пересмотру: {total}")
