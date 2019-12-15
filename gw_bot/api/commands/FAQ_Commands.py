def send_screenshot_to_slack(path, channel, extra_params: list):
    if path is None: path = ''
    url = 'https://open-security-summit.org/' + path
    from gw_bot.api.commands.OSS_Bot_Commands import OSS_Bot_Commands
    params = ["screenshot", url]
    params.extend(extra_params)
    OSS_Bot_Commands().browser({'channel': channel}, params)

class FAQ_Commands:

    @staticmethod
    def attendee(*event):
        return send_screenshot_to_slack('faq/attendee-information'     , event[1], [1200])

    @staticmethod
    def accomodation(*event):
        return send_screenshot_to_slack('faq/accomodation'         , event[1], [1200])

    @staticmethod
    def content(*event):
        return send_screenshot_to_slack('faq/content-support', event[1], [1200])

    @staticmethod
    def types(*event):
        return send_screenshot_to_slack('faq/session-types', event[1], [1200])

    @staticmethod
    def help(*event):
        return send_screenshot_to_slack('faq/i-need-help', event[1], [1200])

    @staticmethod
    def join(*event):
        return send_screenshot_to_slack('faq/id-like-to-join-the-summit', event[1], [1200])

    @staticmethod
    def remote(*event):
        return send_screenshot_to_slack('faq/im-a-remote-participant-faq', event[1], [1200])

    @staticmethod
    def onsite(*event):  return send_screenshot_to_slack('faq/im-an-on-site-participant', event[1], [1200])

    @staticmethod
    def organiser(*event):  return send_screenshot_to_slack('faq/im-an-organiser', event[1], [1200])

    @staticmethod
    def infrastructure(*event):  return send_screenshot_to_slack('faq/infrastructure-needs', event[1], [1200])

    @staticmethod
    def slack(*event):
        return send_screenshot_to_slack('faq/reach-us-in-slack', event[1], [1200])

    @staticmethod
    def registering(*event):
        return send_screenshot_to_slack('faq/registration-info/', event[1], [1200])

    @staticmethod
    def remote(*event):
        return send_screenshot_to_slack('faq/remote-participants', event[1], [1200])

    @staticmethod
    def schedule(*event):
        return send_screenshot_to_slack('faq/schedule', event[1], [1200])

    @staticmethod
    def sponsored(*event):
        return send_screenshot_to_slack('faq/sponsored_tickets', event[1], [1200])

    @staticmethod
    def tickets(*event):
        return send_screenshot_to_slack('faq/sponsored_tickets', event[1], [1200])

    @staticmethod
    def directions(*event):
        return send_screenshot_to_slack('faq/transport-and-directions', event[1], [1200])