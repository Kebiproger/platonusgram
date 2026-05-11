from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Callable, Dict, Any, Awaitable
from models import User # Твоя БД

class UserCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        print(f"DEBUG: Middleware сработал для юзера {event.from_user.id}")
        if isinstance(event, Message):
            if event.text and event.text.startswith("/start"):
                return await handler(event, data)
        # 1. Ищем юзера в базе
        user = await User.get_or_none(telegram_id=event.from_user.id)
        
        # 2. Если юзера нет — отбиваем запрос прямо здесь!
        if not user:
            await event.answer("❌ Пожалуйста, зарегистрируйтесь через /start.")
            # Мы НЕ вызываем handler, поэтому до хэндлеров запрос даже не дойдет
            return 
            
        # 3. Если юзер есть, кладем его в "посылку" (data) 
        data['user'] = user
        
        # 4. Пропускаем сообщение дальше в хэндлер
        return await handler(event, data)