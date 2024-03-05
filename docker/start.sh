set -e

echo 'Starting app...'
uvicorn app.main:app --reload --host ${API_HOST}