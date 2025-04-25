
const overallStats = {
  user: {"KDA Ratio": 4.05, "Kills": 16665, "Deaths": 6826, "Assists": 15171, "Damage": 785500, "Healing": 69232, "Damage Blocked": 280571, "Max Kill Streak": 28, "MVPs": 73, "SVPs": 191},
  friend: {"KDA Ratio": 2.13, "Kills": 12282, "Deaths": 14443, "Assists": 17048, "Damage": 685096, "Healing": 340489, "Damage Blocked": 227136, "Max Kill Streak": 41, "MVPs": 159, "SVPs": 20}
};

const statNames = Object.keys(overallStats.user);

const heroNames = ["Adam Warlock", "Black Panther", "Black Widow", "Captain America", "Cloak and Dagger", "Doctor Strange", "Emma Frost", "Groot", "Hawkeye", "Hela", "Hulk", "Human Torch", "Invisible Woman", "Iron Fist", "Iron Man", "Jeff the Land Shark", "Loki", "Luna Snow", "Magik", "Magneto", "Mantis", "Mister Fantastic", "Moon Knight", "Namor", "Peni Parker", "Psylocke", "The Punisher", "The Thing", "Rocket Raccoon", "Scarlet Witch", "Squirrel Girl", "Spider-Man", "Star-Lord", "Storm", "Thor", "Venom", "Winter Soldier", "Wolverine"];
const heroStats = {
  user: {"Adam Warlock": {"Matches": 84, "WinPct": 65.3, "KDA": 1.6}, "Black Panther": {"Matches": 147, "WinPct": 57.9, "KDA": 8.9}, "Black Widow": {"Matches": 158, "WinPct": 79.8, "KDA": 7.5}, "Captain America": {"Matches": 69, "WinPct": 70.5, "KDA": 7.0}, "Cloak and Dagger": {"Matches": 128, "WinPct": 80.6, "KDA": 1.1}, "Doctor Strange": {"Matches": 40, "WinPct": 41.3, "KDA": 8.9}, "Emma Frost": {"Matches": 83, "WinPct": 63.1, "KDA": 8.2}, "Groot": {"Matches": 151, "WinPct": 77.9, "KDA": 2.2}, "Hawkeye": {"Matches": 162, "WinPct": 38.4, "KDA": 9.5}, "Hela": {"Matches": 153, "WinPct": 36.8, "KDA": 8.6}, "Hulk": {"Matches": 173, "WinPct": 69.7, "KDA": 4.9}, "Human Torch": {"Matches": 39, "WinPct": 51.3, "KDA": 5.5}, "Invisible Woman": {"Matches": 120, "WinPct": 42.1, "KDA": 7.2}, "Iron Fist": {"Matches": 172, "WinPct": 83.1, "KDA": 9.6}, "Iron Man": {"Matches": 112, "WinPct": 67.1, "KDA": 7.9}, "Jeff the Land Shark": {"Matches": 41, "WinPct": 65.2, "KDA": 3.4}, "Loki": {"Matches": 94, "WinPct": 45.4, "KDA": 7.4}, "Luna Snow": {"Matches": 90, "WinPct": 60.7, "KDA": 8.1}, "Magik": {"Matches": 135, "WinPct": 54.0, "KDA": 3.2}, "Magneto": {"Matches": 153, "WinPct": 66.9, "KDA": 6.1}, "Mantis": {"Matches": 96, "WinPct": 59.0, "KDA": 6.4}, "Mister Fantastic": {"Matches": 137, "WinPct": 42.6, "KDA": 5.3}, "Moon Knight": {"Matches": 105, "WinPct": 40.5, "KDA": 5.2}, "Namor": {"Matches": 89, "WinPct": 69.5, "KDA": 8.6}, "Peni Parker": {"Matches": 23, "WinPct": 75.7, "KDA": 2.5}, "Psylocke": {"Matches": 33, "WinPct": 55.6, "KDA": 7.6}, "The Punisher": {"Matches": 183, "WinPct": 84.4, "KDA": 2.9}, "The Thing": {"Matches": 134, "WinPct": 44.5, "KDA": 1.4}, "Rocket Raccoon": {"Matches": 76, "WinPct": 69.1, "KDA": 7.5}, "Scarlet Witch": {"Matches": 39, "WinPct": 45.5, "KDA": 1.5}, "Squirrel Girl": {"Matches": 141, "WinPct": 75.8, "KDA": 8.6}, "Spider-Man": {"Matches": 135, "WinPct": 39.4, "KDA": 4.8}, "Star-Lord": {"Matches": 144, "WinPct": 76.5, "KDA": 3.2}, "Storm": {"Matches": 21, "WinPct": 75.5, "KDA": 9.8}, "Thor": {"Matches": 63, "WinPct": 64.4, "KDA": 5.8}, "Venom": {"Matches": 32, "WinPct": 76.2, "KDA": 5.1}, "Winter Soldier": {"Matches": 141, "WinPct": 50.2, "KDA": 4.5}, "Wolverine": {"Matches": 57, "WinPct": 49.6, "KDA": 2.8}},
  friend: {"Adam Warlock": {"Matches": 25, "WinPct": 51.9, "KDA": 9.1}, "Black Panther": {"Matches": 124, "WinPct": 39.3, "KDA": 8.9}, "Black Widow": {"Matches": 60, "WinPct": 61.9, "KDA": 3.0}, "Captain America": {"Matches": 68, "WinPct": 56.0, "KDA": 7.5}, "Cloak and Dagger": {"Matches": 59, "WinPct": 54.3, "KDA": 3.2}, "Doctor Strange": {"Matches": 157, "WinPct": 62.5, "KDA": 7.3}, "Emma Frost": {"Matches": 165, "WinPct": 68.9, "KDA": 9.6}, "Groot": {"Matches": 104, "WinPct": 70.6, "KDA": 3.2}, "Hawkeye": {"Matches": 198, "WinPct": 37.9, "KDA": 2.3}, "Hela": {"Matches": 24, "WinPct": 72.6, "KDA": 2.0}, "Hulk": {"Matches": 139, "WinPct": 76.2, "KDA": 5.3}, "Human Torch": {"Matches": 170, "WinPct": 50.9, "KDA": 1.4}, "Invisible Woman": {"Matches": 64, "WinPct": 35.9, "KDA": 4.0}, "Iron Fist": {"Matches": 129, "WinPct": 77.1, "KDA": 6.2}, "Iron Man": {"Matches": 24, "WinPct": 44.4, "KDA": 5.5}, "Jeff the Land Shark": {"Matches": 158, "WinPct": 74.9, "KDA": 5.6}, "Loki": {"Matches": 25, "WinPct": 42.9, "KDA": 6.9}, "Luna Snow": {"Matches": 68, "WinPct": 51.3, "KDA": 7.4}, "Magik": {"Matches": 148, "WinPct": 80.0, "KDA": 8.4}, "Magneto": {"Matches": 30, "WinPct": 74.2, "KDA": 8.8}, "Mantis": {"Matches": 110, "WinPct": 54.2, "KDA": 9.6}, "Mister Fantastic": {"Matches": 130, "WinPct": 58.6, "KDA": 7.5}, "Moon Knight": {"Matches": 146, "WinPct": 73.5, "KDA": 8.5}, "Namor": {"Matches": 112, "WinPct": 63.6, "KDA": 6.4}, "Peni Parker": {"Matches": 59, "WinPct": 46.5, "KDA": 9.3}, "Psylocke": {"Matches": 180, "WinPct": 68.5, "KDA": 3.5}, "The Punisher": {"Matches": 48, "WinPct": 35.0, "KDA": 7.6}, "The Thing": {"Matches": 199, "WinPct": 68.2, "KDA": 8.3}, "Rocket Raccoon": {"Matches": 101, "WinPct": 79.4, "KDA": 2.0}, "Scarlet Witch": {"Matches": 196, "WinPct": 67.6, "KDA": 2.2}, "Squirrel Girl": {"Matches": 137, "WinPct": 52.0, "KDA": 9.1}, "Spider-Man": {"Matches": 136, "WinPct": 49.3, "KDA": 7.3}, "Star-Lord": {"Matches": 96, "WinPct": 52.4, "KDA": 7.7}, "Storm": {"Matches": 45, "WinPct": 62.5, "KDA": 2.4}, "Thor": {"Matches": 169, "WinPct": 73.3, "KDA": 8.0}, "Venom": {"Matches": 61, "WinPct": 61.4, "KDA": 8.6}, "Winter Soldier": {"Matches": 189, "WinPct": 45.4, "KDA": 3.2}, "Wolverine": {"Matches": 191, "WinPct": 64.5, "KDA": 8.1}}
};

