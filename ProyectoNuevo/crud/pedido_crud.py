from sqlalchemy.orm import Session
from ProyectoNuevo.models import Pedido, Cliente
import logging


class PedidoCRUD:

    @staticmethod
    def crear_pedido(db: Session, cliente_email: str, descripcion: str):
        # Verificar cliente
        cliente = db.query(Cliente).filter_by(email=cliente_email).first()
        if not cliente:
            logging.error(f"No se encontró el cliente con el email '{cliente_email}'.")
            return None

        # Crear pedido
        pedido = Pedido(descripcion=descripcion, cliente=cliente)
        db.add(pedido)
        db.commit()
        db.refresh(pedido)
        return pedido

    @staticmethod
    def leer_pedidos(db: Session):
        # Retornar todos los pedidos
        return db.query(Pedido).all()

    @staticmethod
    def actualizar_pedido(db: Session, pedido_id: int, nueva_descripcion: str):
        # Buscar pedido
        pedido = db.query(Pedido).get(pedido_id)
        if not pedido:
            logging.error(f"No se encontró el pedido con el ID '{pedido_id}'.")
            return None

        # Actualizar descripción
        pedido.descripcion = nueva_descripcion
        db.commit()
        db.refresh(pedido)
        return pedido

    @staticmethod
    def borrar_pedido(db: Session, pedido_id: int):
        # Buscar pedido
        pedido = db.query(Pedido).get(pedido_id)
        if pedido:
            db.delete(pedido)
            db.commit()
            return pedido
        
        logging.error(f"No se encontró el pedido con el ID '{pedido_id}'.")
        return None
