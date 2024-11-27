from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime,UniqueConstraint
from sqlalchemy.orm import relationship
from ProyectoNuevo.database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    email = Column(String, primary_key=True)
    nombre = Column(String, nullable=False)
    pedidos = relationship("Pedido", back_populates="cliente")

class Ingrediente(Base):
    __tablename__ = "ingredientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    tipo = Column(String, nullable=False)
    cantidad = Column(Float, nullable=False)
    unidad = Column(String, nullable=False)
    

class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)
    ingredientes = relationship("MenuIngrediente", back_populates="menu")

class MenuIngrediente(Base):
    __tablename__ = "menu_ingredientes"
    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"))
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"))
    cantidad = Column(Float, nullable=False)
    menu = relationship("Menu", back_populates="ingredientes")

class Pedido(Base):
    __tablename__ = "pedidos"
    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String)
    total = Column(Float, nullable=False)
    fecha = Column(DateTime, nullable=False)
    cliente_email = Column(String, ForeignKey("clientes.email"))  
    cliente = relationship("Cliente", back_populates="pedidos")