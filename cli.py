import sys
import inspect
import commands


def is_base(module):
    for base in module.__class__.__bases__:
        if base.__name__ == "base":
            return True
    return False


def get_available_commands():
    clist = []
    for c in inspect.getmembers(commands, inspect.isclass):
        m = getattr(commands, c[0])()
        if is_base(m) and m.__class__.__name__ != 'base':
            clist.append(c)
    return clist


def print_available_commands(clist):
    def p(s):
        return "{{{0}}}".format(s)
    print("Available commands:")
    print("===================")    
    for c in clist:
        m = getattr(commands, c[0])()       
        fargs = inspect.getargspec(m.run)
        print("{0} {1}".format(m.__class__.__name__, " ".join(map(p,fargs.args))))
        print("{0: <3}{1}".format(" ", m.__doc__))    


def main():    
    clist = get_available_commands()

    if len(sys.argv) == 1:
        print_available_commands(clist)
        exit(0)

    command = sys.argv[1]
    args = sys.argv[2:]

    for c in clist:
        if command == c[0]:
            module = c[1](args)
            module.run(*args)
            exit(0)

    print('Error: there is no implementation for command: "{0}", or is not declared in commands/__init__.py'.format(command))
    exit(1)


if __name__ == "__main__":
    main()
