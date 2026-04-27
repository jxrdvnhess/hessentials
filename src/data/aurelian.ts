/* ---------- Types ---------- */

export type Sign =
  | "aries"
  | "taurus"
  | "gemini"
  | "cancer"
  | "leo"
  | "virgo"
  | "libra"
  | "scorpio"
  | "sagittarius"
  | "capricorn"
  | "aquarius"
  | "pisces";

export type Placement = "sun" | "moon" | "rising";
export type Element = "fire" | "earth" | "air" | "water";
export type Selection = Sign | "unknown" | "";

type SignProfile = {
  name: string;
  element: Element;
  /** Verbatim Sun blurb from architecture spec, Section 2. */
  sun: string;
  /** Verbatim Moon blurb. */
  moon: string;
  /** Verbatim Rising blurb. */
  rising: string;
  /** Section 4.2 anchor — appears in the placement header line. */
  sunAnchor: string;
  moonAnchor: string;
  risingAnchor: string;
  /** Short surface phrase used for pattern composition (Rising slot). */
  surface: string;
  /** Short interior phrase used for pattern composition (Moon slot). */
  interior: string;
  /** Short identity phrase used for pattern composition (Sun slot). */
  identity: string;
  /** Concrete relationship behavior (lived, specific). */
  relationshipBehavior: string;
  /** Concrete work / decision behavior (lived, specific). */
  workBehavior: string;
  /** Internal felt experience inside the pattern. */
  internalExperience: string;
  /** Friction line — where the system meets resistance from itself. */
  frictionScene: string;
  /** Watch-point scene — present-tense recognition, scene-level. */
  watchScene: string;
};

/* ---------- Sign Library ---------- */

