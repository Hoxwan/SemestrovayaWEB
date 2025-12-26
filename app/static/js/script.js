// Основные функции JavaScript для Task Manager

document.addEventListener('DOMContentLoaded', function() {

    // Подтверждение удаления
    document.querySelectorAll('.btn-danger').forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.closest('form')) {
                // Если кнопка внутри формы, проверяем ее текст
                const buttonText = this.textContent.toLowerCase();
                if (buttonText.includes('удалить')) {
                    if (!confirm('Вы уверены, что хотите удалить этот элемент?')) {
                        e.preventDefault();
                    }
                }
            }
        });
    });

    // Автосабмит чекбокса завершения задачи
    document.querySelectorAll('.form-check-input[onchange]').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            this.form.submit();
        });
    });

    // Очистка сообщений через 5 секунд
    setTimeout(() => {
        const alerts = document.querySelectorAll('.alert');
        alerts.forEach(alert => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Динамическое обновление счетчиков задач (если есть)
    if (document.getElementById('task-counter')) {
        updateTaskCounters();
    }

    // Инициализация всплывающих подсказок
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Функция для обновления счетчиков задач
    function updateTaskCounters() {
        fetch('/api/tasks')
            .then(response => response.json())
            .then(data => {
                if (data.tasks) {
                    const total = data.tasks.length;
                    const completed = data.tasks.filter(task => task.status === 'Завершено').length;

                    document.getElementById('total-tasks').textContent = total;
                    document.getElementById('completed-tasks').textContent = completed;
                    document.getElementById('active-tasks').textContent = total - completed;
                }
            })
            .catch(error => console.error('Ошибка при обновлении счетчиков:', error));
    }

    // Обработка фильтрации
    const statusFilter = document.getElementById('status-filter');
    if (statusFilter) {
        statusFilter.addEventListener('change', function() {
            this.closest('form').submit();
        });
    }

    // Предпросмотр цвета в форме категории
    const colorInput = document.getElementById('color');
    const colorPreview = document.getElementById('color-preview');
    if (colorInput && colorPreview) {
        colorInput.addEventListener('input', function() {
            colorPreview.style.backgroundColor = this.value;
        });
    }

    // Валидация форм
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = this.querySelectorAll('[required]');
            let isValid = true;

            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.classList.add('is-invalid');
                    isValid = false;
                } else {
                    field.classList.remove('is-invalid');
                }
            });

            if (!isValid) {
                e.preventDefault();
                alert('Пожалуйста, заполните все обязательные поля');
            }
        });
    });

    // Динамическая загрузка задач (если нужно)
    const loadMoreBtn = document.getElementById('load-more');
    if (loadMoreBtn) {
        loadMoreBtn.addEventListener('click', function() {
            const page = parseInt(this.dataset.page) || 1;
            loadTasks(page + 1);
            this.dataset.page = page + 1;
        });
    }

    function loadTasks(page) {
        fetch(`/tasks?page=${page}`)
            .then(response => response.text())
            .then(html => {
                const tempDiv = document.createElement('div');
                tempDiv.innerHTML = html;
                const newTasks = tempDiv.querySelector('#tasks-container');
                if (newTasks) {
                    document.getElementById('tasks-container').innerHTML += newTasks.innerHTML;
                }
                // Обновляем кнопку
                const nextPage = page + 1;
                loadMoreBtn.dataset.page = nextPage;
            })
            .catch(error => console.error('Ошибка при загрузке задач:', error));
    }
});

<script>
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.task-complete-checkbox').forEach(function(checkbox) {
        checkbox.addEventListener('change', function() {
            const form = this.closest('form');
            const taskId = form.dataset.taskId;

            fetch(form.action, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: new URLSearchParams(new FormData(form))
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Обновляем строку таблицы, чтобы отразить изменение
                    const row = form.closest('tr');
                    if (this.checked) {
                        row.classList.add('table-success');
                    } else {
                        row.classList.remove('table-success');
                    }
                } else {
                    alert('Ошибка при обновлении задачи');
                    this.checked = !this.checked; // Возвращаем чекбокс в предыдущее состояние
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('Произошла ошибка при отправке запроса');
                this.checked = !this.checked;
            });
        });
    });
});
</script>