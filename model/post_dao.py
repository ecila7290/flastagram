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
        print(rows)
        return [{
            'post_id':post[1],
            'image_url': post[2]
        } for post in rows]