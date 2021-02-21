from sqlalchemy import text

class PostDao:
    def __init__(self, database):
        self.db=database

    def insert_post(self, user_id, content):
        return self.db.execute(text("""
            INSERT INTO posts (
                user_id,
                content
            ) VALUES(
                :id,
                :content
            )
        """),{'id':user_id, 'content':content}).lastrowid

    def insert_post_image(self, user_id, post_id, image_urls):
        for url in image_urls:
            self.db.execute(text("""
            INSERT INTO post_images (
                user_id,
                post_id,
                image_url
            ) VALUES (
                :user_id,
                :post_id,
                :url
            )
        """),{'user_id':user_id,'post_id':post_id, 'url':url}).rowcount
        

    def get_posts(self, user_id):
        rows=self.db.execute(text("""
            SELECT 
                MIN(id),
                post_id,
                ANY_VALUE(image_url)
            FROM post_images
            WHERE user_id=:id
            GROUP BY post_id
            ORDER BY ANY_VALUE(-created_at)
        """),{'id':user_id}).fetchall()
        
        return [{
            'post_id':post['post_id'],
            'image_url': post['ANY_VALUE(image_url)']
        } for post in rows]

    def get_post_detail(self, user_id, post_id):
        content=self.db.execute(text("""
            SELECT
                content
            FROM posts
            WHERE id=:post_id
        """),{'post_id':post_id}).fetchone()

        images=self.db.execute(text("""
            SELECT
                image_url
            FROM post_images
            WHERE user_id=:id AND post_id=:post_id
        """),{'id':user_id, 'post_id':post_id}).fetchall()

        return {
            'content':content['content'],
            'images':[image['image_url'] for image in images]
            }
    
    def get_liked(self, user_id, post_id):
        return self.db.execute(text("""
            SELECT IF (EXISTS (
                SELECT * FROM post_likes
                WHERE user_id=:id AND post_id=:post_id
            ),1,0)
        """),{'id':user_id, 'post_id':post_id}).fetchone()

    def insert_like(self, user_id, post_id):
        return self.db.execute(text("""
            INSERT INTO post_likes(
                user_id,
                post_id
            ) VALUES (
                :id,
                :post_id
            )
        """),{'id':user_id, 'post_id':post_id}).rowcount

    def update_like(self, user_id, post_id, status):
        return self.db.execute(text("""
            UPDATE post_likes
            SET liked=:status
            WHERE user_id=:id AND post_id=:post_id
        """),{'id':user_id, 'post_id':post_id, 'status':status}).rowcount

    def get_post_likes(self, post_id):
        likes=self.db.execute(text("""
            SELECT 
                u.id, 
                u.name
            FROM users u
            LEFT JOIN post_likes pl ON pl.post_id=:post_id
            WHERE u.id=pl.user_id AND liked=1
        """),{'post_id':post_id}).fetchall()

        return {
            'like_count':len(likes),
            'like_users':[{
                'user_id':user['id'],
                'name':user['name']
            } for user in likes]
        }