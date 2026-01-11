import psycopg2

def get_coords_osm(location):
    import requests
    url:str=f'https://nominatim.openstreetmap.org/search?q={location}&format=json&limit=1'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    data=requests.get(url, headers=headers).json()
    latitude=float(data[0]['lat'])
    longitude=float(data[0]['lon'])
    return [latitude, longitude]

class Event:
    def __init__(self, name, location, id=None, coords=None):
        self.id = id
        self.name = name
        self.location = location
        self.coords = coords if coords else get_coords_osm(location)

class Artist:
    def __init__(self, full_name, nickname, location, event_id, id=None, coords=None):
        self.id = id
        self.full_name = full_name
        self.nickname = nickname
        self.location = location
        self.event_id = event_id
        self.coords = coords if coords else get_coords_osm(location)

class Employee:
    def __init__(self, full_name, role, location, event_id, id=None, coords=None):
        self.id = id
        self.full_name = full_name
        self.role = role
        self.location = location
        self.event_id = event_id
        self.coords = coords if coords else get_coords_osm(location)


class MapbookModel:
    def __init__(self):
        self.connection = psycopg2.connect(
            user="postgres", host="localhost", database="cultural_events", password='postgres', port=5432
        )
    
    def fetch_events(self):
        cur = self.connection.cursor()
        cur.execute("SELECT id, name, location, ST_Y(geometry::geometry), ST_X(geometry::geometry) FROM events")
        return [Event(r[1], r[2], id=r[0], coords=[r[3], r[4]]) for r in cur.fetchall()]
    
    def fetch_artists(self):
        cur = self.connection.cursor()
        cur.execute("SELECT id, full_name, nickname, location, event_id, ST_Y(geometry::geometry), ST_X(geometry::geometry) FROM artists")
        return [Artist(r[1], r[2], r[3], r[4], id=r[0], coords=[r[5], r[6]]) for r in cur.fetchall()]

    def fetch_employees(self):
        cur = self.connection.cursor()
        cur.execute("SELECT id, full_name, role, location, event_id, ST_Y(geometry::geometry), ST_X(geometry::geometry) FROM employees")
        return [Employee(r[1], r[2], r[3], r[4], id=r[0], coords=[r[5], r[6]]) for r in cur.fetchall()]
    
    def add_event(self, event):
        cur = self.connection.cursor()
        cur.execute(f"INSERT INTO events (name, location, geometry) VALUES ('{event.name}', '{event.location}', ST_SetSRID(ST_MakePoint({event.coords[1]}, {event.coords[0]}), 4326))")
        self.connection.commit()

    def add_artist(self, artist):
        cur = self.connection.cursor()
        cur.execute("INSERT INTO artists (full_name, nickname, location, event_id, geometry) VALUES (%s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))",
                    (artist.full_name, artist.nickname, artist.location, artist.event_id, artist.coords[1], artist.coords[0]))
        self.connection.commit()

    def add_employee(self, emp):
        cur = self.connection.cursor()
        cur.execute("INSERT INTO employees (full_name, role, location, event_id, geometry) VALUES (%s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326))",
                    (emp.full_name, emp.role, emp.location, emp.event_id, emp.coords[1], emp.coords[0]))
        self.connection.commit()

    