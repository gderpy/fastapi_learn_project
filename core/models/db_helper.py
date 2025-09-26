from asyncio import current_task
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
    async_scoped_session,
)

from core.config import settings


class DataBaseHelper:
    """
    Класс помощник для работы с базой данных.

    Делает:
    1) Создает подключение к базе (engine)
    2) Настраивает "фабрику" для выдачи сессий (sessionmaker)
    3) Управляет сессиями так, чтобы каждая операция с БД получала свою
       отдельную сессию и не мешала другим
    """

    def __init__(self, url: str, echo: bool = False):
        """
        :param url: строка подключения к базе (например sqlite+aiosqlite:///db.sqlite3)
        :param echo: если True — выводит все SQL-запросы в консоль
        """
        # Создаём подключение к базе (engine)
        self.engine = create_async_engine(
            url=url,
            echo=echo,
        )
        # Фабрика для создания новых сессий работы с БД
        self.session_factory = async_sessionmaker(
            bind=self.engine,
            autoflush=False,  # не сохранять изменения автоматически
            autocommit=False,  # не коммитить автоматически
            expire_on_commit=False,  # данные в сессии не протухают после commit
        )

    def get_scoped_session(self):
        """
        Возвращает обертку над фабрикой сессий.

        Эта обертка нужна для того, чтобы:
        - если в коде в одном месте запросили сессию,
          а в другом месте - еще раз,
          то оба раза вернется одна и та же сессия.
        - после завершения работы сессия автоматически закрывается.
        """

        # scopefunc=current_task - привязка к текущей задаче выполнения
        session = async_scoped_session(
            session_factory=self.session_factory, scopefunc=current_task
        )
        return session

    async def session_dependency(self) -> AsyncSession:
        """
        Асинхронная зависимость для FastAPI.

        Создаёт новую сессию для работы с базой данных на каждый запрос.
        Сессия автоматически закрывается после завершения работы.
        Используйте эту зависимость, если нужна отдельная сессия для каждого запроса.
        """
        async with self.session_factory() as session:
            yield session
            await session.close()
        
    async def scoped_session_dependency(self) -> AsyncSession:
        """
        Асинхронная зависимость для FastAPI с использованием scoped session.

        Возвращает сессию, привязанную к текущей асинхронной задаче (например, к запросу).
        Одинаковая сессия будет использоваться в рамках одной задачи.
        Сессия автоматически закрывается после завершения работы.
        Используйте эту зависимость, если нужно, чтобы в рамках одного запроса
        использовалась одна и та же сессия в разных частях кода.
        """
        session = self.get_scoped_session()
        yield session
        await session.close()


db_helper = DataBaseHelper(url=settings.db.url, echo=settings.db.echo)
