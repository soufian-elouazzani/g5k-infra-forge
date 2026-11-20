import logging
import subprocess
from pathlib import Path

import enoslib as en

en.init_logging(level=logging.INFO)
en.check()

# Grid'5000 frontends. `ssh <site>` relies on the usual ~/.ssh/config aliases.
SITES = (
    "grenoble",
    "lille",
    "luxembourg",
    "lyon",
    "nancy",
    "nantes",
    "rennes",
    "sophia",
    "strasbourg",
)


def list_user_jobs():
    """Print the current user's OAR jobs on each Grid'5000 site."""
    for site in SITES:
        print(f"=== {site} ===")
        subprocess.run(
            ["ssh", "-o", "ConnectTimeout=3", site, "oarstat", "-u"],
            check=False,
        )


list_user_jobs()

job_name = Path(__file__).name

conf = (
    en.G5kConf.from_settings(job_name=job_name, walltime="0:10:00")
    .add_machine(roles=["groupA"], cluster="paradoxe", nodes=1)
    .add_machine(roles=["groupB"], cluster="parasilo", nodes=1)
)

# This will validate the configuration, but not reserve resources yet
provider = en.G5k(conf)

# Get actual resources
roles, networks = provider.init()
# Do your stuff here
# ...


# Release all Grid'5000 resources
provider.destroy()