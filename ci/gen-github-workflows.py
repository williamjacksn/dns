import gen
import pathlib

this_file = pathlib.PurePosixPath(
    pathlib.Path(__file__).relative_to(pathlib.Path().resolve())
)

target = ".github/workflows/deploy-dns-settings.yaml"

gen_py = {"branches": ["main"], "paths": ["gen.py"]}
cf_env = {"CLOUDFLARE_TOKEN": "${{ secrets.cloudflare_token }}"}

content = {
    "env": {
        "description": f"This workflow ({target}) was generated from {this_file}",
    },
    "name": "Deploy DNS configuration",
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
        "deploy": {
            "name": "Deploy DNS configuration",
            "runs-on": "ubuntu-latest",
            "steps": [
                {"name": "Check out the repository", "uses": "actions/checkout@v4"},
                {"name": "Install uv", "run": "sh ci/install-uv.sh"},
                {"name": "Generate DNS configuration", "run": "sh ci/gen-config.sh"},
                {
                    "name": "Dry run deploy",
                    "if": "github.event_name == 'pull_request' || (github.event_name == 'workflow_dispatch' && inputs.dry_run)",
                    "env": cf_env,
                    "run": "sh ci/dry-run.sh",
                },
                {
                    "name": "Live deploy",
                    "if": "github.event_name == 'push' || (github.event_name == 'workflow_dispatch' && ! inputs.dry_run)",
                    "env": cf_env,
                    "run": "sh ci/deploy-dns.sh",
                },
            ],
        }
    },
}


gen.gen(content, target)
