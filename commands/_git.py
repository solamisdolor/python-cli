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
            raise ValueError('Error git exec: {0}. {1}'.format(cmd, stderr.decode("utf-8")))
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

        
    def checkout(self, branch):
        return self.execgit("git checkout {0}".format(branch))


    def push(self):
        return self.execgit("git push origin".format(branch))

    
    def add(self):
        return self.execgit("git add .")


    def commit(self, comment):
        return self.execgit("git commit -m {0}".format(comment))


    def config(self):
        result = self._execgit("git config --global http.sslVerify false")
       
