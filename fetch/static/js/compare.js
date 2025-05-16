function getQueryParam(param) {
  const urlParams = new URLSearchParams(window.location.search);
  return urlParams.get(param);
}

document.addEventListener('DOMContentLoaded', () => {
  const friendSelect = document.querySelector('.friend-dropdown select');
  const selectedFriend = getQueryParam('friend');

  if (selectedFriend && friendSelect) {
    friendSelect.value = selectedFriend;
    friendSelect.dispatchEvent(new Event('change'));
  }
});

// -------- Stats Injection --------

const overallStats = {
  user: {
    "KDA Ratio": userStatsFromFlask.kda,
    "Kills": userStatsFromFlask.kills,
    "Deaths": userStatsFromFlask.deaths,
    "Assists": userStatsFromFlask.assists,
    "Damage": userStatsFromFlask.damage,
    "Healing": userStatsFromFlask.healing,
    "Damage Blocked": userStatsFromFlask.blocked,
    "SVPs": userStatsFromFlask.svps
  },
  friend: {
    "KDA Ratio": friendStatsFromFlask.kda,
    "Kills": friendStatsFromFlask.kills,
    "Deaths": friendStatsFromFlask.deaths,
    "Assists": friendStatsFromFlask.assists,
    "Damage": friendStatsFromFlask.damage,
    "Healing": friendStatsFromFlask.healing,
    "Damage Blocked": friendStatsFromFlask.blocked,
    "SVPs": friendStatsFromFlask.svps
  }
};

const heroStats = {
  user: userHeroStatsFromFlask || {},
  friend: friendHeroStatsFromFlask || {}
};

const heroNames = Object.keys(heroStats.user || {});

// 🔒 These are still hardcoded for now
const roleNames = ["Vanguard", "Duelist", "Support"];
const roleStats = {
  user: {
    "Vanguard": { "Matches": 362, "WinPct": 49.4, "KDA": 6.5 },
    "Duelist": { "Matches": 78, "WinPct": 40.8, "KDA": 7.1 },
    "Support": { "Matches": 360, "WinPct": 39.2, "KDA": 6.6 }
  },
  friend: {
    "Vanguard": { "Matches": 497, "WinPct": 51.9, "KDA": 2.9 },
    "Duelist": { "Matches": 302, "WinPct": 42.6, "KDA": 3.1 },
    "Support": { "Matches": 316, "WinPct": 43.8, "KDA": 7.6 }
  }
};

const fmt = new Intl.NumberFormat();
const params = new URLSearchParams(window.location.search);
const selectedFriend = params.get("friend") || "Sp1dermain";

// -------- Helpers --------

function shortenName(name, maxLength = 12) {
  return name.length > maxLength ? name.slice(0, maxLength - 1) + "…" : name;
}

// -------- Rendering --------

const statNames = Object.keys(overallStats.user);

function buildOverallBox(titleText, data, compare) {
  const box = document.createElement('div');
  box.className = 'stat-box overall-box';

  const title = document.createElement('div');
  title.className = 'stat-title';
  title.textContent = titleText;
  box.appendChild(title);

  statNames.forEach(stat => {
    const row = document.createElement('div');
    row.className = 'stat-row';

    const label = document.createElement('span');
    label.className = 'stat-label';
    label.textContent = stat;
    row.appendChild(label);

    const val = document.createElement('span');
    val.className = 'stat-value';
    val.textContent = fmt.format(data[stat]);

    const lowerBetter = (stat === 'Deaths');
    if (lowerBetter ? data[stat] < compare[stat] : data[stat] > compare[stat]) {
      val.classList.add('highlight');
    }

    row.appendChild(val);
    box.appendChild(row);
  });

  return box;
}

function renderOverall() {
  const wrap = document.createElement('div');
  wrap.className = 'overall-flex';
  wrap.appendChild(buildOverallBox('You', overallStats.user, overallStats.friend));
  wrap.appendChild(buildOverallBox(shortenName(selectedFriend), overallStats.friend, overallStats.user));
  return wrap;
}

function buildRoster(namesArr, statsUser, statsFriend, listTitle) {
  const container = document.createElement('div');
  container.className = 'roster-flex';

  const listBox = document.createElement('div');
  listBox.className = 'stat-box roster-list';
  const lt = document.createElement('div');
  lt.className = 'stat-title';
  lt.textContent = listTitle;
  listBox.appendChild(lt);

  namesArr.forEach(name => {
    const item = document.createElement('div');
    item.className = 'roster-item';
    item.textContent = name;
    listBox.appendChild(item);
  });
  container.appendChild(listBox);

  function makeSide(titleArr, statsObj, compareObj) {
    const side = document.createElement('div');
    side.className = 'stat-box roster-side';

    const header = document.createElement('div');
    header.className = 'roster-header';
    titleArr.forEach(t => {
      const h = document.createElement('span');
      h.textContent = t;
      h.className = 'sub-head';
      header.appendChild(h);
    });
    side.appendChild(header);

    namesArr.forEach(name => {
      const row = document.createElement('div');
      row.className = 'roster-row';

      ['Matches', 'WinPct', 'KDA'].forEach(key => {
        const cell = document.createElement('span');
        cell.className = 'sub-stat';

        let val = statsObj[name]?.[key] ?? 0;
        let compareVal = compareObj[name]?.[key] ?? 0;

        if (key === 'Matches') val = fmt.format(val);
        cell.textContent = val;

        if (val > compareVal) {
          cell.classList.add('highlight');
        }

        row.appendChild(cell);
      });

      side.appendChild(row);
    });

    return side;
  }

  const titles = ['Matches', 'Win %', 'KDA'];
  container.appendChild(makeSide(titles, statsUser, statsFriend));
  container.appendChild(makeSide(titles, statsFriend, statsUser));

  return container;
}

function renderHeroes() {
  return buildRoster(heroNames, heroStats.user, heroStats.friend, 'Heroes');
}

function renderRoles() {
  return buildRoster(roleNames, roleStats.user, roleStats.friend, 'Class');
}

function clearContent() {
  document.querySelector('.content-area').innerHTML = '';
}

function renderTab(tab) {
  clearContent();
  const area = document.querySelector('.content-area');
  if (tab === 'Overall') area.appendChild(renderOverall());
  else if (tab === 'Heroes') area.appendChild(renderHeroes());
  else if (tab === 'Roles') area.appendChild(renderRoles());
}

// -------- Tab Events --------

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.tab').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      renderTab(btn.textContent);
    });
  });

  renderTab('Overall');

  const vsSpans = document.querySelectorAll(".player .name");
  if (vsSpans.length > 1) {
    vsSpans[1].textContent = shortenName(selectedFriend);
  }

  const friendDropdown = document.querySelector(".friend-dropdown select");
  if (friendDropdown) {
    for (let option of friendDropdown.options) {
      if (option.value === selectedFriend || option.textContent === selectedFriend) {
        option.selected = true;
        break;
      }
    }
  }

  const friendSelect = document.querySelector('.friend-dropdown select');
  if (friendSelect) {
    friendSelect.addEventListener('change', function () {
      const selected = this.value;
      const base = window.location.pathname;
      window.location.href = `${base}?friend=${encodeURIComponent(selected)}`;
    });
  }
});
