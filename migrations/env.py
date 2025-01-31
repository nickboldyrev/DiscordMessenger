from logging.config import fileConfig

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

from models.models import metadata


from src.config import DB_HOST, DB_NAME, DB_USER, DB_PASS
from src.database import AsyncSessionLocal, engine

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

section = config.config_ini_section
config.set_section_option(section, "DB_HOST", DB_HOST)
config.set_section_option(section, "DB_NAME", DB_NAME)
config.set_section_option(section, "DB_USER", DB_USER)
config.set_section_option(section, "DB_PASS", DB_PASS)

# Interpret the config file for Python logging.
# This line sets up loggers basically.
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
target_metadata = metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


async def run_migrations_online() -> None:
    async with engine.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            transactional_ddl=True,  # Используйте transactional DDL
        )

        async with AsyncSessionLocal() as session:
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                transactional_ddl=True,
                session=session,
            )

            async with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
