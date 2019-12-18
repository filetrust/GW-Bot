def run(event, context):
    return "..CHANGED LOCally..Hello {0} (from lambda)".format(event.get('name'))