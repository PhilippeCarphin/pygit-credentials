import pygit2
from pygit2 import Repository, GitError, RemoteCallbacks, UserPass, Username, GIT_CREDTYPE_USERNAME
import os
import getpass


repo = Repository(os.path.join(os.path.expanduser('~'), '.philconfig', '.git'))
repo.remotes['origin'].fetch()

repo.remotes['origin']
repos = {}
github = os.path.expanduser('~/Documents/GitHub')
for repo in os.listdir(github):
    abspath = os.path.join(github, repo)
    git_dir = os.path.join(abspath, '.git')
    if repo.startswith('.') or not os.path.isdir(abspath):
        continue
    if repo == 'glibc':
        continue
    try:
        repos[repo] = Repository(git_dir)
    except:
        print('could not make repo from non-hidden directory {}'.format(repo))
password = getpass.getpass('Enter password for philippecarphin@github.com')
CREDENTIALS = pygit2.credentials.UserPass('PhilippeCarphin', password)
class MyCreds(pygit2.RemoteCallbacks):
    def credentials(self, url, username_from_url, allowed_types):
        print("My credentials")
        print("url=" + url)
        return CREDENTIALS
rtp = None
for n, r in repos.items():
    try:
        o = r.remotes['origin']
    except KeyError:
        continue

    try:
        cb = RemoteCallbacks(credentials=UserPass('PhilippeCarphin', password))
        rtp = o.fetch(callbacks=cb)
        print(rtp)
    except GitError as e:
        print('Exception while fetching repo {} :: {}'.format(n, e))
        break

    print('successful fetch for repo ' + n)


flasktest = repos['flask_test']
dir(rtp)