import factory

from src.infraestructure.adapters.outputs.db.session import SyncSessionLocal


class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        abstract = True

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        with SyncSessionLocal() as session:
            cls._meta.sqlalchemy_session = session

            obj = model_class(*args, **kwargs)

            session.add(obj)

            session.commit()

            session.refresh(obj)

            return obj
