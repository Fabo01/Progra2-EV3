from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, UniqueConstraint, Text
from sqlalchemy.orm import relationship
from ProyectoNuevo.database import Base

class Cliente(Base):
    __tablename__ = "clientes"
    email = Column(String, unique=True, primary_key=True)
    nombre = Column(String, nullable=False)
    pedidos = relationship("Pedido", back_populates="cliente")

class Ingrediente(Base):
    __tablename__ = "ingredientes"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, nullable=False)
    tipo = Column(String, nullable=False)
    cantidad = Column(Float, nullable=False)
    unidad = Column(String, nullable=False)

    # Relación con MenuIngrediente
    menus = relationship("MenuIngrediente", back_populates="ingrediente")

class Menu(Base):
    __tablename__ = "menus"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    descripcion = Column(String)

    # Relación con MenuIngrediente
    ingredientes = relationship("MenuIngrediente", back_populates="menu")

class MenuIngrediente(Base):
    __tablename__ = "menu_ingredientes"
    id = Column(Integer, primary_key=True, index=True)
    menu_id = Column(Integer, ForeignKey("menus.id"), nullable=False)
    ingrediente_id = Column(Integer, ForeignKey("ingredientes.id"), nullable=False)
    cantidad = Column(Float, nullable=False)

    # Relación bidireccional con Menu e Ingrediente
    menu = relationship("Menu", back_populates="ingredientes")
    ingrediente = relationship("Ingrediente", back_populates="menus")

    # Restricción única para evitar duplicados
    __table_args__ = (UniqueConstraint('menu_id', 'ingrediente_id', name='unique_menu_ingrediente'),)

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    descripcion = Column(Text, nullable=False)
    total = Column(Float, nullable=False)
    fecha = Column(DateTime, nullable=False)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)

    # Relación con Cliente
    cliente = relationship("Cliente", back_populates="pedidos")
