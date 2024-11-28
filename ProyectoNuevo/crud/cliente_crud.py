from sqlalchemy.orm import Session
from ProyectoNuevo.models import Cliente
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
    def update_cliente(db: Session, email_actual: str, nuevo_nombre: str, nuevo_email: str = None):
        # Buscar cliente por email actual
        cliente = db.query(Cliente).get(email_actual)
        if not cliente:
            logging.error(f"No se encontró el cliente con el email '{email_actual}'.")
            return None

        # Verificar si el nuevo email ya está en uso
        if nuevo_email:
            email_existente = db.query(Cliente).filter(Cliente.email == nuevo_email).first()
            if email_existente:
                logging.warning(f"El email '{nuevo_email}' ya está asociado a otro cliente.")
                return None
            cliente.email = nuevo_email

        # Actualizar el nombre del cliente
        cliente.nombre = nuevo_nombre
        db.commit()
        db.refresh(cliente)
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
