# 検索ワードに関連する動画情報をCSVファイルで出力する


import pandas as pd
from apiclient.discovery import build
import csv

api_key = 'AIzaSyB8y97s9ppxsMhDwPdRI_TZzSBp262D-oU'
api_service_name = 'youtube'
api_version = 'v3'
youtube = build(api_service_name, api_version, developerKey=api_key)


def get_videos_data():
    # itemsを格納する用のリスト
    result_list = []
    # 検索キーワード。ANDは「/」「,」 NOTは「-」 ORは「|」
    search_word = input('検索ワードを入力してください:')
    # nums * 5個の動画情報を取得する
    nums = int(input('何回繰り返しますか？'))

    # partには動画情報を含むsnippetを指定
    # order=並び替え方法
    # type=対象を選択（channel,playlist,videoのいずれか）
    response = youtube.search().list(q=search_word, part='snippet', type='video', order='viewCount')
    # APIを実行
    get_response = response.execute()

    # nums * 5個の情報を取得する
    for i in range(nums):
        result_list = result_list + get_response['items'] 　　　　　　　 # itemsをリストに入れ、そのリストと次の実行で得た情報を後ろに追加していく
        response = youtube.search().list_next(response, get_response)   # 1つ前のリクエストとレスポンスを引数に渡すことで次のデータを取得する
        get_response = response.execute()  # API実行

    data = pd.DataFrame(result_list)
    data2 = pd.DataFrame(list(data['id']))['videoId']
    data3 = pd.DataFrame(list(data['snippet']))[['channelTitle', 'publishedAt', 'channelId', 'title']]

    # 関数create_csvへ引き渡しのため
    global final_data
    final_data = pd.concat([data2, data3], axis=1)  # 横方向に連結

    return final_data

get_videos_data()


# csvファイルへの出力
def create_csv():
    file_path = input('csvファイルのパスを入力してください。:')
    final_data.to_csv(file_path, sep=',', index=False, encoding='utf-8')

create_csv()
