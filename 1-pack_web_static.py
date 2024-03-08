#!/usr/bin/env python3
"""
Fabric script that generates a .tgz archive from the contents
of the web_static folder of the AirBnB Clone repo.
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """
    Generate a .tgz archive from the contents of the web_static folder.

    Returns:
        (str): Path to the generated archive, None on failure.
    """
    try:
        # Create the versions folder if it doesn't exist
        local("mkdir -p versions")

        # Get the current date and time
        now = datetime.now()
        date_time = now.strftime("%Y%m%d%H%M%S")

        # Create the archive path
        archive_path = "versions/web_static_{}.tgz".format(date_time)

        # Compress the web_static folder
        local("tar -cvzf {} web_static".format(archive_path))

        print("web_static packed: {} -> {}Bytes".format(archive_path, local("wc -c < {}".format(archive_path), capture=True)))

        return archive_path

    except Exception as e:
        return None

if __name__ == "__main__":
    do_pack()
