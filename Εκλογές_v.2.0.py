from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
from fpdf import FPDF
from pypdf import PdfReader, PdfWriter 
import time
import datetime
import locale
import os
import sys
import shutil
from reportlab.pdfgen import canvas 
from reportlab.pdfbase.ttfonts import TTFont 
from tkinter import filedialog

#color_list
colors = ['#66a3ff', '#0047b3', '#ffffff']

#image_list
images = ['greek_flag.ico', 'greek_flag.png', 'serafina.jpg', 'ballot_box.png', 'qr_code.png']

#save_path_initialization
path = ''

#election_type
election_type = ''

#election_year
year = ''

def create_files():
    '''
        Δημιουργία .pdf αρχείων, εφόσον έχουν δοθεί σωστές επιλογές από τον χρήστη.        
    '''
    #print(create_files.__doc__)
    
    global start_venue2
    global start_venue4
    global year_label2
    global choice2
    global destination
    #βοηθητική μεταβλητή που επιτρέπει - ή όχι - τη δημιουργία αρχείων.
    create = True
    global start
    
    #επιλογές χρήστη
    start = start_venue2.get()
    end = start_venue4.get()
    election_type = choice2.get()
    year_time = year_label2.get()

    #αμυντικός προγ/μός
    try:
        election_type = int(election_type)
    except :
        messagebox.showerror('Σφάλμα:', 'Ο τύπος εκλογών πρέπει να είναι ακέραιος θετικός (1, 2, ή 3).')
        create = False
    else:
        if election_type == '' or float(election_type) < 0 or election_type not in [1, 2, 3]:
            messagebox.showerror('Σφάλμα:', 'Ο τύπος εκλογών πρέπει να είναι ακέραιος θετικός (1, 2, ή 3).')
            create = False
    try:
        start == int(start)        
    except:
        messagebox.showerror('Σφάλμα:', 'Ο αριθμός ΕΤ (από:) πρέπει να είναι ακέραιος θετικός.')
        create = False
    else:
        if float(start) < 0 :
            messagebox.showerror('Σφάλμα:', 'Ο αριθμός ΕΤ (από:) πρέπει να είναι ακέραιος θετικός.')
            create = False
    try:        
        end == int(end)        
    except:
        messagebox.showerror('Σφάλμα:', 'Ο αριθμός ΕΤ (έως:) πρέπει να είναι ακέραιος θετικός (και μεγαλύτερος από τον ΕΤ (από:).')
        create = False
    else:
        if float(end) - float(start) < 0:
            messagebox.showerror('Σφάλμα:', 'Ο αριθμός ΕΤ (έως:) πρέπει να είναι ακέραιος θετικός (και μεγαλύτερος από τον ΕΤ (από:).')
            create = False
    try:
        year_time = int(year_time) 
    except:
        messagebox.showerror('Σφάλμα:', 'Το έτος διεξαγωγής των εκλογών πρέπει να είναι ακέραιος θετικός.')
        create = False
    else:
        if float(year_time) < 0:
            messagebox.showerror('Σφάλμα:', 'Το έτος διεξαγωγής των εκλογών πρέπει να είναι ακέραιος θετικός.')
            create = False

    #επιτυχής είσοδος στοιχείων από τον χρήστη (δημιουργία αρχείων .pdf)
    if create:
        #match case
        match (str(election_type)):
            case '1':
                election = 'ΕΘΝΙΚΕΣ ΕΚΛΟΓΕΣ '
            case '2':
                election = 'ΕΥΡΩΕΚΛΟΓΕΣ '
            case _:
                election = 'ΔΗΜΟΤΙΚΕΣ ΕΚΛΟΓΕΣ '
            
        for i in range(int(start), int(end) + 1):
          
            # αρχικοποίηση μεταβλητών
            fileName = str(i) + '.pdf'
            documentTitle = election + str(year_time) + ' - ΕΚΛΟΓΙΚΟ ΤΜΗΜΑ: ' + str(i)
            title = election + str(year_time)
            subTitle = 'ΔΗΜΟΣ ΝΙΚΑΙΑΣ - ΑΓ. Ι. ΡΕΝΤΗ, ΕΚΛΟΓΙΚΟ ΤΜΗΜΑ: ' + str(i)
            
            # δημιουργία pdf object 
            pdf = canvas.Canvas(fileName) 
              
            # τίτλος εγγράφου
            pdf.setTitle(documentTitle) 
                   
            # font style τίτλου και τοποθέτησή του στον canvas 
            pdf.setFont("Helvetica", 18) 
            pdf.drawCentredString(300, 770, title) 
              
            # font style υποτίτλου και τοποθέτησή του στον canvas 
            pdf.setFont("Helvetica", 12) 
            pdf.drawCentredString(290, 720, subTitle) 
              
            # αποθήκευση του pdf 
            pdf.save()

            #μεταφορά αρχείου (filename) στην επιλεγμένο από τον χρήστη διαδρομή (destination)
            shutil.move(fileName, destination)

        #μήνυμα επιτυχίας
        messagebox.showinfo('Ενημέρωση:', 'Η δημιουργία των .pdf αρχείων ήταν επιτυχής.')

