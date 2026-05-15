# 🎓 Platonusgram (IITU Student Bot)

[![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Aiogram](https://img.shields.io/badge/Aiogram-3.x-orange?logo=telegram&logoColor=white)](https://docs.aiogram.dev/)
[![Docker](https://img.shields.io/badge/Docker-Enabled-blue?logo=docker&logoColor=white)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

> **Высокопроизводительный асинхронный Telegram-бот**, предоставляющий современный, быстрый и безопасный мобильный интерфейс для университетской системы **Platonus**.

**⚠️ Внимание: Данный проект является некоммерческим.** Разработан студентами для студентов в целях упрощения доступа к академическим данным.

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
- **🔔 Авто-уведомления:** Уведомления о новых оценках в реальном времени.

### 🛠 Технологический стек
| Слой | Технологии |
| :--- | :--- |
| **Core** | Python 3.12, `asyncio` |
| **Bot API** | `aiogram 3.x` |
| **Database** | `Tortoise ORM`, `PostgreSQL` (`asyncpg`) |
| **Parsing** | `httpx` (HTTP/2), `BeautifulSoup4` (LXML) |
| **Security** | `cryptography` (RSA + Fernet) |
| **DevOps** | `Docker`, `Docker Compose` |

---

## 🏗 Архитектурные решения (HighLoad & Stealth)

- **🕵️ Стелс-парсинг:** 
  - Динамическая подмена `User-Agent` и заголовков.
  - Имитация поведения человека (алгоритм Jitter — случайные задержки).
  - Поддержка **HTTP/2** для ускорения запросов и обхода WAF.
- **🚥 Ограничение нагрузки (`aiolimiter`):**
  - Использование `asyncio.Semaphore` для контроля конкурентных запросов к серверу Platonus.
  - Двухуровневый Anti-Spam (UI + бизнес-логика).
- **🗄 Надежное хранилище:**
  - Переход на **PostgreSQL** для обеспечения целостности данных и поддержки высоконагруженных операций.
  - Асинхронное взаимодействие через `asyncpg`.
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
   # Обязательно заполните TELEGRAM_TOKEN, FERNET_KEY и параметры БД
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
├── backend/            # Серверная часть и бизнес-логика
│   ├── main.py         # Точка входа
│   ├── parser.py       # Движок парсинга Platonus
│   ├── tasks.py        # Фоновые задачи (APScheduler)
│   ├── crypto.py       # Шифрование (AES & RSA)
│   ├── config.py       # Конфигурация
│   └── db/             # Работа с базой данных
│       ├── models.py   # Модели Tortoise ORM
│       └── db_config.py# Настройки подключения
├── bot/                # Telegram-интерфейс
│   ├── bot_handler.py  # Обработка WebApp и сообщений
│   ├── commands.py     # Команды бота
│   ├── keyboards.py    # Клавиатуры
│   └── middlewares.py  # Промежуточные слои (Throttle и др.)
├── migrations/         # Миграции базы данных (Aerich)
├── docker-compose.yml  # Оркестрация контейнеров
└── .env.example        # Шаблон переменных окружения
```

---

## 🔒 Дисклеймер

Данный проект является **некоммерческой независимой разработкой** и не аффилирован с администрацией IITU или разработчиками системы Platonus. Бот работает методом эмуляции браузера. Используя бота, вы подтверждаете, что делаете это на свой страх и риск.

---

## 🤝 Контрибьютинг

Pull requests приветствуются! Если вы нашли баг или хотите предложить фичу, создайте Issue.

---

## 📄 Лицензия

Проект является полностью **Open-Source** и распространяется на условиях лицензии [MIT](LICENSE).
