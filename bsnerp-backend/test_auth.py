from app.auth.jwt_handler import verify_password, get_password_hash
from app.database import db

admin_user = None
for user in db.users.values():
    if user['email'] == 'admin@bsnerp.com':
        admin_user = user
        break

if admin_user:
    print(f'Admin user found: {admin_user["email"]}')
    print(f'Stored hash: {admin_user["password_hash"]}')
    
    test_password = 'password'
    is_valid = verify_password(test_password, admin_user['password_hash'])
    print(f'Password verification result: {is_valid}')
    
    new_hash = get_password_hash(test_password)
    print(f'New hash for "password": {new_hash}')
    
    is_new_valid = verify_password(test_password, new_hash)
    print(f'New hash verification: {is_new_valid}')
else:
    print('Admin user not found')
