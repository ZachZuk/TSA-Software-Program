from hugchat import hugchat
from hugchat.login import Login

# Log in to huggingface and grant authorization to huggingchat
# DO NOT EXPOSE YOUR EMAIL AND PASSWORD IN CODES, USE ENVIRONMENT VARIABLES OR CONFIG FILES
EMAIL = "ZachZuk"
PASSWD = "Zz-312088!"
cookie_path_dir = "./cookies/" # NOTE: trailing slash (/) is required to avoid errors
sign = Login(EMAIL, PASSWD)
cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

def generate(desc):
    return chatbot.chat("You help people figure out issues with their plants. Your response must be a moderate length, no longer than 400 words. You must provide a description of the issue, treatments, and anything else that you think is important. Do not say anything besides the info, don't say stuff like 'Sure! I can do that for you:' Here is a description of an issue:", web_search=True).wait_until_done()