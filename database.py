import pyodbc
import hashlib
import json
from datetime import datetime
import os
from contextlib import contextmanager

SERVER = 'localhost'  
DATABASE = 'cats_db'
TRUSTED_CONNECTION = 'yes'  

def get_connection_string():
    return f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE};Trusted_Connection={TRUSTED_CONNECTION};'

@contextmanager
def get_db_connection():
    conn = None
    try:
        conn = pyodbc.connect(get_connection_string())
        conn.autocommit = False
        yield conn
    except Exception as e:
        if conn:
            conn.rollback()
        raise e
    finally:
        if conn:
            conn.close()

@contextmanager
def get_db_cursor():
    with get_db_connection() as conn:
        cursor = conn.cursor()
        try:
            yield cursor
            conn.commit()
        except Exception:
            conn.rollback()
            raise

def init_db():
    try:
        with get_db_cursor() as cursor:
                        
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='users' AND xtype='U')
                CREATE TABLE users (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    first_name NVARCHAR(50) NOT NULL,
                    last_name NVARCHAR(50) NOT NULL,
                    email NVARCHAR(100) UNIQUE NOT NULL,
                    password NVARCHAR(100) NOT NULL,
                    gender NVARCHAR(10) CHECK(gender IN ('male', 'female')) DEFAULT 'male',
                    profile_picture NVARCHAR(255) DEFAULT 'default.png',
                    created_at DATETIME2 DEFAULT GETDATE()
                )
            ''')
            
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='posts' AND xtype='U')
                CREATE TABLE posts (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    content NVARCHAR(MAX) NOT NULL,
                    author NVARCHAR(100) NOT NULL,
                    user_id INT NOT NULL,
                    post_type NVARCHAR(20) CHECK(post_type IN ('inquiry', 'lost_cat', 'advice', 'story', 'help', 'other')) DEFAULT 'other',
                    post_image NVARCHAR(255),
                    cluster NVARCHAR(50) DEFAULT 'general',
                    created_at DATETIME2 DEFAULT GETDATE()
                )
            ''')

            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='comments' AND xtype='U')
                CREATE TABLE comments (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    text NVARCHAR(MAX) NOT NULL,
                    author NVARCHAR(100) NOT NULL,
                    user_id INT NOT NULL,
                    post_id INT NOT NULL,
                    created_at DATETIME2 DEFAULT GETDATE()
                )
            ''')
            
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='reactions' AND xtype='U')
                CREATE TABLE reactions (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id INT NOT NULL,
                    post_id INT NOT NULL,
                    reaction_type NVARCHAR(10) CHECK(reaction_type IN ('like', 'love', 'haha', 'wow', 'sad', 'angry')) DEFAULT 'like',
                    created_at DATETIME2 DEFAULT GETDATE(),
                    UNIQUE(user_id, post_id)
                )
            ''')
            
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='search_history' AND xtype='U')
                CREATE TABLE search_history (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id INT,
                    search_uuid NVARCHAR(36) NOT NULL,
                    location NVARCHAR(255) NOT NULL,
                    search_date DATETIME2 DEFAULT GETDATE(),
                    clinics_found INT DEFAULT 0
                )
            ''')
            
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='veterinarians' AND xtype='U')
                CREATE TABLE veterinarians (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    search_uuid NVARCHAR(36) NOT NULL,
                    name NVARCHAR(255) NOT NULL,
                    phone NVARCHAR(50),
                    address NVARCHAR(MAX),
                    website NVARCHAR(500),
                    rating REAL,
                    reviews INT,
                    latitude REAL,
                    longitude REAL,
                    hours NVARCHAR(MAX),
                    saved_at DATETIME2 DEFAULT GETDATE()
                )
            ''')
            
            cursor.execute('''
                IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='chat_history' AND xtype='U')
                CREATE TABLE chat_history (
                    id INT IDENTITY(1,1) PRIMARY KEY,
                    user_id INT NOT NULL,
                    message NVARCHAR(MAX) NOT NULL,
                    response NVARCHAR(MAX) NOT NULL,
                    is_user_message BIT NOT NULL,
                    session_id NVARCHAR(100) NOT NULL,
                    created_at DATETIME2 DEFAULT GETDATE()
                )
            ''')
            
            try:
                cursor.execute('''
                    IF NOT EXISTS (
                        SELECT * FROM sys.foreign_keys 
                        WHERE name = 'FK_posts_user_id'
                    )
                    ALTER TABLE posts 
                    ADD CONSTRAINT FK_posts_user_id 
                    FOREIGN KEY (user_id) REFERENCES users(id)
                ''')
            except Exception:
                pass
            
            try:
                cursor.execute('''
                    IF NOT EXISTS (
                        SELECT * FROM sys.foreign_keys 
                        WHERE name = 'FK_comments_user_id'
                    )
                    ALTER TABLE comments 
                    ADD CONSTRAINT FK_comments_user_id 
                    FOREIGN KEY (user_id) REFERENCES users(id)
                ''')
            except Exception:
                pass
            
            try:
                cursor.execute('''
                    IF NOT EXISTS (
                        SELECT * FROM sys.foreign_keys 
                        WHERE name = 'FK_comments_post_id'
                    )
                    ALTER TABLE comments 
                    ADD CONSTRAINT FK_comments_post_id 
                    FOREIGN KEY (post_id) REFERENCES posts(id)
                ''')
            except Exception:
                pass
            
            try:
                cursor.execute('''
                    IF NOT EXISTS (
                        SELECT * FROM sys.foreign_keys 
                        WHERE name = 'FK_reactions_user_id'
                    )
                    ALTER TABLE reactions 
                    ADD CONSTRAINT FK_reactions_user_id 
                    FOREIGN KEY (user_id) REFERENCES users(id)
                ''')
            except Exception:
                pass
            
            try:
                cursor.execute('''
                    IF NOT EXISTS (
                        SELECT * FROM sys.foreign_keys 
                        WHERE name = 'FK_reactions_post_id'
                    )
                    ALTER TABLE reactions 
                    ADD CONSTRAINT FK_reactions_post_id 
                    FOREIGN KEY (post_id) REFERENCES posts(id)
                ''')
            except Exception:
                pass
            
            try:
                cursor.execute('''
                    IF NOT EXISTS (
                        SELECT * FROM sys.foreign_keys 
                        WHERE name = 'FK_search_history_user_id'
                    )
                    ALTER TABLE search_history 
                    ADD CONSTRAINT FK_search_history_user_id 
                    FOREIGN KEY (user_id) REFERENCES users(id)
                ''')
            except Exception:
                pass
            
            try:
                cursor.execute('''
                    IF NOT EXISTS (
                        SELECT * FROM sys.foreign_keys 
                        WHERE name = 'FK_chat_history_user_id'
                    )
                    ALTER TABLE chat_history 
                    ADD CONSTRAINT FK_chat_history_user_id 
                    FOREIGN KEY (user_id) REFERENCES users(id)
                ''')
            except Exception:
                pass
            
            indexes = [
                ('IX_users_email', 'users(email)'),
                ('IX_posts_user_id', 'posts(user_id)'),
                ('IX_posts_cluster', 'posts(cluster)'),
                ('IX_comments_post_id', 'comments(post_id)'),
                ('IX_reactions_post_id', 'reactions(post_id)'),
                ('IX_search_history_user_id', 'search_history(user_id)'),
                ('IX_chat_history_user_id', 'chat_history(user_id)')
            ]
            
            for index_name, index_definition in indexes:
                try:
                    cursor.execute(f'''
                        IF NOT EXISTS (SELECT * FROM sys.indexes WHERE name='{index_name}')
                        CREATE INDEX {index_name} ON {index_definition}
                    ''')
                except Exception:
                    pass
            
            cursor.execute("SELECT id FROM users WHERE email = 'demo@example.com'")
            if not cursor.fetchone():
                demo_password = hash_password('password123')
                cursor.execute(
                    "INSERT INTO users (first_name, last_name, email, password, gender, profile_picture) OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?, ?)",
                    ('Demo', 'User', 'demo@example.com', demo_password, 'male', 'male.png')
                )
            
    except Exception as e:
        raise

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def create_user(first_name, last_name, email, password, gender='male', profile_picture=None):
    with get_db_cursor() as cursor:
        try:
            cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                raise ValueError("Email already registered")
            
            if gender not in ['male', 'female']:
                gender = 'male'
            
            if not profile_picture:
                if gender == 'male':
                    profile_picture = 'male.png'
                elif gender == 'female':
                    profile_picture = 'female.png'
            
            hashed_pw = hash_password(password)
            cursor.execute(
                "INSERT INTO users (first_name, last_name, email, password, gender, profile_picture) OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?, ?)",
                (first_name, last_name, email, hashed_pw, gender, profile_picture)
            )
            user_id = cursor.fetchone()[0]
            return user_id
        except pyodbc.IntegrityError:
            raise ValueError("Email already registered")
        except Exception as e:
            raise e

