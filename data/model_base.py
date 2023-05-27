from sqlalchemy.orm import declarative_base
from sqlalchemy.engine import Engine


SqlAlchemyBase = declarative_base()

def create_metadata(engine: Engine):
    SqlAlchemyBase.metadata.drop_all(bind=engine)
    SqlAlchemyBase.metadata.create_all(bind=engine)
    
