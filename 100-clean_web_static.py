#!/usr/bin/env python3
"""
Fabric script that deletes out-of-date archives using do_clean function.
"""
from fabric.api import local, run, env
from datetime import datetime

# Define the remote servers
env.hosts = ['<IP web-01>', '<IP web-02>']

def do_clean(number=0):
    """
    Delete out-of-date archives.

    Args:
        number (int): Number of archives to keep.

    Returns:
        bool: True if all operations have been done correctly, False otherwise.
    """
    try:
        # Convert the number of archives to an integer
        number = int(number)

        # Keep only the most recent and 'number' archives in the versions folder
        local("ls -lt versions | awk 'NR>{} {{print $NF}}' | xargs -I {{}} rm versions/{{}}".format(number))

        # Keep only the most recent and 'number' archives in the releases folder on both servers
        run("ls -lt /data/web_static/releases | awk 'NR>{} {{print $NF}}' | xargs -I {{}} rm -rf /data/web_static/releases/{{}}".format(number))

        return True

    except Exception as e:
        return False

if __name__ == "__main__":
    # Example usage: fab -f 100-clean_web_static.py do_clean:number=2 -i my_ssh_private_key -u ubuntu
    do_clean()
