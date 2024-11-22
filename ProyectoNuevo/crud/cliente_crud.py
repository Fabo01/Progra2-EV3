from sqlalchemy.orm import Session
from models import Cliente

class ClienteCRUD:

    @staticmethod
    def create_cliente(db: Session, nombre: str, email: str):
        cliente_existente = db.query(Cliente).filter_by(email=email).first()
        if cliente_existente:
            print(f"El cliente con el email '{email}' ya existe.")
            return cliente_existente
        
        cliente = Cliente(nombre=nombre, email=email)
        db.add(cliente)
        db.commit()
        db.refresh(cliente)
        return cliente
    
    @staticmethod
    def get_clientes(db: Session):
        return db.query(Cliente).all()
    
    @staticmethod
    def update_cliente(db: Session, email_actual: str, nuevo_nombre: str, nuevo_email: str = None):
        cliente = db.query(Cliente).get(email_actual)
        if not cliente:
            print(f"No se encontró el cliente con el email '{email_actual}'.")
            return None

        if nuevo_email and nuevo_email != email_actual:
            nuevo_cliente = Cliente(nombre=nuevo_nombre, email=nuevo_email)
            db.add(nuevo_cliente)
            db.commit()
            db.delete(cliente)
            db.commit()
            return nuevo_cliente
        
        else:
            cliente.nombre = nuevo_nombre
            db.commit()
            db.refresh(cliente)
            return cliente
    
    @staticmethod
    def delete_cliente(db: Session, cliente_id: int):
        cliente = db.query(Cliente).filter(Cliente.id == cliente_id).first()
        if cliente:
            db.delete(cliente)
            db.commit()
            return cliente

        return None