export const SIGNS: Record<Sign, SignProfile> = {
  aries: {
    name: "Aries",
    element: "fire",
    sun: "Forward momentum is the operating system. Decisions get made in motion, and waiting tends to feel like friction more than patience. The signature isn't aggression. It's initiation, and things tend to start because Aries Suns are in the room.",
    moon: "Emotional regulation runs hot and fast. Feelings move through quickly, often expressed as action before language has caught up. The need underneath is autonomy. Without space to move, the system overheats.",
    rising: "Arrival is direct. The first impression reads as confident, slightly impatient, and often more intense than intended. People register the energy before they register the words.",
    sunAnchor: "forward momentum",
    moonAnchor: "fast-moving heat",
    risingAnchor: "direct arrival",
    surface: "decisive entrance",
    interior: "fast hot processing",
    identity: "forward initiation",
    relationshipBehavior:
      "you tend to make the first move and then wait for the other person to catch up to a decision they didn't know was on the table",
    workBehavior:
      "you commit before everyone else has finished talking, which reads as confident and lands as pressure on whoever's still deciding",
    internalExperience:
      "stillness registers as friction long before it registers as rest, which means the rest gets postponed until the body forces it",
    frictionScene:
      "the action gets made before the words have caught up, and the explanation arrives later than the people on the other side of it expected",
    watchScene:
      "the pattern is moving on the impulse, then privately recalibrating once the room has caught up to the move you already made",
  },
  taurus: {
    name: "Taurus",
    element: "earth",
    sun: "Steadiness is the operating system. There tends not to be much pressure to start before the ground feels right. Once committed, the pattern is to stay, by design, not stubbornness.",
    moon: "Emotional regulation runs through the body and the senses. Comfort isn't decadence here. It's nervous system maintenance, and the need underneath is consistency. Disruption registers as threat before it registers as change.",
    rising: "Arrival is grounded and unhurried. People read the presence before they read the personality, and the presence tends to lower the temperature of a room. First impressions skew toward settled.",
    sunAnchor: "steadiness",
    moonAnchor: "sensory grounding",
    risingAnchor: "unhurried presence",
    surface: "unhurried presence",
    interior: "slow sensory recovery",
    identity: "patient steadiness",
    relationshipBehavior:
      "you take longer than most people to commit and then stay longer than most people would, which reads as loyalty and feels, from the inside, like the only honest pace",
    workBehavior:
      "decisions take time at the front and then run without hesitation, which means people sometimes mistake your processing pace for indecision",
    internalExperience:
      "disruption lands in the body before it lands in the schedule, and the body asks for more time to reset than the calendar usually allows",
    frictionScene:
      "the pace looks like reluctance from the outside and like respect for the actual decision from the inside",
    watchScene:
      "the pattern is staying inside something past the point where staying serves you, because leaving costs more than the system is willing to pay this week",
  },
  gemini: {
    name: "Gemini",
    element: "air",
    sun: "Curiosity is the operating system. Identity organizes around inputs, conversations, and connections rather than fixed positions. The pattern looks scattered from outside and feels parallel from inside.",
    moon: "Emotional regulation runs through language and information. Naming a feeling tends to defuse it. The need underneath is variety, and stagnation reads as low-grade panic.",
    rising: "Arrival is quick and verbal. The first impression registers as bright, observant, and slightly elusive. People often feel met but not fully seen on first contact.",
    sunAnchor: "curiosity",
    moonAnchor: "language-led processing",
    risingAnchor: "quick verbal arrival",
    surface: "quick verbal arrival",
    interior: "language-led processing",
    identity: "parallel inquiry",
    relationshipBehavior:
      "you keep several threads open at once and the people closest to you sometimes feel like one of the threads rather than the room",
    workBehavior:
      "you decide by talking through it, often out loud to whoever's nearby, and the decision is usually clearer to you by the end of the sentence than at the start",
    internalExperience:
      "stagnation reads as low-grade panic, which means rest has to come disguised as a different kind of motion",
    frictionScene:
      "what looks like restlessness is actually a system that needs new inputs to keep regulation running, and pressure to settle reads to the body as a threat",
    watchScene:
      "the pattern is having said the thing already and forgetting that the people who weren't in that conversation are still waiting for it",
  },
  cancer: {
    name: "Cancer",
    element: "water",
    sun: "Care is the operating system. Identity organizes around protection of people, places, history, and memory. The pattern reads as soft on the outside and structurally loyal underneath.",
    moon: "Emotional regulation is tidal. Feelings come in waves and need somewhere to land before they pass. The need underneath is safety, and without it the response is to retreat inward, not outward.",
    rising: "Arrival is gentle and slightly guarded. People register warmth and reserve at the same time. First impressions read as approachable but not yet open.",
    sunAnchor: "protective care",
    moonAnchor: "tidal regulation",
    risingAnchor: "guarded warmth",
    surface: "guarded warmth",
    interior: "slow tidal recovery",
    identity: "structural loyalty",
    relationshipBehavior:
      "you absorb more of the room than you announce and then need a quiet hour to put the absorbed part down",
    workBehavior:
      "you remember the texture of every prior conversation and use it to make decisions, which reads as intuitive and is actually a long memory in motion",
    internalExperience:
      "what soothes you is the specific room, the specific light, the specific people, and an unfamiliar version of any of those reads as low-grade unsafety until the body recalibrates",
    frictionScene:
      "the warmth on the outside collects more than the inside has bandwidth to hold by Thursday",
    watchScene:
      "the pattern is taking on the room's mood without checking whether you're holding feelings that aren't yours, and finding out later by being tired in a way the day doesn't account for",
  },
  leo: {
    name: "Leo",
    element: "fire",
    sun: "Expression is the operating system. Identity organizes around being seen, and around giving generously when it is. The signature isn't ego. It's authorship. Leo Suns want their hand visible in their own life.",
    moon: "Emotional regulation runs through being recognized. Acknowledgment isn't vanity here. It's how the system confirms it's safe. The need underneath is dignity, and feeling overlooked registers as feeling unsafe.",
    rising: "Arrival has presence. People read warmth, confidence, and a touch of performance, even when none is intended. First impressions tend to anchor a room.",
    sunAnchor: "visible authorship",
    moonAnchor: "recognition-led regulation",
    risingAnchor: "anchored presence",
    surface: "anchored warm presence",
    interior: "recognition-dependent recovery",
    identity: "visible authorship",
    relationshipBehavior:
      "you give early and generously, and the small wound that doesn't get said out loud is when the giving lands in a room that doesn't notice it landed",
    workBehavior:
      "your hand on the work has to be visible for the work to feel like yours, and unattributed contributions sit heavier than the size of them suggests",
    internalExperience:
      "feeling overlooked doesn't register as a slight, it registers as a small destabilization, which is why the calibration to recover takes longer than people would expect",
    frictionScene:
      "the room reads warmth and assumes it's effortless, which means the cost of producing the warmth doesn't get accounted for",
    watchScene:
      "the pattern is performing more energy than the system has, because the alternative is being seen as someone whose energy ran out, and that reads as more dangerous than the exhaustion",
  },
  virgo: {
    name: "Virgo",
    element: "earth",
    sun: "Refinement is the operating system. Identity organizes around making things work better, including the self. The pattern is precise, useful, and quietly demanding.",
    moon: "Emotional regulation runs through analysis and order. Naming what's wrong helps the system settle. The need underneath is competence. Chaos isn't aesthetic discomfort. It's destabilizing.",
    rising: "Arrival is composed and observant. People register attention to detail, neat edges, and a slight reserve. First impressions skew toward thoughtful and gathered.",
    sunAnchor: "refinement",
    moonAnchor: "analysis-led regulation",
    risingAnchor: "composed observation",
    surface: "composed precision",
    interior: "high-standard internal critique",
    identity: "quiet refinement",
    relationshipBehavior:
      "you notice the small thing that's slightly off in the room and then make the call privately about whether to mention it, which reads to the other person as either care or distance depending on what they needed",
    workBehavior:
      "you produce work other people read as polished, and you privately keep a list of the corrections you didn't have time to make",
    internalExperience:
      "the running internal critique sounds like neutral observation from the inside and like high standards from the outside, and the gap between those readings is one of the quieter costs",
    frictionScene:
      "the precision that serves the work also gets aimed at the self, and there isn't a clean off-switch between the two",
    watchScene:
      "the pattern is finishing the thing and then running the post-mortem alone in the kitchen, which means the win and the critique arrive in the same moment",
  },
  libra: {
    name: "Libra",
    element: "air",
    sun: "Calibration is the operating system. Identity organizes around relationship, fairness, and aesthetic order. The pattern looks effortless and is actually constant adjustment.",
    moon: "Emotional regulation runs through harmony. Conflict isn't avoided out of weakness. It's avoided because dissonance is felt physically. The need underneath is balance.",
    rising: "Arrival is polished and pleasant. People register taste, ease, and social intelligence. First impressions tend to be graceful before they are specific.",
    sunAnchor: "calibration",
    moonAnchor: "harmony-led regulation",
    risingAnchor: "polished arrival",
    surface: "graceful polished entry",
    interior: "harmony-needing recovery",
    identity: "constant calibration",
    relationshipBehavior:
      "you read the room before you enter it and adjust the version of you that arrives, and the adjustment is so practiced that even you sometimes lose track of which version is the unadjusted one",
    workBehavior:
      "you can hold three valid perspectives at once, which makes you useful in collaboration and slow in solo decisions",
    internalExperience:
      "dissonance lands in the body, not the mind, which means a tense room is a physical event before it's a thought",
    frictionScene:
      "the calibration that makes you easy to be around is the same calibration that makes it hard to know what you actually want without other people in the room",
    watchScene:
      "the pattern is saying the version of yes that the room wanted to hear, and only realizing in the car later that you didn't want to say yes at all",
  },
  scorpio: {
    name: "Scorpio",
    element: "water",
    sun: "Depth is the operating system. Identity organizes around what's underneath, in people, in situations, in the self. The pattern is private by default and intense when present.",
    moon: "Emotional regulation runs through control. Feelings are processed inwardly first, often thoroughly, before any outward sign appears. The need underneath is trust, slowly given.",
    rising: "Arrival is quiet and observant. People register intensity before they register friendliness. First impressions often feel watched in a way that isn't unkind.",
    sunAnchor: "depth",
    moonAnchor: "controlled inward processing",
    risingAnchor: "watching reserve",
    surface: "watching reserve",
    interior: "thorough private processing",
    identity: "private depth",
    relationshipBehavior:
      "you tend to hold the real version of what you think back until you've decided the person can carry it, which reads as withholding to people who haven't earned the access yet",
    workBehavior:
      "you can see what's underneath the project before the project has named it, and naming what you see is its own decision, separate from seeing it",
    internalExperience:
      "trust runs on a longer arc than people expect, and small violations of it land heavier and stay longer than the violation itself merits",
    frictionScene:
      "the access to depth is not the same as the willingness to share it, and the assumption that it is causes most of the misreads",
    watchScene:
      "the pattern is having processed something completely on your own and forgetting that the other person hasn't been in that conversation yet",
  },
  sagittarius: {
    name: "Sagittarius",
    element: "fire",
    sun: "Expansion is the operating system. Identity organizes around meaning, perspective, and forward motion. The pattern resists smallness, including smallness of thinking.",
    moon: "Emotional regulation runs through movement and meaning. Feelings need air around them, often literally. The need underneath is freedom, and containment registers as suffocation.",
    rising: "Arrival is open and energetic. People register warmth, candor, and a certain restlessness. First impressions read as easy to talk to, hard to pin down.",
    sunAnchor: "expansion",
    moonAnchor: "movement-led regulation",
    risingAnchor: "open candid arrival",
    surface: "open candid arrival",
    interior: "movement-dependent regulation",
    identity: "expansive reach",
    relationshipBehavior:
      "you say the honest thing before you've checked whether the room can hold it, and your first instinct on someone else's bad news is to reach for the wider frame, even when the wider frame isn't what they wanted",
    workBehavior:
      "you can hold the long view in a meeting where no one else is, and you can also miss the small thing that needed to be done by Tuesday",
    internalExperience:
      "containment lands as suffocation in the body, which is why the next trip, the next idea, the next move always looks slightly closer to necessary than it is",
    frictionScene:
      "the candor that makes you feel honest is not always what the other person was asking for, and you find that out after",
    watchScene:
      "the pattern is reaching for the wider frame before the smaller feeling has been allowed to land, and explaining it back to the person in a way that makes them feel less heard than before you spoke",
  },
  capricorn: {
    name: "Capricorn",
    element: "earth",
    sun: "Construction is the operating system. Identity organizes around long-term outcomes, structure, and earned authority. The pattern is patient, strategic, and self-directed.",
    moon: "Emotional regulation runs through containment. Feelings are managed quietly, often without informing anyone they happened. The need underneath is competence and respect.",
    rising: "Arrival is composed and slightly formal. People register seriousness, dry humor, and presence. First impressions skew toward older than they are.",
    sunAnchor: "construction",
    moonAnchor: "contained processing",
    risingAnchor: "formal composure",
    surface: "formal composed weight",
    interior: "contained quiet processing",
    identity: "long-arc construction",
    relationshipBehavior:
      "you tend to show care through reliability rather than through naming the care, and people who need the naming sometimes don't recognize the reliability as the same gesture",
    workBehavior:
      "you build slowly and the build holds, and the pace looks like ambition from the outside and like minimum responsible speed from the inside",
    internalExperience:
      "feelings get managed quietly, often without informing anyone they happened, which means the cost of the management lives entirely in the body",
    frictionScene:
      "the composure people read as steadiness is not free, and the price of producing it gets paid privately, often at hours when nobody's looking",
    watchScene:
      "the pattern is carrying the weight without naming the weight, and noticing only when the body sends the bill",
  },
  aquarius: {
    name: "Aquarius",
    element: "air",
    sun: "Independence is the operating system. Identity organizes around perspective, system thinking, and a slight outsider position. The pattern is friendly without being available.",
    moon: "Emotional regulation runs through distance. Space is how feelings get processed. The need underneath is autonomy, and pressure to merge registers as a threat to the self.",
    rising: "Arrival is friendly and faintly cool. People register intelligence, openness, and a subtle remove. First impressions tend to be interesting before they're warm.",
    sunAnchor: "independence",
    moonAnchor: "space-led regulation",
    risingAnchor: "cool friendly arrival",
    surface: "cool friendly remove",
    interior: "space-dependent recovery",
    identity: "outsider perspective",
    relationshipBehavior:
      "you offer warmth and access on your own timing, and the people closest to you sometimes feel that timing as withholding even when you mean it as honoring the relationship",
    workBehavior:
      "you can see the system from outside it, which makes you useful when the team is stuck and slightly remote when the team is in the middle of a feeling",
    internalExperience:
      "pressure to merge registers as a threat to the self, which means closeness has to come on your own timing or the system reads it as compromise instead of connection",
    frictionScene:
      "the friendliness is real and the distance is also real, and the assumption that the friendliness should resolve the distance is where most of the misreads come from",
    watchScene:
      "the pattern is being warm and being elsewhere at the same time, and the elsewhere being the part that's actually free of pressure",
  },
  pisces: {
    name: "Pisces",
    element: "water",
    sun: "Permeability is the operating system. Identity organizes around imagination, empathy, and a fluid sense of self. The pattern absorbs more than it announces.",
    moon: "Emotional regulation runs through atmosphere. Feelings often arrive without clear authorship, the room's, someone else's, the day's. The need underneath is solitude as a reset.",
    rising: "Arrival is soft and slightly elsewhere. People register kindness and a quality of attention that doesn't feel bounded. First impressions read as gentle, hard to place.",
    sunAnchor: "permeability",
    moonAnchor: "atmospheric absorption",
    risingAnchor: "soft elsewhere arrival",
    surface: "soft elsewhere arrival",
    interior: "atmospheric absorption",
    identity: "porous absorption",
    relationshipBehavior:
      "you take in the other person's mood before they've named it and then lose track of which mood was theirs and which one became yours by the end of the conversation",
    workBehavior:
      "you sense what the work needs before you can articulate it, and the articulation lags far enough behind the sensing that the explanation feels like a translation into a language that loses something",
    internalExperience:
      "feelings often arrive without clear authorship, which makes solitude less a preference and more a maintenance routine",
    frictionScene:
      "the kindness that makes you generous is the same channel that lets the room's mood walk into your body without permission",
    watchScene:
      "the pattern is absorbing the day and finding out at 9pm that some of what you were carrying was never yours to carry in the first place",
  },
};

