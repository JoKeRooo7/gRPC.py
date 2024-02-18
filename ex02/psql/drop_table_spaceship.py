from set_ships_in_db import ENGINE

from sqlalchemy import MetaData

metadata = MetaData()
metadata.reflect(bind=ENGINE)  # ENGINE - ваш движок базы данных


if 'spaceships' in metadata.tables:
    spaceships_table = metadata.tables['spaceships']
    spaceships_table.drop(bind=ENGINE)
