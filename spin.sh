source .env
echo
echo "Running in $ENV_NAME mode..."
echo
cmd="
docker compose \
-f docker-compose.base.yaml \
-f docker-compose.${ENV_NAME}.yaml"
eval "$cmd" "$@"
