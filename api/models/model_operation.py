"""Common model operations"""

from . import db


class ModelOperation(object):
    """Model operation"""

    def save(self):
        """Save to the database"""

        db.session.add(self)
        db.session.commit()
        return self
