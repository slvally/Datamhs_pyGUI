from tkinter import *
import mysql.connector
from PIL import ImageTk, Image
import tkinter as tk
from tkinter import ttk

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="",
  database="db_tp3"
)

dbcursor = mydb.cursor()

root = Tk()
root.title("Praktikum DPBO")


# Fungsi untuk mengambil data
def getMhs():
    global mydb
    global dbcursor

    dbcursor.execute("SELECT * FROM mahasiswa")
    result = dbcursor.fetchall()

    return result


# Window Input Data
def inputs():
    # Hide root window
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Input")
    dframe = LabelFrame(top, text="Input Data Mahasiswa", padx=10, pady=10)
    dframe.pack(padx=10, pady=10)

    # Input 1
    label1 = Label(dframe, text="Nama Mahasiswa").grid(row=0, column=0, sticky="w")
    input_nama = Entry(dframe, width=30)
    input_nama.grid(row=0, column=1, padx=20, pady=10, sticky="w")

    # Input 2
    label2 = Label(dframe, text="NIM").grid(row=1, column=0, sticky="w")
    input_nim = Entry(dframe, width=30)
    input_nim.grid(row=1, column=1, padx=20, pady=10, sticky="w")

    # Input 3
    options = ["Filsafat Meme", "Sastra Mesin", "Teknik Kedokteran", "Pendidikan Gaming"]
    input_jurusan = StringVar(root)
    input_jurusan.set(options[0])
    label4 = Label(dframe, text="Jurusan").grid(row=2, column=0, sticky="w")
    input4 = OptionMenu(dframe, input_jurusan, *options)
    input4.grid(row=2, column=1, padx=20, pady=10, sticky='w')

    # Input 4
    i = 0
    label5 = Label(dframe, text="Jenis Kelamin").grid(row=3, column=0, sticky="w")
    
    gender = [("Laki-Laki", "Laki-Laki"), ("Perempuan", "Perempuan")]
    jkel = StringVar();
    jkel.set("Laki-Laki")
    for text, kell, in gender:
        input5 = Radiobutton(dframe, value=kell, text=text, variable=kell).grid(row=3+i, column=1, padx=20, pady=10, sticky='w')
        i=i+1

    #input 5
    hobi = ["Menulis", "Membaca", "Bermain", "Tidur", "Makan", "Uji Nyali", "Ketempelan"]
    label6= Label(dframe, text="Hobi").grid(row=6, column=0, sticky='w')
    hobbies = ttk.Combobox(dframe, value=hobi)
    hobbies.grid(row=6, column=1, padx=20, pady=10, sticky='w')
    hobbies.current(0)

    # Button Frame
    frame2 = LabelFrame(dframe, borderwidth=0)
    frame2.grid(columnspan=2, column=0, row=10, pady=10)

    # Submit Button
    btn_submit = Button(frame2, text="Submit Data", anchor="s", command=lambda:[insertData(top, input_nama, input_nim, input_jurusan, jkel, hobbies), top.withdraw()])
    btn_submit.grid(row=3, column=0, padx=10)

    # Cancel Button
    btn_cancel = Button(frame2, text="Teu jadi / Uih deui", anchor="s", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=3, column=1, padx=10)

