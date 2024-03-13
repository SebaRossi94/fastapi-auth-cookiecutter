set -e

echo 'Starting app...'
python -m debugpy --listen 0.0.0.0:5678 -m uvicorn app.main:app --reload --host ${API_HOST}
# uvicorn app.main:app --reload --host ${API_HOST}