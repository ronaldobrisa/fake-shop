import logging
from logging.config import fileConfig

from flask import current_app
from sqlalchemy.engine import make_url

from alembic import context

# Configuração do logger
fileConfig(context.config.config_file_name)
logger = logging.getLogger('alembic.env')

def get_engine():
    """Obtém o motor do SQLAlchemy a partir da aplicação Flask."""
    try:
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError) as e:
        logger.error(f"Erro ao obter o motor do SQLAlchemy: {e}")
        raise

def get_engine_url():
    """Obtém a URL de conexão com o banco de dados."""
    try:
        url_object = get_engine().url
        return str(make_url(url_object)).replace('%', '%%')
    except AttributeError as e:
        logger.error(f"Erro ao obter a URL do banco de dados: {e}")
        raise

def get_metadata():
    """Obtém os metadados do banco de dados."""
    try:
        target_db = current_app.extensions['migrate'].db
        if hasattr(target_db, 'metadatas'):
            return target_db.metadatas[None]
        return target_db.metadata
    except AttributeError as e:
        logger.error(f"Erro ao obter os metadados: {e}")
        raise

def run_migrations_offline():
    """Executa as migrações no modo offline."""
    url = context.config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        logger.info("Iniciando transação para migrações offline.")
        context.run_migrations()
        logger.info("Migrações offline concluídas.")

def run_migrations_online():
    """Executa as migrações no modo online."""
    connectable = get_engine()

    with connectable.connect() as connection:
        logger.info("Conexão com o banco de dados estabelecida.")
        context.configure(
            connection=connection,
            target_metadata=get_metadata(),
            **current_app.extensions['migrate'].configure_args
        )

        with context.begin_transaction():
            logger.info("Iniciando transação para migrações online.")
            context.run_migrations()
            logger.info("Migrações online concluídas.")

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
