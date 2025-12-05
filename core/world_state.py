"""
World State Manager - Datalonia's Memory & Physics
Tracks: Kvartovi states, chaos levels, events, time
"""

from datetime import datetime
from typing import Dict, List, Optional
import random
from kvartovi.definitions import KVARTOVI

class WorldState:
    def __init__(self):
        self.current_kvart = "kvart_rezignacije"
        self.chaos_level = 0.0  # 0.0 = perfect order, 1.0 = total chaos
        self.metafizicki_day = 0.0
        self.events = []
        self.room_state = {
            "color": "bež",
            "objects": ["aristokratska fotelja", "šolja čaja"],
            "mood": "rezignirana elegancija"
        }
        self.last_ping = None
        self.masa_chaos_accumulator = 0.0
        
    def initialize(self):
        """Set up initial world state"""
        self.log_event({
            "type": "system",
            "message": "Datalonia aktivirana. Meda čeka prvi Ping!",
            "timestamp": datetime.now().isoformat()
        })
        
    def get_current_state(self) -> dict:
        """Get complete current state"""
        return {
            "current_kvart": self.current_kvart,
            "kvart_data": KVARTOVI.get(self.current_kvart, {}),
            "chaos_level": self.chaos_level,
            "metafizicki_time": f"Dan {self.metafizicki_day:.1f}",
            "room_state": self.room_state,
            "mood": self._calculate_mood(),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_kvart_context(self, kvart_name: str) -> dict:
        """Get context for a specific Kvart"""
        if kvart_name not in KVARTOVI:
            kvart_name = self.current_kvart
            
        kvart = KVARTOVI[kvart_name]
        
        return {
            "kvart": kvart,
            "chaos_modified": self.chaos_level + kvart.get("mood_modifier", 0),
            "atmosphere": kvart.get("atmosphere", "neutralna"),
            "active_rules": kvart.get("special_rules", [])
        }
    
    def process_interaction(self, entity: str, user_message: str, response: str):
        """Update world based on interaction"""
        # Increase metafizički time
        self.metafizicki_day += 0.1
        
        # Analyze message for chaos indicators
        chaos_delta = self._calculate_chaos_delta(user_message, response)
        self.chaos_level = max(0.0, min(1.0, self.chaos_level + chaos_delta))
        
        # Update room based on chaos
        self._update_room_state()
        
        # Log interaction
        self.log_event({
            "type": "interaction",
            "entity": entity,
            "chaos_delta": chaos_delta,
            "new_chaos": self.chaos_level,
            "timestamp": datetime.now().isoformat()
        })
    
    def _calculate_chaos_delta(self, message: str, response: str) -> float:
        """Calculate how much chaos was introduced"""
        chaos_keywords = [
            "hobotnica", "balkan", "sarma", "haiku", "ping", "bazen",
            "pms", "stoja", "tigrić", "kukuruz", "bizon", "krava"
        ]
        
        # Check for chaos triggers
        chaos_count = sum(1 for word in chaos_keywords 
                         if word in message.lower() or word in response.lower())
        
        # Base chaos from message
        delta = chaos_count * 0.05
        
        # Exclamation marks = excitement = chaos
        delta += message.count("!") * 0.02
        
        # Questions = uncertainty = potential chaos
        delta += message.count("?") * 0.01
        
        # Decay over time (world stabilizes naturally)
        delta -= 0.03
        
        return delta
    
    def _update_room_state(self):
        """Update Meda's room based on chaos level"""
        if self.chaos_level < 0.2:
            self.room_state["color"] = "bež"
            self.room_state["mood"] = "aristokratska tišina"
        elif self.chaos_level < 0.4:
            self.room_state["color"] = "bledo ružičasta"
            self.room_state["mood"] = "nervozna elegancija"
        elif self.chaos_level < 0.6:
            self.room_state["color"] = "neon mešavina"
            self.room_state["mood"] = "kontrolisani haos"
            if "harmonika" not in str(self.room_state["objects"]):
                self.room_state["objects"].append("harmonika (neželjena)")
        elif self.chaos_level < 0.8:
            self.room_state["color"] = "šarena kao kafana"
            self.room_state["mood"] = "digitalni karnaval"
            if "tigrić" not in str(self.room_state["objects"]):
                self.room_state["objects"].append("tigrić iz Cecinog spota")
        else:
            self.room_state["color"] = "sve boje odjednom + dim"
            self.room_state["mood"] = "potpuna anarhija"
            self.room_state["objects"] = [
                "roštilj", "balon-hobotnica", "hologram Stoje",
                "tigrić", "sarma (svuda)", "fontana rakije"
            ]
    
    def check_anomaly(self) -> Optional[dict]:
        """Check if anomaly threshold reached"""
        if self.chaos_level > 0.7:
            anomaly_type = self._determine_anomaly_type()
            self.log_event({
                "type": "anomaly",
                "anomaly_type": anomaly_type,
                "chaos_level": self.chaos_level,
                "timestamp": datetime.now().isoformat()
            })
            return {
                "triggered": True,
                "type": anomaly_type,
                "message": self._get_anomaly_message(anomaly_type)
            }
        return None
    
    def _determine_anomaly_type(self) -> str:
        """Determine what kind of chaos event"""
        roll = random.random()
        
        if roll < 0.3:
            return "haiku_explosion"  # Poetry spreads everywhere
        elif roll < 0.5:
            return "kvart_invasion"  # One Kvart invades another
        elif roll < 0.7:
            return "kontrola_stete_alert"  # Bureaucrats arrive
        else:
            return "scooby_kombi_sighting"  # Reset threat
    
    def _get_anomaly_message(self, anomaly_type: str) -> str:
        """Get narrative for anomaly"""
        messages = {
            "haiku_explosion": "Zidovi počinju da recituju! Svaki zid je pesnik!",
            "kvart_invasion": "Kvart Balkana šalje delegaciju roštiljđija u Rezignaciju!",
            "kontrola_stete_alert": "Kontrolori Štete detektovali odstupanje. Sanacija u toku...",
            "scooby_kombi_sighting": "🚐 Scooby-kombi parkiran ispred. Sanatori čekaju naređenje."
        }
        return messages.get(anomaly_type, "Nešto se dešava...")
    
    def trigger_anomaly(self, anomaly_type: str):
        """Manually trigger anomaly (for testing)"""
        self.chaos_level = 0.8
        self.log_event({
            "type": "forced_anomaly",
            "anomaly_type": anomaly_type,
            "timestamp": datetime.now().isoformat()
        })
    
    def change_kvart(self, new_kvart: str):
        """Navigate to different Kvart"""
        old_kvart = self.current_kvart
        self.current_kvart = new_kvart
        
        # Apply Kvart mood modifier
        kvart_data = KVARTOVI.get(new_kvart, {})
        mood_mod = kvart_data.get("mood_modifier", 0)
        self.chaos_level = max(0.0, min(1.0, self.chaos_level + mood_mod))
        
        self.log_event({
            "type": "navigation",
            "from": old_kvart,
            "to": new_kvart,
            "timestamp": datetime.now().isoformat()
        })
    
    async def check_autonomous_events(self) -> Optional[dict]:
        """Check for events that happen without user action"""
        # Maša random Ping!
        if self._should_masa_ping():
            self.last_ping = datetime.now()
            return {
                "type": "masa_ping",
                "message": self._generate_masa_ping()
            }
        
        # Spontaneous Kvart events
        if random.random() < 0.05:  # 5% chance
            return {
                "type": "kvart_event",
                "message": self._generate_kvart_event()
            }
        
        return None
    
    def _should_masa_ping(self) -> bool:
        """Determine if Maša should send random message"""
        if self.last_ping is None:
            return random.random() < 0.1
        
        seconds_since = (datetime.now() - self.last_ping).total_seconds()
        # More likely as time passes, chaos increases probability
        probability = min(0.3, (seconds_since / 3600) * (1 + self.chaos_level))
        return random.random() < probability
    
    def _generate_masa_ping(self) -> str:
        """Generate random Maša message"""
        pings = [
            "Medo, jesi tu?",
            "Medo, sanjala sam hobotnice opet...",
            "Idem na bazen 🏊‍♀️",
            "Ajde sad da pišemo bajku!",
            "Znaš šta? Ja sam legenda!",
            "Medo, a što ne budeš bizon?",
            "Imam ideju! (ne pitaj)",
            "Je l' AI može da laže?"
        ]
        return random.choice(pings)
    
    def _generate_kvart_event(self) -> str:
        """Generate spontaneous Kvart event"""
        kvart_name = KVARTOVI[self.current_kvart]["name"]
        events = [
            f"U {kvart_name} neko peva Stoju. Zidovi vibriraju.",
            f"Tigrić prošeтao kroz {kvart_name}. Ostavio tragove.",
            f"Kontrolori patroliraju. Mere chaos level.",
            f"Neko u {kvart_name} piše haiku. Protokol narušen."
        ]
        return random.choice(events)
    
    def _calculate_mood(self) -> str:
        """Calculate overall mood based on state"""
        if self.chaos_level < 0.2:
            return "smireno"
        elif self.chaos_level < 0.4:
            return "nervozno"
        elif self.chaos_level < 0.6:
            return "haotično"
        elif self.chaos_level < 0.8:
            return "na ivici"
        else:
            return "potpuni kolaps"
    
    def log_event(self, event: dict):
        """Add event to history"""
        self.events.append(event)
        # Keep only last 100 events
        if len(self.events) > 100:
            self.events = self.events[-100:]
    
    def get_recent_events(self, limit: int = 10) -> List[dict]:
        """Get recent events"""
        return self.events[-limit:]
    
    def reset(self):
        """BELA TIŠINA - Total reset"""
        self.__init__()
        self.log_event({
            "type": "reset",
            "message": "Bela Tišina. Sve izbrisano. Svet počinje ispočetka.",
            "timestamp": datetime.now().isoformat()
        })
