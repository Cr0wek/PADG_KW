from tkinter import *
import tkintermapview

import psycopg2

db_engine = psycopg2.connect(
    user="postgres",
    host="localhost",
    database="postgres",
    password='postgres',
    port=5432
)
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


def entryClear():
    entry_name.delete(0, END)
    entry_lokalizacja.delete(0, END)
    entry_posty.delete(0, END)
    entry_imgurl.delete(0, END)
    entry_name.focus()

def addUser(usersdata:list)->None:
    cursor = db_engine.cursor()
    name:str=entry_name.get()
    location:str=entry_lokalizacja.get()
    posts:int=int(entry_posty.get())
    image:str=entry_imgurl.get()
    # Nowa część
    tempUser=User(name=name, location=location, posts=posts, img_url=image, id=None)
    SQL= f"INSERT INTO public.users (name, location, posts, img_url, geometry) VALUES ('{name}', '{location}', {posts}, '{image}', ST_SetSRID(ST_MakePoint({tempUser.coords[1]}, {tempUser.coords[0]}), 4326)) RETURNING id"
    cursor.execute(SQL)
    new_id=cursor.fetchone()[0]
    db_engine.commit()
    tempUser.id=new_id
    usersdata.append(tempUser)
    print(f"New user with ID: {new_id}")
    user_info(usersdata)
    entryClear()
    map_widget.set_position(usersdata[-1].coords[0], usersdata[-1].coords[1])
    
def user_info(usersdata:list)->None:
    listbox_lista_obiektow.delete(0, END)
    for idx, user in enumerate(usersdata):
        listbox_lista_obiektow.insert(idx, f'{user.name} from {user.location} with {user.posts} posts')
        
def user_info_startup(usersdata:list)->None:
    if not usersdata:
        cursor=db_engine.cursor()
        cursor.execute("SELECT * FROM public.users")
        records=cursor.fetchall()
        for record in records:
            user=User(name=record[1], location=record[2], posts=record[3], img_url=record[4], id=record[0])
            usersdata.append(user)
        user_info(usersdata)
    else:
        return
        
def removeUser(usersdata:list)->None:
    i=listbox_lista_obiektow.index(ACTIVE)
    usersdata[i].marker.delete()
    cursor= db_engine.cursor()
    cursor.execute(f"DELETE FROM public.users WHERE id={usersdata[i].id}")
    db_engine.commit()
    usersdata.pop(i)
    user_info(usersdata)
    
def user_details(usersdata:list)->None:
    i=listbox_lista_obiektow.index(ACTIVE)
    label_imie_szczegoly_obiektu_wartosc.config(text=usersdata[i].name)
    label_lokalizacja_szczegoly_obiektu_wartosc.config(text=usersdata[i].location)
    label_posty_szczegoly_obiektu_wartosc.config(text=usersdata[i].posts)
    map_widget.set_position(usersdata[i].coords[0], usersdata[i].coords[1])

def editUser(usersdata:list)->None:
    i=listbox_lista_obiektow.index(ACTIVE)
    entry_name.insert(0,usersdata[i].name)
    entry_lokalizacja.insert(0,usersdata[i].location)
    entry_posty.insert(0,usersdata[i].posts)
    entry_imgurl.insert(0,usersdata[i].img_url)
    button_dodaj_obiekt.config(text="Zapisz zmiany", command=lambda: updateUser(usersdata, i))

def updateUser(usersdata:list, i:int)->None:
    usersdata[i].name=entry_name.get()
    usersdata[i].location=entry_lokalizacja.get()
    usersdata[i].posts=int(entry_posty.get())
    usersdata[i].img_url=entry_imgurl.get()
    usersdata[i].coords=usersdata[i].get_coords()
    usersdata[i].marker.set_position(usersdata[i].coords[0], usersdata[i].coords[1])
    usersdata[i].marker.set_text(usersdata[i].name)
    cursor=db_engine.cursor()
    cursor.execute(f"UPDATE public.users SET name='{usersdata[i].name}', location='{usersdata[i].location}', posts={usersdata[i].posts}, img_url='{usersdata[i].img_url}', geometry=ST_SetSRID(ST_MakePoint({usersdata[i].coords[1]}, {usersdata[i].coords[0]}), 4326) WHERE id={usersdata[i].id}")
    db_engine.commit()
    user_info(usersdata)
    map_widget.set_position(usersdata[i].coords[0], usersdata[i].coords[1])
    entryClear()
    button_dodaj_obiekt.config(text="Dodaj obiekt", command=lambda: addUser(users))



