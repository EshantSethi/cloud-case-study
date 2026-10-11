import os

# On Render (PaaS) the platform injects DATABASE_URL automatically.
# The AZURE_* variables are kept so the original Azure deployment still works.
DATABASE_URI = os.getenv('DATABASE_URL') or 'postgresql+psycopg2://{dbuser}:{dbpass}@{dbhost}/{dbname}'.format(
    dbuser=os.getenv('AZURE_POSTGRESQL_USER'),
    dbpass=os.getenv('AZURE_POSTGRESQL_PASSWORD'),
    dbhost=os.getenv('AZURE_POSTGRESQL_HOST'),
    dbname=os.getenv('AZURE_POSTGRESQL_NAME')
)
