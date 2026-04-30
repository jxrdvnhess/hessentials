/**
 * JSON-LD <script> renderer.
 *
 * Inserts a single Schema.org structured-data block into the page.
 * Pages call this with one or more schema objects produced by
 * `src/lib/jsonLd.ts`.
 *
 * Why dangerouslySetInnerHTML:
 *   JSON-LD has to live as a literal `<script>` body so crawlers can
 *   parse it. React's standard children API would JSX-escape angle
 *   brackets and break the schema. The `<` → `<` substitution
 *   below prevents an injection vector — any `</script>` substring
 *   inside the JSON gets neutralized to `</script>` so the
 *   surrounding script tag can't be terminated early by user-supplied
 *   content (recipe titles, descriptions, etc.).
 *
 * Where to render:
 *   Anywhere in the component tree below `<head>` is fine. App Router
 *   tolerates JSON-LD inside the body, and Google's crawler will pick
 *   it up regardless. We render at the bottom of each page so the
 *   structured data sits adjacent to the visible content it describes.
 */

type JsonLdProps = {
  /** A single schema object, or an array — we render one <script> per. */
  data: object | object[];
};

function safeJson(payload: object): string {
  return JSON.stringify(payload).replace(/</g, "\\u003c");
}

export default function JsonLd({ data }: JsonLdProps) {
  const items = Array.isArray(data) ? data : [data];
  return (
    <>
      {items.map((item, i) => (
        <script
          key={i}
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: safeJson(item) }}
        />
      ))}
    </>
  );
}
