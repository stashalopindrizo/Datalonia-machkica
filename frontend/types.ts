// TypeScript interfaces za Dataloniju

export interface Message {
  role: 'user' | 'assistant' | 'system';
  content: string;
  internal_thought?: string;
  timestamp: Date;
}

export interface WorldState {
  current_kvart: string;
  chaos_level: number;
  metafizicki_time: string;
  active_entities: string[];
  recent_events: Event[];
}

export interface Event {
  type: string;
  message?: string;
  timestamp: string;
}

export interface ChatResponse {
  response: string;
  world_state: WorldState;
  anomaly?: {
    triggered: boolean;
    type: string;
    message: string;
  };
  internal_monologue?: string;
}

export interface ChatRequest {
  user_id: string;
  message: string;
  current_kvart?: string;
}
