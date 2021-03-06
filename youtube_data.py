import pandas as pd
from apiclient.discovery import build

api_key = '*************************'
youtube = build('youtube', 'v3', developerKey= api_key)

# partにはidとsnippetを指定
# q=検索クエリ
# order=並び替え方法
# type=検索クエリの制限対象

def get_data(part='snippet',q='python programming',order='viewCount',type='video',num=20):
    data_list = []
    search_response = youtube.search().list(part=part,q=q,order=order,type=type)
    output = youtube.search().list(part=part, q=q, order=order, type=type).execute()

    for i in range(num):
        data_list += output['items']
        search_response = youtube.search().list_next(search_response,output)
        output = search_response.execute()

    dataF = pd.DataFrame(data_list)
    # 各動画毎に一意のvideoIdを取得
    df1 = pd.DataFrame(list(dataF['id']))['videoId']
    # 各動画毎に一意のvideoIdを取得必要な動画情報だけ取得
    df2 = pd.DataFrame(list(dataF['snippet']))[['channelTitle', 'publishedAt', 'title']]
    ddf = pd.concat([df1, df2], axis=1)

    ddf.to_csv('youtube_test.csv')



# print(len(search_response['items']))
# print(search_response['items'])