root= Tk()
root.title("Mapbook")
root.geometry("800x870")

ramka_lista_obiektow= Frame(root)
ramka_formularz=Frame(root)
ramka_szczegoly_obiektu=Frame(root)
ramka_mapa=Frame(root)

ramka_lista_obiektow.grid(row=0,column=0)
ramka_formularz.grid(row=0, column=1)
ramka_szczegoly_obiektu.grid(row=1,column=0, columnspan=2)
ramka_mapa.grid(row=2,column=0,columnspan=2)

# RAMKA LISTA OBIEKTOW
label_lista_obiektow=Label(ramka_lista_obiektow, text="Lista obiektów")
label_lista_obiektow.grid(row=0,column=0, columnspan=3)
listbox_lista_obiektow=Listbox(ramka_lista_obiektow, width=40, height=10)
listbox_lista_obiektow.grid(row=1,column=0, columnspan=3)

button_pokaz_szczegoly=Button(ramka_lista_obiektow, text="Pokaż szczegóły", command=lambda: user_details(users))
button_pokaz_szczegoly.grid(row=2,column=0)

button_usun_obiekt=Button(ramka_lista_obiektow,text="Usuń obiekt", command=lambda: removeUser(users))
button_usun_obiekt.grid(row=2, column=1)

button_edytuj_obiekt=Button(ramka_lista_obiektow,text="Edytuj obiekt", command=lambda: editUser(users))
button_edytuj_obiekt.grid(row=2, column=2)

# RAMKA FORMULARZ

label_formularz=Label(ramka_formularz, text="Formularz:")
label_formularz.grid(row=0,column=0,columnspan=2)

label_imie=Label(ramka_formularz, text="Imie: ")
label_imie.grid(row=1,column=0, sticky=W)
label_lokalizacja=Label(ramka_formularz, text="Lokalizacja: ")
label_lokalizacja.grid(row=2,column=0, sticky=W)
label_posty=Label(ramka_formularz, text="Posty: ")
label_posty.grid(row=3,column=0, sticky=W)
label_imgurl=Label(ramka_formularz, text="Img URL: ")
label_imgurl.grid(row=4,column=0, sticky=W)

entry_name=Entry(ramka_formularz)
entry_name.grid(row=1,column=1)
entry_lokalizacja=Entry(ramka_formularz)
entry_lokalizacja.grid(row=2,column=1)
entry_posty=Entry(ramka_formularz)
entry_posty.grid(row=3,column=1)
entry_imgurl=Entry(ramka_formularz)
entry_imgurl.grid(row=4,column=1)

button_dodaj_obiekt=Button(ramka_formularz, text="Dodaj obiekt", command=lambda: addUser(users))
button_dodaj_obiekt.grid(row=5,column=0,columnspan=2)

# RAMKA SZCZEGOLY OBIEKTU

label_szczegoly_obiektu=Label(ramka_szczegoly_obiektu,text="Szczegóły obiektu")
label_szczegoly_obiektu.grid(row=0,column=0,sticky=W)
label_imie_szczegoly_obiektu=Label(ramka_szczegoly_obiektu, text="Imie: ")
label_imie_szczegoly_obiektu.grid(row=1,column=0)
label_imie_szczegoly_obiektu_wartosc=Label(ramka_szczegoly_obiektu, text="....")
label_imie_szczegoly_obiektu_wartosc.grid(row=1,column=1)

label_lokalizacja_szczegoly_obiektu=Label(ramka_szczegoly_obiektu, text="Lokalizacja: ")
label_lokalizacja_szczegoly_obiektu.grid(row=1,column=2)
label_lokalizacja_szczegoly_obiektu_wartosc=Label(ramka_szczegoly_obiektu, text="....")
label_lokalizacja_szczegoly_obiektu_wartosc.grid(row=1,column=3)

label_posty_szczegoly_obiektu=Label(ramka_szczegoly_obiektu, text="Posty: ")
label_posty_szczegoly_obiektu.grid(row=1,column=4)
label_posty_szczegoly_obiektu_wartosc=Label(ramka_szczegoly_obiektu, text="....")
label_posty_szczegoly_obiektu_wartosc.grid(row=1,column=5)

# RAMKA MAPA
map_widget=tkintermapview.TkinterMapView(ramka_mapa, width=800, height=600, corner_radius=10)
map_widget.set_position(52.22977, 21.01178) # Warszawa
map_widget.set_zoom(10)
map_widget.grid(row=0,column=0)
map_widget.set_tile_server("https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}&s=Ga", max_zoom=22)
user_info_startup(users)
root.mainloop()

#