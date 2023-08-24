# Flask + Authlib OAuth 2.0 範例

這是一個 Python Flask + [Authlib](https://authlib.org/) 的 OAuth 2.0 服務範例。
如果你想了解更多 Flask-OAuthlib 可以查看

- Authlib 文件: <https://docs.authlib.org/en/latest/flask/2/>
- Authlib Repo: <https://github.com/lepture/authlib>


## 快速上手

此專案只適用於教學及範例，請勿用於正式環境。
啟動專案之前，需先安裝相關依賴: 

```bash
$ pip install -r requirements.txt
```

設定 Flask and Authlib 環境變數:

```bash
# disable check https (DO NOT SET THIS IN PRODUCTION)
$ export AUTHLIB_INSECURE_TRANSPORT=1
```

啟動腳本運行並建立資料庫(SQLite)

```bash
$ flask run
```

啟動後，您可以訪問 `http://127.0.0.1:5000/`，並輸入任意使用者名稱。

在開始測試之前，需要先建立一個應用:

![create a client](https://user-images.githubusercontent.com/290496/38811988-081814d4-41c6-11e8-88e1-cb6c25a6f82e.png)


### 使用授權碼流程

您可以在瀏覽器裡開啟下列網址，開始授權碼流程
```bash
$ open http://127.0.0.1:5000/oauth/authorize?response_type=code&client_id=${client_id}&scope=access
```

認證之後，頁面將跳轉至 `${redirect_uri}/?code=${code}`。

接著可以將取得的 code，向伺服器請求授權，並取得最終 access token。
Then your app can send the code to the authorization server to get an access token:

```bash
$ curl -u ${client_id}:${client_secret} -XPOST http://127.0.0.1:5000/oauth/token -F grant_type=authorization_code -F scope=access -F code=${code}
```

現在你可以藉甲 access_token 訪問 `/api/me`:

```bash
$ curl -H "Authorization: Bearer ${access_token}" http://127.0.0.1:5000/api/me
```
