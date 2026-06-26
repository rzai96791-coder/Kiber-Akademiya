import os
import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window

Window.clearcolor = (0.05, 0.05, 0.1, 1)

def bazani_oxu():
    if not os.path.exists("kiber_baza.txt"):
        return {}
    
    with open("kiber_baza.txt", "r", encoding="utf-8") as f:
        fayl_metni = f.read()
    
    movzular = fayl_metni.split("===MOVZU===")
    baza = {}
    
    for m in movzular:
        if not m.strip():
            continue
        setirler = [s.strip() for s in m.strip().split("\n") if s.strip()]
        if len(setirler) < 2:
            continue
            
        try:
            movzu_id = int(setirler[0])
            movzu_adi = setirler[1]
            
            suallar = []
            ders_hisseleri = []
            
            for setir in setirler[2:]:
                if setir.startswith("Sual"):
                    hisseler = setir.split("|")
                    if len(hisseler) == 5:
                        suallar.append({
                            "sual": hisseler[0],
                            "A": hisseler[1],
                            "B": hisseler[2],
                            "C": hisseler[3],
                            "duz": hisseler[4].strip().upper()
                        })
                else:
                    ders_hisseleri.append(setir)
            
            ders_metni = "\n".join(ders_hisseleri) if ders_hisseleri else "Bu movzu ucun derslik metni tapilmadi."
            
            baza[movzu_id] = {
                "basliq": f"Movzu {movzu_id}: {movzu_adi}",
                "ders": ders_metni,
                "suallar": suallar
            }
        except Exception as e:
            continue
            
    return baza

DATA_BAZA = bazani_oxu()

class GirisSehifesi(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=20)
        
        logo = Label(text="TECH MASTER RZA KIBER AKADEMIYA", font_size='24sp', color=(0, 1, 1, 1), bold=True, halign='center')
        logo.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0], None)))
        layout.add_widget(logo)
        
        tlimat = Label(text="Xahish edirik, adinizi daxil edin.\nBu ad virtual diplomunuzun uzerine yazilacaq:", 
                       font_size='16sp', halign='center', color=(0.8, 0.8, 0.8, 1))
        tlimat.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0], None)))
        layout.add_widget(tlimat)
        
        self.ad_input = TextInput(hint_text="Adiniz ve Soyadiniz", multiline=False, size_hint_y=None, height=50, font_size='18sp')
        layout.add_widget(self.ad_input)
        
        btn_basla = Button(text="Akademiyaya Daxil Ol", background_color=(0, 0.7, 1, 1), font_size='18sp', size_hint_y=None, height=55)
        btn_basla.bind(on_press=self.sisteme_gir)
        layout.add_widget(btn_basla)
        
        self.add_widget(layout)

    def sisteme_gir(self, instance):
        if self.ad_input.text.strip():
            App.get_running_app().istifadeci_adi = self.ad_input.text.strip()
            self.manager.current = 'qarsilama_sehifesi'

class QarsilamaSehifesi(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=40, spacing=25)
        
        basliq = Label(text="KIBER AKADEMIYA REHBERLIYI SALAMLAYIR", font_size='22sp', color=(1, 1, 0, 1), bold=True, halign='center')
        basliq.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0], None)))
        layout.add_widget(basliq)
        
        # Senin istediyin xusus motivasiya metni
        self.mesaj_label = Label(text="", font_size='17sp', halign='center', color=(0, 1, 0.8, 1), bold=True)
        self.mesaj_label.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0], None)))
        layout.add_widget(self.mesaj_label)
        
        btn_ireli = Button(text="Movzulara Kecid Et", background_color=(0, 1, 0.5, 1), font_size='18sp', size_hint_y=None, height=60)
        btn_ireli.bind(on_press=self.ana_sehifeye_git)
        layout.add_widget(btn_ireli)
        
        self.add_widget(layout)
        
    def on_enter(self):
        ad = App.get_running_app().istifadeci_adi
        self.mesaj_label.text = f"RZA ISMAYILOV terefinden hazirlanan Kiber Akademiyaya xosh gelmisiniz, {ad}!\n\n" \
                               f"Kiber-tehlukesizliyi oyrenmek ucun axira kimi gedin ve hedefinizden, " \
                               f"meqsedinizden geri donmeyin! Axirda virtual diplom alacaqsiniz."

    def ana_sehifeye_git(self, instance):
        self.manager.current = 'ana_sehife'

