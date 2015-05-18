from database import db


class Post(db.Model):
    __tablename__ = 'post'

    id = db.Column('id', db.Integer, primary_key=True)
    slug = db.Column('slug', db.String)
    publish_date = db.Column('publish_date', db.Date)
    summary = db.Column('summary', db.String)
    content = db.Column('content', db.String)
    title = db.Column('title', db.String)
    is_draft = db.Column('is_draft', db.Boolean)
    author_id = db.Column('author_id', db.Integer)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def get(post_id):
        return Post.query.get(post_id)


def get_posts():
    return Post.query.order_by(Post.publish_date.desc())