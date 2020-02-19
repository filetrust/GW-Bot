from gw_bot.helpers.Lambda_Helpers import slack_message
from osbot_aws.Dependencies import load_dependency


def run(event, context):
    action    = event.get('action'   )
    field     = event.get('field'    )
    value     = event.get('value'    )
    user      = event.get('user'     )
    commit    = event.get('commit'   )
    channel   = event.get('channel'  )

    if commit is None: commit = True

    if user is None:
        user = 'OSS_Bot'

    if action:
        load_dependency('lambda-git' )
        load_dependency('frontmatter')


        from gw_bot.api_in_lambda.OSS_Hugo   import OSS_Hugo
        try:
            oss_hugo = OSS_Hugo().setup()
            method   = getattr(oss_hugo,action)

            result = method(event) #name, field, value)
            if commit:
                commit_message = 'Lambda change, requested by user: {0} \n' \
                                 ' - action: {1} \n'             \
                                 ' - field: {2}  \n'             \
                                 ' - value: {3}'                 .format(user, action, field, value)
                oss_hugo.git_commit_and_push(commit_message)
                if channel:
                    slack_message("Changes pushed to GitHub", [], channel)
                return {'status': 'ok'}
            else:
                if channel:
                    slack_message("{0}".format(result), [], channel)
            return {'status': 'ok', 'data': result}
        except Exception as error:
            return {'status': 'error', 'data': "{0}".format(error)}
    return {'status': 'error', 'data': 'error occurred when updating data'}