import os

DEBUG = True

if DEBUG:
    API_TOKEN = os.environ['DEV_TOKEN']
    bot_root = "."
else:
    API_TOKEN = os.environ['DEPLOY_TOKEN']
    bot_root = "./awarebot"

admins = os.environ['ADMINS'].split()
format_logging = u'%s' % os.environ['LOGGING_CONFIG']
api_host_search = os.environ['SEARCH_API_HOST']
cx = os.environ['CX']
api_key = os.environ['SEARCH_API_KEYS'].split()
news_api_key = os.environ['NEWS_API_KEYS'].split()
weather_api_key = os.environ['WEATHER_API_KEYS'].split()
news_check_words = os.environ['NEWS_CHECK_WORDS'].split()
user_agent_static = os.environ['USER_AGENT']
news_default_background = "%s/news-default-background.png" % bot_root
news_finish_background = "%s/news-finish.png" % bot_root