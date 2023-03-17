from sqlalchemy import select, insert, update, delete, bindparam

from ..metadata import rendezvous_table


__all__ = (
    "retrieve_rendezvous_expression",
    "create_rendezvous_expression",
    "update_rendezvous_expression",
    "delete_rendezvous_expression"
)


retrieve_rendezvous_expression = (
    select(rendezvous_table)
    .where(rendezvous_table.c.id == bindparam("rendezvous_id"))
)

create_rendezvous_expression = (
    insert(rendezvous_table)
    .values(
        title=bindparam("rendezvous_title"),
        description=bindparam("rendezvous_description"),
        latitude=bindparam("rendezvous_coordinates_latitude"),
        longitude=bindparam("rendezvous_coordinates_longitude")
    )
    .returning(rendezvous_table)
)

update_rendezvous_expression = (
    update(rendezvous_table)
    .values(
        title=bindparam("rendezvous_title"),
        description=bindparam("rendezvous_description"),
        latitude=bindparam("rendezvous_coordinates_latitude"),
        longitude=bindparam("rendezvous_coordinates_longitude")
    )
    .where(rendezvous_table.c.id == bindparam("rendezvous_id"))
    .returning(rendezvous_table)
)

delete_rendezvous_expression = (
    delete(rendezvous_table)
    .where(rendezvous_table.c.id == bindparam("rendezvous_id"))
    .returning(rendezvous_table)
)
