mamba install "$@"
#mamba env export --from-history >env.yaml
mamba env export >env.yaml
#conda-lock -p linux-64 -f env.yaml
