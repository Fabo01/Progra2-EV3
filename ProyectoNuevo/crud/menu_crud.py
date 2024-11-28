from sqlalchemy.orm import Session
from ProyectoNuevo.models import Menu, MenuIngrediente, Ingrediente
import logging


class MenuCRUD:

    @staticmethod
    def create_menu(db: Session, nombre: str, descripcion: str, ingredientes: list):
        # Verificar existencia de ingredientes
        for ingrediente in ingredientes:
            ingrediente_existente = db.query(Ingrediente).filter(Ingrediente.id == ingrediente["id"]).first()
            if not ingrediente_existente:
                logging.error(f"Ingrediente con ID '{ingrediente['id']}' no existe.")
                return None

        # Crear menú
        menu = Menu(nombre=nombre, descripcion=descripcion)
        db.add(menu)
        db.commit()

        # Asociar ingredientes
        for ingrediente in ingredientes:
            menu_ingrediente = MenuIngrediente(menu_id=menu.id, ingrediente_id=ingrediente["id"], cantidad=ingrediente["cantidad"])
            db.add(menu_ingrediente)

        db.commit()
        db.refresh(menu)
        return menu

    @staticmethod
    def get_menus(db: Session):
        # Retornar todos los menús
        return db.query(Menu).all()

    @staticmethod
    def update_menu(db: Session, menu_id: int, nuevo_nombre: str = None, nueva_descripcion: str = None, nuevos_ingredientes: list = None):
        # Buscar menú
        menu = db.query(Menu).get(menu_id)
        if not menu:
            logging.error(f"No se encontró el menú con el ID '{menu_id}'.")
            return None

        # Actualizar campos
        if nuevo_nombre:
            menu.nombre = nuevo_nombre
        if nueva_descripcion:
            menu.descripcion = nueva_descripcion

        # Actualizar ingredientes si se proporcionaron
        if nuevos_ingredientes is not None:
            db.query(MenuIngrediente).filter_by(menu_id=menu_id).delete()
            for ingrediente in nuevos_ingredientes:
                nuevo_menu_ingrediente = MenuIngrediente(menu_id=menu_id, ingrediente_id=ingrediente["id"], cantidad=ingrediente["cantidad"])
                db.add(nuevo_menu_ingrediente)

        db.commit()
        db.refresh(menu)
        return menu

    @staticmethod
    def delete_menu(db: Session, menu_id: int):
        # Buscar menú
        menu = db.query(Menu).get(menu_id)
        if menu:
            db.query(MenuIngrediente).filter_by(menu_id=menu_id).delete()
            db.delete(menu)
            db.commit()
            return menu
        
        logging.error(f"No se encontró el menú con el ID '{menu_id}'.")
        return None
