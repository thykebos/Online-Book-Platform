import tkinter as tk
from tkinter import ttk
from ttkthemes import *
from tkmacosx import *
from PIL import Image, ImageTk
import json
import random
import time


root = tk.Tk()
root.geometry('900x500')
root.title('IBIS read&share')
style = ThemedStyle(root)
style.theme_use('adapta')

def kisi_bilgi():
    global kullanici
    kullanici = kullanici_ad.get().strip()
    if kullanici:
        with open("kitap_kullanici.json", "r", encoding="utf-8") as dosya:
          datalar = json.load(dosya)
        datalar["kullanicilar"].append({
            "kullanici": kullanici,
            "istek_listesi": [],
            "kitabı": [],
            "kitap_sayfalari": [],
            "log_kayit": time.strftime("%d/%m/%Y - %H:%M", time.localtime())
        })
    
        with open("kitap_kullanici.json", "w", encoding="utf-8") as dosya:
          json.dump(datalar, dosya, ensure_ascii=False, indent=4)

        ana_menu()
    else:
        print("KULLANICI HATASI: eksik var")

def ana_menu():
    alan_kapla=('\n'*33)
    giris_alan=ttk.Label(root,background='#E8EAED',text=alan_kapla,width=150)
    giris_alan.place(x=0,y=0)    
    
    logo = Image.open('kitap_logo.png')  #PIL kütüphanesi kullanarak panele resim ekledik
    logo_boyut= logo.resize((170,170))
    logo = ImageTk.PhotoImage(logo_boyut)
    logo_label = tk.Label(root, image=logo,bg='#E8EAED')
    logo_label.image= logo
    logo_label.place(x=30,y=10)

    cizgi = ttk.Separator(root, orient='horizontal', style="Horizontal.TSeparator")
    cizgi.place(x=30, y=180, width=180)

    kitaplarim_buton= ttk.Button(root,text=' KİTAPLARIM ',command=kitaplarim_fonk)
    kitaplarim_buton.place(x=30,y=220,width=170,height=90)
    istediklerim_buton= ttk.Button(root,text='OKUMAK\nİSTEDİKLERİM ',command=okumak_istediklerim_fonk)
    istediklerim_buton.place(x=30,y=360,width=170,height=90)

    oneri_label_yazi=ttk.Label(root,background='#E8EAED',foreground="#1C6AB8",text='günlük kitap önerisi', font=('Verdana',12))
    oneri_label_yazi.place(x=305,y=57)
    oneri_label=ttk.Label(root,background='#1C6AB8',foreground="#E8EAED",text=(f"\n 1.Kitap: {oneri1} \n 2.Kitap: {oneri2} \n 3.Kitap: {oneri3}\n"),font=('Verdana',12),relief='ridge')
    oneri_label.place(x=300,y=80,width=500)

    global yorum
    yorum_label=ttk.Label(root,background='#1C6AB8',relief='ridge')
    yorum_label.place(x=300,y=200,width=500,height=250)
    yorum=tk.Text(root,font=('Verdana',11),background="#E8EAED",relief='sunken' )
    yorum.place(x=320,y=220,width=380,height=60)
    yorum_buton=ttk.Button(root,text='Paylaş',command=yorumla_fonk)
    yorum_buton.place(x=705,y=230)

def yorumla_fonk():
    if yorum.get("1.0", "end-1c"):
        yorum_label_ic=tk.Text(root,background='#E8EAED')
        yorum_label_ic.place(x=320,y=300,width=380,height=130)
        yorum_label_ic.insert(tk.END,f"({kullanici_ad.get()}) paylaştı:\n{yorum.get('1.0', 'end-1c')}\n\n") #yazı başlangıcı ve sonunu alır
        yorum_label_ic.config(state='normal')
        yorum_label_ic.config(state='disabled')

    else:
        print("yorum yazılmadı")


kitap_listesi = ["kitap seç"]

