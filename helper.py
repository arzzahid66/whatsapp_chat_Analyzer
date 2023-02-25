from urlextract import URLExtract
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import pandas as pd  
from collections import Counter
import emoji 
from collections import Counter
import matplotlib.font_manager as fm
import re


extract = URLExtract()

def fetch_stats(selected_user,df):

    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    # fetch the number of messages
    num_messages = df.shape[0]

    # fetch the total number of words
    words = []
    for message in df['message']:
        words.extend(message.split())

    # fetch number of media messages
    num_media_messages = df[df['message'] == '<Media omitted>'].shape[0]

    # fetch number of links shared
    links = []
    for message in df['message']:
        links.extend(extract.find_urls(message))

    return num_messages,len(words),num_media_messages,len(links)

def most_busy_users(df):
    x = df['user'].value_counts().head()
    df=round((df['user'].value_counts() / df.shape[0])*100,2).reset_index().rename(
        columns={'index':'Name','user':'Percent'})
    return x ,df

def create_wordcloud(selected_user,df):
    f=open('stop_words.txt',encoding='utf-8',errors='ignore')
    stop_words=f.read()
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    df['message'] = df['message'].str.replace('Media omitted', '')
    df['message'] = df['message'].str.replace('Omitted media', '')
    df['message'] = df['message'].str.replace('<>', '')
    df['message'] = df['message'].str.replace('<media', '') 
    df['message'] = df['message'].str.replace('omitted>', '') 

    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)


    wc = WordCloud(width=500, height=500, min_font_size=6, background_color='white', max_words=200)
    df_wc=wc.generate(df['message'].str.cat(sep=" "))
    return df_wc


# most common words
def most_common_words(selected_user,df):
    f=open('stop_words.txt',encoding='utf-8',errors='ignore')
    stop_words=f.read()
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    words = []
    for message in df['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df

# # filter common emojis 
# def emoji_helper(selected_user, df):
#     if selected_user != 'overall':
#         df = df[df['user'] == selected_user]

#     emoji_pattern = re.compile("["
#                        u"\U0001F600-\U0001F64F"  # emoticons
#                        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
#                        u"\U0001F680-\U0001F6FF"  # transport & map symbols
#                        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
#                        u"\U00002702-\U000027B0"  # Dingbats
#                        u"\U0001F918-\U0001F939"  # faces
#                        u"\U0001F1F2"  # flag for China
#                        u"\U0001F1F4"  # flag for Italy
#                        u"\U0001F1E6"  # flag for United States
#                        u"\U0001F1F7"  # flag for Russia
#                        u"\U0001F1FA"  # flag for Spain
#                        u"\U0001F1F8"  # flag for Germany
#                        u"\U0001F1EE"  # flag for France
#                        u"\U0001F1EA"  # flag for Japan
#                        u"\U0001F1EB"  # flag for South Korea
#                        u"\U0001F1F0"  # flag for United Kingdom
#                        u"\U0001F1EE\U0001F1F3" # flag for Italy
#                        u"\U0001F1F7\U0001F1FA" # flag for Spain
#                        "]+", flags=re.UNICODE)

#     emojis=[]
#     for message in df['message']:
#         emojis.extend(emoji_pattern.findall(message))
#     emoji_counts = Counter(emojis)
#     emoji_dict = {emoji: int(count) for emoji, count in emoji_counts.items() if not isinstance(emoji, float)}
#     emoji_df = pd.DataFrame(list(emoji_dict.items()), columns=['emoji', 'count'])
#     emoji_df = emoji_df[emoji_df['emoji'].str.contains('[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+')]
#     emoji_df = emoji_df.sort_values(by='count', ascending=False).head(30)

#     return emoji_df

def emoji_helper(selected_user, df):
    if selected_user != 'overall':
        df = df[df['user'] == selected_user]

    emoji_pattern = re.compile("["
                       u"\U0001F600-\U0001F64F"  # emoticons
                       u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                       u"\U0001F680-\U0001F6FF"  # transport & map symbols
                       u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                       u"\U00002702-\U000027B0"  # Dingbats
                       u"\U0001F918-\U0001F939"  # faces
                       u"\U0001F1F2"  # flag for China
                       u"\U0001F1F4"  # flag for Italy
                       u"\U0001F1E6"  # flag for United States
                       u"\U0001F1F7"  # flag for Russia
                       u"\U0001F1FA"  # flag for Spain
                       u"\U0001F1F8"  # flag for Germany
                       u"\U0001F1EE"  # flag for France
                       u"\U0001F1EA"  # flag for Japan
                       u"\U0001F1EB"  # flag for South Korea
                       u"\U0001F1F0"  # flag for United Kingdom
                       u"\U0001F1EE\U0001F1F3" # flag for Italy
                       u"\U0001F1F7\U0001F1FA" # flag for Spain
                       "]+", flags=re.UNICODE)

    emojis=[]
    for message in df['message']:
        emojis.extend(emoji_pattern.findall(message))
    emoji_counts = Counter(emojis)
    emoji_dict = {emoji: int(count) for emoji, count in emoji_counts.items() if not isinstance(emoji, float)}
    emoji_df = pd.DataFrame(list(emoji_dict.items()), columns=['emoji', 'count'])
    emoji_df = emoji_df[~emoji_df['emoji'].str.contains(u'[\U0001F3FB-\U0001F3FF]')]
    emoji_df = emoji_df[emoji_df['emoji'].str.contains('[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF]+')]
    emoji_df = emoji_df.sort_values(by='count', ascending=False).head(50)
    emoji_df = emoji_df.reset_index(drop=True)[['emoji', 'count']]


    return emoji_df

def monthly_timeline(selected_user,df):
    if selected_user != "overall":
        df=df[df['user']==selected_user]
    timeline=df.groupby(['year','month_num','month_name']).count()['message'].reset_index()
    time=[]

    for i in range(timeline.shape[0]):
        time.append(timeline['month_name'][i]+"_"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline


def daily_timeline(selected_user,df):
    if selected_user != "overall":
        df=df[df['user']==selected_user]

    daily_timeline = df.groupby('only_date').count()['message'].reset_index()
    return daily_timeline
    
def week_activity_map(selected_user,df):
    if selected_user != "overall":
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user != "overall":
        df=df[df['user']==selected_user]
    return df['month_name'].value_counts()

def activity_heatmap(selected_user,df):
    if selected_user != "overall":
        df=df[df['user']==selected_user]
    user_heatmap=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return user_heatmap



