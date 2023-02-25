import streamlit as st
import preprocesser, helper
import matplotlib.pyplot as plt
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")
uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocesser.preprocess(data)
    df.head()
    # fetch unique users
    user_list = df['user'].unique().tolist()
    user_list.sort()
    user_list.insert(0,"overall")
    selected_user = st.sidebar.selectbox("Show analysis wrt",user_list)

    if st.sidebar.button("Show Analysis"):
        # Stats Area
        num_messages, words, num_media_messages, num_links = helper.fetch_stats(selected_user,df)
        st.title("Top Statistics of Whatsapp chat by A_R_Z")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_messages)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Shared")
            st.title(num_media_messages)
        with col4:
            st.header("Links Shared")
            st.title(num_links)
        # Monthly_timeline 
        st.title("Monthly Timeline")
        timeline=helper.monthly_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(timeline['time'],timeline['message'],color='green')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline 
        st.title("Daily Timeline")
        daily_timeline=helper.daily_timeline(selected_user,df)
        fig,ax=plt.subplots()
        ax.plot(daily_timeline['only_date'],daily_timeline['message'],color='blue')
        plt.xticks(rotation='vertical')
        st.pyplot(fig)
        
        # week activity map
        st.title('Activity Map')

        col1,col2 = st.columns(2)
        with col1:
            st.header('Most Busy Day')
            busy_day=helper.week_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_day.index,busy_day.values)
            plt.xticks(rotation='vertical')

            st.pyplot(fig)
        with col2:
            st.header('Most Busy Month')
            busy_moth=helper.month_activity_map(selected_user,df)
            fig,ax=plt.subplots()
            ax.bar(busy_moth.index,busy_moth.values,color='green')
            plt.xticks(rotation='vertical')

            st.pyplot(fig)
        # activity heat map
            
        st.title("Weekly Activity Map")
        user_heatmap=helper.activity_heatmap(selected_user,df)
        fig,ax=plt.subplots()
        ax= sns.heatmap(user_heatmap)
        st.pyplot(fig)






        

        # finding the most busy user in group 
        st.title('Most Busy User')
        x, new_df = helper.most_busy_users(df)
        fig, ax = plt.subplots()
        ax.barh(x.index, x.values,color='red')
        plt.xticks(rotation='vertical')
        st.dataframe(new_df)
        st.pyplot(fig)

        # wordcloud 
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user,df) 
        fig,ax = plt.subplots()
        ax.imshow(df_wc) 
        st.pyplot(fig)         

        # most common words 
        most_common_df=helper.most_common_words(selected_user,df)
        fig,ax=plt.subplots()
        ax.barh(most_common_df[0],most_common_df[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        # emoji analysis
        emoji_df=helper.emoji_helper(selected_user,df)
        st.title('Emoji Analysis')
        col1,col2 =st.columns(2)
        with col1:
            st.dataframe(emoji_df)
        with col2:
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot()
            ax.pie(emoji_df['count'].head(), labels=emoji_df['emoji'].head(), autopct='%1.1f%%')
            st.pyplot(fig)
