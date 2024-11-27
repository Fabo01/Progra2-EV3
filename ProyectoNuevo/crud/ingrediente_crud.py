from sqlalchemy.orm import Session
from models import Ingrediente


class IngredienteCRUD:

    @staticmethod
    def create_ingrediente(db: Session, nombre: str, tipo: str, cantidad: float, unidad: str):
        # Verificar si el ingrediente ya existe por nombre
        ingrediente_existente = db.query(Ingrediente).filter_by(nombre=nombre).first()
        if ingrediente_existente:
            print(f"El ingrediente con el nombre '{nombre}' ya existe.")
            return ingrediente_existente

        # Crear un nuevo ingrediente
        nuevo_ingrediente = Ingrediente(nombre=nombre, tipo=tipo, cantidad=cantidad, unidad=unidad)
        db.add(nuevo_ingrediente)
        db.commit()
        db.refresh(nuevo_ingrediente)  # Actualizar con datos generados
        return nuevo_ingrediente

    @staticmethod
    def get_ingredientes(db: Session):
        # Leer todos los ingredientes
        return db.query(Ingrediente).all()

    @staticmethod
    def get_ingrediente_by_id(db: Session, ingrediente_id: int):
        # Leer un ingrediente por ID
        return db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()

    @staticmethod
    def get_ingrediente_by_nombre(db: Session, nombre: str):
        # Leer un ingrediente por nombre
        return db.query(Ingrediente).filter(Ingrediente.nombre == nombre).first()

    @staticmethod
    def update_ingrediente(db: Session, ingrediente_id: int, cantidad: float = None, tipo: str = None, unidad: str = None):
        # Buscar el ingrediente por ID
        ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
        if not ingrediente:
            print(f"No se encontró el ingrediente con ID '{ingrediente_id}'.")
            return None

        # Actualizar los valores del ingrediente
        if cantidad is not None:
            ingrediente.cantidad = cantidad
        if tipo is not None:
            ingrediente.tipo = tipo
        if unidad is not None:
            ingrediente.unidad = unidad

        db.commit()
        db.refresh(ingrediente)  # Actualizar el objeto
        return ingrediente

    @staticmethod
    def delete_ingrediente(db: Session, ingrediente_id: int):
        # Buscar el ingrediente por ID
        ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
        if not ingrediente:
            print(f"No se encontró el ingrediente con ID '{ingrediente_id}'.")
            return None

        # Eliminar el ingrediente
        db.delete(ingrediente)
        db.commit()
        return ingrediente
