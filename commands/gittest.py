from .base import base
from ._git import _git

class git(base):
    """Get property value"""
    
    @staticmethod
    def run():
        repo = _git("d:/ab/test", "d:/ab/testgit")
        #repo.clone()
        print(repo.config())
        # print(repo.status())
        # print(repo.pull())
        # print(repo.add())
        # print(repo.commit("testnew"))
        # print(repo.push())

