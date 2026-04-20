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
const categoryBtnContainer = document.querySelector('.category_btn_container');
const valueContainer = document.querySelector('.value_container');
const nameInput = document.querySelector('.name_input');
const transactionTypeSelect = document.querySelector('.transaction_type_select');
const sentTransactionBtn = document.querySelector('#sent-transaction-btn');
const addNewCategoryContainer = document.querySelector('.add-new-category-container');

function openCategoryModal() {
    if (modal) {
        modal.style.display = 'block';
        categoryBtnContainer ? categoryBtnContainer.style.display = 'none' : null;
        valueContainer ? valueContainer.style.display = 'none' : null;
        nameInput ? nameInput.style.display = 'none' : null;
        transactionTypeSelect ? transactionTypeSelect.style.display = 'none' : null;
        sentTransactionBtn ? sentTransactionBtn.style.display = 'none' : null;
        addNewCategoryContainer ? addNewCategoryContainer.style.display = 'none' : null;
    }

    if (pageTitle) {
        pageTitle.textContent = 'Selecionar Categoria';
    }

    const backBtn = document.getElementById('back-button-link');
    if (backBtn) {
        backBtn.setAttribute('href', '#'); //corrigir isso depois
        backBtn.onclick = function () {
            modal.style.display = 'none';
            pageTitle.textContent = 'Criar Transação';
            categoryBtnContainer ? categoryBtnContainer.style.display = 'flex' : null;
            valueContainer ? valueContainer.style.display = 'block' : null;
            nameInput ? nameInput.style.display = 'block' : null;
            transactionTypeSelect ? transactionTypeSelect.style.display = 'block' : null;
            sentTransactionBtn ? sentTransactionBtn.style.display = 'block' : null;
            addNewCategoryContainer ? addNewCategoryContainer.style.display = 'none' : null;
        };
    }

}

function selectCategory(categoryValue, categoryLabel) {
    if (modal) {
        modal.style.display = 'none';
        pageTitle.textContent = 'Criar Transação';
        categoryBtnContainer ? categoryBtnContainer.style.display = 'flex' : null;
        valueContainer ? valueContainer.style.display = 'block' : null;
        nameInput ? nameInput.style.display = 'block' : null;
        transactionTypeSelect ? transactionTypeSelect.style.display = 'block' : null;
        sentTransactionBtn ? sentTransactionBtn.style.display = 'block' : null;
        addNewCategoryContainer ? addNewCategoryContainer.style.display = 'none' : null;
    }

    const hiddenCategoryInput = document.getElementById('selected-category');
    if (hiddenCategoryInput) {
        hiddenCategoryInput.value = categoryValue;
    }

    const categoryBtn = document.getElementById('category-btn');
    if (categoryBtn) {
        categoryBtn.innerHTML = `<p>${categoryLabel}</p><span class="edit-icon">></span>`;
    }
}


function openCreateCategory() {
    if (addNewCategoryContainer) {
        addNewCategoryContainer.style.display = 'block';

        if (modal) {
            modal.style.display = 'none';
            
        }
    }
    //add o restante
}