from sqlalchemy.orm import Session
from models import Cliente
import logging


class ClienteCRUD:

    @staticmethod
    def create_cliente(db: Session, nombre: str, email: str):
        # Verificar si el cliente ya existe
        cliente_existente = db.query(Cliente).filter_by(email=email).first()
        if cliente_existente:
            logging.warning(f"El cliente con el email '{email}' ya existe.")
            return cliente_existente
        
        # Crear nuevo cliente
        cliente = Cliente(nombre=nombre, email=email)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente

    @staticmethod
    def get_clientes(db: Session):
        # Retornar todos los clientes
        return db.query(Cliente).all()

    @staticmethod
    def update_cliente(db, email_actual, nuevo_nombre, nuevo_email):
        cliente = db.query(Cliente).filter_by(email=email_actual).first()
        if not cliente:
            return None  # Si no se encuentra el cliente, retorna None

        # Actualizar datos
        cliente.nombre = nuevo_nombre
        cliente.email = nuevo_email
        db.commit()
        return cliente

    @staticmethod
    def delete_cliente(db: Session, cliente_email: str):
        # Buscar cliente por email
        cliente = db.query(Cliente).filter(Cliente.email == cliente_email).first()
        if cliente:
            db.delete(cliente)
            db.commit()
            return cliente
        
        logging.error(f"No se encontró el cliente con el email '{cliente_email}'.")
        return None
