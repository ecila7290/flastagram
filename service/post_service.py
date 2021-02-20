class PostService:
    def __init__(self, post_dao, config):
        self.post_dao=post_dao
        self.config=config

    def post(self, user_id, content):
        new_post_id=self.post_dao.insert_post(user_id, content)
        return new_post_id

    def post_images(self, user_id, post_id, image_urls):
        return self.post_dao.insert_post_image(user_id, post_id, image_urls)

    def get_user_post(self, user_id):
        return self.post_dao.get_posts(user_id)

