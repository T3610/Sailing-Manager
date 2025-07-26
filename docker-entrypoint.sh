#!/bin/sh
echo "--- Starting docker-entrypoint.sh ---"
echo "Current user: $(whoami) (UID=$(id -u), GID=$(id -g))"
echo "Target directory for chown: /sailmanager/staticfiles"
ls -la /sailmanager/staticfiles # Show original permissions before chown

# Attempt to chown the directory
chown -R appuser:appuser /sailmanager/staticfiles
CHOWN_EXIT_CODE=$? # Capture the exit code of the last command

if [ "$CHOWN_EXIT_CODE" -eq 0 ]; then
    echo "chown command completed successfully."
else
    echo "chown command failed with exit code: $CHOWN_EXIT_CODE"
    # Print an error message if chown fails
    echo "Possible reasons: User 'appuser' not found, or insufficient permissions for chown."
fi

echo "Permissions after chown attempt:"
ls -la /sailmanager/staticfiles # Show permissions after chown attempt

echo "--- Executing CMD: \"$@\" ---"
exec "$@"
