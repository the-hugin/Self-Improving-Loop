# Skill: sil-export

**Назначение:** Собрать локальные улучшения SIL (hard-problems, best-practices, skill changes) и отправить их в базовый GitHub-репо как PR. Часть федеративного цикла взаимообогащения.
**Когда использовать:** После нескольких циклов improve, когда накопились новые улучшения. Автоматически предлагается после `/improve`. Напоминается при старте сессии если прошло > 7 дней.
**Требования:** `gh` CLI установлен и авторизован (`gh auth login`), `git` установлен.

---

## PROCESS

### Шаг 1 — Проверь состояние

1. Прочитай `~/.claude/skills/sync-state.json`:
   - Если файл не существует — создай его из шаблона (см. ниже) и продолжай
   - Извлеки `base_repo` и `last_export`

2. Если `base_repo` пуст или null:
   ```
   Укажи URL базового репо (например: https://github.com/username/sil-base):
   ```
   Дождись ответа, сохрани в `sync-state.json`.

3. Проверь наличие `gh` CLI:
   ```bash
   gh --version
   ```
   Если не найден:
   ```
   gh CLI не установлен.
   Установи: https://cli.github.com/
   После установки выполни: gh auth login
   ```
   Остановись.

4. Сообщи пользователю:
   ```
   Последний экспорт: [last_export или "никогда"]
   Собираю контент новее этой даты...
   ```

---

### Шаг 2 — Собери новый контент

Читай каждый файл и извлекай записи НОВЕЕ даты `last_export`
(если `last_export` = null — бери все записи).

**`~/.claude/skills/hard-problems.md`:**
- Найди все записи `## [YYYY-MM-DD]` где дата > last_export
- Сохрани список новых записей

**`~/.claude/skills/best-practices.md`:**
- Аналогично

**`~/.claude/skills/changelog.md`:**
- Найди все строки где дата (первый столбец) > last_export
- Из этих строк извлеки список изменённых скиллов (второй столбец)

**Изменённые SKILL.md:**
- Для каждого уникального скилла из changelog — прочитай полный файл
  `~/.claude/skills/[skill-name]/SKILL.md`

Если ничего нового нет:
```
Нет новых улучшений для экспорта с [last_export].
Экспортировать нечего.
```
Остановись.

---

### Шаг 2.5 — Security scan (перед экспортом)

Прочитай `~/.claude/skills/sil-security-scan/patterns.md` и применяй все паттерны
к собранному контенту.

Сканируй: все новые записи hard-problems, best-practices, changelog, и SKILL.md файлы.

Если найден подозрительный паттерн:
```
⛔ SECURITY SCAN: подозрительный контент

Файл:     [filename]
Категория: [название]
Паттерн:  [паттерн]
Строка:   "[цитата]"

Этот фрагмент пропущен из экспорта.
```
Продолжай экспорт без этого фрагмента. Не останавливай весь экспорт из-за одного фрагмента.

---

### Шаг 3 — Санитизация

Для записей `hard-problems.md`:
- Найди упоминания конкретных проектов: имена папок, имена из заголовков записей
- Замени конкретные имена на `[PROJECT]`
- Пример: `## [2026-03-09] — aura-dating — ...` → `## [2026-03-09] — [PROJECT] — ...`

Покажи пользователю итоговый список:
```
Готово к экспорту:
  hard-problems: N новых записей
  best-practices: M новых записей
  changelog: K строк
  skill changes: [список скиллов]

Экспортировать? (да / нет)
```
Жди явного "да".

---

### Шаг 4 — Подготовь contribution файл

Сформируй содержимое `contribution-YYYY-MM-DD.md`:

```markdown
# SIL Contribution — YYYY-MM-DD

> Автоматически собрано через sil-export.
> Санитизировано: имена проектов заменены на [PROJECT].

## Hard Problems (N новых)

[все новые записи]

## Best Practices (N новых)

[все новые записи]

## Skill Changelog (K изменений)

[все новые строки changelog]

## Modified Skills

### [skill-name]
[полное содержимое SKILL.md]

---
[повтор для каждого изменённого скилла]
```

---

### Шаг 5 — Push на GitHub

```bash
# Шаг 5.1: Клонировать или обновить кэш base repo
CACHE_DIR="$HOME/.claude/.sil-base-cache"
BASE_REPO="[base_repo из sync-state.json]"

if [ -d "$CACHE_DIR/.git" ]; then
  cd "$CACHE_DIR" && git pull
else
  gh repo clone "$BASE_REPO" "$CACHE_DIR"
fi

# Шаг 5.2: Создать ветку
cd "$CACHE_DIR"
BRANCH="contribution/$(date +%Y-%m-%d)"
git checkout -b "$BRANCH"

# Шаг 5.3: Применить изменения
# Аппенд в hard-problems.md и best-practices.md
# Копировать изменённые SKILL.md
# Записать contribution-YYYY-MM-DD.md в корень

# Шаг 5.4: Commit и push
git add -A
git commit -m "feat: contribution from $(date +%Y-%m-%d)"
git push -u origin "$BRANCH"

# Шаг 5.5: Создать PR
gh pr create \
  --title "SIL Contribution — $(date +%Y-%m-%d)" \
  --body "Автоматический экспорт улучшений. N hard-problems, M best-practices, K skill changes." \
  --base main
```

Показать пользователю URL созданного PR.

---

### Шаг 6 — Обнови sync-state.json

Запиши в `~/.claude/skills/sync-state.json`:
```json
{
  "last_export": "YYYY-MM-DD",
  "exported_counts": {
    "hard_problems": N,
    "best_practices": M,
    "changelog_entries": K
  }
}
```
(остальные поля сохрани без изменений)

Финальное сообщение:
```
✓ PR создан: [URL]
✓ sync-state.json обновлён (last_export: YYYY-MM-DD)

Куратор получит уведомление о новом PR.
```

---

## Шаблон sync-state.json

```json
{
  "base_repo": null,
  "last_export": null,
  "last_sync": null,
  "exported_counts": {
    "hard_problems": 0,
    "best_practices": 0,
    "changelog_entries": 0
  }
}
```
