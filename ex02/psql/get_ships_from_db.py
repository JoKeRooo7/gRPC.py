from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError

from set_ships_in_db import ENGINE
import json
import set_ships_in_db

SESSION = sessionmaker(bind=ENGINE)

try:
    session = SESSION()

    all_spaceships = session.query(set_ships_in_db.Spaceship).all()

    for spaceship in all_spaceships:
        spaceship_dict = {
            'alignment': spaceship.alignment,
            'name': spaceship.name,
            'class': spaceship.class_,
            'length': spaceship.length,
            'crew_size': spaceship.crew_size,
            'armed': spaceship.armed,
            'officers': spaceship.officers
        }
        print(json.dumps(spaceship_dict, indent=2, separators=(',', ': ')))

except ProgrammingError as e:
    print("Ошибка:", e)
