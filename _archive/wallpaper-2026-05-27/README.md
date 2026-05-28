# Wallpaper direction — archived 2026-05-27

Archived because the painted-branch storm/clearing/calm wallpaper homepage direction was vetoed before launch. Jordan has a new direction (not yet briefed) and asked for a clean working codebase. Park, don't destroy.

## What's in here

Original paths preserved relative to this folder, so restoration is a clean `mv` back to the repo:

```
_archive/wallpaper-2026-05-27/
  src/
    components/
      HomepageWallpaper.tsx       # zone composition component (storm/clearing/calm)
    app/
      wallpaper-test/
        page.tsx                  # /wallpaper-test test route with placeholder content
  public/
    wallpaper/                    # served WebP tiles
      storm-a.webp                # densest storm variant
      storm-b.webp                # wind-thrown variant
      storm-c.webp                # multi-scale variant
      clearing.webp               # mid-density transition tile
      calm.webp                   # sparse, branches in cream
```

Total ~2.5 MB of WebP assets.

## Related artifacts NOT in this archive (left in place per Jordan's instructions)

- `wallpaper-generation-spec.md` — the locked spec, at the repo root. Decision deferred.
- `wallpaper-assets/` — generation artifacts (hand reference, raw candidates, intermediate composites, final RGBA PNGs, mobile-test previews). Decision deferred.

## To restore

```
cd /Users/jordanhess/hessentials
mv _archive/wallpaper-2026-05-27/src/components/HomepageWallpaper.tsx src/components/
mv _archive/wallpaper-2026-05-27/src/app/wallpaper-test src/app/
mv _archive/wallpaper-2026-05-27/public/wallpaper public/
```

Then remove `"_archive"` from the `exclude` array in `tsconfig.json`.

## Context

The work was complete on storm (three locked tiles, offset-and-inpainted, mobile-validated), calm (programmatic composite from generation candidates, Telea-inpainted), and clearing (single locked tile, inpainted). A `/wallpaper-test` route mounted the full storm-clearing-calm arc against placeholder content for in-context review.

The architecture was sectioned CSS (no parallax, no scroll listeners), with zones sized as percentages of the parent's height so the Addendum B 50/15/35 ratio would map to actual scroll length.

Final review surfaced four publishable-blocker issues — visible bands between variant tiles, density not grading through the middle, text legibility throughout the storm range, and a missing real footer. Realistic finishing estimate was 15–20 hours of focused work across a week. At that point the direction was vetoed.

The generation pipeline learnings — programmatic synthesis of candidates via PIL/NumPy/OpenCV — are captured in memory (`feedback_programmatic_synthesis_first.md`) and would carry forward to any future image-tile work, including the next direction.
