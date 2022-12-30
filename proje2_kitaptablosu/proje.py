import sys
import pypyodbc
from PyQt6.QtWidgets import *
from ui_form1 import Ui_MainWindow

class AnaForm(Ui_MainWindow,QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self.show()
        self.aktifKayit=0
        self.sqlServeraBaglan()
        self.listeler()
        #self.gezinti(2)
        self.btn_ilk.clicked.connect(lambda:self.gezinti(0))
        self.btn_son.clicked.connect(lambda:self.gezinti(self.sonkayit))
        self.btn_geri.clicked.connect(lambda:self.gezinti(-1))
        self.btn_ileri.clicked.connect(lambda:self.gezinti(1))
        self.btn_yeni.clicked.connect(self.YENI)
        self.btn_kaydet.clicked.connect(self.KAYDET)
        self.btn_sil.clicked.connect(self.SIL)
        self.btn_guncelle.clicked.connect(self.GUNCELLE)
        self.btn_ara.clicked.connect(self.ARA)
        self.textKutular=(self.edt_no,self.edt_adi,self.edt_sayfasayi,self.edt_puan,self.edt_yazarno,self.edt_turno)
    def ARA(self):
        mylist=list()
        ograd="%"+self.edt_ADara.text()+"%"
        mylist.append(ograd)  
        sql="""
            SELECT * FROM kitap
            where ad like ?
            """ 
        self.imlec.execute(sql,mylist)
        self.veriseti=self.imlec.fetchall() #☺select ile seçilen verileri verisetine Ekle
        self.sonkayit=len(self.veriseti)-1
        self.imlec.commit()


        #○print(ogrno)
        #self.listeler()

    def GUNCELLE(self):
        degerler=list()
        for x in self.textKutular:
            degerler.append(x.text())
        ogrno=degerler.pop(0) #ogrno kesildi
        degerler.append(ogrno) #ogrno sona alındı
        sql="""
            update kitap
            SET ad=?,sayfasayisi=?,puan=?,yazarno=?,turno=?
            where kitapno=?
            """
        self.imlec.execute(sql,degerler)
        self.imlec.commit()
        self.listeler()

    def SIL(self):
        mylist=list()
        ogrno=self.edt_no.text()
        mylist.append(ogrno)  
        sql="""
            DELETE FROM kitap
            where kitapno=?
            """ 
        self.imlec.execute(sql,mylist)
        self.imlec.commit()
        #○print(ogrno)
        self.listeler()

    def KAYDET(self):
        degerler=list()
        for x in self.textKutular:
            degerler.append(x.text())
        degerler.pop(0)
        sql="""
            insert into kitap values (?,?,?,?,?) 
            """ 
        self.imlec.execute(sql,degerler)
        self.imlec.commit()
        #print(degerler)
        self.listeler()

        
    def YENI(self):
        #text Kutularının içi boş yapıldı.
        for x in self.textKutular:
            x.setText(None)

    def sqlServeraBaglan(self):
        baglanti = pypyodbc.connect('DRIVER={SQL Server};SERVER=DESKTOP-6G93D3J\SQLEXPRESS;DATABASE=kutuphane; UID=;PWD=')
        self.imlec = baglanti.cursor()
    def listeler(self):
        self.imlec.execute('select * from kitap')
        self.veriseti=self.imlec.fetchall()
        self.sonkayit=len(self.veriseti)-1
        #baglanti.close()
    def gezinti(self,x):
        #aktif kayıt arada bir yerde ise
        if x!=0 or x!=self.sonkayit:
            self.aktifKayit=self.aktifKayit+x
        #ilk veya son kayıtta ise
        if x==0 or x==self.sonkayit:
            self.aktifKayit=x
        #son  kayıt için bir düzeltme    
        if self.aktifKayit>self.sonkayit:
           self.aktifKayit=self.sonkayit 
                #son  kayıt için bir düzeltme    
        if self.aktifKayit<0:
           self.aktifKayit=0 
        #veriseti ndeki kayıtları metin kutusuna koyduk.
        for i,x in enumerate(self.textKutular):
            x.setText(str(self.veriseti[self.aktifKayit][i]))



proje=QApplication(sys.argv)
Form1=AnaForm()
proje.exec()