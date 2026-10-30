import requests

url = 'https://www.musashino-u.ac.jp'

#webサーバにリクエストを出します
#レスポンスを変数(res)に格納する

res = requests.get(url)

print(f"レスポンス: {res}")
print(f"レスポンスの型: {type(res)}")

print(f"リクエスト: {res.request}")
print(f"リクエストヘッダー: {res.request.headers}")
print(f"リクエストのメソッド: {res.request.method}")
print(f"リクエストのURL：{res.request.url}")

print(f"ステータスコード：{res.status_code}")
print(f"ステータスメッセージ：{res.reason}")
print(f"レスポンスヘッダー: {res.header}")