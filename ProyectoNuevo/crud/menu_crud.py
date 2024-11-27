from sqlalchemy.orm import Session
from models import Menu, MenuIngrediente

class MenuCRUD:
    @staticmethod
    def create_menu(db: Session, nombre: str, descripcion: str, ingredientes: list):
        menu = Menu(nombre=nombre, descripcion=descripcion)
        db.add(menu)
        db.commit()
        
        for ingrediente in ingredientes:
            menu_ingrediente = MenuIngrediente(menu_id=menu.id, ingrediente_id=ingrediente["id"], cantidad=ingrediente["cantidad"])
            db.add(menu_ingrediente)
        
        db.commit()
        db.refresh(menu)
        return menu
    
    @staticmethod
    def get_menus(db: Session):
        return db.query(Menu).all()
    
    @staticmethod
    def update_menu(db: Session, menu_id: int, nuevo_nombre: str = None, nueva_descripcion: str = None, nuevos_ingredientes: list = None):
        menu = db.query(Menu).get(menu_id)
        if not menu:
            print(f"No se encontró el menú con el ID '{menu_id}'.")
            return None

        if nuevo_nombre:
            menu.nombre = nuevo_nombre
        if nueva_descripcion:
            menu.descripcion = nueva_descripcion
        
        if nuevos_ingredientes is not None:
            db.query(MenuIngrediente).filter_by(menu_id=menu_id).delete()
            # Agregar nuevos ingredientes
            for ingrediente in nuevos_ingredientes:
                nuevo_menu_ingrediente = MenuIngrediente(menu_id=menu_id, ingrediente_id=ingrediente["id"], cantidad=ingrediente["cantidad"])
                db.add(nuevo_menu_ingrediente)
        
        db.commit()
        db.refresh(menu)
        return menu
    
    @staticmethod
    def delete_menu(db: Session, menu_id: int):
        menu = db.query(Menu).get(menu_id)
        if menu:
            db.query(MenuIngrediente).filter_by(menu_id=menu_id).delete()
            db.delete(menu)
            db.commit()
            return menu
        return None
