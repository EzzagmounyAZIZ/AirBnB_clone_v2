# Puppet manifest for setting up web servers for web_static deployment

# Ensure Nginx is installed
package { 'nginx':
  ensure => installed,
}

# Create necessary directories
file { '/data':
  ensure => 'directory',
}

file { '/data/web_static':
  ensure => 'directory',
}

file { '/data/web_static/releases':
  ensure => 'directory',
}

file { '/data/web_static/shared':
  ensure => 'directory',
}

file { '/data/web_static/releases/test':
  ensure => 'directory',
}

# Create a fake HTML file
file { '/data/web_static/releases/test/index.html':
  content => "<html>\n  <head>\n  </head>\n  <body>\n    Holberton School\n  </body>\n</html>",
}

# Create a symbolic link
file { '/data/web_static/current':
  ensure => link,
  target => '/data/web_static/releases/test',
  force  => true,
}

# Set ownership to ubuntu user and group recursively
file { '/data':
  owner   => 'ubuntu',
  group   => 'ubuntu',
  recurse => true,
}

# Configure Nginx to serve content
file { '/etc/nginx/sites-available/default':
  content => "server {\n\tlisten 80 default_server;\n\tserver_name _;\n\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current;\n\t}\n}\n",
  notify  => Service['nginx'],
}

# Restart Nginx service
service { 'nginx':
  ensure => 'running',
  enable => true,
}
