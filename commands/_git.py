import os
import stat
import shutil
import subprocess


class _git(object):
    """A Git library"""
    
    def __init__(self, repo_uri, working_dir, user=None, pwd=None):
        self.repo_uri = repo_uri
        self.working_dir = working_dir
        self.repo_folder_name = "repo"
        self.repo_dir = "{0}/{1}".format(self.working_dir, self.repo_folder_name)
        self.user = user
        self.pwd = pwd


    def _execgit(self, cmd):
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise ValueError('Error git exec: {0}. {1}'.format(cmd, stderr.decode("utf-8")))
        return stdout.decode("utf-8")


    def execgit(self, cmd):
        os.chdir(self.repo_dir)        
        return self._execgit(cmd)


    def clone(self):
        cmd = "git clone {0} {1}".format(self.repo_uri, self.repo_folder_name)
        os.chdir(self.working_dir)                
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        if p.returncode != 0:
            raise ValueError('Error git exec: {0}. {1}\n{2}'.format(cmd, stdout.decode("utf-8"), stderr.decode("utf-8")))
        return stdout.decode("utf-8")


    def force_clean(self):
        """indiscriminately remove all contents under repo_dir"""   
        def remove_readonly(func, path, _):
            """Clear the readonly bit and reattempt the removal"""
            os.chmod(path, stat.S_IWRITE)
            func(path)     
        if os.path.exists(self.repo_dir):
            shutil.rmtree(self.repo_dir, onerror=remove_readonly)


    def status(self):        
        return self.execgit("git status")


    def pull(self):        
        return self.execgit("git pull origin")

        
    def checkout(self, branch_name):
        return self.execgit("git checkout {0}".format(branch_name))


    def push(self):
        return self.execgit("git push origin")


    def push_branch(self, branch_name):
        return self.execgit("git push -u origin {0}".format(branch_name))


    def add(self):
        return self.execgit("git add .")


    def commit(self, comment):
        return self.execgit("git commit -m {0}".format(comment))


    def branch(self, branch_name):
        return self.execgit("git checkout -b {0}".format(branch_name))


    def is_branch_exists(self, branch_name):
        cmd = "git rev-parse --verify remotes/origin/{0}".format(branch_name)
        os.chdir(self.repo_dir)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        return p.returncode == 0 # True == exists


    def config(self):
        result = self._execgit("git config --global http.sslVerify false")
       
