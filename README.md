# dns

1. Update `gen.py` to change DNS configuration.
2. `uv run gen.py` to generate configuration files for octodns.
3. `uv run octodns-sync --config-file config/production.yaml` to see changes.
4. `uv run octodns-sync --config-file config/production.yaml --doit` to apply changes.
