# Script based on https://github.com/realpython/flask-deploy/blob/master/fabfile.py

import sys
import os
from fabric.api import cd, env, lcd, put, prompt, local, sudo, run
from fabric.contrib.files import exists

local_app_directory = './twilix'
local_config_directory = './config_twilix'
remote_app_directory = '/home/www'
remote_git_directory = '/home/git/'
remote_twilix_directory = remote_app_directory + '/twilix'
remote_nginx_directory = '/etc/nginx/sites-enabled'
remote_supervisor_directory = '/etc/supervisor/conf.d'

def install_requirements():
    '''
    Install required packages
  
    '''
    sudo('apt-get update')
    sudo('apt-get install -y python')
    sudo('apt-get install -y python-pip')
    sudo('apt-get install -y python-virtualenv')
    sudo('apt-get install -y nginx')
    sudo('apt-get install -y gunicorn')
    sudo('apt-get install -y supervisor')
    sudo('apt-get install -y git')

def install_flask_dependencies():
    """
    1. Create project directories
    2. Create and activate a virtualenv
    3. Copy Flask files to remote host
    """
    if exists(remote_app_directory) is False:
	sudo('mkdir %s' % remote_app_directory)
	#sudo('mkdir' + remote_app_directory)
    if exists(remote_twilix_directory) is False:
	sudo('mkdir %s' % remote_twilix_directory)
	#sudo('mkdir' + remote_twilix_directory)
    with lcd(local_app_directory):
	with cd(remote_app_directory):
	    sudo('virtualenv venv')
            sudo('source venv/bin/activate')
            sudo('pip install Flask==0.10.1')
            sudo('pip install twilio==3.6.15')
	with cd(remote_twilix_directory):
	    put('*', './', use_sudo=True)

def configure_nginx():
    """
    1. Remove default nginx config file
    2. Create new config file
    3. Setup new symbolic link
    4. Copy local config to remote config
    5. Restart nginx
    """
    sudo('/etc/init.d/nginx start')
    if exists('/etc/nginx/sites-enabled/default'):
	sudo('rm /etc/nginx/sites-enabled/default')
    if exists('/etc/nginx/sites-enabled/twilix_nginx.conf' is False):
	sudo('touch /etc/nginx/sites-available/twilix_nginx.conf')
        sudo('ln -s /etc/nginx/sites-available/twilix_nginx.conf /etc/nginx/sites-enabled/twilix_nginix.conf')
    with lcd(local_config_directory):
	with cd(remote_nginx_directory):
	    put('twilix_nginx.conf', '.', use_sudo=True)
    sudo('/etc/init.d/nginx restart')

def configure_supervisor():
    """
    1. Create new supervisor config file
    2. Copy local config to remote config
    3. Register new command
    """
    if exists('/etc/supervisor/conf.d/twilix.conf') is False:
	with lcd(local_config_directory):
	    with cd(remote_supervisor_directory):
		put('twilix_supervisor.conf', './', use_sudo=True)
		sudo('supervisorctl reread')
		sudo('supervisorctl update')

def run_app():
    '''
    Run the app

    '''
    with cd(remote_twilix_directory):
	sudo('supervisorctl start twilix')

def status():
    '''
    Is the app live?

    '''
    sudo('supervisorctl status')

def create():
    install_requirements()
    install_flask_dependencies()
    configure_nginx()
    configure_supervisor()
