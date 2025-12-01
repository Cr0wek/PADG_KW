
from tkinter import Tk
from book_lib.controller import MapbookController
from book_lib.model import MapbookModel
from book_lib.view import MapbookView

if __name__ == "__main__":
    root = Tk()
    model = MapbookModel()
    view = MapbookView(root)
    controller = MapbookController(model, view)
    root.mainloop()