import logging
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models import Menu, MenuIngrediente, Ingrediente
class MenuCRUD:

    @staticmethod
    def create_menu(db: Session, nombre: str, descripcion: str, ingredientes: list):
        try:
            for ingrediente in ingredientes:
                ingrediente_existente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente["id"]).first()
                if not ingrediente_existente:
                    logging.error(f"Ingrediente con ID '{ingrediente['id']}' no existe.")
                    return None

            menu = Menu(nombre=nombre, descripcion=descripcion)
            db.add(menu)
            db.commit()

            for ingrediente in ingredientes:
                menu_ingrediente = MenuIngrediente(
                    menu_id=menu.id,
                    ingrediente_id=ingrediente["id"],
                    cantidad=ingrediente["cantidad"]
                )
                db.add(menu_ingrediente)

            db.commit()
            db.refresh(menu)
            return menu

        except SQLAlchemyError as e:
            db.rollback()
            logging.error(f"Error al crear menú: {e}")
            return None

    @staticmethod
    def get_menus(db: Session):
        try:
            return db.query(Menu).all()
        except SQLAlchemyError as e:
            logging.error(f"Error al obtener menús: {e}")
            return []

    @staticmethod
    def update_menu(db: Session, menu_id: int, nuevo_nombre: str = None, nueva_descripcion: str = None, nuevos_ingredientes: list = None):
        try:
            menu = db.query(Menu).get(menu_id)
            if not menu:
                logging.error(f"No se encontró el menú con el ID '{menu_id}'.")
                return None

            if nuevo_nombre:
                menu.nombre = nuevo_nombre
            if nueva_descripcion:
                menu.descripcion = nueva_descripcion

            if nuevos_ingredientes is not None:
                db.query(MenuIngrediente).filter_by(menu_id=menu_id).delete()
                for ingrediente in nuevos_ingredientes:
                    nuevo_menu_ingrediente = MenuIngrediente(
                        menu_id=menu_id,
                        ingrediente_id=ingrediente["id"],
                        cantidad=ingrediente["cantidad"]
                    )
                    db.add(nuevo_menu_ingrediente)

            db.commit()
            db.refresh(menu)
            return menu

        except SQLAlchemyError as e:
            db.rollback()
            logging.error(f"Error al actualizar menú: {e}")
            return None

    @staticmethod
    def delete_menu(db: Session, menu_id: int):
        try:
            menu = db.query(Menu).get(menu_id)
            if menu:
                db.query(MenuIngrediente).filter_by(menu_id=menu_id).delete()
                db.delete(menu)
                db.commit()
                return menu

            logging.error(f"No se encontró el menú con el ID '{menu_id}'.")
            return None

        except SQLAlchemyError as e:
            db.rollback()
            logging.error(f"Error al eliminar menú: {e}")
            return None
