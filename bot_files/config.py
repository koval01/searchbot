import os

DEBUG = True

if DEBUG:
    API_TOKEN = os.environ['DEV_TOKEN']
    bot_root = "."
else:
    from dotenv import load_dotenv
    load_dotenv()
    API_TOKEN = os.environ['DEPLOY_TOKEN']
    bot_root = "./awarebot"

# ADMINS GET
admins = os.environ['ADMINS'].split()

# LOGGING CONFIG
format_logging = u'%s' % os.environ['LOGGING_CONFIG']

# SEARCH API CONFIG
api_host_search = os.environ['SEARCH_API_HOST']
cx = os.environ['CX']
api_key = os.environ['SEARCH_API_KEYS'].split()

# NEWS API CONFIG
news_api_key = os.environ['NEWS_API_KEYS'].split()

# WEATHER API CONFIG
weather_api_key = os.environ['WEATHER_API_KEYS'].split()

# NEWS FIND WORDS
news_check_words = os.environ['NEWS_CHECK_WORDS'].split()

# WEB REQUESTS CONFIG
user_agent_static = os.environ['USER_AGENT']

# QIWI
qiwi_api_key = os.environ['QIWI_KEY']
qiwi_api_key_secret = os.environ['QIWI_KEY_SECRET']

# BONUS SEARCHES
default_limit = 50
cut_price = 3.2 # Чем меньше - тем больше цена

# NEWS API
news_default_background = "%s/news-default-background.png" % bot_root
news_finish_background = "%s/news-finish.png" % bot_root