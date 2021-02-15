from flask import Flask, jsonify, request, current_app

def create_endpoints(app, services):
    user_service=services.user_service

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