#Συναρτήσεις
def back_to_start():
    '''
        Επιστροφή στην αρή της εφαρμογής.
    '''
    #print(back_to_start.__doc__)
    
    global InfoFrame
    InfoFrame.grid_forget()
    main()
        
def display_info():
    '''
        Πληροφορίες εφαρμογής, στοιχεια επικοινωνίας.
    '''
    #print(display_info.__doc__)
    
    global MainFrame
    MainFrame.grid_forget()
    global InfoFrame    
    InfoFrame.grid(row = 5, column = 0, columnspan = 20, sticky =  N + S + E + W, pady = 50)

    #φωτογραφία μου
    serafina_label.grid(row = 10, column = 0, padx = 5, pady = 0)

    #πληροφορίες εφαρμογής
    name1 = Label(InfoFrame, text = "This app is powered by Python v.3.12.2\n\nProgrammed, designed and developed by Serafina Panagiotaki.", justify = CENTER, bg = colors[0], fg = colors[2])
    name1.grid(row = 10, column = 2, columnspan = 3, padx = 24)

    #στοιχεία επικοινωνίας
    name2 = Label(InfoFrame, text = "Contact Info:\nemail: sherypanagiotaki@yahoo.com\ntel.: (+30) 6976929404", justify = LEFT, bg = colors[0], fg = colors[2])
    name2.grid(row = 15, column = 0, columnspan = 3, padx = 5, sticky = W)

    #qr_code
    qr_code_label.grid(row = 10, column = 8, padx = 5, pady = 0)
    qr_text = Label(InfoFrame, text = "Scan my CV", justify = CENTER, bg = colors[0], fg = colors[2])
    qr_text.grid(row = 15, column = 8, padx = 5, sticky = N)

    #κουμπιά (επιστροφή, τερματισμός)
    back = Button(InfoFrame, text = 'Επιστροφή', command = back_to_start, bg = colors[1], fg = colors[2], width = 12, pady = 6)
    back.grid(row = 20, column = 2, sticky = E)
    #στο exitbtn πέρασα ως όρισμα το <Esc>, διότι η εφαρμογή τερματίζει ΚΑΙ με πλήκτρο (η έξοδος ελέγχεται από συνάρτηση που παίρνει όρισμα)
    exitbtn = Button(InfoFrame, text = 'Τερματισμός', command = lambda: terminate('<Escape>'), bg = colors[1], fg = colors[2], width = 12, pady = 6)
    exitbtn.grid(row = 20, column = 4, sticky = W, pady = 60)
                 
    
def terminate(event):
    '''
        Τερματισμός του προγράμματος.
        Απαιτεί επιβεβαίωση από τον χρήστη και στην συνέχεια
        τερματίζει με φιλικό μήνυμα.
    '''
    #print(terminate.__doc__)
    
    verification = messagebox.askquestion('Τερματισμός προγράμματος', 'Θέλετε να τερματίσετε το πρόγραμμα;')        
    if verification == 'yes':
        messagebox.showinfo('τερματισμός προγράμματος', "Ευχαριστούμε που χρησιμοποιήσατε την εφραρμογή.\n\n Programmed, designed and developed \nby Serafina Panagiotaki @Copyright 2024")        
        start_window.destroy()
    else:
        InfoFrame.grid_forget()
        main()

def path_info():
    '''
        Επιλογή της διαδρομής (path) από τον χρήστη όπου θα αποθηκευτούν τα αρχεία.
        Αν δεν υπάρχει ο φάκελος, τότεο δημιουργεί το πρόγραμμα.
    '''
    #print(path_info.__doc__)
    
    global destination
    destination = filedialog.askdirectory(initialdir="\\",title='Επιλέξτε φάκελο προορισμού')
    if not os.path.exists(destination): os.mkdir(destination)