const roleNames = ["Vanguard","Duelist","Support"];
const roleStats = {
  user: {"Vanguard": {"Matches": 362, "WinPct": 49.4, "KDA": 6.5}, "Duelist": {"Matches": 78, "WinPct": 40.8, "KDA": 7.1}, "Support": {"Matches": 360, "WinPct": 39.2, "KDA": 6.6}},
  friend: {"Vanguard": {"Matches": 497, "WinPct": 51.9, "KDA": 2.9}, "Duelist": {"Matches": 302, "WinPct": 42.6, "KDA": 3.1}, "Support": {"Matches": 316, "WinPct": 43.8, "KDA": 7.6}}
};

const fmt = new Intl.NumberFormat();

// ----------------- Overall -----------------
function buildOverallBox(titleText, data, compare){
  const box=document.createElement('div');
  box.className='stat-box overall-box';
  const title=document.createElement('div');
  title.className='stat-title';
  title.textContent=titleText;
  box.appendChild(title);

  statNames.forEach(stat=>{
    const row=document.createElement('div');
    row.className='stat-row';

    const label=document.createElement('span');
    label.className='stat-label';
    label.textContent=stat;
    row.appendChild(label);

    const val=document.createElement('span');
    val.className='stat-value';
    val.textContent=fmt.format(data[stat]);

    const lowerBetter = (stat==='Deaths');
    if(lowerBetter ? data[stat] < compare[stat] : data[stat] > compare[stat]){
      val.classList.add('highlight');
    }

    row.appendChild(val);
    box.appendChild(row);
  });
  return box;
}

