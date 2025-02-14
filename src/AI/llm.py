from hugchat import hugchat
from hugchat.login import Login
import re

# Log in to huggingface and grant authorization to huggingchat
# DO NOT EXPOSE YOUR EMAIL AND PASSWORD IN CODES, USE ENVIRONMENT VARIABLES OR CONFIG FILES
EMAIL = "ZachZukosky"
PASSWD = "Zz-312088!"
cookie_path_dir = "./cookies/" # NOTE: trailing slash (/) is required to avoid errors

def generate(desc):
    sign = Login(EMAIL, PASSWD)
    cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())
    formatted_string, sources = chatbot.chat("You help people figure out issues with their plants. Your response must be a moderate length, no longer than 300 words. You must provide a description of the issue, treatments, and anything else that you think is important. Do not say anything besides the info, don't say stuff like 'Sure! I can do that for you:' Here is a description of an issue: " + desc, web_search=True)
    formatted_string = formatted_string.replace('\n', '<br>')
    formatted_string = re.sub(r'\*(.*?)\*', r'<strong>\1</strong>', formatted_string)
    formatted_string = formatted_string.replace('\"', '&quot;').replace('\'' , '&apos;')
    formatted_string = re.sub(r'\[\d+\]', '', formatted_string)
    response = formatted_string
    response += '<br><br><strong>Sources:</strong><br>' + '<br>'.join([f'<a href="{source.link}">{source.title}</a>' for source in sources])
    return response

print(generate("my apple plant's leaves are getting black spots"))