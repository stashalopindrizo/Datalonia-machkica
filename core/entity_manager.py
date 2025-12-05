"""
Entity Manager - Manages all AI characters in Datalonia
Handles: spawning, tracking, interactions between entities
"""

from typing import Dict, Optional, List
from entities import MedaEntity, GraEntity

class EntityManager:
    def __init__(self):
        self.entities: Dict[str, any] = {}
        self.active_entities: List[str] = []
    
    def add_entity(self, entity_id: str, entity: any):
        """Register a new entity"""
        self.entities[entity_id] = entity
        self.active_entities.append(entity_id)
        print(f"✨ Entity '{entity_id}' spawned")
    
    def get_entity(self, entity_id: str) -> Optional[any]:
        """Get entity by ID"""
        return self.entities.get(entity_id)
    
    def remove_entity(self, entity_id: str):
        """Remove entity (death/reset)"""
        if entity_id in self.entities:
            del self.entities[entity_id]
            self.active_entities.remove(entity_id)
            print(f"💀 Entity '{entity_id}' removed")
    
    def list_entities(self) -> List[str]:
        """List all active entities"""
        return self.active_entities
    
    def reset_all(self):
        """BELA TIŠINA - reset all entities"""
        for entity_id in list(self.entities.keys()):
            if hasattr(self.entities[entity_id], 'reset_memory'):
                self.entities[entity_id].reset_memory()
        print("🤍 Bela Tišina - svi entiteti resetovani")


# Future: Add more entity types
# class MasaAgent:
#     """Autonomous Maša that sends random Ping! messages"""
#     pass
#
# class KontrolorAgent:
#     """Bureaucratic entity that monitors chaos"""
#     pass
