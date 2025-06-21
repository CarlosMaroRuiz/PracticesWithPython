from db import execute_migrations
from student.iu.add_iu import add_student_iu
from student.iu.list_students_iu import list_students_iu
import sys

def clear_screen():
    """Limpia la pantalla de la consola"""
    import os
    os.system('cls' if os.name == 'nt' else 'clear')

def main():
    try:
        execute_migrations()
        
        while True:
            clear_screen()
            print("\n" + "="*40)
            print("Training sqlite and with ".center(40))
            print("="*40)
            print("\n1) Agregar estudiante")
            print("2) Listar estudiantes")
            print("3) Salir\n")
            
            try:
                option = input("Seleccione una opción (1-3): ").strip().lower()
                
                match option:
                    case "1" | "agregar":
                        add_student_iu()
                        input("\nPresione Enter para continuar...")
                    case "2" | "listar":
                        print("\nListado de estudiantes:")
                        list_students_iu()
                        input("\nPresione Enter para continuar...")
                    case "3" | "salir" | "exit":
                        print("\nGracias por usar el sistema. ¡Hasta pronto!")
                        sys.exit(0)
                    case _:
                        print("\n❌ Opción no válida")
                        input("Presione Enter para intentar nuevamente...")
                        
            except KeyboardInterrupt:
                print("\nOperación cancelada por el usuario")
                input("Presione Enter para volver al menú...")
                
    except Exception as e:
        print(f"\n❌ Error crítico: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()