def get_user_by_email(email):
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT id, first_name, last_name, password, gender, profile_picture FROM users WHERE email = ?", 
            (email,)
        )
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'password': row[3],
                'gender': row[4],
                'profile_picture': row[5]
            }
        return None

def get_user_by_id(user_id):
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT id, first_name, last_name, email, gender, profile_picture FROM users WHERE id = ?", 
            (user_id,)
        )
        row = cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'email': row[3],
                'gender': row[4],
                'profile_picture': row[5]
            }
        return None

def update_user_profile_picture(user_id, profile_picture):
    with get_db_cursor() as cursor:
        try:
            cursor.execute(
                "UPDATE users SET profile_picture = ? WHERE id = ?",
                (profile_picture, user_id)
            )
            return True
        except Exception as e:
            return False

def get_all_posts():
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT p.id, p.content, p.author, p.user_id, p.post_type, p.post_image, p.cluster, p.created_at, 
                   u.profile_picture as author_picture
            FROM posts p
            LEFT JOIN users u ON p.user_id = u.id
            ORDER BY p.created_at DESC
        ''')
        posts = cursor.fetchall()
        
        posts_data = []
        for post in posts:
            cursor.execute('''
                SELECT reaction_type, COUNT(*) as count 
                FROM reactions 
                WHERE post_id = ? 
                GROUP BY reaction_type
            ''', (post[0],))
            reactions_data = cursor.fetchall()
            
            cursor.execute('''
                SELECT COUNT(*) as total_reactions 
                FROM reactions 
                WHERE post_id = ?
            ''', (post[0],))
            total_reactions = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT c.text, c.author, c.user_id, u.profile_picture as author_picture, c.created_at 
                FROM comments c 
                LEFT JOIN users u ON c.user_id = u.id
                WHERE c.post_id = ? 
                ORDER BY c.created_at ASC
            ''', (post[0],))
            comments = cursor.fetchall()
            
            reactions = {}
            for reaction in reactions_data:
                reactions[reaction[0]] = reaction[1]
            
            posts_data.append({
                'id': post[0],
                'content': post[1],
                'author': post[2],
                'user_id': post[3],
                'author_picture': post[8],
                'post_type': post[4],
                'post_image': post[5],
                'cluster': post[6],
                'created_at': post[7],
                'reactions': reactions,
                'total_reactions': total_reactions,
                'comments': [{
                    'text': comment[0],
                    'author': comment[1],
                    'user_id': comment[2],
                    'author_picture': comment[3],
                    'created_at': comment[4]
                } for comment in comments]
            })
        
        return posts_data

