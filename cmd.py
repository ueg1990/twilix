import os
import subprocess
import errno

cmds = {
    'pwd' : cmd_pwd,
    'ls'  : cmd_ls,
    'cd'  : cmd_cd,
    'mkdir': cmd_mkdir
}

def cmd_pwd(*args):
    return subprocess.check_output(['pwd'])

def cmd_ls(*args):
    return subprocess.check_output(*args)

def cmd_cd(*args):
    if path[0] == '~':
        path[0] = os.path.expanduser(path[0])
    os.chdir(path[0])
    return run_pwd()

def cmd_mkdir(*args):
    try:
        if path[0][0] == '~':
            path[0] = os.path.expanduser(path[0])
	os.makedirs(path[0])
        return "Director {0} created".format(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
	    raise

if __name__ == '__main__':
    a = cmd_mkdir("~/Test/ing")
    print a
