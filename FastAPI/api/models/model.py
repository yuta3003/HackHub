"""
api.db モジュール

このモジュールは SQLAlchemy を使用してデータベースモデルを定義します。
以下は含まれるクラスの簡単な説明です:

- User: ユーザー情報を表すデータベーステーブルのモデルクラス。
- Post: 投稿情報を表すデータベーステーブルのモデルクラス。
- Comment: コメント情報を表すデータベーステーブルのモデルクラス。

これらのクラスはデータベース内の異なるテーブルを表し、それぞれのテーブルに対する関連性も定義されています。
"""
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from api.db import Base


class User(Base):
    """
    ユーザー情報を表すデータベーステーブルのモデルクラスです。

    Attributes:
        user_id (int): ユーザーの一意の識別子。
        user_name (str): ユーザーの名前。
        password_hash (str): ユーザーのパスワードのハッシュ値。
        post (relationship): ユーザーが作成した投稿との関連性。
        comment (relationship): ユーザーが作成したコメントとの関連性。
    """

    __tablename__ = "users"

    user_id = Column(Integer, autoincrement=True, primary_key=True)
    user_name = Column(String(256), nullable=False, unique=True)
    password_hash = Column(String(256), nullable=False)

    post = relationship("Post", back_populates="user", cascade="delete")
    comment = relationship("Comment", back_populates="user", cascade="delete")


class Post(Base):
    """
    投稿情報を表すデータベーステーブルのモデルクラスです。

    Attributes:
        post_id (int): 投稿の一意の識別子。
        user_id (int): 投稿を作成したユーザーの識別子。
        contents (str): 投稿の内容。
        user (relationship): 投稿を作成したユーザーとの関連性。
        comment (relationship): 投稿に対するコメントとの関連性。
    """

    __tablename__ = "posts"

    post_id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    contents = Column(String(256))

    user = relationship("User", back_populates="post")
    comment = relationship("Comment", back_populates="post", cascade="delete")


class Comment(Base):
    """
    コメント情報を表すデータベーステーブルのモデルクラスです。

    Attributes:
        comment_id (int): コメントの一意の識別子。
        user_id (int): コメントを作成したユーザーの識別子。
        post_id (int): コメントが対象とする投稿の識別子。
        contents (str): コメントの内容。
        user (relationship): コメントを作成したユーザーとの関連性。
        post (relationship): コメントが対象とする投稿との関連性。
    """

    __tablename__ = "comments"

    comment_id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    post_id = Column(Integer, ForeignKey("posts.post_id"))
    contents = Column(String(256))

    user = relationship("User", back_populates="comment")
    post = relationship("Post", back_populates="comment")
