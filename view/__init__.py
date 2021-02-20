import jwt

from flask import Flask, jsonify, request, current_app, Response, g
from flask.json import JSONEncoder
from functools import wraps

class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj,set):
            return list(obj)
        return JSONEncoder.default(self,obj)

def login_required(f):
    @wraps(f)
    def decorated_func(*args, **kwargs):
        access_token=request.headers.get('Authorization')
        if access_token is not None:
            try:
                payload=jwt.decode(access_token, current_app.config['JWT_SECRET_KEY'], current_app.config['ALGORITHM'])
            except jwt.InvalidTokenError:
                payload=None
            
            if payload is None: return Response(status=401)

            user_id=payload['user_id']
            g.user_id=user_id
        else:
            return Response(status=401)
        
        return f(*args, **kwargs)
    return decorated_func

def create_endpoints(app, services):
    user_service=services.user_service
    post_service=services.post_service

    @app.route('/signup', methods=['POST'])
    def signup():
        new_user=request.json
        new_user_id=user_service.create_new_user(new_user)
        new_user=user_service.get_user(new_user_id)

        return jsonify(new_user)

    @app.route('/login', methods=['POST'])
    def login():
        credential=request.json
        authorized=user_service.login(credential)

        if authorized:
            user_credential=user_service.get_user_id_and_password(credential['email'])
            user_id=user_credential['id']
            token=user_service.generate_access_token(user_id)

            return jsonify({'user_id':user_id, 'access_token':token})
        else:
            return '', 401
    
    @app.route('/follow', methods=['POST'])
    @login_required
    def follow():
        payload=request.json
        user_id=g.user_id
        follow_id=payload['follow']

        user_service.follow(user_id, follow_id)

        return 'success', 200

    @app.route('/unfollow', methods=['POST'])
    @login_required
    def unfollow():
        payload=request.json
        user_id=g.user_id
        follow_id=payload['follow']

        user_service.unfollow(user_id, follow_id)

        return 'success', 200

    @app.route('/post', methods=['POST'])
    @login_required
    def post():
        user_post=request.json
        content=user_post['content']
        image_urls=user_post['images']
        user_id=g.user_id

        new_post_id=post_service.post(user_id, content)
        post_service.post_images(user_id, new_post_id, image_urls)

        return 'success', 201            

    @app.route('/<int:user_id>/post', methods=['GET'])
    def get_user_post(user_id):
        user_post=post_service.get_user_post(user_id)

        return jsonify({
            'posts':user_post
        })

    # @app.route('/<int:user_id>/post/<int:post_id>', methods=['GET'])
    # def get_user_post_detail(user_id, post_id):
