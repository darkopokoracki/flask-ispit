class Biciklista:
    __id: int
    __broj_prijave: str
    __pol: str
    __sifra: str
    __prva_etapa: int
    __druga_etapa: int

    def __init__(self, id: int, broj_prijave: str, pol: str, sifra: str, prva_etapa: int, druga_etapa: int) -> None:
        self.__id = id
        self.__broj_prijave = broj_prijave
        self.__pol = pol
        self.__sifra = sifra
        self.__prva_etapa = prva_etapa
        self.__druga_etapa = druga_etapa

    # Geteri
    def get_id(self):
        return self.__id

    def get_broj_prijave(self):
        return self.__broj_prijave

    def get_pol(self):
        return self.__pol

    def get_sifra(self):
        return self.__sifra

    def get_prva_etapa(self):
        return self.__prva_etapa

    def get_druga_etapa(self):
        return self.__druga_etapa

    # Seteri
    def set_id(self, novi_id):
        self.__id = novi_id

    def set_broj_prijave(self, novi_broj_prijave):
        self.__broj_prijave = novi_broj_prijave

    def set_pol(self, novi_pol):
        self.__pol = novi_pol

    def set_sifra(self, nova_sifra):
        self.__sifra = nova_sifra

    def set_prva_etapa(self, nova_prva_etapa):
        self.__prva_etapa = nova_prva_etapa

    def set_druga_etapa(self, nova_druga_etapa):
        self.__druga_etapa = nova_druga_etapa

    
    def izracunaj_ukupno_vreme(self):
        #Treba nam string: hh:mm:ss
        ukupno = self.__prva_etapa + self.__druga_etapa

        hh = '00'
        mm = '00'
        ss = '00'
        
        hh = ukupno // 3600
        hh_ostatak = ukupno % 3600

        mm = hh_ostatak // 60
        mm_ostatak = hh_ostatak % 60

        ss = mm_ostatak // 60
        ss_ostatak = mm_ostatak % 60


        print(f"{hh:02}:{mm:02}:{ss_ostatak:02}")
        return f"{hh:02}:{mm:02}:{ss_ostatak:02}"



    def __str__(self) -> None:
        res = f"Id: {self.__id}\n"
        res += f"Broj prijave: {self.__broj_prijave}\n"
        res += f"Pol: {self.__pol}\n"
        res += f"Sifra: {self.__sifra}\n"
        res += f"Prva etapa: {self.__prva_etapa}\n"
        res += f"Druga etapa: {self.__druga_etapa}\n"

        return res

    
biciklista1 = Biciklista(1, 'S23', 'M', '12345', 200, 300)
biciklista1.izracunaj_ukupno_vreme()