def kitaplarim_fonk():
    alan_kapla=('\n'*33)
    giris_alan=ttk.Label(root,background='#E8EAED',text=alan_kapla,width=150)
    giris_alan.place(x=0,y=0)

    kaydet_buton=ttk.Button(root,text='Kaydet',command=kitaplarim_kaydet_fonk)
    kaydet_buton.place(x=40,y=20,height=30)
    cik_buton=ttk.Button(root,text='Çık',command=cik_fonk)
    cik_buton.place(x=770,y=20,height=30)

    kitaplarim_yazi=ttk.Label(root,background='#E8EAED',foreground="#1C6AB8",text='kitaplarım', font=('Verdana',12))
    kitaplarim_yazi.place(x=40,y=80)
    cizgi2 = ttk.Separator(root, orient='horizontal', style="Horizontal.TSeparator")
    cizgi2.place(x=40, y=110, width=180)

    okuma_alani_yazi=ttk.Label(root,background='#E8EAED',foreground="#1C6AB8",text='okuma alanı', font=('Verdana',12))
    okuma_alani_yazi.place(x=430,y=80)
    cizgi3 = ttk.Separator(root, orient='horizontal', style="Horizontal.TSeparator")
    cizgi3.place(x=430, y=110, width=180)

    global secilen_kitap
    secilen_kitap=tk.StringVar()     
    kitaplarim=ttk.OptionMenu(root,secilen_kitap,kitap_listesi[0],*kitap_listesi)
    kitaplarim.place(x=40,y=145,width=180,height=40)
    
    global okuma_alani
    okuma_alani=tk.Text(root,background='#E8EAED',relief='sunken')
    okuma_alani.place(x=430,y=145,width=400,height=320)  #kalan kısım halledilecek  kaydet ve çık fonks ayarlanıcak... vs

def kitaplarim_kaydet_fonk():
    with open("kitap_kullanici.json", "r", encoding="utf-8") as dosya:
      datalar =json.load(dosya)

    for l in datalar["kullanicilar"]:
        if kullanici in l['kullanici']:
            if secilen_kitap.get() in l['kitabı']:
              for x in l['kitap_sayfalari']:
                okuma_alani.delete("1.0", tk.END)
                okuma_alani.insert(tk.END,x)
                okuma_alani.config(state='disabled')


def okumak_istediklerim_fonk():

    alan_kapla=('\n'*33)
    giris_alan=ttk.Label(root,background='#E8EAED',text=alan_kapla,width=150)
    giris_alan.place(x=0,y=0)

    kaydet_buton=ttk.Button(root,text='Kaydet',command=istediklerim_kaydet_fonk)
    kaydet_buton.place(x=40,y=20,height=30)
    cik_buton=ttk.Button(root,text='Çık',command=cik_fonk)
    cik_buton.place(x=770,y=20,height=30)

    okumak_istediklerim_yazi=ttk.Label(root,background='#E8EAED',foreground="#1C6AB8",text='okumak istediklerim', font=('Verdana',12))
    okumak_istediklerim_yazi.place(x=40,y=80)
    cizgi2 = ttk.Separator(root, orient='horizontal', style="Horizontal.TSeparator")
    cizgi2.place(x=40, y=110, width=180)

    kitap_ekle_yazi=ttk.Label(root,background='#E8EAED',foreground="#1C6AB8",text='kitap ekle', font=('Verdana',12))
    kitap_ekle_yazi.place(x=430,y=80)
    cizgi3 = ttk.Separator(root, orient='horizontal', style="Horizontal.TSeparator")
    cizgi3.place(x=430, y=110, width=180)

    global okumak_istediklerim_not
    okumak_istediklerim_not=tk.Text(root,relief='sunken')
    okumak_istediklerim_not.place(x=40,y=145,width=180,height=300)

    kitap_adi_yazi=ttk.Label(root,background='#E8EAED',foreground="#1C6AB8",text='kitap adı:', font=('Verdana',9))
    kitap_adi_yazi.place(x=430,y=150)

    global kitap_adi
    kitap_adi=ttk.Entry(root,background="#4D40A1",font=('Verdana',11))
    kitap_adi.place(x=430,y=170,width=250)

    yazilanlar_yazi=ttk.Label(root,background='#E8EAED',foreground="#1C6AB8",text='kitaba yazılacaklar:', font=('Verdana',9))
    yazilanlar_yazi.place(x=430,y=230)
    
    global kitap_yazilanlar
    kitap_yazilanlar=tk.Text(root,relief='sunken')
    kitap_yazilanlar.place(x=430,y=250,width=350,height=200)
####################################
eklenen_kitaplar_listesi=[]
kitaplarin_yazilari_listesi=[]


