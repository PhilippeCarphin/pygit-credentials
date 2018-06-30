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


# It's going to ask for the password a bunch of times and we don't need that.
# If we want, we can reimplement a method of the RemoteCallbacks class without
# Creating a derived object, we can use the constructor of RemoteCallbacks like so:
password = getpass.getpass("Please enter password")
easy_creds = pygit2.RemoteCallbacks(
    credentials=lambda a, b, c: pygit2.UserPass('PhilippeCarphin', password)
)

# To push, we can do something like this, the function doesn't return anything.
push_result = origin_object.push(specs=['refs/heads/pushtest'], callbacks=easy_creds)
print('push_result={}'.format(push_result))
# We don't want to have to write this string out ourselves, so we're going to
# work out how to obtain these strings.


###############################################################################
# Each repository object has an attribute called branches which is iterable.
# The iterator yields branch names, and with the keys, we get branch objects.
###############################################################################
branches_object = repo_object.branches
the_branches = list(branches_object)
print(the_branches)

# The branches are actually split up into two sub-branches object.  All these
# are objects of type pygit2.Branches with the same methods
local_branches_object = branches_object.local
remote_branches_object = branches_object.remote
print(list(local_branches_object))
print(list(remote_branches_object))

# We can get a branch using a branch_name as a key.
a_branch_object = branches_object['master']
# And so we find out that it's not so much a list but more like a dictionary.
# But not in an obvious way.  It has an iterator that yields branch names, and it has
# a __getitem__, so we can get a dictionary if we want to look at it in the debugger
branches_dict = {name: branches_object[name] for name in branches_object}

# Anyway, a branch object has a bunch of attributes, properties, and methods.  Namely, it
# has a name which is a refspec string (not the pygit2.Refspec class) and a branch_name
# which is what gets yielded by the iterator and is what we use as keys to get
# the branches.
print('branch.name=' + a_branch_object.name)
print('branch.branch_name=' + a_branch_object.branch_name)

# So this is a way we could push all the branches to origin:
origin_object.push(
    specs=[local_branches_object[branch_name].name for branch_name in local_branches_object],
    callbacks=easy_creds
)

# Or like this if, for example, we want to ask the user at each branch if the
# want to push it.
for branch_name in local_branches_object:
    print('pushing branch=' + branch_name)
    branch_object = local_branches_object[branch_name]
    origin_object.push([branch_object.name], callbacks=easy_creds)

# But we can minimize server interactions if we do this:
push_specs = []
for branch_name in local_branches_object:
    # Ask user if they want to push the branch
    if True:
        push_specs.append(local_branches_object[branch_name].name)
print('pushing {}'.format(push_specs))
origin_object.push(specs=push_specs, callbacks=easy_creds)

# So far we have TODO complete this