class AnaSehife(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.basliq = Label(text="", font_size='22sp', halign='center', color=(0, 1, 1, 1), size_hint_y=None, height=80)
        self.basliq.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0], None)))
        self.layout.add_widget(self.basliq)
        
        self.scroll = ScrollView()
        self.btn_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=None)
        self.btn_layout.bind(minimum_height=self.btn_layout.setter('height'))
        self.scroll.add_widget(self.btn_layout)
        self.layout.add_widget(self.scroll)
        
        self.btn_diplom = Button(text="DIPLOMU ELDE ET", background_color=(1, 0.84, 0, 1), font_size='18sp', size_hint_y=None, height=60, disabled=True)
        self.btn_diplom.bind(on_press=self.diploma_git)
        self.layout.add_widget(self.btn_diplom)
        
        self.add_widget(self.layout)

    def on_enter(self):
        app = App.get_running_app()
        self.basliq.text = f"Xosh geldiniz, {app.istifadeci_adi}!\nSeviyyenizi secin:"
        self.btn_layout.clear_widgets()
        
        for m_id in sorted(DATA_BAZA.keys()):
            movzu = DATA_BAZA[m_id]
            btn = Button(text="", font_size='15sp', size_hint_y=None, height=60, halign='center', valign='middle')
            btn.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0] - 20, None)))
            btn.bind(on_press=lambda inst, idx=m_id: self.movzunu_ac(idx))
            
            if m_id <= app.acilmis_level + 1:
                btn.text = f"{movzu['basliq']}\n[ACIQ]"
                btn.background_color = (0, 0.5, 0.8, 1)
                btn.disabled = False
            else:
                btn.text = f"{movzu['basliq']}\n[KILIDLI]"
                btn.background_color = (0.3, 0.3, 0.3, 1)
                btn.disabled = True
                
            self.btn_layout.add_widget(btn)

        btn_51 = Button(text="Movzu 51: YEKUN DIPLOM IMTAHANI", font_size='15sp', size_hint_y=None, height=65, halign='center', valign='middle')
        btn_51.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0] - 20, None)))
        btn_51.bind(on_press=self.yekun_imtahani_baslat)
        
        if app.acilmis_level >= len(DATA_BAZA):
            btn_51.text += "\n[ACIQ - RANDOM SUALLAR]"
            btn_51.background_color = (0, 0.7, 0.4, 1)
            btn_51.disabled = False
        else:
            btn_51.text += "\n[KILIDLI - 50 MOVZUNU BITIRIN]"
            btn_51.background_color = (0.3, 0.2, 0.2, 1)
            btn_51.disabled = True
        self.btn_layout.add_widget(btn_51)

        if app.diplom_qazanildi:
            self.btn_diplom.disabled = False

    def movzunu_ac(self, m_id):
        App.get_running_app().secilmis_movzu_id = m_id
        App.get_running_app().is_diplom_mode = False
        self.manager.get_screen('ders_sehifesi').dersi_yenile()
        self.manager.current = 'ders_sehifesi'

    def yekun_imtahani_baslat(self, instance):
        App.get_running_app().is_diplom_mode = True
        self.manager.get_screen('test_sehifesi').testi_hazirla()
        self.manager.current = 'test_sehifesi'

    def diploma_git(self, instance):
        self.manager.current = 'diplom_sehifesi'

