# Hard-Problems Journal

> **Сквозная эпизодическая память across projects.**
> Единственное честное дополнение к самообучению помимо качества твоей коррекции.
>
> Reflect Skill добавляет записи сюда автоматически при сложных случаях.
> Intake Skill читает этот файл при старте — ищет релевантные паттерны.

---

## Как читать этот журнал

**При старте проекта:** найди записи с похожим стеком или типом задачи — там уже есть решения.
**При застревании:** поищи по ключевым словам проблемы — возможно, это уже решалось.
**При завершении:** Reflect Skill добавит новую запись если что-то было нетривиальным.

---

## Шаблон записи

```markdown
## [YYYY-MM-DD] — [Project] — [Problem title]

**Теги:** [стек / тип проблемы / домен]

Контекст:    [что пытались сделать — одно предложение]
Сложность:   [почему не сработало сразу — конкретно]
Решение:     [что в итоге помогло — конкретно]
Инсайт:      [что помнить в будущих проектах — переносимый урок]
```

---

## Правила ведения

- **Одна запись = одна проблема.** Не объединяй несколько несвязанных случаев.
- **Инсайт должен быть переносимым.** Если он применим только к одному проекту — не стоит записывать.
- **Конкретность важнее полноты.** Лучше короткая точная запись, чем длинная размытая.
- **Не редактируй старые записи.** Если решение изменилось — добавь новую запись со ссылкой на старую.
- **Теги помогают поиску.** Используй стек (python, react, sqlite), тип (async, auth, state, perf, prompt) и домен (api, ui, db, llm).

---

## Записи

<!-- Reflect Skill добавляет новые записи здесь, в хронологическом порядке (новые сверху) -->

## [2026-03-05] — [PROJECT] — Brand color extraction из image-based PDF

**Теги:** pdf, python, color, pymupdf

Контекст:    Нужно было извлечь точные hex-цвета бренда из SoftMall услуги.pdf для CSS палитры.
Сложность:   PDF полностью растровый (сканы/слайды) — `fitz.get_text()` возвращает пустую строку. Стандартные PDF-парсеры (`pdfplumber`, PyPDF2) тоже не дают цвета.
Решение:     Рендеринг страницы в pixmap через `fitz.Page.get_pixmap()`, затем построчный sampling пикселей в ключевых зонах (header y=0–10%, footer y=90–100%, accent-кнопки). Доминантный цвет определяется частотностью RGB-значений.
Инсайт:      При любой задаче "извлечь данные из PDF" — сначала проверь `get_text()`. Если пусто → PDF image-based. Дальше только pixel sampling или OCR. Для цветов pixel sampling достаточен и быстрее OCR.

## [2026-03-05] — [PROJECT] — Python UTF-8 encoding на Windows в bash

**Теги:** python, windows, encoding, cli

Контекст:    Запуск `python generate_guide.py` в bash на Windows 11 давал кракозябры вместо кириллицы.
Сложность:   `python` и `python3` в Windows bash ссылаются на разные бинарники / алиасы с разными настройками кодировки по умолчанию. Консоль Windows по умолчанию — cp1251.
Решение:     Использовать `py` (Python Launcher для Windows 3.12) + `sys.stdout.reconfigure(encoding='utf-8')` в начале скрипта.
Инсайт:      На Windows всегда использовать `py` вместо `python`/`python3` для bash-команд. В скриптах с кириллицей — первая строка после imports: `sys.stdout.reconfigure(encoding='utf-8')`. Это переносимый паттерн для любых Python-скриптов с non-ASCII выводом.

## [2026-03-04] — [PROJECT] — Gamma API 422 для закрытых рынков

**Теги:** api, python, sqlite, polymarket

Контекст:    `_run_resolution_check` вызывал `GET /markets/{conditionId}` для определения победителя — всегда получал 422.
Сложность:   Gamma API намеренно отключил индивидуальный fetch для закрытых рынков. `winnerOutcome` в list-эндпоинте всегда `null`. Нет очевидного публичного способа получить исход рынка.
Решение:     CLOB `GET /last-trade-price?token_id={id}` возвращает финальную цену settled токена. price ≥ 0.99 = winner. token_id→outcome маппинг берётся из таблицы `trades` (каждый трейд содержит оба поля).
Инсайт:      Когда REST API закрывает доступ к resolved-ресурсам — ищи финансовые данные (цены, объёмы) как косвенный источник. Settled рынок всегда оставляет след в ценовой истории.

## [2026-03-04] — [PROJECT] — Рынок settled на CLOB, но active=1 в DB

**Теги:** api, sqlite, state-sync, polymarket

