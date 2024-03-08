#!/usr/bin/env python3
"""
Fabric script that distributes an archive to web servers using do_deploy function.
"""
from fabric.api import run, put, env
from os.path import exists
from datetime import datetime

# Define the remote servers
env.hosts = ['<IP web-01>', '<IP web-02>']

def do_deploy(archive_path):
    """
    Distribute an archive to web servers and deploy it.

    Args:
        archive_path (str): Path to the archive to deploy.

    Returns:
        bool: True if all operations have been done correctly, False otherwise.
    """
    if not exists(archive_path):
        return False

    try:
        # Upload the archive to the /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to the releases folder
        archive_filename = archive_path.split('/')[-1]
        release_folder = '/data/web_static/releases/{}'.format(archive_filename.split('.')[0])
        run('mkdir -p {}'.format(release_folder))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_folder))

        # Remove the uploaded archive
        run('rm /tmp/{}'.format(archive_filename))

        # Move contents from web_static to the release folder
        run('mv {}/web_static/* {}'.format(release_folder, release_folder))

        # Remove the empty web_static folder
        run('rm -rf {}/web_static'.format(release_folder))

        # Remove the current symbolic link
        current_link = '/data/web_static/current'
        run('rm -rf {}'.format(current_link))

        # Create a new symbolic link to the deployed version
        run('ln -s {} {}'.format(release_folder, current_link))

        print('New version deployed!')
        return True

    except Exception as e:
        return False

if __name__ == "__main__":
    # Example usage: fab -f 2-do_deploy_web_static.py do_deploy:archive_path=versions/web_static_20170315003959.tgz -i my_ssh_private_key -u ubuntu
    do_deploy("<path-to-your-archive>")
