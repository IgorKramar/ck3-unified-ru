<div align="center">

# CK3 Unified RU

### Больше историй. Единый мир. Русский язык.

Совместимость и русификация исторической сборки Crusader Kings III для Windows и Steam Deck.

![Status](https://img.shields.io/badge/status-in_development-e0af68?style=flat-square)
![Reference](https://img.shields.io/badge/reference-CK3_1.20.1.1-7aa2f7?style=flat-square)
![Python](https://img.shields.io/badge/tools-Python_3.10+-bb9af7?style=flat-square)

[Состояние](docs/STATUS.md) · [План](ROADMAP.md) · [Состав](docs/MOD_CATALOG.md) · [Права и авторы](CREDITS.md)

</div>

**В разработке. Готового игрового выпуска, установщика и публикации Workshop пока нет.** Этот репозиторий содержит открытое досье проекта и собственные инструменты проверки. Архив репозитория не устанавливает сборку в игру.

## Замысел

Расширить оригинальную историческую CK3: культуры, внешний вид персонажей, события, отношения, вассалы, путешествия, исторические вторжения и география. Объединить выбранные моды логически, устранить конфликты и заполнить пробелы русского перевода. Целевые платформы — Windows PC и Steam Deck/SteamOS. Используются законно приобретённые DLC; проект не предоставляет DLC и не обходит их проверку.

## Что уже проверялось

Последний локальный эталон — **1.20.1.1 Crozier**. Это версия октябрьских испытаний, не обещание поддержки всех новых обновлений.

| Область | Состояние |
|---|---|
| Диагностическое ядро из 15 исходных модов | Локально собрано; прогоны разных ревизий описаны в отчёте |
| Последняя ревизия v6 | Загрузка истории и три целевые проверки; полноценная кампания этой ревизии не подтверждена |
| Русский язык | Объединены существующие переводы и 459 собственных точечных дополнений; остаются пробелы и редакторская проверка |
| Карта | Аудит доноров и прототип Палау; объединённая расширенная карта не готова |
| Steam Deck | Есть статический аудит путей; реального запуска на SteamOS ещё нет |
| Распространение | Требуется отдельное разрешение на материалы ряда авторов |

Сводка оформлена 31 октября 2026 года по сохранённым локальным отчётам. При оформлении репозитория игра повторно не запускалась. Подробности и границы результатов — [STATUS.md](docs/STATUS.md).

## Инструменты

Нужен Python 3.10+. Для этих трёх инструментов внешние библиотеки не требуются.

```sh
python -m unittest discover -s tests -v
python tools/audit_linux_paths.py --game "/path/to/CK3/game" --mod "/path/to/staged-mod" --report paths.json
python tools/compare_runtime_logs.py --baseline vanilla-error.log --core modded-error.log --report comparison.json
```

- `paradox.py` — чтение диапазонов Paradox Script и точечные изменения с сохранением исходного текста. Это небольшой вспомогательный парсер, не полная реализация языка.
- `audit_linux_paths.py` — статическая проверка регистра путей в подготовленном моде. Не проверяет смонтированные DLC и вычисляемые пути, не доказывает работу на Linux.
- `compare_runtime_logs.py` — сравнение точных отпечатков ошибок с запуском без модов. Несовпадение само по себе не доказывает вину мода.

Игра и чужие моды для запуска unit-тестов не нужны. Аудиторы читают указанные локальные каталоги и логи; отчёты могут содержать их фрагменты. Просматривайте отчёты перед публикацией.

## Участие

Предложения и воспроизводимые проблемы — через Issues. См. [CONTRIBUTING.md](CONTRIBUTING.md). Собственный код опубликован под MIT; лицензия не распространяется на CK3 и материалы внешних модов. Исходные игровые файлы, приватные сборки и чужие переводы сюда не включены.

## English

Work in progress: historical Crusader Kings III compatibility and Russian localization project targeting Windows and Steam Deck. This repository publishes original audit utilities and project documentation, not a playable merged mod. The last local reference is CK3 1.20.1.1; SteamOS runtime testing and map integration remain pending. See the status report and credits before using or contributing.
