const username =
      document.body.dataset.username ||
      document.getElementById("playerName")?.textContent?.trim();

const heroImageMap = {
  "adam warlock": "AdamWarlock.png",
  "black panther": "BlackPanther.png",
  "black widow": "BlackWidow.png",
  "captain america": "CaptainAmerica.png",
  "cloak & dagger": "CloakandDagger.png",
  "doctor strange": "DoctorStrange.png",
  "emma frost": "EmmaFrost.png",
  "groot": "Groot.png",
  "hawkeye": "Hawkeye.png",
  "hela": "Hela.png",
  "hulk": "Hulk.png",
  "human torch": "HumanTorch.png",
  "invisible woman": "InvisibleWoman.png",
  "iron fist": "IronFist.png",
  "iron man": "IronMan.png",
  "jeff the land shark": "JefftheLandShark.png",
  "loki": "Loki.png",
  "luna snow": "LunaSnow.png",
  "magik": "Magik.png",
  "magneto": "Magneto.png",
  "mantis": "Mantis.png",
  "mister fantastic": "MisterFantastic.png",
  "moon knight": "MoonKnight.png",
  "namor": "Namor.png",
  "peni parker": "PeniParker.png",
  "psylocke": "Psylocke.png",
  "rocket raccoon": "RocketRaccoon.png",
  "scarlet witch": "ScarletWitch.png",
  "spider-man": "SpiderMan.png",
  "squirrel girl": "SquirrelGirl.png",
  "star-lord": "Star-Lord.png",
  "storm": "Storm.png",
  "the punisher": "ThePunisher.png",
  "the thing": "TheThing.png",
  "thor": "Thor.png",
  "venom": "Venom.png",
  "winter soldier": "WinterSoldier.png",
  "wolverine": "Wolverine.png",

};

const heroSrc = n =>
  `/static/styles/images/heroes/${heroImageMap[n.toLowerCase()] ?? "Unknown.png"}`;

const heroIdToName = {};
async function loadHeroCatalogue() {
  const r = await fetch("/api/heroes");
  (await r.json()).forEach(h => (heroIdToName[h.hero_id] = h.hero_name));
}

const modeName = id =>
  ({ 1: "Convergence", 2: "Domination", 3: "Convoy" }[id] || "Quick Match");

const mapDict = {
  1: "Central Park",
  2: "Royal Palace",
  3: "Midtown",
  4: "Symbiotic Surface",
  5: "Hall of Paiia",
  6: "Shin-Shibuya"
};
const mapName = id => mapDict[id] ?? null;

const kda = (k, d, a) => (d === 0 ? (k + a).toFixed(2) : ((k + a) / d).toFixed(2));

/* ---------- win detector ---------- */
const winCheck = (player, match) =>
  String(player.camp).toUpperCase() ===
  String(match.match_winner_side).toUpperCase();

/* ---------- heat-map bookkeeping ---------- */
const dailyCounts = {};
function bumpHeat(matches) {
  matches.forEach(m => {
    const k = new Date(m.match_time_stamp * 1000).toISOString().slice(0, 10);
    dailyCounts[k] = (dailyCounts[k] ?? 0) + 1;
  });
}
function drawHeat() {
  const grid = document.getElementById("heatmap-grid");
  grid.innerHTML = "";
  const today = new Date();
  for (let i = 59; i >= 0; i--) {
    const d = new Date(today);
    d.setDate(d.getDate() - i);
    const key = d.toISOString().slice(0, 10);
    const cnt = dailyCounts[key] ?? 0;
    const lvl = cnt === 0 ? 0 : cnt < 3 ? 1 : cnt < 6 ? 2 : cnt < 9 ? 3 : 4;
    const cell = document.createElement("div");
    cell.className = `heatmap-cell level-${lvl}`;
    cell.title = `${key}: ${cnt} match${cnt !== 1 ? "es" : ""}`;
    grid.appendChild(cell);
  }
}

/* ---------- per-day aggregation ---------- */
const dayContainers = {};
function getDayBlock(key, label) {
  if (dayContainers[key]) return dayContainers[key];

  const wrap = document.createElement("section");
  wrap.className = "match-day";

  const header = document.createElement("div");
  header.className = "match-date-header";
  header.innerHTML =
    `<span class="date-label">${label}</span>
     <span class="day-stats">0 W // 0 L · Avg KDA 0</span>`;
  wrap.appendChild(header);

  const bucket = document.createElement("div");
  bucket.className = "day-card-list";
  wrap.appendChild(bucket);

  list.insertBefore(wrap, sentinel);

  const stats = { w: 0, l: 0, k: 0, d: 0, a: 0, header };
  return (dayContainers[key] = { bucket, stats });
}
function updateDayStats(s, p, win) {
  win ? s.w++ : s.l++;
  s.k += p.kills;
  s.d += p.deaths;
  s.a += p.assists;
  const ratio = s.d === 0 ? s.k + s.a : (s.k + s.a) / s.d;
  s.header.querySelector(".day-stats").textContent =
    `${s.w} W // ${s.l} L · Avg KDA ${ratio.toFixed(2)}`;
}