class DersSehifesi(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.basliq = Label(text="", font_size='20sp', color=(1, 1, 0, 1), size_hint_y=None, height=50, halign='center')
        self.basliq.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0], None)))
        self.layout.add_widget(self.basliq)
        
        self.scroll = ScrollView()
        self.metn_label = Label(text="", font_size='16sp', halign='left', valign='top', size_hint_y=None)
        self.metn_label.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0], None)))
        self.metn_label.bind(texture_size=self.metn_label.setter('size'))
        self.scroll.add_widget(self.metn_label)
        self.layout.add_widget(self.scroll)
        
        btn_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        btn_geri = Button(text="Geri", background_color=(1, 0.3, 0.3, 1))
        btn_geri.bind(on_press=self.geri)
        btn_layout.add_widget(btn_geri)
        
        btn_test = Button(text="Testi Baslat", background_color=(0, 1, 0.5, 1))
        btn_test.bind(on_press=self.teste_kec)
        btn_layout.add_widget(btn_test)
        
        self.layout.add_widget(btn_layout)
        self.add_widget(self.layout)

    def send_update(self):
        pass

    def dersi_yenile(self):
        m_id = App.get_running_app().secilmis_movzu_id
        target = DATA_BAZA.get(m_id, {"basliq": "Namelum", "ders": "Metn yoxdur."})
        self.basliq.text = target["basliq"]
        self.metn_label.text = target["ders"]

    def text_control(self):
        pass

    def geri(self, instance):
        self.manager.current = 'ana_sehife'

    def teste_kec(self, instance):
        self.manager.get_screen('test_sehifesi').testi_hazirla()
        self.manager.current = 'test_sehifesi'

class TestSehifesi(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        self.sual_label = Label(text="", font_size='18sp', halign='center', size_hint_y=None, height=120)
        self.sual_label.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0], None)))
        self.layout.add_widget(self.sual_label)
        
        self.btnA = Button(text="", font_size='16sp', background_color=(0.2, 0.2, 0.4, 1), halign='center')
        self.btnA.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0]-10, None)))
        self.btnA.bind(on_press=lambda inst: self.cavab_yoxla("A"))
        self.layout.add_widget(self.btnA)
        
        self.btnB = Button(text="", font_size='16sp', background_color=(0.2, 0.2, 0.4, 1), halign='center')
        self.btnB.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0]-10, None)))
        self.btnB.bind(on_press=lambda inst: self.cavab_yoxla("B"))
        self.layout.add_widget(self.btnB)
        
        self.btnC = Button(text="", font_size='16sp', background_color=(0.2, 0.2, 0.4, 1), halign='center')
        self.btnC.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0]-10, None)))
        self.btnC.bind(on_press=lambda inst: self.cavab_yoxla("C"))
        self.layout.add_widget(self.btnC)
        
        self.info_label = Label(text="", font_size='16sp', color=(1, 1, 1, 1), size_hint_y=None, height=40)
        self.layout.add_widget(self.info_label)
        
        self.btn_ana_sehife = Button(text="Ana Sehifeye Qayit", background_color=(1, 0.5, 0, 1), size_hint_y=None, height=50)
        self.btn_ana_sehife.bind(on_press=self.ana_sehifeye_qayit)
        
        self.add_widget(self.layout)

    def testi_hazirla(self):
        app = App.get_running_app()
        self.sual_indeks = 0
        self.xal = 0
        self.btnA.disabled = False
        self.btnB.disabled = False
        self.btnC.disabled = False
        
        if self.btn_ana_sehife in self.layout.children:
            self.layout.remove_widget(self.btn_ana_sehife)
            
        if app.is_diplom_mode:
            butun_suallar = []
            for m_id in DATA_BAZA:
                butun_suallar.extend(DATA_BAZA[m_id]["suallar"])
            random.shuffle(butun_suallar)
            self.suallar = butun_suallar[:50]
        else:
            m_id = app.secilmis_movzu_id
            self.suallar = DATA_BAZA[m_id]["suallar"]
            
        self.suali_goster()

    def suali_goster(self):
        if self.sual_indeks < len(self.suallar):
            hazirki = self.suallar[self.sual_indeks]
            self.sual_label.text = f"Sual {self.sual_indeks + 1}/{len(self.suallar)}:\n\n" + hazirki["sual"]
            self.btnA.text = "A) " + hazirki["A"]
            self.btnB.text = "B) " + hazirki["B"]
            self.btnC.text = "C) " + hazirki["C"]
            self.info_label.text = f"Duzgun Cavab Sayi: {self.xal}"
            self.info_label.color = (1, 1, 1, 1)
        else:
            app = App.get_running_app()
            self.btnA.disabled = True
            self.btnB.disabled = True
            self.btnC.disabled = True
            self.layout.add_widget(self.btn_ana_sehife)
            
            if app.is_diplom_mode:
                if self.xal >= (len(self.suallar) / 2):
                    self.sual_label.text = f"MOHTESHEM! Yekun Imtahandan kecdiniz!\nToplanan duzgun: {self.xal}"
                    app.diplom_qazanildi = True
                else:
                    self.sual_label.text = f"Teessef, diplom imtahandan kesildiniz.\nYeniden cehd edin! (Duzgun: {self.xal})"
            else:
                lazim_olan = len(self.suallar) * 7
                cari_bal = self.xal * 10
                if cari_bal >= lazim_olan:
                    self.sual_label.text = "Tebrik edirik! Bu merheleni ugurla kecdiniz!"
                    if app.secilmis_movzu_id == app.acilmis_level + 1:
                        app.acilmis_level += 1
                else:
                    self.sual_label.text = "Baliniz kecid ucun yeterli olmadi. Yeniden oxuyun!"

    def cavab_yoxla(self, secim):
        duzgun = self.suallar[self.sual_indeks]["duz"]
        if secim == duzgun:
            self.xal += 1
            self.info_label.text = "Dogru cavab!"
            self.info_label.color = (0, 1, 0, 1)
        else:
            self.info_label.text = "Sehv cavab!"
            self.info_label.color = (1, 0, 0, 1)
            
        self.sual_indeks += 1
        self.suali_goster()

    def ana_sehifeye_qayit(self, instance):
        self.manager.current = 'ana_sehife'

