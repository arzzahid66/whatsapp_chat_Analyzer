import re
import pandas as pd

def preprocess(data):
    lines = data.strip().split('\n')

    dates = []
    messages = []

    pattern = r"(\d{1,2}/\d{1,2}/\d{2}), (\d{1,2}:\d{1,2})\s(AM|PM) - ([^:]+):\s(.+)"
    for line in lines:
        match = re.match(pattern, line)
        if match:
            dates.append(match.group(1) + ', ' + match.group(2) + ' ' + match.group(3))
            messages.append(match.group(4) + ': ' + match.group(5))

    df = pd.DataFrame({'user_message': messages, 'message_date': dates})
    df['message_date'] = pd.to_datetime(df['message_date'], format='%m/%d/%y, %I:%M %p')
    df.rename(columns={'message_date': 'date'}, inplace=True)
    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])
    df['only_date']=df['date'].dt.date
    df['user'] = users
    df['message'] = messages
    df=df.drop("user_message",axis=1)
    df['date'] = pd.to_datetime(df['date'])
    df["year"]=df["date"].dt.year
    df['month_num']=df['date'].dt.month
    df["month_name"]=df["date"].dt.month_name()
    df["day"]=df["date"].dt.day
    df['day_name']=df['date'].dt.day_name()
    df["hour"]=df["date"].dt.hour
    df["minute"]=df["date"].dt.minute
    df['message'] = df['message'].str.replace('Media Omitted', '').str.replace('Omitted Media', '')

    period=[]
    for hour in df[["day_name",'hour']]['hour']:
        if hour==23:
            period.append(str(hour) + "_" + str('00'))
        elif hour ==0:
            period.append(str('00') + "_" + str(hour+1))
        else:
            period.append(str(hour) + "_" + str(hour+1))
    df['period']=period

    
    

    
    return df
