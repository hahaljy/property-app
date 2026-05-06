from flask import Flask, request, jsonify, g
from flask_cors import CORS
import sqlite3
import hashlib
import jwt
import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
CORS(app)

DATABASE = 'property.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def generate_token(user_id, role):
    payload = {
        'user_id': user_id,
        'role': role,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')
    role = data.get('role')
    address = data.get('address', '')
    department = data.get('department', '')

    if not username or not password or not role:
        return jsonify({'error': '缺少必要参数'}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT id FROM users WHERE username = ?', (username,))
    if cursor.fetchone():
        return jsonify({'error': '用户名已存在'}), 400

    hashed_password = hash_password(password)
    cursor.execute(
        'INSERT INTO users (username, password, phone, role, address, department) VALUES (?, ?, ?, ?, ?, ?)',
        (username, hashed_password, phone, role, address, department)
    )
    db.commit()

    return jsonify({'message': '注册成功'}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({'error': '缺少必要参数'}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    user = cursor.fetchone()

    if not user or user['password'] != hash_password(password):
        return jsonify({'error': '用户名或密码错误'}), 401

    token = generate_token(user['id'], user['role'])
    
    return jsonify({
        'token': token,
        'user': {
            'id': user['id'],
            'username': user['username'],
            'phone': user['phone'],
            'role': user['role'],
            'address': user['address'],
            'department': user['department'],
            'avatar': user['avatar']
        }
    }), 200

@app.route('/api/user/profile', methods=['GET'])
def get_profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload:
        return jsonify({'error': 'token无效'}), 401

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM users WHERE id = ?', (payload['user_id'],))
    user = cursor.fetchone()

    if not user:
        return jsonify({'error': '用户不存在'}), 404

    return jsonify({
        'id': user['id'],
        'username': user['username'],
        'phone': user['phone'],
        'role': user['role'],
        'address': user['address'],
        'department': user['department'],
        'avatar': user['avatar']
    }), 200

@app.route('/api/user/profile', methods=['PUT'])
def update_profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload:
        return jsonify({'error': 'token无效'}), 401

    data = request.get_json()
    phone = data.get('phone')
    address = data.get('address')
    department = data.get('department')
    avatar = data.get('avatar')

    db = get_db()
    cursor = db.cursor()

    update_fields = []
    update_values = []

    if phone:
        update_fields.append('phone = ?')
        update_values.append(phone)
    if address:
        update_fields.append('address = ?')
        update_values.append(address)
    if department:
        update_fields.append('department = ?')
        update_values.append(department)
    if avatar:
        update_fields.append('avatar = ?')
        update_values.append(avatar)

    if not update_fields:
        return jsonify({'error': '没有更新字段'}), 400

    update_values.append(payload['user_id'])
    cursor.execute('UPDATE users SET ' + ', '.join(update_fields) + ' WHERE id = ?', update_values)
    db.commit()

    return jsonify({'message': '更新成功'}), 200

@app.route('/api/user/password', methods=['PUT'])
def update_password():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload:
        return jsonify({'error': 'token无效'}), 401

    data = request.get_json()
    old_password = data.get('old_password')
    new_password = data.get('new_password')

    if not old_password or not new_password:
        return jsonify({'error': '缺少必要参数'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT password FROM users WHERE id = ?', (payload['user_id'],))
    user = cursor.fetchone()

    if not user or user['password'] != hash_password(old_password):
        return jsonify({'error': '原密码错误'}), 401

    cursor.execute('UPDATE users SET password = ? WHERE id = ?', (hash_password(new_password), payload['user_id']))
    db.commit()

    return jsonify({'message': '密码修改成功'}), 200

@app.route('/api/repairs', methods=['POST'])
def create_repair():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload or payload['role'] != 'owner':
        return jsonify({'error': '权限不足'}), 403

    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')

    if not title:
        return jsonify({'error': '缺少必要参数'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO repairs (user_id, title, description) VALUES (?, ?, ?)',
        (payload['user_id'], title, description)
    )
    db.commit()

    return jsonify({'message': '报修提交成功', 'id': cursor.lastrowid}), 201

@app.route('/api/repairs', methods=['GET'])
def get_repairs():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload:
        return jsonify({'error': 'token无效'}), 401

    db = get_db()
    cursor = db.cursor()

    if payload['role'] == 'owner':
        cursor.execute('SELECT * FROM repairs WHERE user_id = ? ORDER BY create_time DESC', (payload['user_id'],))
    else:
        cursor.execute('SELECT * FROM repairs ORDER BY create_time DESC')

    repairs = []
    for row in cursor.fetchall():
        repairs.append({
            'id': row['id'],
            'user_id': row['user_id'],
            'title': row['title'],
            'description': row['description'],
            'status': row['status'],
            'create_time': row['create_time'],
            'update_time': row['update_time']
        })

    return jsonify(repairs), 200

@app.route('/api/repairs/<int:repair_id>', methods=['PUT'])
def update_repair(repair_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload or payload['role'] != 'staff':
        return jsonify({'error': '权限不足'}), 403

    data = request.get_json()
    status = data.get('status')

    if not status or status not in ['pending', 'processing', 'completed']:
        return jsonify({'error': '无效状态'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE repairs SET status = ?, update_time = CURRENT_TIMESTAMP WHERE id = ?', (status, repair_id))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({'error': '报修记录不存在'}), 404

    return jsonify({'message': '状态更新成功'}), 200

@app.route('/api/feedbacks', methods=['POST'])
def create_feedback():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload or payload['role'] != 'owner':
        return jsonify({'error': '权限不足'}), 403

    data = request.get_json()
    content = data.get('content')

    if not content:
        return jsonify({'error': '缺少必要参数'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO feedbacks (user_id, content) VALUES (?, ?)', (payload['user_id'], content))
    db.commit()

    return jsonify({'message': '反馈提交成功', 'id': cursor.lastrowid}), 201

@app.route('/api/feedbacks', methods=['GET'])
def get_feedbacks():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload:
        return jsonify({'error': 'token无效'}), 401

    db = get_db()
    cursor = db.cursor()

    if payload['role'] == 'owner':
        cursor.execute('SELECT * FROM feedbacks WHERE user_id = ? ORDER BY create_time DESC', (payload['user_id'],))
    else:
        cursor.execute('SELECT * FROM feedbacks ORDER BY create_time DESC')

    feedbacks = []
    for row in cursor.fetchall():
        feedbacks.append({
            'id': row['id'],
            'user_id': row['user_id'],
            'content': row['content'],
            'status': row['status'],
            'reply': row['reply'],
            'create_time': row['create_time']
        })

    return jsonify(feedbacks), 200

@app.route('/api/feedbacks/<int:feedback_id>', methods=['PUT'])
def reply_feedback(feedback_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload or payload['role'] != 'staff':
        return jsonify({'error': '权限不足'}), 403

    data = request.get_json()
    reply = data.get('reply')
    status = data.get('status', 'replied')

    if not reply:
        return jsonify({'error': '缺少回复内容'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE feedbacks SET reply = ?, status = ? WHERE id = ?', (reply, status, feedback_id))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({'error': '反馈不存在'}), 404

    return jsonify({'message': '回复成功'}), 200

@app.route('/api/evaluations', methods=['POST'])
def create_evaluation():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload or payload['role'] != 'owner':
        return jsonify({'error': '权限不足'}), 403

    data = request.get_json()
    repair_id = data.get('repair_id')
    rating = data.get('rating')
    comment = data.get('comment', '')

    if not repair_id or not rating:
        return jsonify({'error': '缺少必要参数'}), 400

    if rating < 1 or rating > 5:
        return jsonify({'error': '评分必须在1-5之间'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM repairs WHERE id = ? AND user_id = ?', (repair_id, payload['user_id']))
    repair = cursor.fetchone()

    if not repair:
        return jsonify({'error': '报修记录不存在或不属于当前用户'}), 404

    cursor.execute('INSERT INTO evaluations (user_id, repair_id, rating, comment) VALUES (?, ?, ?, ?)',
                  (payload['user_id'], repair_id, rating, comment))
    db.commit()

    return jsonify({'message': '评价成功'}), 201

@app.route('/api/lost_items', methods=['POST'])
def create_lost_item():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload:
        return jsonify({'error': 'token无效'}), 401

    data = request.get_json()
    title = data.get('title')
    description = data.get('description', '')
    location = data.get('location', '')
    contact_phone = data.get('contact_phone', '')

    if not title:
        return jsonify({'error': '缺少必要参数'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        'INSERT INTO lost_items (title, description, location, contact_phone) VALUES (?, ?, ?, ?)',
        (title, description, location, contact_phone)
    )
    db.commit()

    return jsonify({'message': '发布成功', 'id': cursor.lastrowid}), 201

@app.route('/api/lost_items', methods=['GET'])
def get_lost_items():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload:
        return jsonify({'error': 'token无效'}), 401

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM lost_items ORDER BY create_time DESC')

    items = []
    for row in cursor.fetchall():
        items.append({
            'id': row['id'],
            'title': row['title'],
            'description': row['description'],
            'location': row['location'],
            'contact_phone': row['contact_phone'],
            'status': row['status'],
            'create_time': row['create_time']
        })

    return jsonify(items), 200

@app.route('/api/lost_items/<int:item_id>', methods=['PUT'])
def update_lost_item(item_id):
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload or payload['role'] != 'staff':
        return jsonify({'error': '权限不足'}), 403

    data = request.get_json()
    status = data.get('status')

    if not status or status not in ['lost', 'found']:
        return jsonify({'error': '无效状态'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE lost_items SET status = ? WHERE id = ?', (status, item_id))
    db.commit()

    if cursor.rowcount == 0:
        return jsonify({'error': '记录不存在'}), 404

    return jsonify({'message': '状态更新成功'}), 200

@app.route('/api/notifications', methods=['POST'])
def create_notification():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload or payload['role'] != 'staff':
        return jsonify({'error': '权限不足'}), 403

    data = request.get_json()
    title = data.get('title')
    content = data.get('content')

    if not title or not content:
        return jsonify({'error': '缺少必要参数'}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO notifications (title, content) VALUES (?, ?)', (title, content))
    db.commit()

    return jsonify({'message': '通知发布成功', 'id': cursor.lastrowid}), 201

@app.route('/api/notifications', methods=['GET'])
def get_notifications():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'error': '未登录'}), 401

    payload = verify_token(token)
    if not payload:
        return jsonify({'error': 'token无效'}), 401

    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM notifications ORDER BY create_time DESC')

    notifications = []
    for row in cursor.fetchall():
        notifications.append({
            'id': row['id'],
            'title': row['title'],
            'content': row['content'],
            'create_time': row['create_time']
        })

    return jsonify(notifications), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=True)