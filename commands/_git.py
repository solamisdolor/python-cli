import os
import subprocess


class _git(object):
    """A Git library"""
    
    def __init__(self, repo_uri, working_dir, user=None, pwd=None):
        self.repo_uri = repo_uri
        self.working_dir = working_dir
        self.repo_dir = self.working_dir + "/repo"
        self.user = user
        self.pwd = pwd


    def clone(self):
        os.chdir(self.working_dir)
        subprocess.call(["git", "clone", self.repo_uri, "repo"], shell=True)
        

    def status(self):
        print (self.repo_dir)
        os.chdir(self.repo_dir)
        cmd = "git status"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        return stdout.decode("utf-8")


    def pull(self):        
        os.chdir(self.repo_dir)
        cmd = "git pull origin"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()        
        return stdout.decode("utf-8")

        
    def checkout(self, branch):
        os.chdir(self.repo_dir)
        cmd = "git checkout {0}".format(branch)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()
        return stdout.decode("utf-8")

    def push(self):
        os.chdir(self.repo_dir)
        cmd = "git push origin"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()        
        if len(stderr) > 0:
            pass
            #TODO: need to filter out the typical git non-error msgs from stderr
        return stdout.decode("utf-8")
    
    def add(self):
        os.chdir(self.repo_dir)
        cmd = "git add ."
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()        
        return stdout.decode("utf-8")

    def commit(self, comment):
        os.chdir(self.repo_dir)
        cmd = "git commit -m {0}".format(comment)
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()        
        return stdout.decode("utf-8")

    def config(self):
        os.chdir(self.repo_dir)
        cmd = "git config --global http.sslVerify false"
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        stdout, stderr = p.communicate()        
        print (stderr)
        return stdout.decode("utf-8")
        