def create_post(content, author, user_id, post_type='other', post_image=None, cluster='general'):
    with get_db_cursor() as cursor:
        cursor.execute(
            "INSERT INTO posts (content, author, user_id, post_type, post_image, cluster) OUTPUT INSERTED.id VALUES (?, ?, ?, ?, ?, ?)",
            (content, author, user_id, post_type, post_image, cluster)
        )
        post_id = cursor.fetchone()[0]
        return post_id

def get_posts_by_cluster(cluster):
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT p.id, p.content, p.author, p.user_id, p.post_type, p.post_image, p.cluster, p.created_at, 
                   u.profile_picture as author_picture
            FROM posts p
            LEFT JOIN users u ON p.user_id = u.id
            WHERE p.cluster = ?
            ORDER BY p.created_at DESC
        ''', (cluster,))
        posts = cursor.fetchall()
        
        posts_data = []
        for post in posts:
            cursor.execute('''
                SELECT reaction_type, COUNT(*) as count 
                FROM reactions 
                WHERE post_id = ? 
                GROUP BY reaction_type
            ''', (post[0],))
            reactions_data = cursor.fetchall()
            
            cursor.execute('''
                SELECT COUNT(*) as total_reactions 
                FROM reactions 
                WHERE post_id = ?
            ''', (post[0],))
            total_reactions = cursor.fetchone()[0]
            
            cursor.execute('''
                SELECT c.text, c.author, c.user_id, u.profile_picture as author_picture, c.created_at 
                FROM comments c 
                LEFT JOIN users u ON c.user_id = u.id
                WHERE c.post_id = ? 
                ORDER BY c.created_at ASC
            ''', (post[0],))
            comments = cursor.fetchall()
            
            reactions = {}
            for reaction in reactions_data:
                reactions[reaction[0]] = reaction[1]
            
            posts_data.append({
                'id': post[0],
                'content': post[1],
                'author': post[2],
                'user_id': post[3],
                'author_picture': post[8],
                'post_type': post[4],
                'post_image': post[5],
                'cluster': post[6],
                'created_at': post[7],
                'reactions': reactions,
                'total_reactions': total_reactions,
                'comments': [{
                    'text': comment[0],
                    'author': comment[1],
                    'user_id': comment[2],
                    'author_picture': comment[3],
                    'created_at': comment[4]
                } for comment in comments]
            })
        
        return posts_data

def get_all_clusters():
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT DISTINCT cluster, COUNT(*) as post_count
            FROM posts 
            GROUP BY cluster
            ORDER BY post_count DESC
        ''')
        
        clusters = cursor.fetchall()
        return [{'cluster': cluster[0], 'post_count': cluster[1]} for cluster in clusters]

