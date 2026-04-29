import { redirect } from "next/navigation";

/**
 * /home → /.
 *
 * The homepage now lives at the canonical `/` URL so visitors land on
 * hessentials.co (not hessentials.co/home). This file is kept as a
 * permanent redirect so any legacy links to /home (internal or
 * external) bounce cleanly to the new canonical URL. Belt-and-
 * suspenders: next.config.ts also handles this at the edge.
 */
export default function HomeRedirect() {
  redirect("/");
}
