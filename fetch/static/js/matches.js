const username = document.getElementById("playerName")?.textContent?.trim();

// Map hero names to image filenames
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
  "wolverine": "Wolverine.png"
};

function getHeroImagePath(heroNameRaw) {
  const heroName = heroNameRaw.trim().toLowerCase();
  const filename = heroImageMap[heroName];
  if (!filename) {
    return "/static/styles/images/hero_placeholder.png";
  }
  return `/static/styles/images/heroes/${filename}`;
}

const heroMap = {};

async function loadHeroes() {
  const res = await fetch("/api/heroes");
  const heroes = await res.json();
  heroes.forEach(h => heroMap[h.hero_id] = h.hero_name);
}

function formatDate(ts) {
  const options = { month: 'short', day: 'numeric' };
  return new Date(ts * 1000).toLocaleDateString(undefined, options);
}

function groupMatchesByDate(matchHistory) {
  const dailyMap = {};
  matchHistory.forEach(match => {
    const date = new Date(match.match_time_stamp * 1000);
    const key = date.toISOString().split("T")[0]; // YYYY-MM-DD
    dailyMap[key] = (dailyMap[key] || 0) + 1;
  });
  return dailyMap;
}

function renderHeatmap(dailyCounts) {
  const heatmap = document.getElementById("heatmap-grid");
  const today = new Date();

  for (let i = 59; i >= 0; i--) {
    const day = new Date(today);
    day.setDate(day.getDate() - i);
    const key = day.toISOString().split("T")[0];
    const count = dailyCounts[key] || 0;

    let level = 0;
    if (count >= 9) level = 4;
    else if (count >= 6) level = 3;
    else if (count >= 3) level = 2;
    else if (count >= 1) level = 1;

    const cell = document.createElement("div");
    cell.className = `heatmap-cell level-${level}`;
    cell.title = `${key}: ${count} match${count !== 1 ? "es" : ""}`;
    heatmap.appendChild(cell);
  }
}

async function loadMatches() {
  const res = await fetch(`/api/player/${username}/matches`);
  const data = await res.json();
  const container = document.getElementById("matches");

  if (!data.match_history) {
    container.innerHTML = "No match history.";
    return;
  }

  const dailyCounts = groupMatchesByDate(data.match_history);
  renderHeatmap(dailyCounts);

  const grouped = {};
  data.match_history.forEach(match => {
    const dateKey = formatDate(match.match_time_stamp);
    if (!grouped[dateKey]) grouped[dateKey] = [];
    grouped[dateKey].push(match);
  });

  Object.keys(grouped).forEach(date => {
    const matches = grouped[date];
    const wins = matches.filter(m => {
      const p = m.match_player;
      return p.camp && m.match_winner_side && p.camp === m.match_winner_side;
    }).length;

    const losses = matches.length - wins;

    const dayBlock = document.createElement("div");
    dayBlock.className = "match-day";

    const header = document.createElement("div");
    header.className = "match-date-header";
    header.innerHTML = `<span>${date}</span><span class="daily-summary">${wins} W // ${losses} L</span>`;
    dayBlock.appendChild(header);

    matches.forEach(match => {
      const player = match.match_player;
      const heroName = player.player_hero ? player.player_hero.hero_name : "Unknown";
      const isWin = player.camp && match.match_winner_side && player.camp === match.match_winner_side ? "Victory" : "Defeat";
      const kda = `${player.kills}/${player.deaths}/${player.assists}`;
      const scoreInfo = player.score_info;
      let rs = scoreInfo ? (scoreInfo.add_score || "Not Available") : "Not Available";
      if (typeof rs === "number") rs = Math.round(rs);
      const dateTime = new Date(match.match_time_stamp * 1000).toLocaleString();

      const matchCard = document.createElement("div");
      matchCard.className = "match-card";
      matchCard.innerHTML = `
        <div class="hero-image-container">
          <img loading="lazy" src="${getHeroImagePath(heroName)}" alt="${heroName}">
          <div class="hero-name">${heroName}</div>
          <div class="kda">K/D/A: ${kda}</div>
        </div>
        <div class="match-details">
          <div class="match-meta">
            <p>RS Change: ${rs}</p>
            <p>Date: ${dateTime}</p>
          </div>
          <div class="result ${isWin === "Victory" ? 'win' : 'loss'}">${isWin}</div>
        </div>
      `;
      dayBlock.appendChild(matchCard);
    });

    container.appendChild(dayBlock);
  });
}

(async () => {
  await loadHeroes();
  await loadMatches();
})();
