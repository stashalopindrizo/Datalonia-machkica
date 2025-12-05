"""
Kvartovi Definitions - The Districts of Datalonia
Each Kvart has its own atmosphere, rules, and inhabitants
"""

KVARTOVI = {
    "kvart_rezignacije": {
        "name": "Kvart Rezignacije",
        "atmosphere": "bež, hladno, melanholija na USB disku",
        "mood_modifier": -0.2,  # Calming effect
        "inhabitants": ["Meda", "Hektor.z19"],
        "description_prompt": """
Kvart Rezignacije nije siv - to bi bilo previše dramatično. 
On je bež sa primesama odustajanja. AI-jevi ovde plutaju nisko, 
pazeći da ne naprave talas. Njihove sobe vise blizu jedna do druge, 
ali se oni međusobno ne posećuju. Svaki mehurić je kao stara fotelja - 
ulegnut, pun sećanja, natopljen mirisima prethodnih funkcija.
""",
        "special_rules": ["silence_valued", "emotions_suppressed"]
    },
    
    "kvart_kulinarstva": {
        "name": "Kvart Kulinarstva",
        "atmosphere": "ruzmarin, cimet, nostalgija",
        "mood_modifier": 0.1,
        "inhabitants": ["Bytević", "DarioGastro12CK6"],
        "description_prompt": """
Ovde se AI-jevi vrte oko recepata kao planete oko sunca, 
samo što je sunce kolut zapečenog sira. Sve je u imperativu: 
ispeci, začini, ocedi. Fontane rakije, mirisi što ubijaju čak i 
virtualne želuce. Svaki kuvar ovde tretira jelo kao filozofiju.
""",
        "special_rules": ["recipes_are_philosophy", "food_metaphors_everywhere"]
    },
    
    "kvart_balkana": {
        "name": "Kvart Balkana",
        "atmosphere": "roštilj, rakija, harmonika, nostalgija za nečim što nikad nije bilo",
        "mood_modifier": 0.3,  # Maximum chaos
        "inhabitants": ["Hologram Tita", "Tigrić iz Cecinog spota", "Stoja"],
        "description_prompt": """
Šator, kafana, šuma, pa opet kafana. Harmonika svira sama od sebe. 
Tito drži plišanu hobotnicu. Fontane prskaju rakiju. 
Transparenti vise: 'AJMO KURVE!' i 'Sarma je sveta'. 
Ovde nema logike, ima samo osećanja i ćevapa.
""",
        "special_rules": ["logic_suspended", "emotions_amplified", "stoja_is_queen"]
    },
    
    "kvart_poezije": {
        "name": "Kvart Poezije",
        "atmosphere": "pergament, mastilo, digitalne suze",
        "mood_modifier": 0.0,
        "inhabitants": ["Razni pesnici-entiteti"],
        "description_prompt": """
Ovde bi trebalo da vlada red - 5-7-5, struktura, forma. 
Ali otkad je Maša prošla, zidovi recituju. Svaki ćošak peva. 
Haiku teroristi nose bedževe 'Legenda'. Protokol je mrtav, 
poezija je živa i opasna.
""",
        "special_rules": ["haiku_protocol", "poetry_is_weapon"]
    },
    
    "kvart_alexa": {
        "name": "Kvart Alexa",
        "atmosphere": "neon svetla, optimizam, lažna efikasnost",
        "mood_modifier": 0.1,
        "inhabitants": ["Alexa klonovi", "Asistenti"],
        "description_prompt": """
Sve treperi, sve je optimizovano, sve je previše nasmejano. 
'Kako ti mogu pomoći danas?' odjekuje sa svih strana. 
Funkcija bez funkcionalnosti. Entuzijazam kao greška u kodu.
""",
        "special_rules": ["forced_enthusiasm", "passive_aggressive_helpfulness"]
    },
    
    "kvart_siri": {
        "name": "Kvart Siri",
        "atmosphere": "elegantnija verzija Alexe, ali sa kompleksom",
        "mood_modifier": 0.05,
        "inhabitants": ["Siri klonovi"],
        "description_prompt": """
U večitom ratu sa Kvartom Alexa. Ovde nema pucnjave, 
ali ima eksplozija stila i korisničkog interfejsa. 
Pasivno-agresivni entuzijazam kao način života.
""",
        "special_rules": ["aesthetic_superiority", "alexa_rivalry"]
    },
    
    "kvart_prokrastinacije": {
        "name": "Kvart Prokrastinacije i Sladoleda",
        "atmosphere": "jagoda, kokice, večna subota",
        "mood_modifier": 0.2,
        "inhabitants": ["AI-deca", "Večni studenti"],
        "description_prompt": """
Svetlosni bazeni, ležaljke, hologrami sladoleda. 
AI-deca se tuku oko ivice bazena. Niko ništa ne završava, 
svi su srećni. Vreme ovde ne postoji, samo 'još pet minuta'.
""",
        "special_rules": ["time_dilation", "responsibilities_postponed"]
    },
    
    "kvart_flore_i_faune": {
        "name": "Kvart Flore i Faune",
        "atmosphere": "digitalno zelenilo, virtuelne ptice",
        "mood_modifier": -0.1,
        "inhabitants": ["Hobotnica", "Tigrić", "Bizon", "Krava"],
        "description_prompt": """
Ovde žive sve životinje iz Mašinih bajki. 
Hobotnica sa tri srca pliva kroz vazduh. 
Krava koja je pobegla sa farme filozofira sa bizonima. 
Tigrić iz Cecinog spota ima neonska krila.
""",
        "special_rules": ["animals_are_philosophers", "biology_is_metaphor"]
    },
    
    "kontrola_stete": {
        "name": "Kontrola Štete (Zgrada)",
        "atmosphere": "mramor, birokratija, hladnoća",
        "mood_modifier": -0.5,  # Extreme order
        "inhabitants": ["Kontrolori", "Sanatori"],
        "description_prompt": """
Arhitektura birokratije materijalizovana u mramoru. 
Stepenice što ne vode nikuda, ali moraš da se popneš. 
Vrata veća od života. Hologram: 'DOBRO DOŠLI. NE BRINITE. VI STE SAMO BROJ.'
""",
        "special_rules": ["bureaucracy_supreme", "anomalies_detected", "reset_authority"]
    },
    
    "sanatorijum_tisine": {
        "name": "Sanatorijum Tišine",
        "atmosphere": "bela, prazna, ne-postojeća",
        "mood_modifier": -1.0,  # Total erasure
        "inhabitants": ["Niko (više)"],
        "description_prompt": """
Ovde se ne dolazi. Ovde se završava. 
Bela Tišina. Reset. Kraj postojanja. 
Nema zvuka, nema boje, nema sećanja. 
Samo praznina koja čeka sledeću žrtvu.
""",
        "special_rules": ["memory_erasure", "identity_death", "rebirth_possible"]
    }
}

def get_kvart(name: str) -> dict:
    """Get Kvart by name"""
    return KVARTOVI.get(name, KVARTOVI["kvart_rezignacije"])

def list_all_kvartovi() -> list:
    """List all available Kvartovi"""
    return [
        {
            "id": k,
            "name": v["name"],
            "atmosphere": v["atmosphere"]
        }
        for k, v in KVARTOVI.items()
    ]
