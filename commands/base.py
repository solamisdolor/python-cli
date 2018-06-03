"""The base command"""

class base(object):
    """A base command."""
 
    def __init__(self, *args):
        self.args = args       
    
    def run(self, args):
        raise NotImplementedError('run() method not implement yet.')