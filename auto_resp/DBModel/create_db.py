from .__init__ import Base,engine

def create_db(engine=engine):
    Base.metadata.create_all(engine)

if __name__ == '__main__':

    create_db()