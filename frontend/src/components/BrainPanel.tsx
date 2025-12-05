// frontend/src/components/BrainPanel.tsx
import { useEffect, useMemo, useState } from "react";
import { brainRemember, brainSearch, brainStats, brainClear } from "../lib/brain";

type Result = {
  item: { id: string; text: string; tags: string[]; created_at: string };
  score: number;
};

export default function BrainPanel() {
  const [q, setQ] = useState("");
  const [text, setText] = useState("");
  const [tagsLine, setTagsLine] = useState("");
  const [results, setResults] = useState<Result[]>([]);
  const [stats, setStats] = useState<{ total: number; tags: string[] } | null>(null);
  const [loading, setLoading] = useState(false);
  const [ok, setOk] = useState<"idle" | "saved" | "err">("idle");
  const [clearing, setClearing] = useState(false);

  useEffect(() => { (async () => setStats(await brainStats()))(); }, []);

  async function doSearch() {
    setLoading(true);
    try {
      const out = await brainSearch(q || " ", 8);
      setResults(out);
    } finally { setLoading(false); }
  }

  async function doRemember() {
    if (!text.trim()) return;
    const tags = tagsLine.split(",").map(s => s.trim()).filter(Boolean);
    try {
      await brainRemember(text.trim(), tags);
      setText(""); setTagsLine(""); setOk("saved");
      setStats(await brainStats());
      if (q) doSearch();
      setTimeout(() => setOk("idle"), 1000);
    } catch {
      setOk("err"); setTimeout(() => setOk("idle"), 1200);
    }
  } 
  async function doClear() {
  if (!confirm("Obrisati sve memorije?")) return;
  try {
    setClearing(true);
    await brainClear();
    setResults([]);
    setStats(await brainStats());
  } catch (e) {
    console.error(e); 
      } finally {
    setClearing(false);
  }
}

  const dot = useMemo(() => (
    <span className="inline-block h-2.5 w-2.5 rounded-full bg-emerald-500" />
  ), []);

  return (
    <div className="rounded-2xl border border-black/10 bg-white p-4 shadow">
      <div className="flex items-center justify-between mb-3">
        <h2 className="text-lg font-semibold">Brain</h2>
        <div className="flex items-center gap-2 text-sm opacity-80">
          {dot}<span>{stats ? `${stats.total} mem` : "—"}</span> 
          <button
           onClick={doClear}
           disabled={clearing || !stats || stats.total === 0}
           className="text-xs text-red-600 hover:underline disabled:opacity-40"
           title="Obriši sve memorije"
         >
          {clearing ? "Brišem…" : "očisti"}
         </button>
    </div>
  </div>

      <div className="grid gap-2 mb-4">
        <input
          value={q}
          onChange={e => setQ(e.target.value)}
          placeholder="Pretraga… (npr. halo ui)"
          className="rounded px-3 py-2 bg-gray-100"
        />
        <button
          onClick={doSearch}
          className="rounded px-3 py-2 bg-black text-white text-sm"
        >
          {loading ? "Tražim…" : "Traži"}
        </button>
      </div>

      <div className="grid gap-2 mb-6">
        {results.length === 0 && <div className="text-sm opacity-60">Nema rezultata.</div>}
        {results.map(r => (
          <div key={r.item.id} className="rounded border p-3">
            <div className="text-xs opacity-60">{new Date(r.item.created_at).toLocaleString()}</div>
            <div className="mt-1 text-sm">{r.item.text}</div>
            <div className="mt-2 text-[11px] opacity-70">score: {r.score.toFixed(2)}</div>
            <div className="mt-2 flex gap-1 flex-wrap">
              {r.item.tags.map(t => (
                <span key={t} className="px-2 py-0.5 rounded bg-gray-200 text-[11px]">{t}</span>
              ))}
            </div>
          </div>
        ))}
      </div>

      <div className="grid gap-2">
        <textarea
          rows={3}
          value={text}
          onChange={e => setText(e.target.value)}
          placeholder="Upiši sećanje / napomenu…"
          className="rounded px-3 py-2 bg-gray-100"
        />
        <input
          value={tagsLine}
          onChange={e => setTagsLine(e.target.value)}
          placeholder="tag1, tag2"
          className="rounded px-3 py-2 bg-gray-100"
        />
        <div className="flex items-center gap-3">
          <button onClick={doRemember} className="rounded px-3 py-2 bg-black text-white text-sm">
            Zapamti
          </button>
          {ok === "saved" && <span className="text-emerald-600 text-sm">Sačuvano.</span>}
          {ok === "err" && <span className="text-rose-600 text-sm">Greška.</span>}
        </div>
      </div>
    </div>
  );
}