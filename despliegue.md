# Inventario de configuración y secretos

Producido siguiendo `04_Playbooks/03_Preparar_Despliegue/PLAYBOOK.md` (Paso 1). Segunda búsqueda de literales en `src/` ya repetida antes de cerrar este archivo — sin hallazgos nuevos.

DATABASE_URL (secreto) — cadena de conexión completa a PostgreSQL, distinta en cada entorno
POSTGRES_USER (secreto)
POSTGRES_PASSWORD (secreto)
POSTGRES_DB (no secreto, nombre de la base de datos)
APP_PORT (no secreto, valor por defecto 8000)

Entorno de destino de este proyecto (ver `docs/deployment.md` y `spec.md` — alcance deliberadamente local): Docker Compose en la propia máquina, no una plataforma cloud. Ningún literal hardcodeado quedó en `src/` tras la segunda búsqueda: `src/database.py` ya leía `DATABASE_URL` de una variable de entorno desde M2 (ver `os.environ.get(...)`), con un valor por defecto solo para desarrollo local sin Docker.
