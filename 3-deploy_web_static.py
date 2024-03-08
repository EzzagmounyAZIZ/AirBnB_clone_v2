#!/usr/bin/env python3
"""
Fabric script that creates and distributes an archive to web servers using deploy function.
"""
from fabric.api import local, run, put, env
from datetime import datetime

# Import the do_pack and do_deploy functions from previous scripts
from 1-pack_web_static import do_pack
from 2-do_deploy_web_static import do_deploy

# Define the remote servers
env.hosts = ['<IP web-01>', '<IP web-02>']

def deploy():
    """
    Create and distribute an archive to web servers using deploy function.

    Returns:
        bool: True if all operations have been done correctly, False otherwise.
    """
    # Call the do_pack function and store the path of the created archive
    archive_path = do_pack()

    if not archive_path:
        return False

    try:
        # Call the do_deploy function using the new path of the new archive
        return do_deploy(archive_path)

    except Exception as e:
        return False

if __name__ == "__main__":
    # Example usage: fab -f 3-deploy_web_static.py deploy -i my_ssh_private_key -u ubuntu
    deploy()