/* ---------- Public helpers ---------- */

export const SIGN_LABELS: Array<{ value: Sign; label: string }> = (
  Object.entries(SIGNS) as Array<[Sign, SignProfile]>
).map(([value, p]) => ({ value, label: p.name }));

export const PLACEMENT_LABEL: Record<Placement, string> = {
  sun: "Sun",
  moon: "Moon",
  rising: "Rising",
};

function isResolved(s: Selection): s is Sign {
  return Boolean(s) && s !== "unknown";
}

/* ---------- Reading shape ---------- */

export type PlacementSection = {
  placement: Placement;
  signKey: Sign;
  signName: string;
  anchor: string;
  text: string;
};

export type ReadingResult = {
  /** The named behavioral pattern that threads through synthesis/real-life/watch-point. */
  pattern: string;
  opening: string;
  placements: PlacementSection[];
  synthesis: string;
  realLife: string;
  watchPoint: string;
  closing: string;
  /** Used by the calculator to render the empty state. */
  partialNote?: string;
};

/* ---------- Pattern naming ---------- */

/**
 * Build the named pattern. Tension is the spine — two things in motion against
 * each other. Equilibrium is the failure mode. Same-sign overlap collapses into
 * a concentration phrase. Otherwise: surface vs interior, with the Sun's
 * identity inserted when there's no Rising to carry the surface.
 */
