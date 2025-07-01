from sqlalchemy import Column, Integer, String, Boolean, text, ForeignKey, DECIMAL, Date
from sqlalchemy.orm import relationship

from app.config import Base


class UserModel(Base):
    __tablename__ = "usuarios"

    id = Column("id_usuario", Integer, primary_key=True, index=True)
    user_code = Column(
        "codigo_usuario", String, server_default=text("uuid_generate_v4()")
    )
    username = Column("nombre_usuario", String(25))
    email = Column("correo_electronico", String(100))
    password = Column("contrasenia", String)
    session_version = Column("version_sesion", Integer)

    categories = relationship(
        "ExpenseCategoryModel", secondary="usuarios_categorias", back_populates="users"
    )
    expenses = relationship("ExpenseModel", back_populates="user")


class ExpenseCategoryModel(Base):
    __tablenmae__ = "categorias_gastos"

    category_id = Column("id_categoria", Integer, primary_key=True, index=True)
    category_name = Column("nombre_categoria", String(50))

    users = relationship(
        "UserModel", secondary="usuarios_categorias", back_populates="categories"
    )
    expenses = relationship("ExpenseModel", back_populates="category")


class UserCategory(Base):
    __tablename__ = "usuarios_categorias"

    id = Column("id_usuario_categoria", Integer, primary_key=True)
    user_id = Column("id_usuario", Integer, ForeignKey("usuarios.id_usuario"))
    category_id = Column(
        "id_categoria", Integer, ForeignKey("categorias_gastos.id_categoria")
    )


class ExpenseModel(Base):
    __tablename__ = "gastos"

    expense_id = Column("id_gasto", Integer, primary_key=True)
    category_id = Column(
        "id_categoria", Integer, ForeignKey("categorias_gastos.id_categoria")
    )
    description = Column("descripcion", String(250))
    amount = Column("monto", DECIMAL(precision=18, scale=2))
    expense_date = Column("fecha_gasto", Date)
    user_id = Column("id_usuario", Integer, ForeignKey("usuarios.id_usuario"))

    user = relationship("UserModel", back_populates="expenses")
    category = relationship("ExpenseCategoryModel", back_populates="expenses")