class DiplomSehifesi(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical', padding=30, spacing=15)
        cerçive = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        cerçive.add_widget(Label(text="VIRTUAL CERTIFICATE OF COMPLETION", font_size='22sp', color=(1, 0.84, 0, 1), bold=True))
        cerçive.add_widget(Label(text="Bu sened resmi olaraq tesdiq edir ki,", font_size='14sp', color=(1, 1, 1, 1)))
        
        self.ad_label = Label(text="", font_size='24sp', color=(0, 1, 0.8, 1), bold=True)
        cerçive.add_widget(self.ad_label)
        
        tebrik = Label(text="TECH MASTER RZA KIBER AKADEMIYASI\n"
                            "terefinden hazirlanan Kiber-Tehlukesizlik telimini "
                            "mveffeqiyyetle bitirerek 'KIBER TEHLUKESIZLIK MUTEXESSISI' statusuna layiq gorulmusdur.", 
                       font_size='14sp', halign='center', color=(0.9, 0.9, 0.9, 1))
        tebrik.bind(size=lambda inst, val: setattr(inst, 'text_size', (val[0], None)))
        cerçive.add_widget(tebrik)
        
        cerçive.add_widget(Label(text="Bash Direktor: Tech Master Rza\nTarix: 2026", font_size='12sp', color=(0.6, 0.6, 0.6, 1), halign='center'))
        
        layout.add_widget(cerçive)
        
        btn_cixis = Button(text="Ana Sehifeye Don", background_color=(0, 0.5, 0.5, 1), size_hint_y=None, height=50)
        btn_cixis.bind(on_press=lambda inst: setattr(self.manager, 'current', 'ana_sehife'))
        layout.add_widget(btn_cixis)
        
        self.add_widget(layout)

    def on_enter(self):
        self.ad_label.text = App.get_running_app().istifadeci_adi.upper()

class KiberAkademiyaApp(App):
    def build(self):
        self.secilmis_movzu_id = 0
        self.acilmis_level = 0
        self.istifadeci_adi = "Istifadeci"
        self.is_diplom_mode = False
        self.diplom_qazanildi = False
        
        sm = ScreenManager()
        sm.add_widget(GirisSehifesi(name='giris_sehifesi'))
        sm.add_widget(QarsilamaSehifesi(name='qarsilama_sehifesi'))
        sm.add_widget(AnaSehife(name='ana_sehife'))
        sm.add_widget(DersSehifesi(name='ders_sehifesi'))
        sm.add_widget(TestSehifesi(name='test_sehifesi'))
        sm.add_widget(DiplomSehifesi(name='diplom_sehifesi'))
        return sm

if __name__ == '__main__':
    KiberAkademiyaApp().run()
