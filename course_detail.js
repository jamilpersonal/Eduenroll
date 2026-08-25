document.addEventListener('DOMContentLoaded', function () {
    var checkboxes = document.querySelectorAll('.topic__checkbox');
    var progressFill = document.getElementById('progress-fill');
    var progressPct = document.getElementById('progress-pct');
    var progressCount = document.getElementById('progress-count');
    var progressTotal = document.getElementById('progress-total');

    checkboxes.forEach(function (checkbox) {
        checkbox.addEventListener('change', function () {
            var topicId = checkbox.getAttribute('data-topic-id');
            var listItem = document.querySelector('.topic[data-topic-id="' + topicId + '"]');
            var desiredState = checkbox.checked;

            // Optimistic UI update.
            listItem.classList.toggle('topic--done', desiredState);
            checkbox.disabled = true;

            fetch(window.EDUENROLL_TOGGLE_URL_BASE + topicId + '/toggle/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': window.EDUENROLL_CSRF_TOKEN,
                    'X-Requested-With': 'XMLHttpRequest'
                },
                body: JSON.stringify({ is_completed: desiredState })
            })
                .then(function (response) {
                    if (!response.ok) {
                        throw new Error('Request failed');
                    }
                    return response.json();
                })
                .then(function (data) {
                    checkbox.checked = data.is_completed;
                    listItem.classList.toggle('topic--done', data.is_completed);
                    if (progressFill) {
                        progressFill.style.width = data.progress_percent + '%';
                    }
                    if (progressPct) {
                        progressPct.textContent = data.progress_percent;
                    }
                    if (progressCount) {
                        progressCount.textContent = data.completed_count;
                    }
                    if (progressTotal) {
                        progressTotal.textContent = data.total_topics;
                    }
                })
                .catch(function () {
                    // Roll back the optimistic update on failure.
                    checkbox.checked = !desiredState;
                    listItem.classList.toggle('topic--done', !desiredState);
                    alert('Could not save your progress. Please try again.');
                })
                .finally(function () {
                    checkbox.disabled = false;
                });
        });
    });
});
