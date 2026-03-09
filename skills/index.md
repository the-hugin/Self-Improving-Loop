# Skills Index

> Реестр всех скиллов системы. Живёт в `~/.claude/skills/` — работает across all projects.
> Обновляется через Improve Skill после каждого цикла reflect → improve.
> **Правило:** перед созданием нового скилла — проверь этот файл на дубликаты.

---

## Группа: Цикл (Meta-Loop)

> Три скилла, которые образуют self-improving loop. Запускаются в этом порядке.

| # | Скилл     | Назначение                                | Теги           | Использований | Статус   |
|---|-----------|-------------------------------------------|----------------|---------------|----------|
| 1 | `intake`  | Онбординг проекта → заполненный CLAUDE.md | meta, start    | 0             | ✅ Ready |
| 2 | `reflect` | Анализ сессии → reflection.md             | meta, loop     | 4             | ✅ Ready |
| 3 | `improve` | Обновление скиллов по reflection.md       | meta, loop     | 2             | ✅ Ready |

```
Поток: intake → [работа] → reflect → [строка коррекции] → improve → обновлённые скиллы
```

---

## Группа: Система (Meta-Tools)

> Скиллы для обслуживания самой системы скиллов.

| Скилл           | Назначение                              | Теги         | Использований | Статус   |
|-----------------|-----------------------------------------|--------------|---------------|----------|
| `skill-creator` | Создание нового скилла по шаблону       | meta, tools  | 0             | ✅ Ready |

---

## Группа: Security

> Специализированные скиллы для security-аудита кода. Адаптированы из методологии Trail of Bits.

| Скилл | Назначение | Теги | Статус |
|-------|-----------|------|--------|
| `differential-review` | Security-ревью PR/diff: blast radius, adversarial modeling, 7-фазный workflow | security, review | ✅ Ready |
| `insecure-defaults` | Поиск fail-open уязвимостей: слабые env var defaults, hardcoded creds, слабые алгоритмы | security, config | ✅ Ready |

---

## Группа: Домен

> Специализированные скиллы для конкретных типов задач разработки.

| Скилл                 | Назначение                                          | Теги              | Статус   |
|-----------------------|-----------------------------------------------------|-------------------|----------|
| `backend-code-review` | Ревью backend-кода на качество и безопасность       | code, review      | ✅ Ready |
| `design-master`       | Unified mega-skill: landing, dashboard, poster, interactive — с quality gate | code, ui, design | 1 | ✅ Ready |
| `frontend-design`     | Создание production-grade интерфейсов               | code, ui          | ✅ Ready |
| `ui-ux-pro-max`       | 67 стилей, 96 палитр, 57 шрифтов, Python-генератор дизайн-систем | code, ui, design | ✅ Ready |
| `electron-dev`        | Desktop-приложения с Electron + React + Vite        | code, desktop     | ✅ Ready |
| `data-analyst`        | SQL, pandas, статистический анализ данных           | data, sql         | ✅ Ready |
| `web-scraper`         | Скрапинг и извлечение данных с веб-страниц          | data, scraping    | ✅ Ready |
| `ui-component-library`| Каталог HTML/CSS/JS компонентов для dashboard-проектов | code, ui       | ✅ Ready |
| `doc-creator`         | Создание документов/гайдов из источников (PDF, DOCX, сайт) | code, docs  | ✅ Ready |
| `extract-brand-palette`| Извлечение hex-палитры бренда из image-based PDF/PNG | data, pdf        | ✅ Ready |
| `api-endpoint-probe`  | Разведка параметров API-эндпоинта перед реализацией (фильтры, пагинация, лимиты) | data, api | ✅ Ready |
| `sales-guide`         | Онбординг и создание продуктовых/портфельных гайдов из документов (docx, PDF, сайт) | docs, sales | ✅ Ready |

---

## Группа: Поиск и данные

| Скилл            | Назначение                                        | Теги          | Статус   |
|------------------|---------------------------------------------------|---------------|----------|
| `searxng-search` | Поиск в интернете через локальный SearXNG         | search, data  | ✅ Ready |

---

## Группа: Автоматизация

| Скилл                    | Назначение                                            | Теги               | Статус   |
|--------------------------|-------------------------------------------------------|--------------------|----------|
| `hooks-automation`       | Автоматизация через Claude Code hooks + MCP           | automation, tools  | ✅ Ready |
| `configure-notifications`| Настройка уведомлений (Telegram, Discord, Slack)      | automation, tools  | ✅ Ready |

---

## Группа: Federation (SIL распределённый цикл)

> Скиллы для взаимообогащения SIL между пользователями через GitHub.

| Скилл | Назначение | Теги | Использований | Статус |
|-------|-----------|------|---------------|--------|
| `sil-export` | Собрать улучшения и отправить PR в base repo | meta, federation | 0 | ✅ Ready |
| `sil-sync` | Получить обновления из base repo с security scan | meta, federation | 0 | ✅ Ready |
| `sil-security-scan` | Паттерны безопасности для входящего/исходящего контента | meta, security, federation | 0 | ✅ Ready |

---

## Группа: Мета

| Скилл                 | Назначение                                         | Теги          | Статус   |
|-----------------------|----------------------------------------------------|---------------|----------|
| `skill-generator`     | Создание новых скиллов с правильной структурой     | meta, tools   | ✅ Ready |
| `extract-errors`      | Добавление кодов ошибок в React-проекты            | code, react   | ✅ Ready |
| `multi-agent-patterns`| Оркестрация multi-agent архитектур                 | meta, agents  | ✅ Ready |
| `project-planner`     | Декомпозиция проектов на задачи с зависимостями    | meta, planning| ✅ Ready |
| `security-baseline`   | Генерация секции SECURITY CONSTRAINTS в CLAUDE.md  | meta, security| ✅ Ready |
| `validate-claude-md`  | Проверка CLAUDE.md на соответствие стандарту intake | meta, quality | ✅ Ready |
| `migrate-claude-md`   | Приведение старого CLAUDE.md к актуальному стандарту | meta, quality | ✅ Ready |

---

## Как вызвать скилл

```
"Используй скилл [название]"
"@~/.claude/skills/[название]/SKILL.md"
```

Или через slash-команду:

| Команда          | Файл                                      |
|------------------|-------------------------------------------|
| `/intake`        | `~/.claude/commands/intake.md`            |
| `/reflect`       | `~/.claude/commands/reflect.md`           |
| `/improve`       | `~/.claude/commands/improve.md`           |
| `/sil`           | `~/.claude/commands/sil.md`               |
| `/weekly-review` | `~/.claude/commands/weekly-review.md`     |
| `/diff-review`   | `~/.claude/commands/diff-review.md`       |

**Файлы базы знаний:**
- `~/.claude/skills/hard-problems.md` — журнал сложных случаев
- `~/.claude/skills/best-practices.md` — журнал успешных паттернов
- `~/.claude/reflection.md` — текущий pending reflection (глобальный)
- `~/.claude/reflection-*.md` — архив завершённых рефлексий

---

## Как добавить новый скилл

1. Запусти `skill-creator` — он создаст `~/.claude/skills/[name]/SKILL.md` по шаблону
2. Добавь строку в нужную группу выше
3. Опционально: создай `~/.claude/commands/[name].md`

---

## Архив (устаревшие скиллы)

| Скилл | Причина архивации | Дата |
|-------|-------------------|------|
| —     | —                 | —    |
