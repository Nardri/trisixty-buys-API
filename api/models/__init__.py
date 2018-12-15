"""Models"""

from sqlalchemy import event

from .user import User

from api.utilities.push_id import PushID


def generate_unique_id(mapper, connection, target):
    """Generates a firebase fancy unique Id

        Args:
            mapper (obj): The current model class
            connection (obj): The current database connection
            target (obj): The current model instance
    Returns:
        None

    """
    push_id = PushID()
    target.id = push_id.next_id()


tables = [
    User,
]

for table in tables:
    event.listen(table, 'before_insert', generate_unique_id)
