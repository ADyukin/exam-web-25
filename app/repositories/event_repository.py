from datetime import date, datetime

class EventRepository:
    def __init__(self, db_connector):
        self.db_connector = db_connector

    def get_all_active(self, page=1, per_page=10):
        """Получить все мероприятия с пагинацией"""
        with self.db_connector.connect().cursor() as cursor:
            # Получаем общее количество записей
            cursor.execute("SELECT COUNT(*) FROM events")
            total = cursor.fetchone()[0]
            
            # Получаем записи для текущей страницы
            offset = (page - 1) * per_page
            cursor.execute("""
                SELECT e.id, e.title, e.description, e.event_date, e.location, 
                       e.required_volunteers, e.image_filename,
                       CONCAT(u.last_name, ' ', u.first_name, ' ', COALESCE(u.middle_name, '')) as organizer_name,
                       (SELECT COUNT(*) FROM volunteer_registrations WHERE event_id = e.id AND status = 'accepted') as volunteers_count
                FROM events e
                JOIN users u ON e.organizer_id = u.id
                # WHERE e.event_date >= CURDATE()
                ORDER BY e.event_date ASC
                LIMIT %s OFFSET %s
            """, (per_page, offset))
            
            events = []
            for row in cursor.fetchall():
                event = {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'event_date': row[3],
                    'location': row[4],
                    'required_volunteers': row[5],
                    'image_filename': row[6],
                    'organizer_name': row[7],
                    'volunteers_count': row[8]
                }

                events.append(event)
            
            return {
                'items': events,
                'total': total,
                'pages': (total + per_page - 1) // per_page,
                'current_page': page
            }
    
    def get_by_id(self, event_id):
        """Получить мероприятие по ID"""
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("""
                SELECT e.id, e.title, e.description, e.event_date, e.location, 
                       e.required_volunteers, e.image_filename, e.organizer_id
                FROM events e
                WHERE e.id = %s
            """, (event_id,))
            row = cursor.fetchone()
            if row:
                return {
                    'id': row[0],
                    'title': row[1],
                    'description': row[2],
                    'event_date': row[3],
                    'location': row[4],
                    'required_volunteers': row[5],
                    'image_filename': row[6],
                    'organizer_id': row[7]
                }
            return None

    def create(self, event_data):
        """Создание нового мероприятия"""
        query = """
            INSERT INTO events (
                title, description, event_date, location, 
                required_volunteers, image_filename, organizer_id
            ) VALUES (
                %(title)s, %(description)s, %(event_date)s, %(location)s,
                %(required_volunteers)s, %(image_filename)s, %(organizer_id)s
            )
        """
        connection = self.db_connector.connect()
        cursor = connection.cursor()
        cursor.execute(query, event_data)
        connection.commit()
        return cursor.lastrowid
    
    def update(self, event_id, event_data):
        """Обновление мероприятия"""
        query = """
            UPDATE events 
            SET title = %(title)s,
                description = %(description)s,
                event_date = %(event_date)s,
                location = %(location)s,
                required_volunteers = %(required_volunteers)s,
                image_filename = %(image_filename)s
            WHERE id = %(id)s
        """
        event_data['id'] = event_id
        connection = self.db_connector.connect()
        cursor = connection.cursor()
        cursor.execute(query, event_data)
        connection.commit()
        return True
    
    def delete(self, event_id):
        """Удалить мероприятие и все связанные с ним регистрации"""
        conn = self.db_connector.connect()
        try:
            with conn.cursor() as cursor:
                # Сначала удаляем все регистрации волонтеров для этого мероприятия
                cursor.execute("DELETE FROM volunteer_registrations WHERE event_id = %s", (event_id,))
                
                # Затем удаляем само мероприятие
                cursor.execute("DELETE FROM events WHERE id = %s", (event_id,))
                
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            print(f"Ошибка при удалении мероприятия: {e}")
            return False
        finally:
            conn.close()
    
    def get_total_active_count(self):
        """Получить общее количество мероприятий"""
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM events")
            return cursor.fetchone()[0]

    def get_volunteers(self, event_id):
        """Получение списка принятых волонтеров мероприятия"""
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("""
                SELECT u.id, u.last_name, u.first_name, u.middle_name, 
                       vr.contact_info, vr.registration_date
                FROM users u
                JOIN volunteer_registrations vr ON u.id = vr.volunteer_id
                WHERE vr.event_id = %s AND vr.status = 'accepted'
                ORDER BY vr.registration_date DESC
            """, (event_id,))
            volunteers = cursor.fetchall()
            return [self._row_to_dict(volunteer, cursor.description) for volunteer in volunteers]

    def get_pending_volunteers(self, event_id):
        """Получение списка ожидающих волонтеров мероприятия"""
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("""
                SELECT u.id, u.last_name, u.first_name, u.middle_name, 
                       vr.contact_info, vr.registration_date
                FROM users u
                JOIN volunteer_registrations vr ON u.id = vr.volunteer_id
                WHERE vr.event_id = %s AND vr.status = 'pending'
                ORDER BY vr.registration_date DESC
            """, (event_id,))
            volunteers = cursor.fetchall()
            return [self._row_to_dict(volunteer, cursor.description) for volunteer in volunteers]

    def get_user_registration(self, event_id, user_id):
        """Получение информации о регистрации пользователя"""
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("""
                SELECT vr.*
                FROM volunteer_registrations vr
                WHERE vr.event_id = %s AND vr.volunteer_id = %s
            """, (event_id, user_id))
            registration = cursor.fetchone()
            return self._row_to_dict(registration, cursor.description) if registration else None

    def add_volunteer(self, event_id, user_id, contact_info):
        """Добавление волонтера на мероприятие"""
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("""
                INSERT INTO volunteer_registrations (event_id, volunteer_id, contact_info, status, registration_date)
                VALUES (%s, %s, %s, 'pending', NOW())
            """, (event_id, user_id, contact_info))
            cursor._connection.commit()

    def accept_volunteer(self, event_id, volunteer_id):
        """Принятие заявки волонтера"""
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("""
                UPDATE volunteer_registrations 
                SET status = 'accepted' 
                WHERE event_id = %s AND volunteer_id = %s
            """, (event_id, volunteer_id))
            cursor._connection.commit()

    def reject_volunteer(self, event_id, volunteer_id):
        """Отклонение заявки волонтера"""
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("""
                UPDATE volunteer_registrations 
                SET status = 'rejected' 
                WHERE event_id = %s AND volunteer_id = %s
            """, (event_id, volunteer_id))
            cursor._connection.commit()

    def reject_pending_volunteers(self, event_id):
        """Отклонение всех ожидающих заявок"""
        with self.db_connector.connect().cursor() as cursor:
            cursor.execute("""
                UPDATE volunteer_registrations 
                SET status = 'rejected' 
                WHERE event_id = %s AND status = 'pending'
            """, (event_id,))
            cursor._connection.commit()

    def _row_to_dict(self, row, description):
        if row is None:
            return None
        return dict(zip([col[0] for col in description], row)) 