# Задание

Разработать эмулятор для языка оболочки ОС. Необходимо сделать работу  
эмулятора как можно более похожей на сеанс shell в UNIX-подобной ОС.  
Эмулятор должен запускаться из реальной командной строки, а файл с  
виртуальной файловой системой не нужно распаковывать у пользователя.  
Эмулятор принимает образ виртуальной файловой системы в виде файла формата  
zip. Эмулятор должен работать в режиме CLI.

Конфигурационный файл имеет формат toml и содержит:  
- Имя пользователя для показа в приглашении к вводу.  
- Имя компьютера для показа в приглашении к вводу.  
- Путь к архиву виртуальной файловой системы.  
- Путь к лог-файлу.

Лог-файл имеет формат json и содержит все действия во время последнего  
сеанса работы с эмулятором. Для каждого действия указан пользователь.

Необходимо поддержать в эмуляторе команды `ls`, `cd` и `exit`, а также  
следующие команды:  
1. `clear`  
2. `touch`

---

## Описание проекта

Данный проект представляет собой эмулятор простой командной оболочки (shell emulator), который имитирует работу с файлами и директориями, используя сжатую файловую систему (ZIP-архив) и конфигурационный файл. С помощью этой оболочки можно выполнять базовые команды:

- `ls` – просмотр содержимого текущей директории
- `cd` – переход между директориями
- `touch` – создание пустого файла
- `clear` – очистка экрана
- `exit` – выход из эмулятора

Все выполняемые действия логируются в специальный JSON-файл.

## Структура проекта

```
.
├── config.toml             # Конфигурационный файл
├── emulator_shell.py        # Основной скрипт эмулятора оболочки
├── session_log.json         # Пример лог-файла с историей действий пользователя
└── filesystem.zip           # ZIP-архив с виртуальной файловой системой
```

## Основной функционал

- **Чтение конфигурации** из `config.toml`:
  - Имя пользователя
  - Имя компьютера
  - Путь к ZIP-архиву с файловой системой
  - Путь к лог-файлу

- **Инициализация файловой системы**:
  - Извлечение файловой системы из ZIP-архива во временную директорию
  - Навигация и управление файлами в рамках этой виртуальной среды

- **Команды эмулятора**:
  - `ls`: вывести список файлов и директорий
  - `cd <путь>`: перейти в указанную директорию
  - `touch <имя_файла>`: создать новый пустой файл
  - `clear`: очистить терминал
  - `exit`: выйти из эмулятора и сохранить лог действий

- **Логирование действий**:
  - Все действия пользователя фиксируются в `session_log.json` с временными метками

## Установка зависимостей

```bash
pip install toml
```

Все остальные используемые библиотеки (`os`, `zipfile`, `json`, `shutil`, `tempfile`, `pathlib`, `datetime`, `argparse`) входят в стандартную библиотеку Python.

## Запуск

1. Проверьте, что в `config.toml` указаны корректные пути к `filesystem.zip` и `session_log.json`.
2. Запустите проект:
   ```bash
   python3 emulator_shell.py config.toml
   ```
3. В терминале появится приглашение, например:
   ```bash
   test_user@test_computer:/$
   ```
   Вводите доступные команды для управления виртуальной файловой системой.

## Автор

Автор: *Nedavi*  
