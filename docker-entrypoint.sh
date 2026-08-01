#!/bin/sh
set -e

# Named volumes (static_data/media_data in docker-compose.yml) shadow whatever
# ownership was baked into the image at these paths on first mount, and stay
# root-owned if the volume already existed before this fix — so permissions
# are fixed here at every container start, not just at build time.
mkdir -p /app/staticfiles /app/media /app/logs
chown -R appuser:appgroup /app/staticfiles /app/media /app/logs

exec setpriv --reuid=appuser --regid=appgroup --clear-groups -- "$@"
