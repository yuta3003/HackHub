from sqlalchemy import create_engine

from api.models.model import Base

DB_URL = "mysql+pymysql://root@db:3306/prod?charset=utf8"
engine = create_engine(DB_URL, echo=True)


def reset_database():
    """
    データベースをリセットする関数。

    この関数は現在のデータベースのテーブルを全て削除し、
    Base.metadataに定義されているテーブルを再作成します。

    Args:
        なし

    Returns:
        なし
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    reset_database()
