def run(event, context):
    return "Hello {0} (from lambda)".format(event.get('name'))