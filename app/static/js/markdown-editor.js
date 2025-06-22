document.addEventListener('DOMContentLoaded', (event) => {
    if (document.getElementById('markdown-editor')) {
        const easyMDE = new EasyMDE({
            element: document.getElementById('markdown-editor'),
            spellChecker: false,
            placeholder: "Введите описание...",
            // Привязка к скрытому полю, если оно используется
            // syncSideBySide: true, 
        });
    }
}); 