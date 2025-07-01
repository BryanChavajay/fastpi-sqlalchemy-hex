from sqlalchemy import Column, Integer, String, Boolean, text

from app.config import Base


class UserModel(Base):
    __tablename__ = "usuarios"

    id = Column("id_usuario", Integer, primary_key=True, index=True)
    user_code = Column("codigo_usuario", String, server_default=text("uuid_generate_v4()"))
    username = Column("nombre_usuario", String(25))
    email = Column("correo_electronico", String(100))
    password = Column("contrasenia", String)
    session_version = Column("version_sesion", Integer)
