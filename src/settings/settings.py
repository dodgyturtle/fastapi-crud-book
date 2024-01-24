import os

# For more information about these environment variables, see README.MD

# ==== Postgres settings ====
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
POSTGRES_HOSTNAME = os.getenv("POSTGRES_HOSTNAME", "localhost")
DATABASE_PORT = int(os.getenv("DATABASE_PORT", "5432"))
POSTGRES_DB = os.getenv("POSTGRES_DB", "bookcrud")


# Programm Settings
AGE_LIMIT = int(os.getenv("AGE_LIMIT", "18"))