function buildPattern(
  selected: { sun?: Sign; moon?: Sign; rising?: Sign }
): string {
  const { sun, moon, rising } = selected;

  const allThreeSame =
    sun && moon && rising && sun === moon && moon === rising;
  if (allThreeSame) {
    return `concentrated ${SIGNS[sun!].sunAnchor}, fewer counterweights`;
  }

  const sunMoonSame = sun && moon && sun === moon;
  const sunRisingSame = sun && rising && sun === rising;
  const moonRisingSame = moon && rising && moon === rising;

  // Three placements — surface vs interior, primary tension is Rising vs Moon.
  if (sun && moon && rising) {
    if (sunRisingSame) {
      // Sun and Rising are the same gesture. Pattern shifts to identity vs interior.
      return `${SIGNS[sun].surface}, ${SIGNS[moon].interior}`;
    }
    if (moonRisingSame) {
      // Inside and outside running on the same channel. Tension lives in the Sun's drive.
      return `${SIGNS[rising].surface}, ${SIGNS[sun].identity}`;
    }
    if (sunMoonSame) {
      // Identity and inner regulation aligned. Tension is between that aligned inside and the Rising.
      return `${SIGNS[rising].surface}, ${SIGNS[moon].interior}`;
    }
    return `${SIGNS[rising].surface}, ${SIGNS[moon].interior}`;
  }

  // Two placements
  if (sun && moon) {
    if (sunMoonSame) return `concentrated ${SIGNS[sun].sunAnchor}`;
    return `${SIGNS[sun].identity}, ${SIGNS[moon].interior}`;
  }
  if (sun && rising) {
    if (sunRisingSame) return `${SIGNS[sun].surface}, same gesture inside`;
    return `${SIGNS[rising].surface}, ${SIGNS[sun].identity}`;
  }
  if (moon && rising) {
    if (moonRisingSame) return `${SIGNS[rising].surface}, same channel inside`;
    return `${SIGNS[rising].surface}, ${SIGNS[moon].interior}`;
  }

  // Single placement
  if (sun) return SIGNS[sun].identity;
  if (moon) return SIGNS[moon].interior;
  if (rising) return SIGNS[rising].surface;

  return "";
}

