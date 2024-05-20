from customtkinter import *
from tkinter import filedialog, messagebox
from PIL import Image
from datetime import datetime as dt
import humanfriendly
import os
import io
import sqlite3 as db


orange = '#fe6f27'
darkorange = '#DA672D'
darkerorange = '#A45025'
darkgray = '#2f2f2f'
fonttype = 'SF Pro Display Regular'

sql = db.connect('database.db')
cur = sql.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS products
                  (id INTEGER PRIMARY KEY,
                  name TEXT NOT NULL,
                  price INTEGER NOT NULL,
                  stock INTEGER NOT NULL,
                  imgdata BLOB,
                  dateadded TEXT NOT NULL,
                  dateupdated TEXT)''')
sql.commit()


app = CTk()
app.geometry("1000x630")
app.title('Product Profiling')
app.resizable(False, False)
app.config(bg = darkgray)

settingspath = 'C:\\Users\\USER\\Desktop\\Python Codes\\John GUI\\settings\\'
#CTkImage(light_image = Image.open(f'{settingspath}{img}.png'), size = (25, 25))

panel_on_display = False
addproduct_on_display = False
product_on_display = False


class ImageUploader:
    def __init__(self, app):
        self.app = app
        self.image_data = None
        self.filename = None
        
    def upload_image(self):
        file = filedialog.askopenfilename(filetypes = [('Image Files', "*.png;*.jpg")])
        if file:
            with open(file, 'rb') as f:
                self.filename = os.path.basename(file)
                self.image_data = f.read()
                print("Image uploaded!", self.filename)
                
    def insert_image(self):
        if self.image_data:
            cur.execute("""insert into products (imgdata) values (?)""", (db.Binary(self.image_data),))
            sql.commit()
            print("Image saved to database!")
        
        else:
            mb = messagebox.showwarning('Warning', 'No Image File Uploaded')
    def returnimg(self):
        if self.image_data == None:
            with open('settings/default-product.png', 'rb') as f:
                self.image_data = f.read()
            return self.image_data
        else:
            return self.image_data


class ProductTable():
    def __init__(self, product_table):
        self.product_table = product_table
        self.refresh_table(order_by='id DESC')

    def refresh_table(self, order_by):
        for widget in self.product_table.winfo_children():
            widget.destroy()

        cur.execute('SELECT {} FROM products ORDER BY {}'.format(", ".join(column_select), order_by))
        rows = cur.fetchall()

        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                entry = CTkEntry(self.product_table, border_color = 'white', width = 155, fg_color = darkorange, font = (fonttype, 16), text_color = 'white')
                entry.grid(row = i, column = j)
                entry.insert(END, value)
                entry.configure(state='disabled')


class DraggableFrame(CTkFrame):
    def __init__(self, master, **kwargs):
        CTkFrame.__init__(self, master, **kwargs)
        self.bind("<ButtonPress-1>", self.on_drag_start)
        self.bind("<B1-Motion>", self.on_drag_motion)
    
    def on_drag_start(self, event):
        self.start_x = event.x
        self.start_y = event.y
    
    def on_drag_motion(self, event):
        x = self.winfo_x() + event.x - self.start_x
        y = self.winfo_y() + event.y - self.start_y
        self.place(x=x, y=y)


def getimg(img):
    pic = CTkImage(light_image = Image.open(f'settings/{img}.png'), size = (25, 25))
    return pic


def displaypanel():
    if product_on_display == True or addproduct_on_display == True:
        return
    else:
        panel_on_display = True
        def panelclose():
            panelframe.destroy()

        panelframe = CTkFrame(app, width = 150, height = 640, border_width = 1, border_color = darkgray, fg_color = darkerorange, bg_color = darkerorange)
        panelframe.place(x = -3, y = -4)
        panelclosebtn = CTkButton(panelframe, command = panelclose, width = 5, height = 5, corner_radius = 10, text = '', image = getimg('close'), bg_color = darkerorange, fg_color = darkerorange, hover_color = darkorange).place(x = 10, y = 15)
        dashboardbtn = CTkButton(panelframe, command = dashboard, width = 40, height = 5, border_width = 1, border_color = darkgray, corner_radius = 20, hover_color = darkorange, text = 'Dashboard', font = (fonttype, 20), fg_color = 'transparent', bg_color = darkerorange)
        dashboardbtn.place(x = 25, y = 60)

    
def addproduct():
    if panel_on_display == True or product_on_display == True:
        return
    else:
        
                
        addproduct_on_display = True
        def validation(value):
            if value.isdigit() or value == '':
                return True
            else:
                return False
        def cancel():
            newprodframe.destroy()
        upload = ImageUploader(app)
        def submit():
            def success():
                def closeall():
                    newprodframe.destroy()

                itemname.configure(state = 'disabled')
                itemprice.configure(state = 'disabled')
                itemstock.configure(state = 'disabled')
                frame = CTkFrame(newprodframe, width = 200, height = 100, bg_color = darkorange, fg_color = darkorange)
                frame.place(x = 125, y = 93)
                img = CTkLabel(frame, image = getimg('check'), text = '')
                img.place(x = 20, y = 20)
                lbl = CTkLabel(frame, text = 'Added new product!', text_color = 'white', font = (fonttype, 15))
                lbl.place(x = 50, y = 22)
                closebtn = CTkButton(frame, command = closeall, width = 15, border_width = 1, border_color = darkgray, text = 'Close', font = (fonttype, 15), hover_color = darkorange, text_color = 'white', bg_color = darkorange, fg_color = darkerorange)
                closebtn.place(x = 75, y = 60)
            
            name = itemname.get().title()
            price = itemprice.get()
            stock = itemstock.get()
            if name == '' or price == '' or stock == '':
                def closeframe():
                    frame.destroy()
                    itemname.configure(state = 'normal')
                    itemprice.configure(state = 'normal')
                    itemstock.configure(state = 'normal')

                itemname.configure(state = 'disabled')
                itemprice.configure(state = 'disabled')
                itemstock.configure(state = 'disabled')
                frame = CTkFrame(newprodframe, width = 200, height = 100, bg_color = darkorange, fg_color = darkorange)
                frame.place(x = 125, y = 93)
                img = CTkLabel(frame, image = getimg('close'), text = '')
                img.place(x = 20, y = 20)
                lbl = CTkLabel(frame, text = 'Missing input/s!', text_color = 'white', font = (fonttype, 15))
                lbl.place(x = 50, y = 22)
                closebtn = CTkButton(frame, command = closeframe, width = 15, border_width = 1, border_color = darkgray, text = 'Close', font = (fonttype, 15), hover_color = darkorange, text_color = 'white', bg_color = darkorange, fg_color = darkerorange)
                closebtn.place(x = 75, y = 60)
            else:
                img = upload.returnimg()
                current_date = dt.now().strftime('%m-%d-%y | %I:%M %p')
                cur.execute("""INSERT INTO products (name, price, stock, imgdata, dateadded) VALUES (?, ?, ?, ?, ?)""", (name, price, stock, db.Binary(img), current_date))
                sql.commit()
                success()
            
        valid = app.register(validation)

        cur.execute('''select max(id) from products''')
        last_id = cur.fetchone()[0]
        if last_id == None:
            last_id = 1
        else:
            last_id += 1
        newprodframe = CTkFrame(app, width = 450, height = 330, fg_color = darkerorange, bg_color = darkgray, corner_radius = 10)
        newprodframe.place(x = 280, y = 150)
        lbl = CTkLabel(newprodframe, text = 'New Product', font = (fonttype, 25), text_color = 'white', bg_color = darkerorange, fg_color = darkerorange).place(x = 160, y = 5)
        submitbtn = CTkButton(newprodframe, command = submit, width = 15, border_width = 1, border_color = darkgray, text = 'Submit', font = (fonttype, 20), hover_color = darkorange, text_color = 'white', bg_color = darkerorange, fg_color = darkerorange).place(x = 150, y = 280)
        cancelbtn = CTkButton(newprodframe, command = cancel, width = 15, border_width = 1, border_color = darkgray, text = 'Cancel', font = (fonttype, 20), hover_color = darkorange, text_color = 'white', bg_color = darkerorange, fg_color = darkerorange).place(x = 230, y = 280)
        itemname = CTkEntry(newprodframe, width = 330, height = 35, corner_radius = 5, font = (fonttype, 15), border_color = darkorange, fg_color = darkgray, text_color = 'white')
        itemname.place(x = 85, y = 50)
        namelbl = CTkLabel(newprodframe, text = 'Name:', fg_color = darkerorange, bg_color = darkerorange, text_color = 'white', font = (fonttype, 20)).place(x = 20, y = 50)
        itemprice = CTkEntry(newprodframe, width = 330, height = 35, validate = 'key', validatecommand = (valid, '%P'), corner_radius = 5, font = (fonttype, 15), border_color = darkorange, fg_color = darkgray, text_color = 'white')
        itemprice.place(x = 85, y = 100)
        namelbl = CTkLabel(newprodframe, text = 'Price:', fg_color = darkerorange, bg_color = darkerorange, text_color = 'white', font = (fonttype, 20)).place(x = 20, y = 100)
        itemstock = CTkEntry(newprodframe, width = 330, height = 35, validate = 'key', validatecommand = (valid, '%P'), corner_radius = 5, font = (fonttype, 15), border_color = darkorange, fg_color = darkgray, text_color = 'white')
        itemstock.place(x = 85, y = 150)
        namelbl = CTkLabel(newprodframe, text = 'Stock:', fg_color = darkerorange, bg_color = darkerorange, text_color = 'white', font = (fonttype, 20)).place(x = 20, y = 150)
        productidlbl = CTkLabel(newprodframe, text = f'Product ID: {last_id}', font = (fonttype, 20), text_color = 'white', bg_color = darkerorange, fg_color = darkerorange).place(x = 170, y = 200)
        productimage = CTkButton(newprodframe, text = 'Upload Image', command = upload.upload_image, font = (fonttype, 20), bg_color = darkerorange, fg_color = 'transparent', hover_color = orange, border_width = 1, border_color = darkorange).place(x = 160, y = 230)


def searchitem():
    if panel_on_display == True or addproduct_on_display == True:
        return
    else:
        if searchbar.get().title() == "":
            def close():
                missing.destroy()
            missing = CTkFrame(app, width = 250, height = 100, bg_color = darkgray, fg_color = darkorange)
            missing.place(x = 400, y = 200)
            lbl = CTkLabel(missing, text = 'Search bar is empty!', font = (fonttype, 20), text_color = 'white', bg_color = darkorange, fg_color = darkorange).place(x = 50, y = 25)
            img = CTkLabel(missing, text = '', image = getimg('close'), bg_color = darkorange, fg_color = darkorange).place(x = 20, y = 25)
            close = CTkButton(missing, command = close, width = 10, height = 10, text = 'Close', text_color = 'red', font = (fonttype, 20), bg_color = darkorange, fg_color = darkerorange, hover_color = orange).place(x = 95, y = 60)
        else:
            product_on_display = True
            def close():
                displayproduct.destroy()

            displayproduct = DraggableFrame(app, width = 720, height = 290, bg_color = darkgray, fg_color = darkorange)
            displayproduct.place(x = 100, y = 90)
            cur.execute('''select * from products where name = ?''', (searchbar.get().title(),))
            i = []
            for x in cur.fetchall():
                for z in x:
                    i.append(z)

            img = CTkImage(light_image = Image.open(io.BytesIO(i[4])), size = (130, 130))

            description = CTkFrame(displayproduct, width = 450, height = 240, bg_color = darkorange, fg_color = darkerorange)
            description.place(x = 200, y = 20)
            descriptionlbl = CTkLabel(description, text = "No description | WIP!", font = (fonttype, 15), text_color = 'white', bg_color = darkerorange, fg_color = darkerorange)
            descriptionlbl.place(x = 10, y = 10)

            imgframe = CTkFrame(displayproduct, width = 150, height = 150, bg_color = darkorange, fg_color = darkerorange)
            imgframe.place(x = 20, y = 20)
            imglbl = CTkLabel(imgframe, text = '', image = img ).place(x = 10, y = 10)
            itemname = CTkLabel(displayproduct, text = f'Name: {i[1]}', text_color = 'white', bg_color = darkorange, fg_color = darkorange, font = (fonttype, 20)).place(x = 20, y = 175)
            itemprice = CTkLabel(displayproduct, text = f'Price: {humanfriendly.format_number(i[2])}', text_color = 'white', bg_color = darkorange, fg_color = darkorange, font = (fonttype, 20)).place(x = 20, y = 215)
            itemstock = CTkLabel(displayproduct, text = f'Stock: {humanfriendly.format_number(i[3])}', text_color = 'white', bg_color = darkorange, fg_color = darkorange, font = (fonttype, 20)).place(x = 20, y = 245)
            closebtn = CTkButton(displayproduct, command = close , text = '', image = getimg('close'), bg_color = darkorange, fg_color = 'transparent', width = 30, hover_color = darkerorange).place(x = 675, y = 5)

headerframe = CTkFrame(app, width = 1300, height = 50, bg_color = darkgray, fg_color = darkorange)
headerframe.place(x = -5, y = 0)
#headertitle = CTkLabel(headerframe, text = 'John Anthony Becera', font = (fonttype, 25), bg_color = darkorange, text_color = 'white')
#headertitle.place(x = 20, y = 10)
dotbtn = CTkButton(headerframe, command = displaypanel, width = 25, height = 30, text = '', image = getimg('3lines'), bg_color = darkorange, fg_color = darkorange, hover_color = darkerorange).place(x = 10, y = 10)
addbtn = CTkButton(headerframe, width = 15, height = 20, text = '', image = getimg('add'), bg_color = darkorange, fg_color = darkorange, font = (fonttype, 20), corner_radius = 15, border_width = 0, border_color = darkgray, hover_color = darkerorange, command = addproduct)
addbtn.place(x = 940, y = 9)
searchbar = CTkEntry(headerframe, width = 350, height = 35, corner_radius = 5, font = (fonttype, 15), border_color = darkorange, fg_color = darkgray, placeholder_text = 'Enter product name', placeholder_text_color = 'white', text_color = 'white')
searchbar.place(x = 270, y = 8)
searchbtn = CTkButton(headerframe, command = searchitem, width = 25, height = 30, text = '', image = getimg('loupe'), border_color = darkorange, fg_color = darkorange, corner_radius = 10, hover_color = darkerorange).place(x = 620, y = 9)

col_ignore = ['imgdata', 'dateupdated']
cur.execute('''pragma table_info(products)''')
table_info = cur.fetchall()
column_names = [column[1] for column in table_info]
column_select = [column for column in column_names if column not in col_ignore]

cur.execute('select {} from products'.format(", ".join(column_select)))
row = cur.fetchall()

productlist = row

total_rows = len(productlist)
total_col = len(productlist[0])

def dashboard():
    def close():
        productframe.destroy()

    def update_table_order(option):
        if option == 'Latest to Oldest':
            t.refresh_table(order_by = 'id DESC')
        elif option == 'Oldest to Latest':
            t.refresh_table(order_by = 'id ASC')

    productframe = CTkFrame(app, width = 830, height = 520, bg_color = darkgray, fg_color = darkerorange)
    productframe.place(x = 80, y = 80)
    option_var = StringVar(value = 'Latest to Oldest')
    order_option = CTkOptionMenu(productframe, command = update_table_order, width = 150, height = 30, values = ['Latest to Oldest', 'Oldest to Latest'], variable = option_var, corner_radius = 10, fg_color = darkorange, bg_color = darkerorange, button_color = darkorange, button_hover_color = orange, dropdown_fg_color = darkerorange, dropdown_hover_color = orange, dropdown_text_color = 'white', dropdown_font = (fonttype, 15), font = (fonttype, 20))
    order_option.place(x = 150, y = 5)
    lblframe = CTkFrame(productframe, width = 803, height = 30, fg_color = darkorange, bg_color = darkerorange)
    lblframe.place(x = 15, y = 40)
    idlbl = CTkLabel(lblframe, text = 'Product ID', text_color = 'white', font = (fonttype, 20), width = 0, height = 0, bg_color = darkorange, fg_color = darkorange)
    idlbl.place(x = 40, y = 1)
    namelbl = CTkLabel(lblframe, text = 'Name', text_color = 'white', font = (fonttype, 20), width = 0, height = 0, bg_color = darkorange, fg_color = darkorange)
    namelbl.place(x = 210, y = 1)
    pricelbl = CTkLabel(lblframe, text = 'Price', text_color = 'white', font = (fonttype, 20), width = 0, height = 0, bg_color = darkorange, fg_color = darkorange)
    pricelbl.place(x = 370, y = 1)
    stocklbl = CTkLabel(lblframe, text = 'Stock', text_color = 'white', font = (fonttype, 20), width = 0, height = 0, bg_color = darkorange, fg_color = darkorange)
    stocklbl.place(x = 520, y = 1)
    datelbl = CTkLabel(lblframe, text = 'Date Added', text_color = 'white', font = (fonttype, 20), width = 0, height = 0, bg_color = darkorange, fg_color = darkorange)
    datelbl.place(x = 650, y = 1)
    product_table = CTkScrollableFrame(master = productframe, width = 780, height = 440, bg_color = darkorange, fg_color = darkorange)
    product_table.place(x = 15, y = 60)
    product_table_lbl = CTkLabel(productframe, text = 'Added Products', font = (fonttype, 18), text_color = 'white', bg_color = darkerorange, fg_color = darkerorange).place(x = 15, y = 5)
    closebtn = CTkButton(productframe, command = close , text = '', image = getimg('close'), bg_color = darkerorange, fg_color = 'transparent', width = 30, hover_color = orange).place(x = 780, y = 3)

    t = ProductTable(product_table)
app.mainloop()
sql.close()