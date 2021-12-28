from sqlalchemy.orm import sessionmaker, clear_mappers, scoped_session, class_mapper
from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from AnonymousPlatform.models import Conversation, Message, Base
def connect_database(app):
    database_uri = app.config.get('ANONYMOUSPLATFORM_SQLALCHEMY_DATABASE_URI', 'sqlite:///AnonymousPlatform.db')
    database_echo = app.config.get('ANONYMOUSPLATFORM_SQLALCHEMY_ECHO', False)
    database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                    echo=database_echo)
    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)
    if len(database_engine.table_names()) == 0:
        print("REPOPULATING DATABASE for AnonymousPlatform Plugin ...")
        Base.metadata.create_all(database_engine)
        session = session_factory()
        session.commit()
        print("REPOPULATING DATABASE for AnonymousPlatform Plugin ... FINISHED")
    return session_factory
