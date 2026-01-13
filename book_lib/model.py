
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
        self.events = []
        self.artists = []
        self.employees = []
        
        self.add_event(Event("Festiwal Kukurydzy", "Kobyłka"))
        self.add_artist(Artist('Piotrek','Piter','Ząbki','1'))
        self.add_artist(Artist('Tomasz','Tomi','Radzymin','2'))
        self.add_employee(Employee('Adrian Nowak', 'Bramkarz', 'Warszawa', 1))
        self.add_employee(Employee('Beata Nowicka', 'Piwo', 'Łomianki', 1))
        
    def fetch_events(self):
        return self.events
    
    def fetch_artists(self):
        return self.artists

    def fetch_employees(self):
        return self.employees    
        
    def add_event(self, event):
        event.id = len(self.events) + 1
        self.events.append(event)
    def add_artist(self, artist):
        artist.id = len(self.artists) + 1
        self.artists.append(artist)
    def add_employee(self, employee):
        employee.id = len(self.employees) + 1
        self.employees.append(employee)
        
    def delete_event(self, index):
        if 0 <= index < len(self.events):
            del self.events[index]

    def delete_artist(self, index):
        if 0 <= index < len(self.artists):
            del self.artists[index]

    def delete_employee(self, index):
        if 0 <= index < len(self.employees):
            del self.employees[index]

    def update_event(self, index, new_data):
        if 0 <= index < len(self.events):
            evt = self.events[index]
            evt.name = new_data['p1']
            evt.location = new_data['p2']
            evt.coords = get_coords_osm(evt.location)

    def update_artist(self, index, new_data):
        if 0 <= index < len(self.artists):
            art = self.artists[index]
            art.full_name = new_data['p1']
            art.location = new_data['p2']
            art.nickname = new_data['p3']
            art.event_id = int(new_data['p4']) if new_data['p4'].isdigit() else 0
            art.coords = get_coords_osm(art.location)

    def update_employee(self, index, new_data):
        if 0 <= index < len(self.employees):
            emp = self.employees[index]
            emp.full_name = new_data['p1']
            emp.location = new_data['p2']
            emp.role = new_data['p3']
            emp.event_id = int(new_data['p4']) if new_data['p4'].isdigit() else 0
            emp.coords = get_coords_osm(emp.location)
    
    