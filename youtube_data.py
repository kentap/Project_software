# 検索ワードに関連する動画情報をCSVファイルで出力する

import pandas as pd
from apiclient.discovery import build

api_key = 'xxxxxxxxx' # Enter your API key in here.
api_service_name = 'youtube'
api_version = 'v3'
youtube = build(api_service_name, api_version, developerKey=api_key)


# クエリに応じた動画情報をnums*5個取得する関数
def get_videos_data():
    result_list = []  # itemsを格納する用のリスト
    search_word = input('検索ワードを入力してください:')  # 検索キーワード。ANDは「/」「,」 NOTは「-」 ORは「|」
    nums = int(input('何回繰り返しますか？'))  # nums * 5個の動画情報を取得する

    # partには動画情報を含むsnippetを指定
    # order=並び替え方法
    # type=対象を選択（channel,playlist,videoのいずれか）
    request = youtube.search().list(q=search_word, part='snippet', type='video', order='viewCount')
    get_response = request.execute()  # APIを実行

    # nums * 5個の情報を取得する
    for i in range(nums):
        result_list = result_list + get_response['items']  # itemsをリストに入れ、そのリストと次の実行で得た情報を後ろに追加していく
        request = youtube.search().list_next(request, get_response)  # 1つ前のリクエストとレスポンスを引数に渡すことで次のデータを取得する
        get_response = request.execute()  # API実行

    data = pd.DataFrame(result_list)
    data2 = pd.DataFrame(list(data['id']))['videoId']
    data3 = pd.DataFrame(list(data['snippet']))[['channelTitle', 'publishedAt', 'channelId', 'title']]

    # 関数create_csvへ引き渡しのため
    global final_data
    final_data = pd.concat([data2, data3], axis=1)  # 横方向に連結

    return final_data


get_videos_data()


# 個別の動画ごとの統計情報を取得する関数
def get_statistics(video_id):
    statistics_data = youtube.videos().list(part='statistics', id=video_id).execute()['items'][0][
        'statistics']  # videos().listメソッドで'statistics'のところだけ取得
    return statistics_data

# ラムダ関数で一意のvideo_idをget_statistics関数の引数として入れ、applyで全てのvideo_idにget_statistics関数を実行
# video_idとstatistics_dataのデータフレームを作成(カラムは[['viewCount', 'likeCount', 'dislikeCount', 'commentCount']])
df_static_data = pd.DataFrame(list(final_data['videoId'].apply(lambda x: get_statistics(x))))[
    ['viewCount', 'likeCount', 'dislikeCount', 'commentCount']]
df_output = pd.concat([final_data, df_static_data], axis=1)  # 横方向に結合


# DataFrameをcsvファイルへ出力する関数
def create_csv():
    file_path = input('csvファイルのパスを入力してください。:')
    df_output.to_csv(file_path, sep=',', index=False, encoding='utf-8')
    print('出力しました。')

create_csv()
