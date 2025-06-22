class UserRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def _row_to_dict(self, row, description):
        if row is None:
            return None
        return {desc[0]: value for desc, value in zip(description, row)}

    def get_role(self, role_id):
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("""
                SELECT * FROM roles WHERE id = %s
            """, (role_id,))
            role = cursor.fetchone()
            return self._row_to_dict(role, cursor.description)

    def get_by_id(self, user_id):
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("""
                SELECT u.*, r.name as role_name, r.description as role_description
                FROM users u
                JOIN roles r ON u.role_id = r.id
                WHERE u.id = %s
            """, (user_id,))
            user = cursor.fetchone()
            return self._row_to_dict(user, cursor.description)


    def get_by_login_and_password(self, login, password_hash):
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("""
                SELECT u.*, r.name as role_name, r.description as role_description
                FROM users u
                JOIN roles r ON u.role_id = r.id
                WHERE BINARY u.login = %s AND u.password_hash = %s
            """, (login, password_hash))
            user = cursor.fetchone()
            return self._row_to_dict(user, cursor.description)

    def get_all_roles(self):
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("SELECT * FROM roles")
            roles = cursor.fetchall()
            return [self._row_to_dict(role, cursor.description) for role in roles]