def toggle_reaction(user_id, post_id, reaction_type='like'):
    with get_db_cursor() as cursor:
        try:
            cursor.execute(
                "SELECT id, reaction_type FROM reactions WHERE user_id = ? AND post_id = ?",
                (user_id, post_id)
            )
            existing_reaction = cursor.fetchone()
            
            if existing_reaction:
                if existing_reaction[1] == reaction_type:
                    cursor.execute(
                        "DELETE FROM reactions WHERE user_id = ? AND post_id = ?",
                        (user_id, post_id)
                    )
                    action = 'removed'
                else:
                    cursor.execute(
                        "UPDATE reactions SET reaction_type = ? WHERE user_id = ? AND post_id = ?",
                        (reaction_type, user_id, post_id)
                    )
                    action = 'updated'
            else:
                cursor.execute(
                    "INSERT INTO reactions (user_id, post_id, reaction_type) VALUES (?, ?, ?)",
                    (user_id, post_id, reaction_type)
                )
                action = 'added'
            
            cursor.execute('''
                SELECT reaction_type, COUNT(*) as count 
                FROM reactions 
                WHERE post_id = ? 
                GROUP BY reaction_type
            ''', (post_id,))
            reactions_data = cursor.fetchall()
            
            cursor.execute('''
                SELECT COUNT(*) as total_reactions 
                FROM reactions 
                WHERE post_id = ?
            ''', (post_id,))
            total_reactions = cursor.fetchone()[0]
            
            cursor.execute(
                "SELECT reaction_type FROM reactions WHERE user_id = ? AND post_id = ?",
                (user_id, post_id)
            )
            user_reaction_row = cursor.fetchone()
            user_reaction = user_reaction_row[0] if user_reaction_row else None
            
            reactions = {}
            for reaction in reactions_data:
                reactions[reaction[0]] = reaction[1]
            
            return {
                'reactions': reactions,
                'total_reactions': total_reactions,
                'user_reaction': user_reaction,
                'action': action
            }
                
        except Exception as e:
            raise e

