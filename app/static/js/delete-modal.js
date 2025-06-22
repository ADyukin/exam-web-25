document.addEventListener('DOMContentLoaded', function () {
    const deleteButtons = document.querySelectorAll('.delete-event-btn');

    deleteButtons.forEach(button => {
        button.addEventListener('click', (event) => {
            const button = event.currentTarget;
            const eventId = button.dataset.eventId;
            const eventTitle = button.dataset.eventTitle;
            const csrfToken = button.dataset.csrfToken;
            const deleteUrl = button.dataset.deleteUrl;
            showDeleteModal(eventId, eventTitle, csrfToken, deleteUrl);
        });
    });
});

function showDeleteModal(eventId, eventTitle, csrfToken, deleteUrl) {
    const existingModal = document.getElementById('deleteModal');
    if (existingModal) {
        existingModal.remove();
    }

    const modalHtml = `
        <div class="custom-modal-backdrop" id="deleteModalBackdrop">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">Подтверждение удаления</h5>
                        <button type="button" class="btn-close close-modal-btn"></button>
                    </div>
                    <div class="modal-body">
                        <p>Вы действительно хотите удалить мероприятие "<strong>${eventTitle}</strong>"?</p>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary close-modal-btn">Отмена</button>
                        <form action="${deleteUrl}" method="POST" class="d-inline">
                            <input type="hidden" name="csrf_token" value="${csrfToken}">
                            <button type="submit" class="btn btn-danger">Удалить</button>
                        </form>
                    </div>
                </div>
            </div>
        </div>
    `;

    document.body.insertAdjacentHTML('beforeend', modalHtml);
    document.body.style.overflow = 'hidden'; // Запрещаем прокрутку фона

    // Добавляем обработчики для закрытия
    document.querySelectorAll('.close-modal-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            closeDeleteModal();
        });
    });
     document.getElementById('deleteModalBackdrop').addEventListener('click', (event) => {
        if (event.target.id === 'deleteModalBackdrop') {
            closeDeleteModal();
        }
    });
}

function closeDeleteModal() {
    const modalBackdrop = document.getElementById('deleteModalBackdrop');
    if (modalBackdrop) {
        modalBackdrop.remove();
    }
    document.body.style.overflow = 'auto'; // Возвращаем прокрутку
}