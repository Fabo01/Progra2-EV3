from sqlalchemy.orm import Session
from models import Ingrediente

# Crear un nuevo ingrediente
def crear_ingrediente(db: Session, nombre: str, tipo: str, cantidad: float, unidad: str):
    nuevo_ingrediente = Ingrediente(nombre=nombre, tipo=tipo, cantidad=cantidad, unidad=unidad)
    db.add(nuevo_ingrediente)
    db.commit()
    db.refresh(nuevo_ingrediente)  # Actualiza el objeto con datos como el ID generado
    return nuevo_ingrediente

# Leer todos los ingredientes
def leer_ingredientes(db: Session):
    return db.query(Ingrediente).all()

# Leer un ingrediente por ID
def leer_ingrediente_por_id(db: Session, ingrediente_id: int):
    return db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()

# Leer un ingrediente por nombre
def leer_ingrediente_por_nombre(db: Session, nombre: str):
    return db.query(Ingrediente).filter(Ingrediente.nombre == nombre).first()

# Actualizar un ingrediente
def actualizar_ingrediente(db: Session, ingrediente_id: int, cantidad: float = None, tipo: str = None, unidad: str = None):
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if not ingrediente:
        return None  # Si el ingrediente no existe, retorna None
    if cantidad is not None:
        ingrediente.cantidad = cantidad
    if tipo is not None:
        ingrediente.tipo = tipo
    if unidad is not None:
        ingrediente.unidad = unidad
    db.commit()
    db.refresh(ingrediente)
    return ingrediente

# Eliminar un ingrediente
def eliminar_ingrediente(db: Session, ingrediente_id: int):
    ingrediente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente_id).first()
    if not ingrediente:
        return None  # Si el ingrediente no existe, retorna None
    db.delete(ingrediente)
    db.commit()
    return ingrediente
