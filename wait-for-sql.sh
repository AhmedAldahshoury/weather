#!/bin/sh
# wait-for-sql.sh

set -e

HOST="$1"
PORT="$2"
shift 2

echo "Waiting for SQL Server at $HOST:$PORT..."

while ! nc -z "$HOST" "$PORT" && ! timeout 1 bash -c "echo > /dev/tcp/$HOST/$PORT"; do
  echo "SQL Server not available yet. Waiting..."
  sleep 15
done

echo "SQL Server is up - executing command."
exec "$@"
