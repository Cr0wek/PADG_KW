import psycopg2

class User:
    def __init__(self, name: str, location: str, posts: int, img_url: str, id: int = None):
        self.id = id
        self.name = name
        self.location = location
        self.posts = posts
        self.img_url = img_url
        self.coords = self.get_coords_osm()

    def get_coords_osm(self):
        import requests
        url:str=f'https://nominatim.openstreetmap.org/search?q={self.location}&format=json&limit=1'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        data=requests.get(url, headers=headers).json()
        latitude=float(data[0]['lat'])
        longitude=float(data[0]['lon'])
        return [latitude, longitude]

class Artist(User):
    def __init__(self, name:str, surname:str, location:str, event:str, img_url:str, genre:str, nickname:str, id=None):
        super().__init__(name, surname, location, event, img_url, id)
        self.genre = genre
        self.nickname = nickname
        
class Organizer(User):
    def __init__(self, name:str, surname:str, location:str, event:str, img_url:str, company_name:str, id=None):
        super().__init__(name, surname, location, event, img_url, id)
        self.company_name = company_name


class MapbookModel:
    def __init__(self):
        self.connection = psycopg2.connect(
            user="postgres", host="localhost", database="postgres", password='postgres', port=5432
        )
        self.users = []

    def fetch_all_users(self):
        cursor = self.connection.cursor()
        cursor.execute("""
            SELECT id, name, location, posts, img_url, 
            ST_Y(geometry::geometry) as lat, ST_X(geometry::geometry) as lon 
            FROM public.users
        """)
        rows = cursor.fetchall()
        self.users.clear()
        for row in rows:
            # row: 0=id, 1=name, 2=loc, 3=posts, 4=img, 5=lat, 6=lon
            user = User(row[1], row[2], row[3], row[4], id=row[0])
            self.users.append(user)
        return self.users

    def add_user(self, user: User):
        cursor = self.connection.cursor()
        query = """
            INSERT INTO public.users (name, location, posts, img_url, geometry) 
            VALUES (%s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326)) 
            RETURNING id
        """
        cursor.execute(query, (user.name, user.location, user.posts, user.img_url, user.coords[1], user.coords[0]))
        user.id = cursor.fetchone()[0]
        self.connection.commit()
        self.users.append(user)

    def delete_user(self, user_index):
        user = self.users[user_index]
        cursor = self.connection.cursor()
        cursor.execute("DELETE FROM public.users WHERE id=%s", (user.id,))
        self.connection.commit()
        self.users.pop(user_index)

    def update_user(self, user_index, updated_data: dict):
        user = self.users[user_index]
        user.name = updated_data['name']
        user.location = updated_data['location']
        user.posts = int(updated_data['posts'])
        user.img_url = updated_data['img_url']
        user.coords = user.get_coords_osm()
        # Update DB
        cursor = self.connection.cursor()
        query = """
            UPDATE public.users 
            SET name=%s, location=%s, posts=%s, img_url=%s, 
            geometry=ST_SetSRID(ST_MakePoint(%s, %s), 4326) 
            WHERE id=%s
        """
        cursor.execute(query, (user.name, user.location, user.posts, user.img_url, user.coords[1], user.coords[0], user.id))
        self.connection.commit()
        
        return user