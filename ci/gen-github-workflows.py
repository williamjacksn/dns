import gen

gen_py = {"branches": ["main"], "paths": ["gen.py"]}

workflow = {
    "name": "Compile octoDNS settings and deploy to production",
    "on": {
        "pull_request": gen_py,
        "push": gen_py,
        "workflow_dispatch": {
            "inputs": {
                "dry_run": {
                    "default": True,
                    "description": "Perform a dry run, do not actually change any DNS records",
                    "type": "boolean",
                }
            }
        },
    },
    "jobs": {
        "compile": {
            "name": "Compile and deploy octoDNS settings",
            "runs-on": "ubuntu-latest",
            "steps": [
                {"name": "Check out the repository", "uses": "actions/checkout@v4"},
                {"name": "Install uv", "run": "sh ci/install-uv.sh"},
                {"name": "Compile octoDNS settings", "run": "sh ci/gen-config.sh"},
                {
                    "name": "Sync dry run",
                    "if": "github.even_name == 'pull_request' || (github.event_name == 'workflow_dispatch' && inputs.dry_run)",
                    "env": {"CLOUDFLARE_TOKEN": "${{ secrets.cloudflare_token }}"},
                    "run": "sh ci/dry-run.sh",
                },
                {
                    "name": "Sync for real",
                    "if": "github.even_name == 'push' || (github.event_name == 'workflow_dispatch' && ! inputs.dry_run)",
                    "env": {"CLOUDFLARE_TOKEN": "${{ secrets.cloudflare_token }}"},
                    "run": "sh ci/deploy-dns.sh",
                },
            ],
        }
    },
}


gen.gen(workflow, ".github/workflows/deploy-dns-settings.yaml")
