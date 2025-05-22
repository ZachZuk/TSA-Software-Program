from hugchat import hugchat
from hugchat.login import Login
# login info not uploaded to github
from config import EMAIL, PASSWD
import re

# login info
cookie_path_dir = "./cookies/" 

# Function for gettung a formatted responce from huggingchat with sources
def generate(desc):
    # "logging in" to huggingchat with cookies and login info
    sign = Login(EMAIL, PASSWD)
    cookies = sign.login(cookie_dir_path=cookie_path_dir, save_cookies=True)

    # creating the chatbot object
    chatbot = hugchat.ChatBot(cookies=cookies.get_dict())

    # Chat function from a library was modified so we can get sources seperate
    # generating a response from huggingchat, and splitting it into the text and sources using a specialized prompt
    formatted_string, sources = chatbot.chat("You help people figure out issues with their plants. Your response must be a moderate length, no longer than 300 words. You must provide a description of the issue, treatments, and anything else that you think is important. Do not say anything besides the info, don't say stuff like 'Sure! I can do that for you:' Here is a description of an issue: " + desc, web_search=True)
    
    # reformatting the responce for html
    formatted_string = formatted_string.replace('\n', '<br>')
    formatted_string = re.sub(r'\*(.*?)\*', r'<strong>\1</strong>', formatted_string)
    formatted_string = formatted_string.replace('\"', '&quot;').replace('\'' , '&apos;')
    formatted_string = re.sub(r'\[\d+\]', '', formatted_string)
    response = formatted_string

    # adding on the sources
    response += '<br><br><strong>Sources:</strong><br>' + '<br>'.join([f'<a href="{source.link}">{source.title}</a>' for source in sources])
    return response
