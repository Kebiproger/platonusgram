# 🎓 Platonusgram (IITU Student Bot)

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-orange?logo=telegram&logoColor=white)](https://docs.aiogram.dev/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker&logoColor=white)](https://www.docker.com/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **Высокопроизводительный асинхронный Telegram-бот**, предоставляющий современный, быстрый и безопасный мобильный интерфейс для университетской системы **Platonus**. 

Проект решает проблему сложной навигации по официальному порталу IITU, предоставляя студентам мгновенный доступ к оценкам прямо в мессенджере.

---

## 🌟 Ключевые особенности

### 👨‍🎓 Для студентов
- **⚡ Мгновенный отклик:** Благодаря системе кэширования (TTL 1 час), оценки загружаются за доли секунды.
- **📱 Идеальный UI/UX:** Интерактивное меню с кнопками. Бот редактирует сообщения, сохраняя чистоту чата.
- **🔒 Zero-Trust Безопасность:** 
  - Авторизация через **Telegram Web App**.
  - Пароль шифруется асимметричным ключом (RSA) на стороне клиента перед отправкой.
  - На сервере данные хранятся в зашифрованном виде (**AES-128 Fernet**).
- **🔔 Авто-уведомления:** (В разработке) Уведомления о новых оценках в реальном времени.

### 🛠 Технологический стек
| Слой | Технологии |
| :--- | :--- |
| **Core** | Python 3.12, `asyncio` |
| **Bot API** | `aiogram 3.x` |
| **Database** | `Tortoise ORM`, `aiosqlite` (WAL mode) |
| **Parsing** | `httpx` (HTTP/2), `BeautifulSoup4` (LXML) |
| **Security** | `cryptography` (RSA + Fernet) |
| **DevOps** | `Docker`, `Docker Compose` |

---

## 🏗 Архитектурные решения (HighLoad & Stealth)

- **🕵️ Стелс-парсинг:** 
  - Динамическая подмена `User-Agent` и заголовков.
  - Имитация поведения человека (алгоритм Jitter — случайные задержки).
  - Поддержка **HTTP/2** для ускорения запросов и обхода WAF.
- **🚥 Ограничение нагрузки (Rate Limiting):**
  - Использование `asyncio.Semaphore` для контроля конкурентных запросов к серверу Platonus.
  - Двухуровневый Anti-Spam (UI + бизнес-логика).
- **🗄 Оптимизация БД:**
  - Включен режим **Write-Ahead Logging (WAL)** для SQLite, что исключает блокировки `database is locked` при асинхронном доступе.
- **🍪 Умное управление сессиями:**
  - Кастомная обработка CookieJar для корректной работы с legacy-системами (Tomcat).

---

## 🚀 Быстрый старт

### Требования
* Docker & Docker Compose
* Telegram Bot Token (от [@BotFather](https://t.me/BotFather))

### Установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone https://github.com/Kebiproger/platonusgram.git
   cd platonusgram
   ```

2. **Настройте окружение:**
   ```bash
   cp .env.example .env
   # Обязательно заполните TELEGRAM_TOKEN и FERNET_KEY
   ```

3. **Сгенерируйте RSA ключи (для WebApp):**
   Проект требует `private.pem` для расшифровки данных из WebApp.
   ```bash
   openssl genrsa -out private.pem 2048
   openssl rsa -in private.pem -pubout -out public.pem
   ```

4. **Запустите через Docker:**
   ```bash
   docker-compose up -d --build
   ```

---

## 📁 Структура проекта

```text
├── main.py             # Точка входа, инициализация бота
├── bot_handler.py      # Логика обработки команд и WebApp данных
├── parser.py           # Асинхронный движок парсинга Platonus
├── models.py           # Схемы базы данных (Tortoise ORM)
├── crypto.py           # Модуль шифрования (AES & RSA)
├── keyboards.py        # Генерация интерактивных кнопок
├── config.py           # Конфигурация и логгирование
└── Dockerfile          # Инструкции для сборки контейнера
```

---

## 🔒 Дисклеймер

Данный проект является **независимой разработкой** и не аффилирован с администрацией IITU или разработчиками системы Platonus. Бот работает методом эмуляции браузера. Используя бота, вы подтверждаете, что делаете это на свой страх и риск.

---

## 🤝 Контрибьютинг

Pull requests приветствуются! Если вы нашли баг или хотите предложить фичу, создайте Issue.
