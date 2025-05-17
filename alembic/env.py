from logging.config import fileConfig
from sqlalchemy import engine_from_config
from sqlalchemy import pool
from alembic import context

import sys
import os

# --- DEBUGGING PRINTS ---
print("env.py running")
print("Current working dir:", os.getcwd())
print("env.py __file__:", __file__)

# --- ENSURE PROJECT ROOT IS IN sys.path ---
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
print("Adding to sys.path:", PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)
print("sys.path:", sys.path)

# --- IMPORT BASE METADATA ---
from app.models import Base
target_metadata = Base.metadata

# --- ALEMBIC CONFIGURATION ---
config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

def run_migrations_offline():
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online():
    """Run migrations in 'online' mode."""
    section = config.get_section(config.config_ini_section)
    if section is None:
        section = {}

    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
