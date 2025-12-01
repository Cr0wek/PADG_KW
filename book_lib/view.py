from tkinter import *
import tkintermapview

class MapbookView:
    def __init__(self, root):
        self.root = root
        self.root.title("Mapbook MVC")
        self.root.geometry("800x870")
        self.markers = {}

        self._setup_frames()
        self._setup_listbox()
        self._setup_form()
        self._setup_details()
        self._setup_map()

    def _setup_frames(self):
        self.frame_list = Frame(self.root)
        self.frame_form = Frame(self.root)
        self.frame_details = Frame(self.root)
        self.frame_map = Frame(self.root)

        self.frame_list.grid(row=0, column=0)
        self.frame_form.grid(row=0, column=1)
        self.frame_details.grid(row=1, column=0, columnspan=2)
        self.frame_map.grid(row=2, column=0, columnspan=2)

    def _setup_listbox(self):
        Label(self.frame_list, text="Lista obiektów").grid(row=0, column=0, columnspan=3)
        self.listbox = Listbox(self.frame_list, width=40, height=10)
        self.listbox.grid(row=1, column=0, columnspan=3)

        self.btn_details = Button(self.frame_list, text="Pokaż szczegóły")
        self.btn_details.grid(row=2, column=0)
        self.btn_delete = Button(self.frame_list, text="Usuń obiekt")
        self.btn_delete.grid(row=2, column=1)
        self.btn_edit = Button(self.frame_list, text="Edytuj obiekt")
        self.btn_edit.grid(row=2, column=2)

    def _setup_form(self):
        Label(self.frame_form, text="Formularz:").grid(row=0, column=0, columnspan=2)
        Label(self.frame_form, text="Imie: ").grid(row=1, column=0, sticky=W)
        Label(self.frame_form, text="Lokalizacja: ").grid(row=2, column=0, sticky=W)
        Label(self.frame_form, text="Posty: ").grid(row=3, column=0, sticky=W)
        Label(self.frame_form, text="Img URL: ").grid(row=4, column=0, sticky=W)

        self.entry_name = Entry(self.frame_form)
        self.entry_name.grid(row=1, column=1)
        self.entry_loc = Entry(self.frame_form)
        self.entry_loc.grid(row=2, column=1)
        self.entry_posts = Entry(self.frame_form)
        self.entry_posts.grid(row=3, column=1)
        self.entry_img = Entry(self.frame_form)
        self.entry_img.grid(row=4, column=1)

        self.btn_add_save = Button(self.frame_form, text="Dodaj obiekt")
        self.btn_add_save.grid(row=5, column=0, columnspan=2)

    def _setup_details(self):
        Label(self.frame_details, text="Szczegóły obiektu").grid(row=0, column=0, sticky=W)
        
        Label(self.frame_details, text="Imie: ").grid(row=1, column=0)
        self.lbl_val_name = Label(self.frame_details, text="....")
        self.lbl_val_name.grid(row=1, column=1)

        Label(self.frame_details, text="Lokalizacja: ").grid(row=1, column=2)
        self.lbl_val_loc = Label(self.frame_details, text="....")
        self.lbl_val_loc.grid(row=1, column=3)

        Label(self.frame_details, text="Posty: ").grid(row=1, column=4)
        self.lbl_val_posts = Label(self.frame_details, text="....")
        self.lbl_val_posts.grid(row=1, column=5)

    def _setup_map(self):
        self.map_widget = tkintermapview.TkinterMapView(self.frame_map, width=800, height=600, corner_radius=10)
        self.map_widget.set_position(52.22977, 21.01178)
        self.map_widget.set_zoom(10)
        self.map_widget.grid(row=0, column=0)


    def get_form_data(self):
        return {
            'name': self.entry_name.get(),
            'location': self.entry_loc.get(),
            'posts': self.entry_posts.get(),
            'img_url': self.entry_img.get()
        }

    def clear_form(self):
        self.entry_name.delete(0, END)
        self.entry_loc.delete(0, END)
        self.entry_posts.delete(0, END)
        self.entry_img.delete(0, END)

    def fill_form(self, user):
        self.clear_form()
        self.entry_name.insert(0, user.name)
        self.entry_loc.insert(0, user.location)
        self.entry_posts.insert(0, str(user.posts))
        self.entry_img.insert(0, user.img_url)

    def refresh_list(self, users):
        self.listbox.delete(0, END)
        self.map_widget.delete_all_marker() # Czyszczenie mapy
        self.markers.clear()
        
        for user in users:
            self.listbox.insert(END, f'{user.name} from {user.location}')
            # Re-add marker
            marker = self.map_widget.set_marker(user.coords[0], user.coords[1], text=user.name)
            self.markers[user.id] = marker

    def show_details(self, user):
        self.lbl_val_name.config(text=user.name)
        self.lbl_val_loc.config(text=user.location)
        self.lbl_val_posts.config(text=str(user.posts))
        self.map_widget.set_position(user.coords[0], user.coords[1])
        
    def get_selected_index(self):
        if not self.listbox.curselection():
            return None
        return self.listbox.index(ACTIVE)