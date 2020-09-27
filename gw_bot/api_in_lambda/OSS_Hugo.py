import json
from gw_bot.api_in_lambda.Git_Lambda import Git_Lambda

class OSS_Hugo:
    def __init__(self):
        self.repo_path  = '/tmp/oss2019'
        self.git_lambda = Git_Lambda('oss2019')

    def setup(self):
        self.git_lambda.clone()                     # clone (if needed)
        return self

    def git_status(self, _):
        return "{0}".format(self.git_lambda.status())

    def git_diff(self, _):
        return "{0}".format(self.git_lambda.diff())

    def git_commit_and_push(self,commit_message):
        self.git_lambda.pull()
        self.git_lambda.commit(commit_message)
        self.git_lambda.push()
        return self

    def git_reset(self, _):
        return "{0}".format(self.git_lambda.reset_hard())

    def git_pull(self, _):
        return "{0}".format(self.git_lambda.pull())

    def participant_get(self, user_name):
        import sys
        sys.path.append('/tmp/oss2019/notebooks/api');
        from oss_hugo.OSS_Participant import OSS_Participant # shows error on PyCharm

        return  OSS_Participant(name=user_name, folder_oss=self.repo_path)

    def participant_info(self, event):
        self.git_lambda.pull()
        name = event.get('name')
        participant = self.participant_get(name)
        if participant.exists():
            return "```{0}```".format(json.dumps(participant.metadata(),indent=2))
        return 'error: user not found'


    def participant_url(self,event):
        name = event.get('name')
        participant = self.participant_get(name)
        return participant.path_md_file.split('content/')[1].replace('.md', '')

    def participant_edit_field(self, event):
        name  = event.get('name')
        field = event.get('field')
        value = event.get('value')
        participant = self.participant_get(name)
        if participant.exists():
            participant.field(field, value)
            participant.save()
            return True
        return False

    def participant_append_to_field(self, event):
        name  = event.get('name')
        field = event.get('field')
        value = event.get('value')
        participant = self.participant_get(name)
        if participant.exists():
            current_value = participant.field(field)
            if current_value is not None:
                if type(current_value) is list:
                    new_value = current_value.append(value)
                    participant.field(field, new_value)
                else:
                    participant.field(field,current_value + value)
            else:
                participant.field(field, value)
            participant.save()
            return True
        return False

    def participant_remove_from_field(self, event):
        name  = event.get('name')
        field = event.get('field')
        value = event.get('value')
        participant = self.participant_get(name)
        if participant.exists():
            current_value = participant.field(field)
            if current_value:
                if type(current_value) is list:
                    if value in current_value:
                        current_value.remove(value)
                        participant.field(field,current_value)
                    else:
                        return False
                else:
                    new_value = current_value.replace(value, '')
                    participant.field(field,new_value)
            else:
                participant.field(field, value)
            participant.save()
            return True
        return False