#!/usr/bin/env bash

set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
APP_FILE="test_drive_page.py"
PORT="${PORT:-8080}"
HOST="${HOST:-0.0.0.0}"
LOG_DIR="$ROOT_DIR/logs"
LOG_FILE="$LOG_DIR/streamlit.log"
PID_FILE="$ROOT_DIR/.streamlit.pid"

mkdir -p "$LOG_DIR"

if [[ -x "$ROOT_DIR/.venv/bin/python" ]]; then
    PYTHON_BIN="$ROOT_DIR/.venv/bin/python"
elif [[ -x "$ROOT_DIR/.venv-1/bin/python" ]]; then
    PYTHON_BIN="$ROOT_DIR/.venv-1/bin/python"
else
    PYTHON_BIN="$(command -v python3)"
fi

echo "Stopping any existing Streamlit process for $APP_FILE..."

if [[ -f "$PID_FILE" ]]; then
    OLD_PID="$(cat "$PID_FILE")"
    if [[ -n "$OLD_PID" ]] && kill -0 "$OLD_PID" 2>/dev/null; then
        kill "$OLD_PID" 2>/dev/null || true
        sleep 1
        kill -9 "$OLD_PID" 2>/dev/null || true
    fi
    rm -f "$PID_FILE"
fi

pkill -f "streamlit run $APP_FILE" 2>/dev/null || true

PORT_PIDS="$(lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null || true)"
if [[ -n "$PORT_PIDS" ]]; then
    echo "$PORT_PIDS" | xargs kill 2>/dev/null || true
    sleep 1
    PORT_PIDS="$(lsof -tiTCP:"$PORT" -sTCP:LISTEN 2>/dev/null || true)"
    if [[ -n "$PORT_PIDS" ]]; then
        echo "$PORT_PIDS" | xargs kill -9 2>/dev/null || true
    fi
fi

echo "Starting Streamlit on $HOST:$PORT..."
nohup "$PYTHON_BIN" -m streamlit run "$ROOT_DIR/$APP_FILE" --server.address "$HOST" --server.port "$PORT" >"$LOG_FILE" 2>&1 < /dev/null &
NEW_PID=$!
echo "$NEW_PID" > "$PID_FILE"

sleep 2

if kill -0 "$NEW_PID" 2>/dev/null; then
    echo "Streamlit started successfully."
    echo "PID: $NEW_PID"
    echo "URL: http://localhost:$PORT"
    echo "Log: $LOG_FILE"
else
    echo "Streamlit failed to start. Check $LOG_FILE for details." >&2
    exit 1
fi