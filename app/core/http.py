import httpx

# backend/services/http.py
import httpx

# Настраиваем лимиты один раз здесь
http_limits = httpx.Limits(max_connections=20, max_keepalive_connections=10)

# Создаем ОДИН экземпляр на весь проект
http_client = httpx.AsyncClient(limits=http_limits, timeout=15.0)