/* ---------- Opening frames ---------- */

function buildOpening(
  selected: { sun?: Sign; moon?: Sign; rising?: Sign },
  count: number
): string {
  if (count === 3) {
    return "With your Sun, Moon, and Rising selected, here's how the system reads. Three placements is enough to see the full operating system. Identity, inner regulation, arrival.";
  }

  if (count === 2) {
    const labels: string[] = [];
    if (selected.sun) labels.push("Sun");
    if (selected.moon) labels.push("Moon");
    if (selected.rising) labels.push("Rising");
    const pair = `${labels[0]} and ${labels[1]}`;

    if (selected.sun && selected.moon)
      return `With ${pair} selected, the read is on the inside of the system. Public direction and private regulation, without the way you arrive in the room.`;
    if (selected.sun && selected.rising)
      return `With ${pair} selected, the read is on identity and arrival. What you're moving toward and what people see on first contact.`;
    return `With ${pair} selected, the read is on inner regulation and outward presentation. The private system and the surface that meets the world.`;
  }

  // Single
  if (selected.sun)
    return "A single placement is one note, not the full chord. Your Sun reads as direction without inner texture or the way you arrive.";
  if (selected.moon)
    return "A single placement is one note, not the full chord. Your Moon reads as inner regulation without identity or arrival around it.";
  return "A single placement is one note, not the full chord. Your Rising reads as arrival without the inner system or identity behind it.";
}

