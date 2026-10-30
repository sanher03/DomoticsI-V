#!/bin/sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT_DIR"

if ! command -v docker >/dev/null 2>&1; then
    echo "Docker is required. Install Docker Desktop or Docker Engine with Compose." >&2
    exit 1
fi

docker compose up --build --detach

echo
WEB_URL="http://localhost:${WEB_PORT:-8000}"
echo "The application is starting. Open ${WEB_URL}"
if command -v xdg-open >/dev/null 2>&1; then
    if xdg-open "$WEB_URL" >/dev/null 2>&1; then
        echo "Opened the application in the browser."
    else
        echo "Could not open a browser automatically; use ${WEB_URL}."
    fi
elif command -v open >/dev/null 2>&1; then
    if open "$WEB_URL" >/dev/null 2>&1; then
        echo "Opened the application in the browser."
    else
        echo "Could not open a browser automatically; use ${WEB_URL}."
    fi
fi
echo "To reach it from another device on the same network, use this computer's LAN IP:"
if command -v ip >/dev/null 2>&1; then
    LAN_IP=$(ip -4 route get 1.1.1.1 2>/dev/null | awk '{ for (i = 1; i <= NF; i++) if ($i == "src") { print $(i + 1); exit } }')
    if [ -n "$LAN_IP" ]; then
        echo "  http://${LAN_IP}:${WEB_PORT:-8000}"
    else
        echo "  Find this computer's local IPv4 address and use http://<IP>:${WEB_PORT:-8000}"
    fi
else
    echo "  Find this computer's local IPv4 address and use http://<IP>:${WEB_PORT:-8000}"
fi
echo
echo "View logs:   docker compose logs -f"
echo "Stop:        ./scripts/stop.sh"
