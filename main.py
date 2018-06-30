import pygit2
from pygit2 import Repository, GitError, RemoteCallbacks, UserPass, Username, GIT_CREDTYPE_USERNAME
import os
import getpass

################################################################################
# The repo is https://github.com/EscherCone which is a repo that is on my
# computer but is private on github.
################################################################################
repo_path = os.path.join(os.path.expanduser('~'), 'Documents', 'GitHub', 'EscherCone')
repo_object = Repository(os.path.join(repo_path, '.git'))
origin_object = repo_object.remotes['origin']

################################################################################
# We want to fetch from the remote origin, so we're going to do
#
#       origin_object.fetch()
#
# Since this will require credentials, we're actually going to call the function
# like this:
#
#       origin_object.fetch(callbacks=a_pygit2.RemoteCallbacks)
#
# And the RemoteCallbacks thing is an object that implements four
#
#       certificate_check(certificate, valid, host)
#       credentials(url, username_from_url, allowed_types)
#       push_update_reference(refname, message)
#       sideband_progress(string)
#       transfer_progress(stats)
#       update_tips(refname, old, new)
#
# We reimplement the credentials function whose job it is to take some
# parameters and use those to figure out how to obtain those credentials
# by whatever means.  When it's done, it is expected to return an instance of
# some classes that contain various types of Credentials.  The Username class
# just contains a username.  The UserPass class contains the fields username and
# password.  THere are two others fo doing different types of authentication
################################################################################

# Our object that groups some callbacks that will get called
class MyCreds(pygit2.RemoteCallbacks):
    @staticmethod
    def credentials(url, username_from_url, allowed_types):
        # allowed_types tells us what type of Credential object the server wants
        if allowed_types == pygit2.GIT_CREDTYPE_USERPASS_PLAINTEXT:
            # Our problem: do what you need to do in order to find out what to
            # put into the UserPass object.
            password = getpass.getpass('Enter password for url={}'.format(url))
            return UserPass('philippecarphin', password)
        # Deal with other types of credential requirements
        # elif allowed_types == pygit2.GITCREDTYPE_USERNAME:
        #    raise NotImplemented


# So here's an instance of this thing we just made
my_remote_callback = RemoteCallbacks(credentials=MyCreds.credentials)

################################################################################
# And that's it!
# Doing the fetch and giving it the callback.  It returns a
# pygit2.TransferProgress.  Anyway the point is calling fetch with the callback.
################################################################################
transfer_process_thingy= origin_object.fetch(callbacks=my_remote_callback)
