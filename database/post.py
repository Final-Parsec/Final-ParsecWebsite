from database import db
from database.user import User
from datetime import date
from sqlalchemy.orm import backref


class Post(db.Model):
    from database.post_tag import PostTag

    __tablename__ = 'post'

    id = db.Column('id', db.Integer, primary_key=True)
    slug = db.Column('slug', db.String)
    publish_date = db.Column('publish_date', db.Date)
    summary = db.Column('summary', db.String)
    content = db.Column('content', db.String)
    title = db.Column('title', db.String)
    is_draft = db.Column('is_draft', db.Boolean)
    author_id = db.Column('author_id', db.Integer, db.ForeignKey('user_account.id'))
    author = db.relationship(User, backref=backref('authored_posts', order_by='desc(Post.publish_date)'))
    tags = db.relationship(PostTag)

    def add(self):
        db.session.add(self)
        db.session.commit()
        return self

    @staticmethod
    def get(post_id):
        return Post.query.get(post_id)


def get_post_by_slug(slug):
    return Post.query.filter_by(slug=slug).first()


def get_posts(include_unpublished_posts=False):
    if include_unpublished_posts:
        return Post.query.order_by(Post.publish_date.desc())
    else:
        today = date.today()
        return Post.query.filter(Post.publish_date <= today).filter_by(is_draft=False)\
            .order_by(Post.publish_date.desc())


def get_posts_with_tag(tag_name):
    from database.tag import Tag
    today = date.today()
    return db.session.query(Post.publish_date, Post.slug, Post.summary, Post.title)\
        .join('tags', 'tag')\
        .filter(Post.is_draft == False)\
        .filter(Post.publish_date <= today)\
        .filter(Tag.name == tag_name)\
        .order_by(Post.publish_date.desc())


def get_related_posts(post_id):
    today = date.today()

    query = '''
        select distinct p.title, p.slug, p.publish_date, p.summary
        from post p
        join post_tag pt on pt.post_id = p.id
        join post_tag pt2 on pt2.tag_id = pt.tag_id
        where pt.post_id != ''' + str(post_id) + '''
          and pt2.post_id = ''' + str(post_id) + '''
          and p.is_draft = 0
          and p.publish_date < \'''' + str(today) + '''\'
        order by rand()
        limit 5;
    '''

    return db.engine.execute(query)