def main():
    '''
        Συνάρτηση main.
        Δημιουργεί το παραθυρικό περιβάλλον και, ανάλογα με τις επιλογές του χρήστη,
        καλεί τις αντίστοιχες συναρτήσεις.
    '''
    #print(main.__doc__)
    
    #τίτλος
    start_window.title('Εκλογές - Δημιουργία αρχείων .pdf για προσομοίωση εκλογών v.2.0')
    
    #εικονίδιο (πάνω αριστερά)    
    start_window.iconbitmap(images[0])

    #παράθυρο   
    start_window.geometry('600x400+550+220')
    start_window.option_add("*Button.cursor", "hand2")  #attribute για όλα τα Buttons, cursor="hand2" 
    start_window.configure(bg=colors[0])    

    global MainFrame
    MainFrame = Frame(start_window, bg = colors[0], highlightthickness = 0)
    MainFrame.grid(row = 5, column = 0, columnspan = 9, sticky =  N + S + E + W)
    picFrame = Frame(MainFrame, bg = colors[0], highlightthickness = 0, padx = 250)    
    picFrame.grid(row = 5, column = 0, columnspan = 9)
    menu = Label(picFrame, text = 'Επιλογές:', font  = ('bold', 14), bg = colors[0], fg = colors[2])
    menu.grid(row = 5, column = 2, padx = 25, pady = 5)

    #εικόνα αρχικής εφαρμογής
    picture = ImageTk.PhotoImage(Image.open(images[3]))
    picture_label = Label(picFrame, image = picture, bg = colors[0])
    picture_label.grid(row = 6, column = 2, pady = 20)
    
    #καντρική οθόνη (options)
    global start_venue2
    global start_venue4
    global year_label2
    global choice2
    national = Label(MainFrame, fg = colors[2], bg = colors[0], text = ' 1. Εθνικές Εκλογές')
    national.grid(row = 15, column = 1, padx = 0, pady = 10)
    euro = Label(MainFrame, fg = colors[2], bg = colors[0], text = '2. Ευρωεκλογές')
    euro.grid(row = 15, column = 2, padx = 5, pady = 5)
    municipal = Label(MainFrame, fg = colors[2], bg = colors[0], text = '3. Δημοτικές εκλογές')
    municipal.grid(row = 15, column = 3, padx = 5, pady = 5)
    choice1 = Label(MainFrame, fg = colors[2], bg = colors[0], text = 'Επιλογή:', padx = 0)
    choice1.grid(row = 15, column = 4, padx = 10, pady = 5, sticky = E)
    choice2 = Entry(MainFrame, fg = colors[2], bg = colors[0], width = 5)
    choice2.grid(row = 15, column = 5, padx = 0, pady = 5, sticky = W)
    SecondFrame = Frame(MainFrame, bg = colors[0], highlightthickness = 0)
    SecondFrame.grid(row = 20, column = 0, columnspan = 9, sticky =  N + S + E + W)
    year_label1 = Label(SecondFrame, fg = colors[2], bg = colors[0], text = 'Έτος:', padx = 10)
    year_label1.grid(row = 20, column = 2, padx = 21, pady = 5, sticky = W)
    year_label2 = Entry(SecondFrame, fg = colors[2], bg = colors[0], width = 8)
    year_label2.grid(row = 20, column = 3, padx = 4, pady = 5, sticky = W)
    start_venue1 = Label(SecondFrame, fg = colors[2], bg = colors[0], text = 'Εκλογικά Τμήματα (από):', padx = 32)
    start_venue1.grid(row = 22, column = 2, padx = 0, pady = 5, sticky = E)
    start_venue2 = Entry(SecondFrame, fg = colors[2], bg = colors[0], width = 8)
    start_venue2.grid(row = 22, column = 3, padx = 5, pady = 5, sticky = W)
    start_venue3 = Label(SecondFrame, fg = colors[2], bg = colors[0], text = '\t(έως):')
    start_venue3.grid(row = 22, column = 4, padx = 0, pady = 10, sticky = E)
    start_venue4 = Entry(SecondFrame, fg = colors[2], bg = colors[0], width = 8)
    start_venue4.grid(row = 22, column = 5, padx = 5, pady = 5, sticky = W)

    
    #κουμπιά (browse, create .pdf, contact)
    PathButton = Button (MainFrame, text = "Browse...", bg = colors[1], fg = colors[2], width = 12, pady = 6, command = path_info)
    PathButton.grid(row = 25, column = 2, pady = 25, padx = 10)
    createButton= Button (MainFrame, text = "Create .pdf", bg = colors[1], fg = colors[2], width = 12, pady = 6, command = create_files)
    createButton.grid(row = 25, column = 3, pady = 10, padx = 10)
    InfoButton = Button (MainFrame, text = "Contact", bg = colors[1], fg = colors[2], width = 12, pady = 6, command = display_info)
    InfoButton.grid(row = 25, column = 4, pady = 10, padx = 10)

    #εικονίδιο ελληνικής σημαίας
    global greek_label
    global greek_img
    greek_img = ImageTk.PhotoImage(Image.open(images[1]))
    
    #εικόνα δική μου
    global serafina_label    
    global InfoFrame
    InfoFrame = Frame(start_window, bg = colors[0], highlightthickness = 0)
    serafina_img = ImageTk.PhotoImage(Image.open(images[2]))
    serafina_label = Label(InfoFrame, image = serafina_img, bg = colors[0])
    
    #qr_code
    global qr_code_label
    qr_code_img = ImageTk.PhotoImage(Image.open(images[4]))
    qr_code_label = Label(InfoFrame, image = qr_code_img, bg = colors[0])

    #σύνδεση του <Escape> με τον τερματισμό του προγράμματος
    start_window.bind("<Escape>", terminate)

    start_window.mainloop()
    
#δημιουργία αρχικού παράθυρου για το πρόγραμμα
start_window = Tk()
main()