/* ---------- Placements + same-sign repetition rules ---------- */

function buildPlacements(
  selected: { sun?: Sign; moon?: Sign; rising?: Sign }
): PlacementSection[] {
  const result: PlacementSection[] = [];
  const { sun, moon, rising } = selected;

  const allSame = sun && moon && rising && sun === moon && moon === rising;
  const sunMoonSame = sun && moon && sun === moon;
  const sunRisingSame = sun && rising && sun === rising;
  const moonRisingSame = moon && rising && moon === rising;

  if (sun) {
    const p = SIGNS[sun];
    result.push({
      placement: "sun",
      signKey: sun,
      signName: p.name,
      anchor: p.sunAnchor,
      text: p.sun,
    });
  }

  if (moon) {
    const p = SIGNS[moon];
    if (allSame) {
      result.push({
        placement: "moon",
        signKey: moon,
        signName: p.name,
        anchor: p.moonAnchor,
        text: `With Moon and Rising also in ${p.name}, this is a concentration chart. One frequency, very clearly. The strength is clarity. The cost is fewer internal counterweights, so the dominant pattern doesn't get balanced from inside the system itself.`,
      });
    } else if (sunMoonSame) {
      result.push({
        placement: "moon",
        signKey: moon,
        signName: p.name,
        anchor: p.moonAnchor,
        text: `With Moon also in ${p.name}, the inner experience matches the public direction. There's less internal contradiction, and less internal contrast to balance it.`,
      });
    } else {
      result.push({
        placement: "moon",
        signKey: moon,
        signName: p.name,
        anchor: p.moonAnchor,
        text: p.moon,
      });
    }
  }

  if (rising) {
    const p = SIGNS[rising];
    if (allSame) {
      // Rising is collapsed into the Moon section's concentration paragraph.
      // Skip rendering Rising as its own block.
    } else if (sunRisingSame) {
      result.push({
        placement: "rising",
        signKey: rising,
        signName: p.name,
        anchor: p.risingAnchor,
        text: `With Rising also in ${p.name}, the way you arrive and the way you operate are the same gesture. People are reading you accurately on first contact, which is rare.`,
      });
    } else if (moonRisingSame) {
      result.push({
        placement: "rising",
        signKey: rising,
        signName: p.name,
        anchor: p.risingAnchor,
        text: `With Moon also in ${p.name}, your private regulation and public presentation are running on the same channel. What's happening inside tends to be visible. ${p.rising}`,
      });
    } else {
      result.push({
        placement: "rising",
        signKey: rising,
        signName: p.name,
        anchor: p.risingAnchor,
        text: p.rising,
      });
    }
  }

  return result;
}

