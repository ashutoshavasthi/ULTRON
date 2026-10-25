// Helpers that shrink agent output to what fits a small watch screen.

const CARD_LIMIT = 180;

/** Split text into pages of at most `limit` chars, breaking on sentence/line boundaries. */
export function toWatchCards(text: string, limit = CARD_LIMIT): string[] {
  const clean = text
    .replace(/```[\s\S]*?```/g, " [code] ")
    .replace(/[*_`#>]+/g, "")
    .replace(/\s+/g, " ")
    .trim();
  if (!clean) return [];
  // Only split where punctuation is followed by whitespace, so "hello.txt" stays whole.
  const pieces = clean.split(/(?<=[.!?])\s+/);
  const cards: string[] = [];
  let cur = "";
  for (const raw of pieces) {
    let piece = raw.trim();
    if (!piece) continue;
    while (piece.length > limit) {
      const cut = piece.lastIndexOf(" ", limit);
      const at = cut > limit / 2 ? cut : limit;
      if (cur) { cards.push(cur); cur = ""; }
      cards.push(piece.slice(0, at).trim());
      piece = piece.slice(at).trim();
    }
    if (!piece) continue;
    if (cur && cur.length + 1 + piece.length > limit) {
      cards.push(cur);
      cur = piece;
    } else {
      cur = cur ? `${cur} ${piece}` : piece;
    }
  }
  if (cur) cards.push(cur);
  return cards.length > 1 ? cards.map((c, i) => `${i + 1}/${cards.length} ${c}`) : cards;
}

/** One-line description of a tool call for approval titles. */
export function summarizeTool(tool: string, input: Record<string, unknown>): string {
  const s = (v: unknown) => (typeof v === "string" ? v : "");
  switch (tool) {
    case "Bash": return `Run: ${s(input.command).slice(0, 120)}`;
    case "Write": return `Write ${s(input.file_path)}`;
    case "Edit": return `Edit ${s(input.file_path)}`;
    case "NotebookEdit": return `Edit notebook ${s(input.notebook_path)}`;
    case "WebFetch": return `Fetch ${s(input.url)}`;
    case "WebSearch": return `Search: ${s(input.query)}`;
    default: return tool;
  }
}
