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
$ open http://127.0.0.1:5000/oauth/authorize?response_type=code&client_id=${client_id}&scope=profile buy buy_history&state=unique_state_code
```

認證之後，頁面將跳轉至 `${redirect_uri}/?code=${code}&state=unique_state_code`。

接著可以將取得的 code，向伺服器請求授權，並取得最終 access token。

```bash
$ curl -u ${client_id}:${client_secret} -XPOST http://127.0.0.1:5000/oauth/token -F grant_type=authorization_code -F scope=profile buy buy_history -F code=${code}

# 返回值
{
    "access_token": "VfmFVoBsWYIOPNY77f5gcivzVYixM1LHKZzZHLYRaL", 
    "expires_in": 864000, 
    "scope": "profile buy buy_history", 
    "token_type": "Bearer"
}
```

現在你可以藉由 access_token 訪問 `/api/me`:

```bash
$ curl -H "Authorization: Bearer ${access_token}" http://127.0.0.1:5000/api/me
```

## 相關 API

### OAuth 登入

#### [POST] /oauth/authorize

#### 請求參數:

?client_id=my_client_id&response_type=code&scope=profile buy buy_history&state=my_state

#### 返回值:

登入 HTML

### 取得 OAuth Token

#### [POST] /oauth/token

#### 請求參數:

grant_type=authorization_code&scope=profile buy buy_history&code=my_authorize_code

#### 返回值:
```json
{
    "access_token": "VfmFVoBsWYIOPNY77f5gcivzVYixM1LHKZzZHLYRaL", 
    "expires_in": 864000, 
    "scope": "profile buy buy_history", 
    "token_type": "Bearer"
}
```

### 查看個人資料 

#### [GET] /api/me

#### 請求頭:

Authorization: Bearer <my_access_token>

#### 請求參數:

#### 返回值:
```json
{
    "code": 0, 
    "success": true, 
    "username": "my_username", 
    "server_id": "my_server_id",
    "msg": "查詢成功",
    "ts": 1695613372,    
}
```

### 購買品項

#### [POST] /api/items/buy

#### 請求頭:

Authorization: Bearer <my_access_token>

#### 請求參數:

```json
{
    "item_id": "YOUR_ITEM_ID",
    "tx_id": "MY_ORDER_ID",
    "buy_at": "2023-09-01 13:22:22",
}
```

#### 返回值:
```json
{
    "code": 0,
    "success": true,
    "msg": "購買成功",
    "ts": 1695613372
}
```

### 購買記錄

#### [GET] /api/orders

#### 請求頭:

Authorization: Bearer <my_access_token>

#### 請求參數:

#### 返回值:
```json
{
    "code": 0, 
    "success": true, 
    "msg": "查詢成功",
    "ts": 1695613372,
    "orders": [
        {
            "tx_id": "20230901120000123456",
            "item_id": "ITEM_001",
            "item_name": "品項1",
            "item_img_url": "https://img.example.com/img/item_001.png",
            "amount": "100",
            "buy_at": "1692805697"
        },
        {
            "tx_id": "20230901120000233441",
            "item_id": "ITEM_002",
            "item_name": "品項2",
            "item_img_url": "https://img.example.com/img/item_002.png",
            "amount": "100",
            "buy_at": "1692816112"
        }
    ]
}
```