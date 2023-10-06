import time, json
from flask import Blueprint, request, session, url_for
from flask import render_template, redirect, jsonify
from werkzeug.security import gen_salt
from authlib.integrations.flask_oauth2 import current_token
from authlib.oauth2 import OAuth2Error
from .models import db, User, OAuth2Client
from .oauth2 import authorization, require_oauth

bp = Blueprint('home', __name__)

def current_user():
    if 'id' in session:
        uid = session['id']
        return User.query.get(uid)
    return None


def split_by_crlf(s):
    return [v for v in s.splitlines() if v]


@bp.route('/', methods=('GET', 'POST'))
def home():
    if request.method == 'POST':
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        session['id'] = user.id
        # if user is not just to log in, but need to head back to the auth page, then go for it
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect('/')
    user = current_user()
    if user:
        clients = OAuth2Client.query.filter_by(user_id=user.id).all()
    else:
        clients = []

    return render_template('home.html', user=user, clients=clients)


@bp.route('/logout')
def logout():
    del session['id']
    return redirect('/')


@bp.route('/create_client', methods=('GET', 'POST'))
def create_client():
    user = current_user()
    if not user:
        return redirect('/')
    if request.method == 'GET':
        return render_template('create_client.html')

    client_id = gen_salt(24)
    client_id_issued_at = int(time.time())
    client = OAuth2Client(
        client_id=client_id,
        client_id_issued_at=client_id_issued_at,
        user_id=user.id,
    )

    form = request.form
    client_metadata = {
        "client_name": form["client_name"],
        "client_uri": form["client_uri"],
        "grant_types": split_by_crlf(form["grant_type"]),
        "redirect_uris": split_by_crlf(form["redirect_uri"]),
        "response_types": split_by_crlf(form["response_type"]),
        "scope": form["scope"],
        "token_endpoint_auth_method": form["token_endpoint_auth_method"]
    }
    client.set_client_metadata(client_metadata)

    if form['token_endpoint_auth_method'] == 'none':
        client.client_secret = ''
    else:
        client.client_secret = gen_salt(48)

    db.session.add(client)
    db.session.commit()
    return redirect('/')


@bp.route('/oauth/authorize', methods=['GET', 'POST'])
def authorize():
    user = current_user()
    # if user log status is not true (Auth server), then to log it in
    if not user:
        return redirect(url_for('home.home', next=request.url))
    if request.method == 'GET':
        try:
            grant = authorization.get_consent_grant(end_user=user)
        except OAuth2Error as error:
            return error.error
        return render_template('authorize.html', user=user, grant=grant)
    if not user and 'username' in request.form:
        username = request.form.get('username')
        user = User.query.filter_by(username=username).first()
    if request.form['confirm']:
        grant_user = user
    else:
        grant_user = None
    return authorization.create_authorization_response(grant_user=grant_user)


@bp.route('/oauth/token', methods=['POST'])
def issue_token():
    return authorization.create_token_response()


@bp.route('/oauth/revoke', methods=['POST'])
def revoke_token():
    return authorization.create_endpoint_response('revocation')


@bp.route('/api/me', methods=['GET'])
@require_oauth('profile')
def me():
    
    # 查詢登入者資料
    # success = true 表示查詢成功

    return jsonify(code=0, success=True,  msg='查詢成功', username='my_username', name='my_name', server_id='my_server_id')

@bp.route('/api/items/buy', methods=['POST'])
@require_oauth('buy')
def buy():
    item_id = request.form.get('item_id')
    tx_id = request.form.get('tx_id')
    buy_at = time.time

    # 購買品項羅輯
    # success = true 表示購買成功

    return jsonify(code=0, success=True, msg='購買成功', data=None, ts=int(time.time()))

@bp.route('/api/orders', methods=['GET'])
@require_oauth('buy_history')
def history():
    start_at = request.form.get('start_at')
    end_at = request.form.get('end_at')

    # 查詢品項羅輯
    # success = true 表示查詢成功

    data = [
        {
            'tx_id': '20230901120000123456',
            'item_id': 'ITEM_001',
            'item_name': '品項1',
            'item_img_url': 'https://img.example.com/img/item_001.png',
            'amount': '100',
            'buy_at': '1692805697'
        },
        {
            'tx_id': '20230901120000233441',
            'item_id': 'ITEM_002',
            'item_name': '品項2',
            'item_img_url': 'https://img.example.com/img/item_002.png',
            'amount': '100',
            'buy_at': '1692816112'
        }
    ]
    return jsonify(code=0, success=True, msg='查詢成功', data=json.dumps(data), ts=int(time.time()))