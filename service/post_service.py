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

    def get_post_detail(self, user_id, post_id):
        return self.post_dao.get_post_detail(user_id, post_id)

    def like(self, like_id, post_id):
        liked=self.post_dao.get_liked(like_id, post_id)

        if liked[0]:
            return self.post_dao.update_like(like_id, post_id, 1)
        else:
            return self.post_dao.insert_like(like_id, post_id)

    def unlike(self, unlike_id, post_id):
        return self.post_dao.update_like(unlike_id, post_id, 0)

    def get_post_likes(self, post_id):
        return self.post_dao.get_post_likes(post_id)