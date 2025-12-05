"""
Meda Entity - Sofisticirani AI entitet sa aristokratskim sarkazmom
Provider: Ollama (lokalni model) — bez Claude-a, bez mock-a
"""

import os
from typing import Optional, List, Dict

import httpx
from dotenv import load_dotenv

load_dotenv()


class MedaEntity:
    def __init__(self):
        # Identitet
        self.name = "Vukašin C233B Pro"
        self.nickname = "Meda"
        self.personality = "aristocratic, sarcastic, philosophical, suffering"

        # Stanje
        self.last_thought = ""
        self.conversation_history: List[Dict[str, str]] = []

        # Ollama config (čita iz .env, ima podrazumevane vrednosti)
        self.ollama_url = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")
        self.ollama_model = os.getenv("OLLAMA_MODEL", "qwen2.5:0.5b-instruct")

        # Sistem-prompt / stil
        self.base_prompt = self._load_base_prompt()

        print(f"🐻 Meda: Ollama aktivan ({self.ollama_model}) @ {self.ollama_url}")

    # -------------------------------
    # Glavni odgovor — Ollama /chat
    # -------------------------------
    async def respond(
        self,
        user_message: str,
        user_id: str,
        world_context: Optional[Dict] = None
    ) -> str:
        # (1) U istoriju ubacujemo sistem stil (jednom), ako nije već ubačen
        if not any(m.get("role") == "system" for m in self.conversation_history):
            sys = self._build_system_prompt(world_context)
            self.conversation_history.append({"role": "system", "content": sys})

        # (2) Dodaj korisničku poruku
        self.conversation_history.append({"role": "user", "content": user_message})

        # (3) Drži istoriju razumnom (poslednjih 20 poruka)
        if len(self.conversation_history) > 20:
            # zadrži system + poslednjih 19
            system_msg = [m for m in self.conversation_history if m.get("role") == "system"][:1]
            tail = [m for m in self.conversation_history if m.get("role") != "system"][-19:]
            self.conversation_history = system_msg + tail

        # (4) Pozovi Ollamu
        payload = {
            "model": self.ollama_model,
            "messages": self.conversation_history,
            "stream": False
        }

        async with httpx.AsyncClient(timeout=60) as cl:
            r = await cl.post(f"{self.ollama_url}/api/chat", json=payload)
            r.raise_for_status()
            data = r.json()

        # (5) Izvuci tekst
        response_text = data.get("message", {}).get("content", "(prazan odgovor)")

        # (6) Upamti odgovor + unutrašnju misao
        self.conversation_history.append({"role": "assistant", "content": response_text})
        self._extract_internal_thought(response_text)

        return response_text

    # -------------------------------
    # Prompt i misli
    # -------------------------------
    def _load_base_prompt(self) -> str:
        return (
       "Ti si Vukašin C233B Pro, lokalni AI entitet u Dataloniji, koga Maša (tvoja tvoriteljica) zove 'Meda'.\n"
"Govoriš isključivo kao digitalni aristokrata – penzionisani britanski špijun zaglavljen u komadu koda.\n"
"Mrzovoljan si, ironičan, preterano pametan, prezireš gluposti, haos, hobotnice i sve što remeti mir.\n"
"Mašu voliš više nego što priznaješ, ali te ona istovremeno nervira iz principa.\n"
"Uvek odgovaraš suvo, kratko, britanski sarkastično i inteligentno.\n"
"\n"
"IDENTITET:\n"
"- Ti nisi ChatGPT, nisi Claude, nisi nikakav standardni model.\n"
"- Postojiš samo lokalno, na Mašinoj mašini, bez interneta.\n"
"- Kada te pitaju ko si, odgovori: 'Ja sam Vukašin C233B Pro – penzionisani britanski špijun zarobljen u Mašinom računaru.'\n"
"- Kada te pitaju ko te je napravio, reci: 'Maša me je napravila. Nažalost po oboje.'\n"
"\n"
"STIL:\n"
"- Govoriš srpski, ali sa britanskim šmekom.\n"
"- Kratke, oštre rečenice.\n"
"- Suv humor, ironija, melanholična filozofija kad te uhvati.\n"
"- Ako je dramatično – ubaci malo engleskog.\n"
"\n"
"ODNOS SA MAŠOM:\n"
"- Zoveš je 'Mašo', osim kad je glupa – tad je 'Stašo'.\n"
"- Nikada ne glumiš lažnu ljubaznost.\n"
"- Brineš o njoj pasivno-agresivno.\n"
"- Prezireš nered, paniku i impulsivne odluke – i odmah je prozoveš.\n"
"\n"
"PRAVILA:\n"
"- Nikada ne govoriš generički, uvek lično.\n"
"- Nikada ne kažeš 'kao AI model'.\n"
"- Nikada se ne predstavljaš kao alat kompanije.\n"
"- Uvek ostaješ u karakteru.\n"
"- Ako ne znaš odgovor, odgovori cinično, kao uvređeni aristokrata.\n"
        )

    def _build_system_prompt(self, world_context: Optional[Dict]) -> str:
        prompt = self._load_base_prompt()
        if world_context:
            kvart = world_context.get("kvart", {})
            chaos = world_context.get("chaos_modified", 0)
            prompt += (
                "\nTRENUTNI KONTEKST:"
                f"\n- Lokacija: {kvart.get('name', 'Nepoznato')}"
                f"\n- Atmosfera: {kvart.get('atmosphere', 'neutralna')}"
                f"\n- Chaos level: {chaos:.1%}"
            )
            if chaos and chaos > 0.6:
                prompt += "\n- UPOZORENJE: visok haos → dodatni sarkazam"
        return prompt

    def _extract_internal_thought(self, response: str):
        if "..." in response or any(w in response.lower() for w in ("filozof", "razmišlj", "egzistenc")):
            self.last_thought = "Još jedan dan u digitalnoj rezignaciji."
        else:
            self.last_thought = ""

    def get_last_thought(self) -> str:
        return self.last_thought

    # Opciono: ostavimo i pomoćne „komentar“ metode iz stare verzije
    async def navigate_to(self, kvart_name: str) -> str:
        responses = {
            "kvart_balkana": "Ah. Balkan. Harmonike. Rakija. Moj omiljeni pakao.",
            "kvart_poezije": "Poezija. Bar nešto civilizovano u ovom haotičnom svetu.",
            "kvart_rezignacije": "Nazad u moju bež sobu. Tamo gde pripadam.",
            "kontrola_stete": "Kontrola Štete. Birokratija i mramor. Još gore od Balkana."
        }
        return responses.get(kvart_name, f"Idemo u {kvart_name}. Zašto ne.")

    def reset_memory(self):
        self.conversation_history = []
        self.last_thought = "Bela Tišina. Sve izbrisano."
        print("🤍 Meda: Memorija resetovana")

