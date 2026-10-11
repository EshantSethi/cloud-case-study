import os

# On Render (PaaS) the platform injects DATABASE_URL automatically.
# The AZURE_* variables are kept so the original Azure deployment still works.
_render_url = os.getenv('DATABASE_URL')
if _render_url:
    # SQLAlchemy needs the driver name (psycopg2) in the URL
    DATABASE_URI = _render_url.replace('postgres://', 'postgresql://', 1).replace('postgresql://', 'postgresql+psycopg2://', 1)
else:
    DATABASE_URI = 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
        dbuser=os.getenv('AZURE_POSTGRESQL_USER'),
        dbpass=os.getenv('AZURE_POSTGRESQL_PASSWORD'),
        dbhost=os.getenv('AZURE_POSTGRESQL_HOST'),
        dbname=os.getenv('AZURE_POSTGRESQL_NAME')
    )
