from sqlalchemy import (
    create_engine,
    inspect,
    Column,
    Integer,
    String,
    Float,
    JSON,
)

from sqlalchemy.orm import (
    sessionmaker,
    declarative_base,
)

import json

DATABASE_URL = 'postgresql://lynseypi@localhost/python_dat_six'
ENGINE = create_engine(DATABASE_URL)
SESSION = sessionmaker(autocommit=False, autoflush=False, bind=ENGINE)
BASE = declarative_base()
INSPECTOR = inspect(ENGINE)


class Spaceship(BASE):
    __tablename__ = "spaceships"

    id = Column(Integer, primary_key=True)
    alignment = Column(String)
    name = Column(String)
    class_ = Column(String)
    length = Column(Float)
    crew_size = Column(Integer)
    speed = Column(Float)
    armed = Column(String)
    officers = Column(JSON)

    def __repr__(self):
        officers_info = ', '.join([
            "{{first_name: '{}', last_name: '{}', rank: '{}'}}".format(
                officer['first_name'], officer['last_name'], officer['rank']
            ) for officer in self.officers
        ])

        return (
            f"<Spaceship(name='{self.name}', "
            f"alignment='{self.alignment}', "
            f"class='{self.class_}', "
            f"length='{self.length}', "
            f"crew_size='{self.crew_size}', "
            f"armed='{self.armed}', "
            f"officers=[{officers_info}])>"
        )


def add_spaceship_in_db(spaceship_dict):
    if not INSPECTOR.has_table("spaceships"):
        BASE.metadata.create_all(bind=ENGINE)

    session = SESSION()
    ship_name = spaceship_dict["name"]
    ship_officers = spaceship_dict["officers"]

    exit_spaceship = session.query(Spaceship).filter_by(name=ship_name).first()

    if exit_spaceship:
        exit_officers = exit_spaceship.officers
        if exit_officers == ship_officers:
            # корабль с офицерами существует
            session.close()
            return
    spaceship = Spaceship(**spaceship_dict)
    session.add(spaceship)
    session.commit()
    session.close()


def find_traitors():
    session = SESSION()

    if ENGINE.dialect.has_table(ENGINE.connect(), "spaceships"):
        ally_officers = (
            session.query(Spaceship)
            .filter(Spaceship.alignment == "Ally")
            .all()
        )
        enemy_officers = (
            session.query(Spaceship)
            .filter(Spaceship.alignment == "Enemy")
            .all()
        )

        traitor_officers = [
            officer.officers for officer in ally_officers if officer in enemy_officers
        ]


        if not traitor_officers:
            print("None")
        else:
            traitor_officers_json = json.dumps(traitor_officers, indent=2)
            print(traitor_officers_json)

    session.close()

# def add_spaceship_in_db(spaceship_dict):
#     if not INSPECTOR.has_table("spaceships"):
#         BASE.metadata.create_all(bind=ENGINE)
#     session = SESSION()
#     spaceship = Spaceship(**spaceship_dict)
#     session.add(spaceship)
#     session.commit()
#     session.close()