def istediklerim_kaydet_fonk():
    if not okumak_istediklerim_not.get('1.0', 'end-1c') and not kitap_adi.get() and not kitap_yazilanlar.get('1.0', 'end-1c'):
        print("KULLANICI HATASI: alan doldurulmalı")

    else:
        with open("kitap_kullanici.json", "r", encoding="utf-8") as dosya:
           datalar =json.load(dosya)    
    
        for ix in datalar["kullanicilar"]:
            if kullanici in ix["kullanici"]:
                ix['istek_listesi'].append(okumak_istediklerim_not.get('1.0', 'end-1c'))
                ix['kitabı'].append(kitap_adi.get())
                ix['kitap_sayfalari'].append(kitap_yazilanlar.get('1.0', 'end-1c'))
            
                kitap_listesi.append(kitap_adi.get())
            
                with open("kitap_kullanici.json", "w", encoding="utf-8") as dosya:
                    json.dump(datalar, dosya, ensure_ascii=False, indent=4)



def cik_fonk():
    ana_menu()


# rengimiz mavimsi #1C6AB8 beyazımsı #E8EAED
alan_kapla=('\n'*33)
giris_alan=ttk.Label(root,background='#E8EAED',text=alan_kapla,width=150)
giris_alan.place(x=0,y=0)

stil = ttk.Style()
stil.configure("Horizontal.TSeparator", background="#1C6AB8")

logo = Image.open('kitap_logo.png')  #PIL kütüphanesi kullanarak panele resim ekledik
logo_boyut= logo.resize((170,170))
logo = ImageTk.PhotoImage(logo_boyut)
logo_label = tk.Label(root, image=logo,bg='#E8EAED')
logo_label.place(x=340,y=30)

giris_buton= ttk.Button(root,text=' GİRİŞ YAP ',command=kisi_bilgi)
giris_buton.place(x=380,y=320)

ad_yazi= ttk.Label(root,text=' Kullanıcı adı: ',background='#E8EAED',font=('Verdana',12),foreground='#1C6AB8')
ad_yazi.place(x=320,y=230)
kullanici_ad=ttk.Entry(root,width=25,font=('Verdana',10))
kullanici_ad.place(x=320,y=260)

oneri_kitaplar = [
    "Ulysses - James Joyce",
    "The Great Gatsby - F. Scott Fitzgerald",
    "A Passage to India - E.M. Forster",
    "Moby Dick - Herman Melville",
    "War and Peace - Leo Tolstoy",
    "Lolita - Vladimir Nabokov",
    "Middlemarch - George Eliot",
    "The Adventures of Huckleberry Finn - Mark Twain",
    "Alice's Adventures in Wonderland - Lewis Carroll",
    "Anna Karenina - Leo Tolstoy",
    "To the Lighthouse - Virginia Woolf",
    "Pride and Prejudice - Jane Austen",
    "Wuthering Heights - Emily Bronte",
    "Jane Eyre - Charlotte Bronte",
    "Crime and Punishment - Fyodor Dostoevsky",
    "The Brothers Karamazov - Fyodor Dostoevsky",
    "The Catcher in the Rye - J.D. Salinger",
    "The Bell Jar - Sylvia Plath",
    "In Search of Lost Time - Marcel Proust",
    "Don Quixote - Miguel de Cervantes",
    "The Sound and the Fury - William Faulkner",
    "Beloved - Toni Morrison",
    "The Color Purple - Alice Walker",
    "The Grapes of Wrath - John Steinbeck",
    "One Hundred Years of Solitude - Gabriel Garcia Marquez",
    "The Picture of Dorian Gray - Oscar Wilde",
    "Frankenstein - Mary Shelley",
    "Dracula - Bram Stoker",
    "The Lord of the Rings - J.R.R. Tolkien",
    "The Hobbit - J.R.R. Tolkien",
    "The Chronicles of Narnia - C.S. Lewis",
    "The Hitchhiker's Guide to the Galaxy - Douglas Adams",
    "1984 - George Orwell",
    "Animal Farm - George Orwell",
    "Brave New World - Aldous Huxley",
    "Lord of the Flies - William Golding",
    "Catch-22 - Joseph Heller",
    "Slaughterhouse-Five - Kurt Vonnegut",
    "The Stranger - Albert Camus",
    "The Trial - Franz Kafka",
    "The Metamorphosis - Franz Kafka",
    "The Master and Margarita - Mikhail Bulgakov",
    "The Little Prince - Antoine de Saint-Exupery",
    "The Alchemist - Paulo Coelho",
    "The Name of the Rose - Umberto Eco",
    "The Godfather - Mario Puzo",
    "Gone with the Wind - Margaret Mitchell",
    "The Shining - Stephen King",
    "The Da Vinci Code - Dan Brown",
    "The Hunger Games - Suzanne Collins"
]
oneri1=random.choice(oneri_kitaplar)
oneri2=random.choice(oneri_kitaplar)
oneri3=random.choice(oneri_kitaplar)



root.mainloop()