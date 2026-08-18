import { useState } from "react";
import { Button } from "../@/components/ui/button";
import { Input } from "../@/components/ui/input";
import { Card, CardContent } from "../@/components/ui/card";
import ReactMarkdown from "react-markdown";

type Source = { section: string; page: number };

export default function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [sources, setSources] = useState<Source[]>([]);
  const [loading, setLoading] = useState(false);

  const handleAsk = async () => {
    setLoading(true);
    const res = await fetch("http://localhost:8000/query", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });
    const data = await res.json();
    setAnswer(data.answer);
    setSources(data.sources);
    setLoading(false);
  };

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-4">
      <h1 className="text-2xl font-bold">GATE OS RAG</h1>
      <div className="flex gap-2">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Ask an OS question..."
        />
        <Button onClick={handleAsk} disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </Button>
      </div>

      {answer && (
        <Card>
          <CardContent className="pt-4">
            <ReactMarkdown>{answer}</ReactMarkdown>
            <div className="mt-3 text-sm text-gray-500">
              Sources: {sources.map((s) => `${s.section} (p.${s.page})`).join(", ")}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
}