/* ---------- compact card template ---------- */
function cardFor(match) {
  const p = match.match_player;
  const hero =
    p.player_hero
      ? p.player_hero.hero_name
      : heroIdToName[p.player_hero?.hero_id] ?? "Unknown";
  const img = heroSrc(hero);
  const win = winCheck(p, match);

  const card = document.createElement("div");
  card.className = "match-card--compact";

  /* portrait */
  const pic = document.createElement("img");
  pic.className = "hero-thumb";
  pic.src = img;
  pic.alt = hero;
  card.appendChild(pic);

  /* meta */
  const meta = document.createElement("div");
  meta.className = "match-meta";

  const ts = new Date(match.match_time_stamp * 1000).toLocaleString(undefined, {
    month: "short",
    day: "numeric",
    hour: "2-digit",
    minute: "2-digit"
  });
  const map = mapName(match.match_map_id);

  meta.innerHTML = `
    <div class="meta-row mode-map">
      ${modeName(match.game_mode_id)}${map ? ` • ${map}` : ""} • ${ts}
    </div>

    <div class="meta-row kda-row">
      <span>Kills ${p.kills}</span>
      <span>Deaths ${p.deaths}</span>
      <span>Assists ${p.assists}</span>
      <span>KDA ${kda(p.kills,p.deaths,p.assists)}</span>
    </div>

    <div class="meta-row dmg-row">
      <span>Damage ${Math.round(p.player_hero?.total_hero_damage ?? 0).toLocaleString()}</span>
      <span>Healing ${Math.round(p.player_hero?.total_hero_heal ?? 0).toLocaleString()}</span>
      <span>Blocked ${Math.round(
        p.player_hero?.total_hero_blocked ??
          p.player_hero?.total_damage_taken ??
          0
      ).toLocaleString()}</span>
    </div>`;
  card.appendChild(meta);

  /* result pill */
  const pill = document.createElement("div");
  pill.className = `result-pill ${win ? "victory" : "defeat"}`;
  pill.textContent = win ? "Victory" : "Defeat";
  card.appendChild(pill);

  return { card, win };
}

let nextSkip = 0,
  loading = false;
const PAGE = 20;

/* 4 shimmer placeholders */
function showPH() {
  for (let i = 0; i < 4; i++) {
    const ph = document.createElement("div");
    ph.className = "match-card--compact placeholder";
    list.insertBefore(ph, sentinel);
    placeholders.push(ph);
  }
}
function hidePH() {
  placeholders.splice(0).forEach(p => p.remove());
}
const placeholders = [];

async function fetchPage() {
  loading = true;
  showPH();
  const r = await fetch(`/api/player/${username}/matches?skip=${nextSkip}`);
  hidePH();
  loading = false;
  if (!r.ok) throw new Error(r.statusText);
  nextSkip += PAGE;
  return (await r.json()).match_history ?? [];
}

/* ---------- render pipeline ---------- */
const list = document.getElementById("matches");
const sentinel = document.createElement("div");
sentinel.id = "scroll-sentinel";
list.appendChild(sentinel);

async function loadMore() {
  if (loading) return;
  try {
    const rows = await fetchPage();
    if (!rows.length) {
      observer.disconnect();
      return;
    }

    bumpHeat(rows);
    drawHeat();

    rows.forEach(row => {
      const d = new Date(row.match_time_stamp * 1000);
      const key = d.toISOString().slice(0, 10);
      const label = d.toLocaleDateString(undefined, { month: "long", day: "numeric" });
      const { bucket, stats } = getDayBlock(key, label);

      const { card, win } = cardFor(row);
      bucket.appendChild(card);
      updateDayStats(stats, row.match_player, win);
    });
  } catch (e) {
    console.error(e);
  }
}

/* ---------- infinite scroll ---------- */
const observer = new IntersectionObserver(
  e => {
    if (e[0].isIntersecting) loadMore();
  },
  { threshold: 0.1 }
);

/* ---------- boot ---------- */
(async () => {
  await loadHeroCatalogue();
  await loadMore();
  observer.observe(sentinel);
})();
