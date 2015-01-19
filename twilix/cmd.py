import os
import subprocess
import errno

def cmd_pwd(*args):
    return subprocess.check_output(['pwd'])

def cmd_ls(*args):
    return subprocess.check_output(*args)

def cmd_cd(*args):
    if args[0][1] == '~':
        args[0][1] = os.path.expanduser(args[0][1])
    os.chdir(args[0][1])
    return cmd_pwd()

def cmd_mkdir(*args):
    try:
        if args[0][1][0] == '~':
            args[0][1] = os.path.expanduser(args[0][1])
	os.makedirs(args[0][1])
        return "Director {0} created".format(args[0][1])
    except OSError as exception:
        if exception.errno != errno.EEXIST:
	    raise

def cmd_pipe(*args):
    p1 = subprocess.Popen(args[0][0], stdout=subprocess.PIPE)
    p2 = subprocess.Popen(args[0][1], stdin=p1.stdout, stdout=subprocess.PIPE)
    output = p2.communicate()[0]
    return output
 
cmds = {
    'pwd' : cmd_pwd,
    'ls'  : cmd_ls,
    'cd'  : cmd_cd,
    'mkdir': cmd_mkdir,
    'pipe': cmd_pipe
}

if __name__ == '__main__':
    a = cmd_mkdir("~/ue/mhacks")
    print a
