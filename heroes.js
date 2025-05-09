function toggleStats(heroItem) {
    const stats = heroItem.querySelector('.hero-stats');
    heroItem.classList.toggle('open');
    stats.classList.toggle('show');
}

let allExpanded = false; 

function toggleExpandAll() {
    const heroes = document.querySelectorAll('.hero-item');
    heroes.forEach(hero => {
        if (allExpanded) {
            hero.classList.remove('open');
            hero.querySelector('.hero-stats').classList.remove('show');
        } else {
            hero.classList.add('open');
            hero.querySelector('.hero-stats').classList.add('show');
        }
    });
    
    allExpanded = !allExpanded;

    const button = document.getElementById('expand-button');
    button.textContent = allExpanded ? "Collapse All" : "Expand All";
}