/* ---------- Element synthesis line (Section 6) ---------- */

function buildElementLine(
  sun: Sign,
  moon: Sign,
  rising: Sign
): string {
  const elements = [SIGNS[sun].element, SIGNS[moon].element, SIGNS[rising].element];
  const [a, b, c] = elements;
  const allSame = a === b && b === c;

  if (allSame) {
    if (a === "fire")
      return "All three placements run on momentum. The strength is initiative. The cost is outrunning your own foundation.";
    if (a === "earth")
      return "All three placements run on structure. The strength is reliability. The cost is resisting necessary change.";
    if (a === "air")
      return "All three placements run on concept. The strength is range. The cost is dissociation from body and feeling.";
    return "All three placements run on feeling. The strength is attunement. The cost is being flooded.";
  }

  return "Different parts of the system are asking for different types of movement, which is what gives the pattern its complexity.";
}

/* ---------- Synthesis ---------- */

function buildSynthesis(
  selected: { sun?: Sign; moon?: Sign; rising?: Sign },
  pattern: string
): string {
  const { sun, moon, rising } = selected;
  const count = [sun, moon, rising].filter(Boolean).length;

  // Single-placement readings — short, partial, still pattern-aware, still bridges to lived experience.
  if (count === 1) {
    if (sun) {
      const p = SIGNS[sun];
      return `On its own, this read is direction without inner texture. The pattern here is ${pattern}. In practice, that means the part of you that ${p.workBehavior.split(",")[0]} is visible, and the part that processes the cost of running that way isn't on the page yet.`;
    }
    if (moon) {
      return `On its own, this read is inner regulation without identity or arrival around it. The pattern here is ${pattern}. In practice, that means what soothes you and what destabilizes you are visible, and the way that shapes how you appear to the room isn't on the page yet.`;
    }
    return `On its own, this read is arrival without the inner system behind it. The pattern here is ${pattern}. In practice, that means the way you land in a room is visible, and what's actually running underneath that arrival isn't on the page yet.`;
  }

  // Two-placement readings
  if (count === 2) {
    if (sun && moon) {
      const s = SIGNS[sun];
      const m = SIGNS[moon];
      const aligned = s.element === m.element;
      const lead = aligned
        ? `Sun and Moon share an element, which means identity and inner regulation are aligned and unmoderated by their own contrast.`
        : `Sun and Moon are pulling in different directions, which means the public direction and the private regulation are doing different work.`;
      return `${lead} The pattern is ${pattern}. In practice, that means the way you operate in the world is one register and the way you metabolize the cost of operating that way is another, and the gap between those two is where most of your private negotiation happens. The third placement, Rising, would name how this internal pattern tends to arrive.`;
    }
    if (sun && rising) {
      const s = SIGNS[sun];
      const r = SIGNS[rising];
      const same = sun === rising;
      const lead = same
        ? `Sun and Rising are the same gesture, which is rare. The way you operate and the way you arrive are doing the same work.`
        : `Sun and Rising are doing different work. What you're moving toward and what people see on first contact aren't the same shape.`;
      return `${lead} The pattern is ${pattern}. In practice, that means the room reads ${r.surface} and finds, once it gets closer, ${s.identity} underneath that surface. The Moon would name what that's like to live inside.`;
    }
    // Moon + Rising
    const m = SIGNS[moon!];
    const r = SIGNS[rising!];
    const same = moon === rising;
    const lead = same
      ? `Moon and Rising are the same channel. Your private regulation and your public presentation are running together, which means what's happening inside tends to be visible.`
      : `Moon and Rising are two different signals. What soothes you privately and what people meet on the surface aren't running on the same channel.`;
    return `${lead} The pattern is ${pattern}. In practice, that means the surface is ${r.surface} and the recovery underneath that surface runs on ${m.interior}. The Sun would name the direction the picture is moving toward.`;
  }

  // Full Big Three
  const s = SIGNS[sun!];
  const m = SIGNS[moon!];
  const r = SIGNS[rising!];
  const allSame = sun === moon && moon === rising;
  const elementLine = buildElementLine(sun!, moon!, rising!);

  if (allSame) {
    return `These three placements run on a single frequency. ${elementLine} The pattern is ${pattern}. In practice, that means the way you operate, the way you process feeling, and the way you arrive are all the same gesture, which gives the system unusual coherence and removes the internal counterweights that would otherwise balance the dominant register from inside.`;
  }

  return `Together, these three placements form a system. The Sun is moving the picture toward ${s.identity}. The Moon is regulating it through ${m.interior}. The Rising is presenting it as ${r.surface}. ${elementLine} The pattern is ${pattern}. In practice, that means the room reads you as ${r.surface} and finds, once the interaction holds, that the inside is moving on a different timeline than the surface suggested.`;
}

