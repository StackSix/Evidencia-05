from __future__ import annotations
from modulos_main.menu_crud_automatizaciones import menu_crud_automatizacion
from modulos_main.menu_crud_dispositivos import menu_crud_dispositivos
from modulos_main.menu_crud_domicilios import menu_crud_domicilios
from modulos_main.menu_crud_usuarios import menu_crud_usuarios
from dao.dispositivos_dao import DispositivoDAO
from dao.usuarios_dao import UsuarioDAO
from dao.domicilios_dao import DomiciliosDAO

def menu_usuario(session):
    print(f"\nBienvenido/a {session['nombre']} ({session['rol']})")
    while True:
        print("\n1) Ver mis domicilios") 
        print("2) Ver mis dispositivos") 
        print("3) Ver mis datos personales") 
        if session["rol"] == "admin":
            print("4) [ADMIN] Gestionar CRUDs")
            
        print("0) Salir")
        op = input("> ").strip()

        if op == "1":
            ver_domicilios_usuario(session["dni"])

        elif op == "2":
            ver_dispositivos_usuario(session["id_usuario"])

        elif op == "3":
            ver_datos_personales(session["dni"])

        elif op == "4" and session["rol"] == "admin":
            # Submenú CRUD
            while True:
                print("\n[Menú CRUD]")
                print(" 1) Menú CRUD Usuarios")
                print(" 2) Menú CRUD Domicilios")
                print(" 3) Menú CRUD Dispositivos")
                print(" 4) Menú CRUD Automatización")
                print(" 0) Volver al menú anterior")
                sop = input("> ").strip()
                
                if sop == "1":
                    menu_crud_usuarios(session)
                    
                elif sop == "2":
                    menu_crud_domicilios(session)
                        
                elif sop == "3":
                    menu_crud_dispositivos(session)
                    
                elif op == "4":
                    menu_crud_automatizacion(session)
                
                elif sop == "0":
                    break
                
                else:
                    print("Ingrese una opción válida. Intentelo de nuevo")
             
        elif op == "0":
            break
        
        else:
            print("Ingrese una opción válida. Intentelo de nuevo")
            
def ver_domicilios_usuario(dni: int):
    domicilios_usuario = DomiciliosDAO.obtener_domicilio_usuario(dni)
    if domicilios_usuario:    
        for du in domicilios_usuario:
            print(f"{du.id_domicilio} - {du.nombre_domicilio} - {du.direccion} - {du.ciudad}")
    else:
        print("❌ No se encontró domicilio del usuario.")
        
def ver_dispositivos_usuario(id_usuario: int):
    dispositivos_usuario = DispositivoDAO.obtener_dispositivo_usuario(id_usuario)
    if dispositivos_usuario:
        for disp in dispositivos_usuario:
            print(f"{disp.id_dispositivo} - {disp.id_domicilio} - {disp.id_tipo} - {disp.estado} - {disp.etiqueta}")
    else:
        print("❌ No se encontraron dispositivos del usuario.")
        
def ver_datos_personales(dni: int):
    usuario = UsuarioDAO.obtener_por_dni(dni)
    if usuario:
        print(f"{usuario['dni']} - {usuario['nombre']} - {usuario['apellido']} - "
              f"{usuario['email']} - {usuario['rol']}")
    else:
        print("❌ No se encontró ningún usuario con ese DNI.")