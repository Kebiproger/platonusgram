# ==========================================
# ЭТАП 1: Builder (Сборщик)
# Здесь мы ставим gcc и компилируем пакеты
# ==========================================
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Создаем виртуальное окружение и ставим туда все пакеты.
# Если pip потребуется скомпилировать asyncpg из исходников — gcc ему поможет.
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir -r requirements.txt

# ==========================================
# ЭТАП 2: Production (Чистовик)
# Никакого gcc, только минимальная среда
# ==========================================
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

ARG UID=1000
ARG GID=1000
RUN groupadd -g "${GID}" app \
    && useradd -m -u "${UID}" -g "${GID}" app

WORKDIR /app

# Копируем уже готовое, скомпилированное виртуальное окружение из этапа builder!
COPY --from=builder /opt/venv /opt/venv

# Копируем код бота
COPY --chown=app:app . .

USER app

CMD ["python", "-m", "backend.main"]