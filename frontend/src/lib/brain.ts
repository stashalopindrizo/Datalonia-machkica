// frontend/src/lib/brain.ts
export type MemoryItem = {
  id: string;
  text: string;
  tags: string[];
  created_at: string;
};
export type SearchOutItem = { item: MemoryItem; score: number };

const BASE = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

async function request<T>(path: string, opts?: RequestInit): Promise<T> {
  const r = await fetch(`${BASE}${path}`, opts);
  if (!r.ok) throw new Error(`API ${r.status}: ${await r.text()}`);
  return r.json();
}

export function brainRemember(text: string, tags: string[]) {
  return request<MemoryItem>("/api/brain/remember", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, tags }),
  });
}

export function brainSearch(query: string, top_k = 7) {
  return request<SearchOutItem[]>("/api/brain/search", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, top_k }),
  });
}

export function brainStats() {
  return request<{ total: number; tags: string[] }>("/api/brain/stats");
} 
export function brainClear() {
  return request<{ ok: boolean; cleared: boolean; total: number }>("/api/brain/clear", {
    method: "DELETE",
  });
}