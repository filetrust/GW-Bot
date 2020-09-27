import os
import git
from osbot_aws.apis.Secrets import Secrets
from osbot_utils.utils.Files import Files


class Git_Lambda:

    def __init__(self,repo_name):
        self.repo_name      = repo_name
        self.aws_secret     = 'git-{0}'.format(self.repo_name)
        self.git_org        = None
        self.git_repo       = None
        self.path_temp      = '/tmp'
        self.path_repo      = '{0}/{1}'.format(self.path_temp,repo_name)
        self.remote         = 'origin'
        self.branch         = 'master'
        self.author_name    = 'oss-bot-dinis'
        self.author_email   = 'dinis@opensecsummit.org'
        self.commit_message = 'Lambda auto-commit:'
        self.exec_stdout    = None
        self.exec_stderr    = None
        self.set_up_commit_user()


    def git_exec(self, *params,cwd=None):
        if cwd is None:
            cwd = self.path_repo
        stdout, stderr  = git.exec_command(*params,cwd=cwd)
        self.exec_stderr = stderr.decode()
        self.exec_stdout = stdout.decode()
        return self.exec_stdout

    def repo_url(self):
        data = Secrets(self.aws_secret).value_from_json_string()
        return 'https://{0}:{1}@github.com/{2}/{3}.git'.format(data.get('username'),
                                                               data.get('password'),
                                                               data.get('git_org' ),
                                                               self.repo_name)

        # os.environ['GIT_USERNAME'] = data.get('username')      # not working
        # os.environ['GIT_PASSWORD'] = data.get('password')
        #return 'https://github.com/{2}/{3}.git'.format(data.get('username'),data.get('password'),self.git_org, self.git_repo)

    def repo_files(self):
        return Files.files(Files.path_combine(self.path_repo,'**'))

    def set_up_commit_user(self):
        os.environ['GIT_AUTHOR_NAME'    ] = self.author_name
        os.environ['GIT_AUTHOR_EMAIL'   ] = self.author_email
        os.environ['GIT_COMMITTER_NAME' ] = self.author_name
        os.environ['GIT_COMMITTER_EMAIL'] = self.author_email

    def exists(self):
        return Files.exists(self.path_repo)

    # git commands

    def commit(self, message=None):
        if message is None:
            message = "{0}: {1}".format(self.commit_message, self.status())
        self.git_exec('commit', '-a', '-m', message)
        return self

    def clone     (self):
        if self.exists() is False:
            self.git_exec('clone' , self.repo_url()    , cwd=self.path_temp)
        return self

    def diff (self):
        return self.git_exec('diff')

    def log_pretty(self):
        return self.git_exec('log', '--pretty=oneline', '-n10')

    def pull(self):
        self.git_exec('pull', '--no-edit', self.remote, self.branch)
        return self

    def push(self):
        self.git_exec('push', self.remote, self.branch)
        return self

    def status (self):
        return self.git_exec('status')

    def reset_hard (self):
        return self.git_exec('reset','--hard','HEAD')



