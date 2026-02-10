# DVC demo

Краткая инструкция по работе с данными через **DVC**.

## 1. Подготовка окружения

```bash
make project-init
```

Что делает команда:
- устанавливает зависимости (`uv sync`),
- инициализирует DVC (`dvc init`, если ещё не инициализирован),
- настраивает DVC remote через `scripts/init_dvc.py` на основе `.env`.

> Важно: если вы запускаете DVC с хоста, убедитесь, что `MINIO_HOST` в `.env`
> доступен из вашей среды (часто это `http://localhost`, а не `http://minio`).

## 2. Поднять MinIO

```bash
docker compose up -d
```

Сервис MinIO поднимается из `docker-compose.yml`.

## 3. Добавить данные под контроль DVC

Пример для папки датасета:

```bash
uv run dvc add data/dataset
git add data/dataset.dvc
git commit -m "Track dataset with DVC"
```

После `dvc add` сами большие файлы не хранятся в Git — в репозиторий попадает
`.dvc`-файл (метаданные) и обновлённый `.gitignore`.

## 4. Отправить данные в remote (MinIO)

```bash
uv run dvc push
```

Проверить состояние относительно remote:

```bash
uv run dvc status -c
```

## 5. Как скачать данные в новом клоне

```bash
git clone <repo-url>
cd dvc-demo
make project-init
docker compose up -d
uv run dvc pull
```

Команда `dvc pull` скачает данные из MinIO и восстановит их в рабочей директории.

## 6. Ежедневный workflow

Когда данные изменились:

```bash
uv run dvc add data/dataset
git add data/dataset.dvc .gitignore
git commit -m "Update dataset"
uv run dvc push
git push
```

Когда нужно просто получить актуальные данные:

```bash
git pull
uv run dvc pull
```

## Полезные команды

```bash
uv run dvc remote list      # список remote-хранилищ
uv run dvc pull             # скачать данные из remote
uv run dvc push             # загрузить данные в remote
uv run dvc status -c        # сравнить локальные данные с remote
uv run dvc doctor           # диагностика окружения DVC
```

