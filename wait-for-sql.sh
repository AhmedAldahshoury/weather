#!/bin/sh
# wait-for-sql.sh

set -e

HOST="$1"
PORT="$2"
shift 2

echo "Waiting for SQL Server at $HOST:$PORT..."

# Loop until the connection to the specified host and port is successful.
while ! nc -z "$HOST" "$PORT"; do
  echo "SQL Server not available yet. Waiting..."
  sleep 2
done

echo "SQL Server is up - executing command."
exec "$@"
