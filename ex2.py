import requests

url = 'https://www.musashino-u.ac.jp'

#webサーバにリクエストを出します
#レスポンスを変数(res)に格納する
res = requests.get(url)

#取得したHTMLデータは、res.textに保存されている
print(res.text)

# ここでは取得したHTMLをmusashino-u.htmlファイルに書き込む
with open('musashino-u.html', 'w') as f:
	f.write(res.text)
