function toggleStats(card) {
    const statsTile = card.nextElementSibling;
    card.classList.toggle('open');
    statsTile.classList.toggle('show');
}

function toggleExpandAll(button) {
    const openAll = button.dataset.state !== 'open';

    const allCards = document.querySelectorAll('.hero-card');
    allCards.forEach(card => {
        const statsTile = card.nextElementSibling; 
        card.classList.toggle('open', openAll);
        statsTile.classList.toggle('show', openAll);
    });

    button.textContent = openAll ? 'Collapse All' : 'Expand All';
    button.dataset.state = openAll ? 'open' : 'closed';
}
