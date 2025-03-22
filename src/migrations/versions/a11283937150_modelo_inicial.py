"""modelo inicial

Revision ID: a11283937150
Revises: 
Create Date: 2024-10-29 19:10:34.007299

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
from models.product import Product
import logging

# Configuração do logger
logger = logging.getLogger(__name__)

# revision identifiers, used by Alembic.
revision = 'a11283937150'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ... (criação das tabelas)

    # Inserir produtos após a criação da tabela
    bind = op.get_bind()
    session = Session(bind=bind)

    products = [
        # ... (lista de produtos)
    ]

    try:
        session.bulk_save_objects(products)
        session.commit()
        logger.info("Produtos inseridos com sucesso.")
    except Exception as e:
        logger.error(f"Erro ao inserir produtos: {e}")
        session.rollback()
    finally:
        session.close()


def downgrade():
    # ... (remoção das tabelas)