def get_user_reaction(user_id, post_id):
    with get_db_cursor() as cursor:
        cursor.execute(
            "SELECT reaction_type FROM reactions WHERE user_id = ? AND post_id = ?",
            (user_id, post_id)
        )
        reaction = cursor.fetchone()
        return reaction[0] if reaction else None

def create_comment(text, author, user_id, post_id):
    with get_db_cursor() as cursor:
        cursor.execute("SELECT id FROM posts WHERE id = ?", (post_id,))
        if not cursor.fetchone():
            raise ValueError("Post not found")
        
        cursor.execute(
            "INSERT INTO comments (text, author, user_id, post_id) VALUES (?, ?, ?, ?)",
            (text, author, user_id, post_id)
        )
        
        cursor.execute(
            "SELECT COUNT(*) FROM comments WHERE post_id = ?",
            (post_id,)
        )
        comment_count = cursor.fetchone()[0]
        
        return comment_count

def get_comments_for_post(post_id):
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT c.text, c.author, c.user_id, u.profile_picture as author_picture, c.created_at 
            FROM comments c 
            LEFT JOIN users u ON c.user_id = u.id
            WHERE c.post_id = ? 
            ORDER BY c.created_at ASC
        ''', (post_id,))
        comments = cursor.fetchall()
        
        return [{
            'text': comment[0],
            'author': comment[1],
            'user_id': comment[2],
            'author_picture': comment[3],
            'created_at': comment[4]
        } for comment in comments]

def save_search_history(user_id, search_uuid, location, clinics_found):
    with get_db_cursor() as cursor:
        try:
            cursor.execute(
                "INSERT INTO search_history (user_id, search_uuid, location, clinics_found) OUTPUT INSERTED.id VALUES (?, ?, ?, ?)",
                (user_id, search_uuid, location, clinics_found)
            )
            return cursor.fetchone()[0]
        except Exception as e:
            raise e

def save_veterinarian_details(search_uuid, clinic_data):
    with get_db_cursor() as cursor:
        try:
            cursor.execute('''
                INSERT INTO veterinarians 
                (search_uuid, name, phone, address, website, rating, reviews, latitude, longitude, hours)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                search_uuid,
                clinic_data.get('name', ''),
                clinic_data.get('phone', ''),
                clinic_data.get('address', ''),
                clinic_data.get('website', ''),
                clinic_data.get('rating', 0),
                clinic_data.get('reviews', 0),
                clinic_data.get('latitude'),
                clinic_data.get('longitude'),
                json.dumps(clinic_data.get('hours', {})) if clinic_data.get('hours') else None
            ))
            return cursor.fetchone()[0]
        except Exception as e:
            raise e

