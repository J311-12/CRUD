from tortoise import Tortoise, fields, models, run_async
from tortoise.transactions import in_transaction

class User(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255)


async def init():
    await Tortoise.init(
        db_url='//dataBase.db',
        modules={'models': ['__main__']},
    )
    await Tortoise.generate_schemas()


async def create_user():
    name = input("Nombre del usuario: ")
    email = input("Correo electrónico del usuario: ")
    
    async with in_transaction() as conn:
        user = await User.create(name=name, email=email)
        await conn.commit()
    
    print(f"Usuario creado con ID: {user.id}")


async def list_users():
    users = await User.all()
    for user in users:
        print(f"ID: {user.id}, Nombre: {user.name}, Email: {user.email}")

async def get_user_by_id():
    user_id = int(input("Ingrese el ID del usuario que desea obtener: "))
    user = await User.get(id=user_id)
    if user:
        print(f"ID: {user.id}, Nombre: {user.name}, Email: {user.email}")
    else:
        print("Usuario no encontrado")

async def delete_user_by_id():
    user_id = int(input("Ingrese el ID del usuario que desea eliminar: "))
    deleted_count = await User.filter(id=user_id).delete()
    if deleted_count > 0:
        print("Usuario eliminado exitosamente")
    else:
        print("Usuario no encontrado")

async def main():
    await init()
    
    while True:
        print("Operaciones disponibles:")
        print("1. Crear usuario")
        print("2. Listar usuarios")
        print("3. Obtener usuario por ID")
        print("4. Eliminar usuario por ID")
        print("5. Salir")
        
        operation_choice = input("Seleccione la operación que desea realizar (1/2/3/4/5): ")
        
        if operation_choice == "1":
            await create_user()
        elif operation_choice == "2":
            await list_users()
        elif operation_choice == "3":
            await get_user_by_id()
        elif operation_choice == "4":
            await delete_user_by_id()
        elif operation_choice == "5":
            break
        else:
            print("Selección no válida")

if __name__ == "__main__":
    run_async(main())
