/**
 * UnderRenovation — hand-drawn placeholder graphic.
 *
 * Scaffolding, a few renovation tools, and a hanging sign reading
 * "sorry for the mess. / under renovation." Approved by Jordan and
 * landed alongside Version Next.
 *
 * Inline SVG component per the brief — not <img> or background-image —
 * so CSS-variable theming and crisp scaling survive. The hand-drawn
 * wobble (the displacement filter on the main scene) is intentional;
 * don't clean it up.
 *
 * Theming. Palette is driven by CSS variables on the `svg.under-renovation`
 * selector: --linen (ground), --ink (lines + text), --accent (paint
 * highlight), --paper (sign face), --ink-soft (secondary text). To recolor,
 * override those variables on the same selector; don't edit the paths.
 *
 * Scoping. The original brief's style block used a bare `svg{...}` selector
 * that would have leaked the CSS variables to every SVG on the page. Here
 * the rules are scoped to `svg.under-renovation` so other SVGs (Symbol,
 * Wordmark, etc.) keep their own theming.
 *
 * ID namespacing. The filter and pattern IDs are prefixed (`ur-rough`,
 * `ur-weave`) per the brief — if this component is ever rendered more
 * than once on the same page, the IDs won't collide.
 *
 * Sits on the site's cream ground (the SVG carries its own slightly-warmer
 * --linen #ece3d2 ground, by design, so it reads as a contained moment
 * against the page).
 */

export default function UnderRenovation() {
  return (
    <div className="mx-auto w-full max-w-[860px] px-6 sm:px-10 md:px-12">
      <svg
        className="under-renovation block h-auto w-full"
        viewBox="0 0 860 600"
        xmlns="http://www.w3.org/2000/svg"
        role="img"
        aria-label="A hand-drawn scaffolding and renovation-tools scene with a hanging sign reading 'sorry for the mess. under renovation.'"
      >
        <style>{`
svg.under-renovation{--linen:#ece3d2;--ink:#28323f;--accent:#c1894a;--paper:#f5eddc;--ink-soft:#6a727d;}
svg.under-renovation .s{stroke:var(--ink);fill:none;stroke-width:2.4;stroke-linecap:round;stroke-linejoin:round;}
svg.under-renovation .thin{stroke:var(--ink);fill:none;stroke-width:1.5;stroke-linecap:round;}
svg.under-renovation .t{fill:var(--ink);font-family:Georgia,'Times New Roman',serif;font-style:italic;}
        `}</style>
        <defs>
          <filter id="ur-rough" x="-6%" y="-6%" width="112%" height="112%">
            <feTurbulence type="fractalNoise" baseFrequency="0.016" numOctaves="2" seed="6" result="n" />
            <feDisplacementMap in="SourceGraphic" in2="n" scale="2.6" xChannelSelector="R" yChannelSelector="G" />
          </filter>
          <pattern id="ur-weave" width="7" height="7" patternUnits="userSpaceOnUse">
            <path d="M0 0H7M0 0V7" stroke="#5a4a30" strokeOpacity="0.05" strokeWidth="0.6" />
          </pattern>
        </defs>
        <rect width="860" height="600" fill="var(--linen)" />
        <rect width="860" height="600" fill="url(#ur-weave)" />
        <g filter="url(#ur-rough)">
          <path className="thin" d="M70 530 Q300 524 500 530 T800 527" opacity="0.85" />
          <line className="s" x1="255" y1="204" x2="257" y2="528" />
          <line className="s" x1="625" y1="204" x2="623" y2="528" />
          <path className="s" d="M232 188 L648 186 L648 202 L232 204 Z" />
          <line className="s" x1="257" y1="361" x2="623" y2="363" />
          <path className="s" d="M250 352 L452 351 L452 366 L250 367 Z" />
          <line className="s" x1="259" y1="360" x2="623" y2="206" />
          <path className="s" d="M247 537 L256 528 L264 537" />
          <path className="s" d="M615 537 L624 528 L632 537" />
          <line className="s" x1="120" y1="530" x2="205" y2="210" />
          <line className="s" x1="150" y1="530" x2="235" y2="210" />
          <line className="s" x1="205" y1="210" x2="235" y2="210" />
          <line className="s" x1="133" y1="482" x2="163" y2="482" />
          <line className="s" x1="147" y1="428" x2="177" y2="428" />
          <line className="s" x1="162" y1="370" x2="192" y2="370" />
          <line className="s" x1="178" y1="312" x2="208" y2="312" />
          <line className="s" x1="192" y1="258" x2="222" y2="258" />
          <path className="s" d="M133 492 L182 492 L177 530 L138 530 Z" />
          <ellipse className="s" cx="157" cy="492" rx="25" ry="6" />
          <ellipse cx="157" cy="492" rx="19" ry="4" fill="var(--accent)" stroke="none" />
          <path className="s" d="M134 491 Q157 469 180 491" />
          <line className="s" x1="168" y1="489" x2="206" y2="451" />
          <path d="M203 455 L214 446 L219 453 L208 462 Z" fill="var(--ink)" stroke="none" />
          <path d="M211 449 L216 445 L218 449 Z" fill="var(--accent)" stroke="none" />
          <path className="s" d="M612 528 L596 472" />
          <path className="s" d="M596 472 L580 461" />
          <rect className="s" x="556" y="452" width="30" height="13" rx="6" />
          <path className="s" d="M452 533 Q468 506 500 513 Q526 519 546 507 Q566 500 561 533 Z" />
          <path className="thin" d="M472 521 Q502 525 542 516" />
          <path className="thin" d="M466 528 Q505 533 553 524" />
          <line className="thin" x1="350" y1="536" x2="358" y2="536" />
          <line className="thin" x1="690" y1="532" x2="697" y2="532" />
        </g>
        <path className="thin" d="M390 202 L322 250" />
        <path className="thin" d="M510 202 L578 250" />
        <g transform="rotate(-1.5 450 302)">
          <rect x="300" y="250" width="300" height="104" rx="3" fill="var(--paper)" stroke="var(--ink)" strokeWidth="2.4" />
          <rect x="309" y="259" width="282" height="86" rx="2" fill="none" stroke="var(--ink)" strokeWidth="1" opacity="0.35" />
          <text x="450" y="299" textAnchor="middle" className="t" fontSize="28">
            sorry for the mess.
          </text>
          <text x="450" y="330" textAnchor="middle" className="t" fontSize="18" fill="var(--ink-soft)">
            under renovation.
          </text>
        </g>
        <text x="790" y="572" textAnchor="end" fontFamily="Georgia,'Times New Roman',serif" fontSize="15" fill="var(--ink)" opacity="0.5">
          Hessentials
        </text>
      </svg>
    </div>
  );
}
