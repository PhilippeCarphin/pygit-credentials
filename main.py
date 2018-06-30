################################################################################
# This is the simplest code that will allow you to fetch from a repository that
# requires username-password authentication.
################################################################################
import pygit2
import os
import getpass

################################################################################
# The repo is https://github.com/EscherCone which is a repo that is on my
# computer but is private on github.
################################################################################
# it is at this path
repo_path = os.path.join(os.path.expanduser('~'), 'Documents', 'GitHub', 'EscherCone')
# the Repository contructor wants the .git directory
repo_object = pygit2.Repository(os.path.join(repo_path, '.git'))
# Remotes are the objects that allow us to do fetch and push for the remote that
# it is.
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

# Our object that groups some callbacks that will get called.  An instance of
# this will be passed as the 'callbacks' parameter of the fetch method.
class MyCreds(pygit2.RemoteCallbacks):
    # It has to implement some methods, but we're only going to use it in a way
    # where this method will be called.
    def credentials(self, url, username_from_url, allowed_types):
        print(self, url, username_from_url, allowed_types)
        # allowed_types tells us what type of Credential object the server wants
        if allowed_types == pygit2.GIT_CREDTYPE_USERPASS_PLAINTEXT:
            # Our problem: do what you need to do in order to find out what to
            # put into the UserPass object.
            password = getpass.getpass('Enter password for url={}'.format(url))
            return pygit2.UserPass('philippecarphin', password)
        elif allowed_types == pygit2.GITCREDTYPE_USERNAME:
            raise NotImplemented

################################################################################
# And that's it!
# Doing the fetch and giving it the callback.  It returns a
# pygit2.TransferProgress.  Anyway the point is calling fetch with the callback.
################################################################################
transfer_process_thingy = origin_object.fetch(callbacks=MyCreds())
                                            #           ^^^^^^^^^
                                            # pass an instance of MyCreds as
                                            # the paramater callbacks.

# To push, we can do something like this, the function doesn't return anything.
# push_result = origin_object.push(specs=['refs/heads/pushtest'], callbacks=MyCreds())
# print('push_result={}'.format(push_result))
