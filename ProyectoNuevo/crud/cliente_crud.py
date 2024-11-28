import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Cliente
class ClienteCRUD:

    @staticmethod
    def create_cliente(db: Session, nombre: str, email: str):
        try:
            cliente_existente = db.query(Cliente).filter_by(email=email).first()
            if cliente_existente:
                logging.warning(f"El cliente con el email '{email}' ya existe.")
                return cliente_existente
            
            cliente = Cliente(nombre=nombre, email=email)
            db.add(cliente)
            db.commit()
            db.refresh(cliente)
            return cliente

        except SQLAlchemyError as e:
            db.rollback()
            logging.error(f"Error al crear cliente: {e}")
            return None

    @staticmethod
    def get_clientes(db: Session):
        try:
            return db.query(Cliente).all()
        except SQLAlchemyError as e:
            logging.error(f"Error al obtener clientes: {e}")
            return []

    @staticmethod
    def update_cliente(db: Session, email_actual: str, nuevo_nombre: str, nuevo_email: str):
        try:
            cliente = db.query(Cliente).filter_by(email=email_actual).first()
            if not cliente:
                logging.error(f"No se encontró el cliente con el email '{email_actual}'.")
                return None

            cliente.nombre = nuevo_nombre
            cliente.email = nuevo_email
            db.commit()
            db.refresh(cliente)
            return cliente

        except SQLAlchemyError as e:
            db.rollback()
            logging.error(f"Error al actualizar cliente: {e}")
            return None

    @staticmethod
    def delete_cliente(db: Session, cliente_email: str):
        try:
            cliente = db.query(Cliente).filter(Cliente.email == cliente_email).first()
            if cliente:
                db.delete(cliente)
                db.commit()
                return cliente
            
            logging.warning(f"No se encontró el cliente con el email '{cliente_email}'.")
            return None

        except SQLAlchemyError as e:
            db.rollback()
            logging.error(f"Error al eliminar cliente: {e}")
            return None