Контекст:    Алерт-маркеты показывали CLOB price=0.999 (явно resolved), но в DB стояло `active=1 closed=0`.
Сложность:   Монитор фетчит только active рынки от Gamma → состояние `closed` обновляется только если рынок попал в следующий цикл сбора. При простое монитора ≥ 1 цикл переход мог быть пропущен.
Решение:     В `_run_resolution_check` добавить отдельный проход по `alert_cids - closed_cids` — проверять CLOB для алерт-рынков вне зависимости от их статуса в DB.
Инсайт:      Локальный DB-статус ресурса может отставать от реального состояния внешней системы. Для критичных проверок (winner determination) — всегда запрашивай внешний источник напрямую, не полагайся на кэшированный флаг.

## [2026-03-04] — [PROJECT] — SVG progress ring: circumference formula

**Теги:** ui, svg, dashboard, math

Контекст:    Нужно было сделать score ring (0–100) на SVG без JS-расчётов в шаблоне.
Сложность:   `stroke-dasharray` требует знать полную длину окружности, иначе кольцо заполняется неверно.
Решение:     `C = floor(2π × r)`. Для r=13 → C=82; для r=20 → C=126. В шаблоне: `dash = (score/100 * C)|int`, `stroke-dasharray="{{ dash }} {{ C }}"`. SVG повёрнут на -90deg для старта с 12 часов.
Инсайт:     Всегда считай circumference заранее и хардкоди как константу в шаблон — это избавляет от JS и filter-вычислений. Разные размеры кольца = разные константы, но формула одна.

## [2026-03-04] — [PROJECT] — innerHTML overwrite уничтожает child-элементы DOM

**Теги:** ui, javascript, async, dom

Контекст:    Lazy-load wallet names через fetch → `el.innerHTML = '<span>name</span>'` — теряется ⚑ flag внутри элемента.
Сложность:   Флаг рендерился как child-span при серверном рендере, а async-замена перезаписывала весь innerHTML.
Решение:     Перед заменой читать `el.innerHTML.includes('⚑')` и условно реинсертировать символ в новый innerHTML.
Инсайт:      При async-обновлении DOM-узла, содержащего несколько дочерних элементов, либо обновляй только нужный child (querySelector внутри el), либо явно сохраняй состояние флагов перед overwrite.

---

## [2026-03-08] — [PROJECT] — Python MS Store stub: exit code 49 в bash на Windows

**Теги:** python, windows, bash, http-server

Контекст:    Запуск `python -m http.server 3000` в bash (Git Bash / Claude Code shell) на Windows — сервер не стартует.
Сложность:   `where python` показывает первым `C:\Users\...\WindowsApps\python.exe` — это Microsoft Store stub. Он выводит "Python" и завершается с exit code 49 (не запускает интерпретатор).
Решение:     Использовать `py -m http.server 3000` (Python Launcher, обходит stub). На конкретной машине можно также указать полный путь к python.exe минуя WindowsApps.
Инсайт:      Exit code 49 от `python` на Windows = MS Store stub. Диагностика: `where python` — если первый путь содержит `WindowsApps` → stub активен. Всегда использовать `py` (launcher) вместо `python` в bash-командах на Windows. Это уточнение к записи [2026-03-05].

---

## Индекс по тегам

<!-- Обновляется вручную или через Improve Skill -->

| Тег | Записи |
|-----|--------|
| llm | — |
| prompt | — |
| async | 2026-03-04 innerHTML overwrite |
| auth | — |
| state | 2026-03-04 Рынок settled, но active=1 в DB |
| perf | — |
| pdf | 2026-03-05 Brand color extraction из image-based PDF |
| python | 2026-03-05 Brand color extraction; 2026-03-05 UTF-8 encoding |
| color | 2026-03-05 Brand color extraction |
| pymupdf | 2026-03-05 Brand color extraction |
| windows | 2026-03-05 UTF-8 encoding |
| encoding | 2026-03-05 UTF-8 encoding |
| ui | 2026-03-04 SVG ring formula; 2026-03-04 innerHTML overwrite |
| svg | 2026-03-04 SVG ring formula |
| math | 2026-03-04 SVG ring formula |
| dom | 2026-03-04 innerHTML overwrite |
| api | 2026-03-04 Gamma 422 для закрытых рынков; 2026-03-04 active=1 state-sync |
| sqlite | 2026-03-04 Gamma 422; 2026-03-04 state-sync |
| polymarket | 2026-03-04 Gamma 422; 2026-03-04 state-sync |
| state-sync | 2026-03-04 active=1 в DB при settled CLOB |
