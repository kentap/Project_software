from apiclient.discovery import build
import pandas
import json


api_key = 'AIzaSyBbIEbIQr3ObkLMFh7JLg0Zo21TcdnmHzs'

youtube = build('youtube', 'v3', developerKey=api_key)

search_result = youtube.search().list(
part='snippet',
#検索したい文字列を指定
q='Python programming',
#視聴回数が多い順に取得
order='viewCount',
type='video',
).execute()

print(len(search_result['items']))
# print(type(search_result['items'][0])) ///辞書型

# with open("youtube.json",mode='wt',encoding='utf-8') as file:
#     json.dump(search_result['items'][0],file)






