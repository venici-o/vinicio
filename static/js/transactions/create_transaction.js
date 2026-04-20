(function () {
    const input = document.getElementById('value-input');
    if (!input) return;

    input.addEventListener('input', function () {
        let raw = this.value.replace(/[^\d,]/g, '');
        const parts = raw.split(',');
        let intPart = parts[0].replace(/^0+(?=\d)/, '');
        const decPart = parts.length > 1 ? ',' + parts[1].slice(0, 2) : '';
        intPart = intPart.replace(/\B(?=(\d{3})+(?!\d))/g, '.');
        this.value = intPart + decPart;
    });

    input.closest('form').addEventListener('submit', function () {
        input.value = input.value.replace(/\./g, '');
    });
}());

const modal = document.getElementById('category-modal');
const pageTitle = document.querySelector('h2');

function openCategoryModal() {
    if (modal) {
        modal.style.display = 'block';
    }

    if (pageTitle) {
        pageTitle.textContent = 'Selecionar Categoria';
    }

    const backBtn = document.getElementById('back-btn');
    if (backBtn) {
        backBtn.onclick = function () {
            modal.style.display = 'none';
            console.log('botao clicado')
            pageTitle.textContent = 'Criar Transação';
            console.log(pageTitle.textContent)
        };
    }

}

function selectCategory(categoryValue, categoryLabel) {
    if (modal) {
        modal.style.display = 'none';
        pageTitle.textContent = 'Criar Transação';
    }

    const hiddenCategoryInput = document.getElementById('selected-category');
    if (hiddenCategoryInput) {
        hiddenCategoryInput.value = categoryValue;
    }

    const categoryBtn = document.getElementById('category-btn');
    if (categoryBtn) {
        categoryBtn.innerHTML = `<p>${categoryLabel}</p>`;
    }
}

