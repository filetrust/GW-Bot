from pbx_gs_python_utils.utils.Misc import Misc


def send_screenshot_to_slack(path, channel, extra_params: list):
    if path is None: path = ''
    url = 'https://open-security-summit.org/' + path
    from gw_bot.api.commands.OSS_Bot_Commands import OSS_Bot_Commands
    params = ["screenshot", url]
    params.extend(extra_params)
    OSS_Bot_Commands().browser({'channel': channel}, params)

class Site_Commands:

    @staticmethod
    def faq         (*event):  return send_screenshot_to_slack('faq'         , event[1], event[2])

    @staticmethod
    def home_page   (*event):  return send_screenshot_to_slack(''            , event[1], [1200]  )

    @staticmethod
    def page_404    (*event):  return send_screenshot_to_slack('404'         , event[1], event[2])

    @staticmethod
    def schedule    (*event):  return send_screenshot_to_slack('schedule'    , event[1], event[2])

    @staticmethod
    def participants(*event):  return send_screenshot_to_slack('participant' , event[1], [1500]  )

    @staticmethod
    def tracks      (*event):  return send_screenshot_to_slack('tracks'      , event[1], [1200]  )

    @staticmethod
    def venue_map   (*event):  return send_screenshot_to_slack('img/venue-map.jpg'      , event[1], event[2]  )


    @staticmethod
    def page(*event):
        path = Misc.array_pop(event[2],0)
        return send_screenshot_to_slack(path, event[1], event[2])