def get_search_history(user_id, limit=10):
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT sh.id, sh.search_uuid, sh.location, sh.search_date, sh.clinics_found,
                   COUNT(v.id) as vets_saved
            FROM search_history sh
            LEFT JOIN veterinarians v ON sh.search_uuid = v.search_uuid
            WHERE sh.user_id = ?
            GROUP BY sh.id, sh.search_uuid, sh.location, sh.search_date, sh.clinics_found
            ORDER BY sh.search_date DESC
            OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY
        ''', (user_id, limit))
        
        history = cursor.fetchall()
        
        return [{
            'id': item[0],
            'search_uuid': item[1],
            'location': item[2],
            'search_date': item[3],
            'clinics_found': item[4],
            'vets_saved': item[5]
        } for item in history]

def get_search_results(search_uuid):
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT sh.location, sh.search_date, sh.clinics_found
            FROM search_history sh
            WHERE sh.search_uuid = ?
        ''', (search_uuid,))
        
        search_info = cursor.fetchone()
        if not search_info:
            return None
        
        cursor.execute('''
            SELECT name, phone, address, website, rating, reviews, latitude, longitude, hours
            FROM veterinarians
            WHERE search_uuid = ?
            ORDER BY rating DESC
        ''', (search_uuid,))
        
        clinics = cursor.fetchall()
        
        clinics_data = []
        for clinic in clinics:
            clinic_info = {
                'name': clinic[0],
                'phone': clinic[1],
                'address': clinic[2],
                'website': clinic[3],
                'rating': clinic[4],
                'reviews': clinic[5],
                'latitude': clinic[6],
                'longitude': clinic[7]
            }
            
            if clinic[8]:
                try:
                    clinic_info['hours'] = json.loads(clinic[8])
                except:
                    clinic_info['hours'] = {}
            
            clinics_data.append(clinic_info)
        
        return {
            'location': search_info[0],
            'search_date': search_info[1],
            'clinics_found': search_info[2],
            'clinics': clinics_data
        }

def save_chat_message(user_id, message, response, is_user_message, session_id):
    with get_db_cursor() as cursor:
        try:
            cursor.execute('''
                INSERT INTO chat_history (user_id, message, response, is_user_message, session_id)
                OUTPUT INSERTED.id
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, message, response, is_user_message, session_id))
            
            return cursor.fetchone()[0]
        except Exception as e:
            raise e

def get_chat_history(user_id, session_id=None, limit=50):
    with get_db_cursor() as cursor:
        if session_id:
            cursor.execute('''
                SELECT message, response, is_user_message, created_at, session_id
                FROM chat_history
                WHERE user_id = ? AND session_id = ?
                ORDER BY created_at ASC
                OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY
            ''', (user_id, session_id, limit))
        else:
            cursor.execute('''
                SELECT message, response, is_user_message, created_at, session_id
                FROM chat_history
                WHERE user_id = ?
                ORDER BY created_at DESC
                OFFSET 0 ROWS FETCH NEXT ? ROWS ONLY
            ''', (user_id, limit))
        
        messages = cursor.fetchall()
        
        return [{
            'message': msg[0],
            'response': msg[1],
            'is_user_message': bool(msg[2]),
            'created_at': msg[3],
            'session_id': msg[4]
        } for msg in messages]

def get_chat_sessions(user_id):
    with get_db_cursor() as cursor:
        cursor.execute('''
            SELECT DISTINCT session_id, MAX(created_at) as last_activity,
                   (SELECT TOP 1 message FROM chat_history 
                    WHERE user_id = ? AND session_id = ch.session_id 
                    ORDER BY created_at DESC) as last_message
            FROM chat_history ch
            WHERE user_id = ?
            GROUP BY session_id
            ORDER BY last_activity DESC
            OFFSET 0 ROWS FETCH NEXT 20 ROWS ONLY
        ''', (user_id, user_id))
        
        sessions = cursor.fetchall()
        
        return [{
            'session_id': session[0],
            'last_activity': session[1],
            'last_message': session[2] or 'No messages'
        } for session in sessions]

def delete_chat_session(user_id, session_id):
    with get_db_cursor() as cursor:
        try:
            cursor.execute('''
                DELETE FROM chat_history
                WHERE user_id = ? AND session_id = ?
            ''', (user_id, session_id))
            
            return cursor.rowcount
        except Exception as e:
            raise e