/* ---------- Real-life pattern ---------- */

function buildRealLife(
  selected: { sun?: Sign; moon?: Sign; rising?: Sign }
): string {
  const { sun, moon, rising } = selected;

  // Friction lives in the Moon when present (it's where the system meets resistance from itself).
  // Otherwise pull friction from whichever placement is selected.
  const frictionSign = moon ?? sun ?? rising!;
  const frictionLine = SIGNS[frictionSign].frictionScene;

  // Relationship behavior: Moon if present, else Sun, else Rising.
  const relSign = moon ?? sun ?? rising!;
  const relLine = SIGNS[relSign].relationshipBehavior;

  // Work behavior: Sun if present, else Rising, else Moon.
  const workSign = sun ?? rising ?? moon!;
  const workLine = SIGNS[workSign].workBehavior;

  // Internal experience: Moon if present, else Sun, else Rising.
  const internalSign = moon ?? sun ?? rising!;
  const internalLine = SIGNS[internalSign].internalExperience;

  // Avoid stacking three sentences from the same sign on a single-placement read.
  const count = [sun, moon, rising].filter(Boolean).length;

  if (count === 1) {
    return `In relationships, ${relLine}. In work, ${workLine}. Internally, ${internalLine}. The friction shows up where ${frictionLine}.`;
  }

  return `In relationships, ${relLine}. In work, ${workLine}. Internally, ${internalLine}. The friction lives in the gap where ${frictionLine}.`;
}

/* ---------- Watch point ---------- */

function buildWatchPoint(
  selected: { sun?: Sign; moon?: Sign; rising?: Sign },
  pattern: string
): string {
  const { sun, moon, rising } = selected;

  // Watch scene: the shadow side of the same pattern.
  // Prefer Rising's watch scene when present (the surface is where the cost is most visible);
  // fall back to Moon, then Sun.
  const watchSign = rising ?? moon ?? sun!;
  const sceneLine = SIGNS[watchSign].watchScene;

  return `The shadow side of ${pattern} isn't fatal and isn't fixed. ${sceneLine.charAt(0).toUpperCase() + sceneLine.slice(1)}. This isn't a future caution. It's a present-tense behavior the system is already running.`;
}

/* ---------- Closing ---------- */

const CLOSING =
  "This is one lens, not the whole map. Aurelian reads patterns. The rest is yours.";

/* ---------- Public generator ---------- */

export function generateReading(
  sunSel: Selection,
  moonSel: Selection,
  risingSel: Selection
): ReadingResult | null {
  const sun = isResolved(sunSel) ? sunSel : undefined;
  const moon = isResolved(moonSel) ? moonSel : undefined;
  const rising = isResolved(risingSel) ? risingSel : undefined;

  const count = [sun, moon, rising].filter(Boolean).length;
  if (count === 0) return null;

  const selected = { sun, moon, rising };
  const pattern = buildPattern(selected);
  const opening = buildOpening(selected, count);
  const placements = buildPlacements(selected);
  const synthesis = buildSynthesis(selected, pattern);
  const realLife = buildRealLife(selected);
  const watchPoint = buildWatchPoint(selected, pattern);

  return {
    pattern,
    opening,
    placements,
    synthesis,
    realLife,
    watchPoint,
    closing: CLOSING,
  };
}

/* Backwards-compatible alias (some callers may still import). */
export type ReadingResultLegacy = ReadingResult;