# Untuk memasukan data
def insertData(parent, nama, nim, jurusan, jenisKelamin, hobi):
    top = Toplevel()
    # Get data
    nama = nama.get()
    nim = nim.get()
    jurusan = jurusan.get()
    jenisKelamin = jenisKelamin.get()
    hobi = hobi.get()

    #cek inputan terisi atau belum
    if nama == "" or nim == "" or jurusan == "" or jenisKelamin == "" or hobi == "" :
        btn_ok = Button(top, text="Terdapat data yang masih kosong, data tidak boleh kosong!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)

    # Input data disini
    else:
        myCursor = mydb.cursor()                #https://www.w3schools.com/python/python_mysql_insert.asp
        #query sql
        sql = "INSERT INTO mahasiswa (nim, nama, jurusan, JenisKelamin, Hobi) VALUES (%s, %s, %s, %s, %s)"
        #values yang dimasukkan
        val = (nim, nama, jurusan, jenisKelamin, hobi)
        #execute query
        myCursor.execute(sql, val)
        mydb.commit()
        print(myCursor.rowcount, "Berhasil menambahkan data")
        btn_ok = Button(top, text="Siiaappp!", anchor="s", command=lambda:[top.destroy(), parent.deiconify()])
        btn_ok.pack(padx=10, pady=10)
  
# Window Semua Mahasiswa
def viewAll():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Semua Mahasiswa")
    frame = LabelFrame(top, borderwidth=0)
    frame.pack()
    # Cancel Button
    btn_cancel = Button(frame, text="Kembali", anchor="w", command=lambda:[top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=0, padx=10, pady=10, sticky="w")
    # Head title
    head = Label(frame, text="Data Mahasiswa")
    head.grid(row=0, column=1, padx=10, pady=10, sticky="w")

    tableFrame = LabelFrame(frame)
    tableFrame.grid(row=1, column = 0, columnspan=2)

    # Get All Data
    result = getMhs()

    # Title
    title1 = Label(tableFrame, text="No.", borderwidth=1, relief="solid", width=3, padx=5).grid(row=0, column=0)
    title2 = Label(tableFrame, text="NIM", borderwidth=1, relief="solid", width=15, padx=5).grid(row=0, column=1)
    title3 = Label(tableFrame, text="Nama", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=2)
    title4 = Label(tableFrame, text="Jurusan", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=3)
    title5 = Label(tableFrame, text="Jenis Kelamin", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=4)
    title6 = Label(tableFrame, text="Hobi", borderwidth=1, relief="solid", width=20, padx=5).grid(row=0, column=5)

    # Print content
    i = 0
    for data in result:
        label1 = Label(tableFrame, text=str(i+1), borderwidth=1, relief="solid", height=2, width=3, padx=5).grid(row=i+1, column=0)
        label2 = Label(tableFrame, text=data[1], borderwidth=1, relief="solid", height=2, width=15, padx=5).grid(row=i+1, column=1)
        label3 = Label(tableFrame, text=data[2], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=2)
        label4 = Label(tableFrame, text=data[3], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=3)
        label5 = Label(tableFrame, text=data[4], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=4)
        label6 = Label(tableFrame, text=data[5], borderwidth=1, relief="solid", height=2, width=20, padx=5).grid(row=i+1, column=5)
        i += 1

# Dialog konfirmasi hapus semua data
def clearAll():
    top = Toplevel()
    lbl = Label(top, text="Apakah anda yakin untuk menghapus semua data?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes

    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), delAll()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Gajadi deh", bg="red", fg="white", command=top.destroy)
    btn_no.grid(row=0, column=1, padx=10)

# Dialog konfirmasi keluar GUI
def exitDialog():
    global root
    root.withdraw()
    top = Toplevel()
    lbl = Label(top, text="Yakin mau keluar?")
    lbl.pack(padx=20, pady=20)
    btnframe = LabelFrame(top, borderwidth=0)
    btnframe.pack(padx=20, pady=20)
    # Yes
    btn_yes = Button(btnframe, text="Gass", bg="green", fg="white", command=lambda:[top.destroy(), root.destroy()])
    btn_yes.grid(row=0, column=0, padx=10)
    # No
    btn_no = Button(btnframe, text="Gajadi deh", bg="red", fg="white", command=lambda:[top.destroy(), root.deiconify()])
    btn_no.grid(row=0, column=1, padx=10)

#menghapus semua data
def delAll():
    top = Toplevel()
    # Delete data disini
    query = "DELETE from mahasiswa"
    #execute query
    dbcursor.execute(query)
    mydb.commit()
    btn_ok = Button(top, text="Zeeb", command=top.destroy)
    btn_ok.pack(pady=20)

def fasilitas():
    global root
    root.withdraw()

    top = Toplevel()
    top.title("Fasilitas Kampus")
    dframe = LabelFrame(top, text="Fasilitas Kampus", padx=20, pady=20)
    dframe.pack(padx=10, pady=10)

    img1 = ImageTk.PhotoImage(Image.open('img/class.jpg'))
    img2 = ImageTk.PhotoImage(Image.open('img/library.jpg'))
    img3 = ImageTk.PhotoImage(Image.open('img/artroom.jpg'))
    img4 = ImageTk.PhotoImage(Image.open('img/gamingroom.jpg'))
    image_list = [img1, img2, img3, img4]
    idx = 0

    # image label
    imageLabel = Label(dframe, image=img1)
    imageLabel.image = img1
    imageLabel.grid(row=0, column=0)


    # Frame btn
    buttonFrame = LabelFrame(dframe, text="", borderwidth=0)
    buttonFrame.grid(row=2, column=0, pady=10)

    # Prev btn
    btn_prev = Button(buttonFrame, text="<<", anchor="s", command=lambda: [imgPrev(idx-1, image_list, dframe, buttonFrame, btn_prev, btn_next)], state=DISABLED)
    btn_prev.grid(row=0, column=0)

    # Cancel btn
    btn_cancel = Button(buttonFrame, text="Back", anchor="s", command=lambda: [top.destroy(), root.deiconify()])
    btn_cancel.grid(row=0, column=1, padx=20)

    # next btn
    if len(image_list) == 1 :
        btn_next = Button(buttonFrame, text=">>", anchor="s", command=lambda: imgNext(idx,  image_list,  dframe, buttonFrame, btn_prev, btn_next), state=DISABLED)
    else :
        btn_next = Button(buttonFrame, text=">>", anchor="s", command=lambda: imgNext(idx+1,  image_list,  dframe, buttonFrame, btn_prev, btn_next))
    btn_next.grid(row=0, column=2)

def imgPrev(idx, image_list,  dframe, buttonFrame, btn_prev, btn_next):
    imageLabel.grid_forget()
    btn_prev.grid_forget()
    btn_next.grid_forget()

    imageLabel = Label(dframe, image=image_list[idx])
    imageLabel.image = image_list[idx]
    btn_next = Button(buttonFrame, text=">>", command=lambda: imgNext(idx+1,  image_list,  dframe, buttonFrame, btn_prev, btn_next))

    if idx == 0:
        btn_prev = Button(buttonFrame, text="<<", command=lambda: imgPrev(idx-1,  image_list,  dframe, buttonFrame, btn_prev, btn_next), state=DISABLED)
    else :
        btn_prev = Button(buttonFrame, text="<<", command=lambda: imgPrev(idx-1,  image_list,  dframe, buttonFrame, btn_prev, btn_next))

    imageLabel.grid(row=1, column=0)
    btn_prev.grid(row=0, column=0)
    btn_next.grid(row=0, column=2)

def imgNext(idx,  image_list,  dframe, buttonFrame, btn_prev, btn_next):
    imageLabel.grid_forget()
    btn_prev.grid_forget()
    btn_next.grid_forget()

    imageLabel = Label(dframe, image=image_list[idx])
    imageLabel.image = image_list[idx]
    btn_prev = Button(buttonFrame, text="<<", command=lambda: imgPrev(idx-1,  image_list,  dframe, buttonFrame, btn_prev, btn_next))

    if idx == len(image_list)-1:
        btn_next = Button(buttonFrame, text=">>", command=lambda: imgNext(idx+1,  image_list,  dframe, buttonFrame, btn_prev, btn_next), state=DISABLED)
    else :
        btn_next = Button(buttonFrame, text=">>", command=lambda: imgNext(idx+1,  image_list,  dframe, buttonFrame, btn_prev, btn_next))

    imageLabel.grid(row=1, column=0)
    btn_prev.grid(row=0, column=0)
    btn_next.grid(row=0, column=2)


# Title Frame
frame = LabelFrame(root, text="Praktikum DPBO", padx=10, pady=10)
frame.pack(padx=10, pady=10)

# ButtonGroup Frame
buttonGroup = LabelFrame(root, padx=10, pady=10)
buttonGroup.pack(padx=10, pady=10)

# Title
label1 = Label(frame, text="Data Mahasiswa", font=(30))
label1.pack()

# Description
label2 = Label(frame, text="Ini database mahasiswa (ceritanya ygy)")
label2.pack()

# Input btn
b_add = Button(buttonGroup, text="Input Data Mahasiswa", command=inputs, width=30)
b_add.grid(row=0, column=0, pady=5)

# All data btn
b_add = Button(buttonGroup, text="Tampilkan Data Mahasiswa", command=viewAll, width=30)
b_add.grid(row=1, column=0, pady=5)

# Clear all btn
b_clear = Button(buttonGroup, text="Hapus Semua Data Mahasiswa", command=clearAll, width=30)
b_clear.grid(row=2, column=0, pady=5)

# fasilitas btn
b_fasilitas = Button(buttonGroup, text="Fasilitas Kampus", command=fasilitas, width=30)
b_fasilitas.grid(row=3, column=0, pady=5)

# Exit btn
b_exit = Button(buttonGroup, text="Exit", command=exitDialog, width=30)
b_exit.grid(row=4, column=0, pady=5)

root.mainloop()