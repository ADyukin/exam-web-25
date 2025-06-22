function confirmDelete(eventId, eventTitle) {
    console.log('Opening delete modal for event:', eventId, eventTitle);
    const modal = document.getElementById('deleteModal');
    document.getElementById('eventTitle').textContent = eventTitle;
    document.getElementById('deleteForm').action = `/events/${eventId}/delete`;
    
    // Показываем модальное окно
    modal.classList.add('show');
}

function closeModal() {
    const modal = document.getElementById('deleteModal');
    modal.classList.remove('show');
} 

document.addEventListener('DOMContentLoaded', function () {
    const registerBtn = document.getElementById('registerBtn');

    if (registerBtn) {
        registerBtn.addEventListener('click', (event) => {
            const button = event.currentTarget;
            const registerUrl = button.dataset.registerUrl;
            const csrfToken = button.dataset.csrfToken;
            showRegistrationModal(registerUrl, csrfToken);
        });
    }
});

function showRegistrationModal(registerUrl, csrfToken) {
    const existingModal = document.getElementById('registerModalBackdrop');
    if (existingModal) {
        existingModal.remove();
    }

    const modalHtml = `
        <div class="custom-modal-backdrop" id="registerModalBackdrop">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <form action="${registerUrl}" method="POST">
                        <div class="modal-header">
                            <h5 class="modal-title">Регистрация волонтера</h5>
                            <button type="button" class="btn-close close-modal-btn"></button>
                        </div>
                        <div class="modal-body">
                            <input type="hidden" name="csrf_token" value="${csrfToken}">
                            <div class="mb-3">
                                <label for="contact_info" class="form-label">Контактная информация</label>
                                <input type="text" class="form-control" id="contact_info" name="contact_info" required placeholder="Например: +7 (999) 123-45-67">
                            </div>
                        </div>
                        <div class="modal-footer">
                            <button type="button" class="btn btn-secondary close-modal-btn">Отмена</button>
                            <button type="submit" class="btn btn-primary">Отправить заявку</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHtml);
    document.body.style.overflow = 'hidden'; // Запрещаем прокрутку фона

    // Добавляем обработчики для закрытия
    document.querySelectorAll('.close-modal-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            closeRegistrationModal();
        });
    });
    document.getElementById('registerModalBackdrop').addEventListener('click', (event) => {
        if (event.target.id === 'registerModalBackdrop') {
            closeRegistrationModal();
        }
    });
}

function closeRegistrationModal() {
    const modalBackdrop = document.getElementById('registerModalBackdrop');
    if (modalBackdrop) {
        modalBackdrop.remove();
    }
    document.body.style.overflow = 'auto'; // Возвращаем прокрутку
} 