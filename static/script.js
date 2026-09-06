// Flash მესიჯების ავტომატური გაქრობა 5 წამში
document.querySelectorAll('.alert').forEach(
    (alert) => setTimeout(() => alert.remove(), 5000)
);

// მიმდინარე წელი
const currentYear = new Date().getFullYear();
document.querySelectorAll('.current-year').forEach(
    (element) => element.textContent = currentYear
);

// (read more - read less) გარე ვაკანსიების აღწერისთვის
document.querySelectorAll('.read-more').forEach((button) => {
    button.addEventListener('click', () => {
        const description = button.previousElementSibling;
        const isExpanded = description.classList.toggle('is-expanded');

        button.setAttribute('aria-expanded', isExpanded);
        button.textContent = isExpanded ? 'read less' : 'read more';
    });
});

// ვაკანსიის წაშლის დადასტურების დიალოგური ფანჯარა
document.querySelectorAll('form[action*="/delete"]').forEach((form) => {
    form.addEventListener('submit', (e) => {
        const confirmed = confirm('ნამდვილად გსურთ ამ ვაკანსიის წაშლა?');
        if (!confirmed) e.preventDefault();
    });
});

// კატეგორიის არჩევისას ფორმის ავტომატური გაგზავნა
const categorySelect = document.querySelector('.search-panel select[name="category"]');
if (categorySelect) {
    categorySelect.addEventListener('change', () => categorySelect.closest('form').submit());
}

// სიმბოლოების მთვლელი მოკლე და სრული აღწერის ველებისთვის
const summaryInput = document.querySelector('textarea[name="summary"]');
if (summaryInput) {
    const counter = document.createElement('small');
    counter.className = 'text-muted d-block mt-1';
    summaryInput.parentNode.appendChild(counter);

    const updateCounter = () => {
        const length = summaryInput.value.length;
        counter.textContent = `სიმბოლოები: ${length} / 280`;
        counter.style.color = length > 280 ? '#b42318' : 'var(--muted)';
    };

    summaryInput.addEventListener('input', updateCounter);
    updateCounter();
}

// პროფილის ფოტოს წინასწარი დათვალიერება ატვირთვისას
const imageInput = document.querySelector('input[type="file"][name="image"]');
if (imageInput) {
    imageInput.addEventListener('change', function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                const previewImg = document.querySelector('.avatar img');
                if (previewImg) previewImg.src = e.target.result;
            };
            reader.readAsDataURL(file);
        }
    });
}