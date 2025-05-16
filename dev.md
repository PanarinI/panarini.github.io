<a href="projects/project‑alpha.html">Подробнее</a>



┌────────────────────────────────────────────────────┐
│ [Изображение проекта: иллюстрация, скриншот]     │
├────────────────────────────────────────────────────┤
│ Заголовок проекта (Project Title)                 │
│ ─────────────────────────────────────────────────  │
│ Краткое описание (1–2 предложения)                │
│                                                    │
│ • Результат: что получил пользователь / бизнес    │
│ • Технологии: иконки или короткий список (3–5)    │
│ • Моя роль: (аналитик, разработчик, архитектор)   │
│                                                    │
│ [Кнопка или ссылка «Подробнее» → project‑*.html]  │
└────────────────────────────────────────────────────┘


index.html
└── <header> + навигация (Home, Projects, Contact)
└── <main>
    └── <section class="cards">
        ├── <article class="card">…</article>
        ├── <article class="card">…</article>
        └── …
└── <footer>© 2025 Иван Панарин</footer>

projects/
└── project-alpha.html
└── project-orphan-index.html
└── project-slp-assistant.html
└── …
assets/
└── css/style.css
└── img/*.jpg, *.svg
.nojekyll
