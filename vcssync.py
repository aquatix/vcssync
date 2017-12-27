import logging
import os
import sys

import click
import git
import yaml


## Create logger
logger = logging.getLogger('vcssync')
logger.setLevel(logging.DEBUG)

# create file handler which logs even debug messages
fh = logging.FileHandler('vcssync.log')
fh.setLevel(logging.DEBUG)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
# add the handlers to the logger
logger.addHandler(fh)

# create stdout logger
ch = logging.StreamHandler(sys.stdout)
ch.setLevel(logging.WARNING)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


try:
    import settings
except ModuleNotFoundError:
    print('Please create a settings.py from settings.example.py with your own configuration')
    sys.exit(-1)


def get_repo_basename(repo_url):
    """
    Extract repository basename from its url, as that will be the name of  directory it will be cloned into1
    """
    result = os.path.basename(repo_url)
    filename, file_extension = os.path.splitext(result)
    if file_extension == '.git':
        # Strip the .git from the name, as Git will do the same on non-bare checkouts
        result = filename
    return result


def update_repo(config):
    """
    Update (pull) the Git repo
    """
    projectname = config[0]
    triggerconfig = config[1]

    repo_url = triggerconfig['repo']
    repo_parent = settings.REPOS_CACHE_DIR
    if 'repoparent' in triggerconfig and triggerconfig['repoparent']:
        repo_parent = triggerconfig['repoparent']

    logger.info('[' + projectname + '] Updating ' + repo_url)
    logger.info('[' + projectname + '] Repo parent ' + repo_parent)

    # Ensure cache dir for webhaak exists and is writable
    fileutil.ensure_dir_exists(repo_parent) # throws OSError if repo_parent is not writable

    # TODO: check whether dir exists with different repository
    repo_dir = os.path.join(repo_parent, get_repo_basename(repo_url))
    logger.info('[' + projectname + '] Repo dir ' + repo_dir)
    if os.path.isdir(repo_dir):
        # Repo already exists locally, do a pull
        logger.info('[' + projectname + '] Repo exists, pull')

        apprepo = git.Repo(repo_dir)
        origin = apprepo.remote('origin')
        result = origin.fetch()                  # assure we actually have data. fetch() returns useful information
        origin.pull()
        logger.info('[' + projectname + '] Done pulling, checkout()')
        #logger.debug(apprepo.git.branch())
        result = apprepo.git.checkout()
    else:
        # Repo needs to be cloned
        logger.info('[' + projectname + '] Repo does not exist yet, clone')
        apprepo = git.Repo.init(repo_dir)
        origin = apprepo.create_remote('origin', repo_url)
        origin.fetch()                  # assure we actually have data. fetch() returns useful information
        # Setup a local tracking branch of a remote branch
        apprepo.create_head('master', origin.refs.master).set_tracking_branch(origin.refs.master)
        # push and pull behaves similarly to `git push|pull`
        result = origin.pull()
        logger.info('[' + projectname + '] Done pulling, checkout()')
        #logger.debug(apprepo.git.branch())
        result = apprepo.git.checkout()
    return result


## Main program
@click.group()
def cli():
    """
    whosthere
    """
    pass


@cli.command()
def pull_everything():
    """
    Pull all configured repositories, with all their branches and tags
    """
    # update_repo()
    pass


if not hasattr(main, '__file__'):
    """
    Running in interactive mode in the Python shell
    """
    print("vcssync running interactively in Python shell")

elif __name__ == '__main__':
    """
    vcssync is ran standalone, rock and roll
    """
    cli()