function renderOverall(){
  const wrap=document.createElement('div');
  wrap.className='overall-flex';
  wrap.appendChild(buildOverallBox('You', overallStats.user, overallStats.friend));
  wrap.appendChild(buildOverallBox('Jordan', overallStats.friend, overallStats.user));
  return wrap;
}

// --------- Heroes / Roles ----------
function buildRoster(namesArr, statsUser, statsFriend, listTitle){
  const container=document.createElement('div');
  container.className='roster-flex';

  // list column
  const listBox=document.createElement('div');
  listBox.className='stat-box roster-list';
  const lt=document.createElement('div');
  lt.className='stat-title';
  lt.textContent=listTitle;
  listBox.appendChild(lt);

  namesArr.forEach(name=>{
    const item=document.createElement('div');
    item.className='roster-item';
    item.textContent=name;
    listBox.appendChild(item);
  });
  container.appendChild(listBox);

  // Function to make side column
  function makeSide(titleArr, statsObj, compareObj){
    const side=document.createElement('div');
    side.className='stat-box roster-side';

    // header row
    const header=document.createElement('div');
    header.className='roster-header';
    titleArr.forEach(t=>{
      const h=document.createElement('span');
      h.textContent=t;
      h.className='sub-head';
      header.appendChild(h);
    });
    side.appendChild(header);

    // rows
    namesArr.forEach(name=>{
      const row=document.createElement('div');
      row.className='roster-row';

      ['Matches','WinPct','KDA'].forEach(key=>{
        const cell=document.createElement('span');
        cell.className='sub-stat';
        let val=statsObj[name][key];
        if(key==='Matches') val=fmt.format(val);
        cell.textContent=val;

        if(statsObj[name][key] > compareObj[name][key]){
          cell.classList.add('highlight');
        }
        row.appendChild(cell);
      });
      side.appendChild(row);
    });
    return side;
  }

  const titles=['Matches','Win %','KDA'];
  container.appendChild(makeSide(titles, statsUser, statsFriend));
  container.appendChild(makeSide(titles, statsFriend, statsUser));

  return container;
}

function renderHeroes(){
  return buildRoster(heroNames, heroStats.user, heroStats.friend, 'Heroes');
}

function renderRoles(){
  return buildRoster(roleNames, roleStats.user, roleStats.friend, 'Class');
}

// ---------------- Tab handling -----------------
function clearContent(){ document.querySelector('.content-area').innerHTML=''; }

function renderTab(tab){
  clearContent();
  const area=document.querySelector('.content-area');
  if(tab==='Overall') area.appendChild(renderOverall());
  else if(tab==='Heroes') area.appendChild(renderHeroes());
  else if(tab==='Roles') area.appendChild(renderRoles());
}

document.addEventListener('DOMContentLoaded', ()=>{
  document.querySelectorAll('.tab').forEach(btn=>{
    btn.addEventListener('click', ()=>{
      document.querySelectorAll('.tab').forEach(b=>b.classList.remove('active'));
      btn.classList.add('active');
      renderTab(btn.textContent);
    });
  });
  renderTab('Overall');
});
