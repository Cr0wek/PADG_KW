class User:
    def __init__(self, name:str, surname:str, location:str, event:str, img_url:str, id=None):
        self.id = id
        self.name = name
        self.surname = surname
        self.location = location
        self.event = event
        self.img_url = img_url
        self.coords = self.getting_coords_osm()
        
    def getting_coords_osm(self):
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
