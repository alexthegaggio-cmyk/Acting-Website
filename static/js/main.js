(function () {
    'use strict';

    document.addEventListener('DOMContentLoaded', function () {
        var flashes = document.querySelectorAll('.flash');
        flashes.forEach(function (el) {
            setTimeout(function () {
                el.style.transition = 'opacity 0.3s ease';
                el.style.opacity = '0';
                setTimeout(function () {
                    el.remove();
                }, 300);
            }, 5000);
        });
    });

    document.addEventListener('click', function (e) {
        var anchor = e.target.closest('a[href^="#"]');
        if (!anchor) return;
        var target = document.querySelector(anchor.getAttribute('href'));
        if (target) {
            e.preventDefault();
            target.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
    });

    document.addEventListener('DOMContentLoaded', function () {
        const openQuizBtn = document.getElementById('open-quiz-btn');
        const notesSection = document.getElementById('notes-section');
        const quizForm = document.getElementById('quiz-form');
        const quizSection = document.getElementById('quiz-section');
        const quizFail = document.getElementById('quiz-fail');
        const failScore = document.getElementById('fail-score');
        const retryBtn = document.getElementById('retry-btn');

        if (openQuizBtn) {
            openQuizBtn.addEventListener('click', function () {
                notesSection?.classList.add('hidden');
                if (quizForm) quizForm.style.display = 'block';
                this.style.display = 'none';
            });
        }

        if (quizForm) {
            quizForm.addEventListener('submit', async function (e) {
                e.preventDefault();
                const formData = new FormData(this);
                try {
                    const response = await fetch(this.action, {
                        method: 'POST',
                        body: formData,
                        headers: {
                            'Accept': 'application/json'
                        }
                    });
                    const data = await response.json();
                    // Reset previous highlights
                    document.querySelectorAll('.option-wrapper').forEach(el => {
                        el.style.background = 'none';
                        el.style.border = 'none';
                        el.style.padding = '0';
                    });

                    if (data.passed) {
                        const moduleNumber = document.querySelector('main[data-module]')?.dataset.module || '1';
                        quizSection.innerHTML = `
                            <div class="quiz-pass-state">
                                <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="var(--gold)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="margin-bottom: 12px;">
                                    <polyline points="20 6 9 17 4 12"></polyline>
                                </svg>
                                <div class="quiz-pass-label">QUIZ PASSED — ${data.score}%</div>
                                <span class="quiz-rule-gold"></span>
                                <form method="POST" action="/module/${moduleNumber}/quiz" style="margin-top: 20px;">
                                    <button type="submit" class="btn-secondary btn-sm" style="font-size:10px; padding: 10px 20px;">RESTART QUIZ</button>
                                </form>
                            </div>`;
                    } else {
                        if (quizFail) quizFail.style.display = 'block';
                        if (failScore) failScore.textContent = data.score;

                        if (data.results) {
                            Object.keys(data.results).forEach(qKey => {
                                const result = data.results[qKey];
                                const questionBlock = document.querySelector(`input[name="${qKey}"]`)?.closest('.question-block');

                                if (questionBlock) {
                                    const options = questionBlock.querySelectorAll('.option-wrapper');

                                    const correctEl = options[result.correct_index];
                                    if (correctEl) {
                                        correctEl.style.background = 'rgba(74, 103, 65, 0.1)';
                                        correctEl.style.border = '1px solid var(--success)';
                                        correctEl.style.borderRadius = '6px';
                                        correctEl.style.padding = '8px';
                                    }

                                    if (!result.is_correct && result.user_index !== null) {
                                        const wrongEl = options[result.user_index];
                                        if (wrongEl) {
                                            wrongEl.style.background = 'rgba(139, 58, 58, 0.1)';
                                            wrongEl.style.border = '1px solid var(--error)';
                                            wrongEl.style.borderRadius = '6px';
                                            wrongEl.style.padding = '8px';
                                        }
                                    }
                                }
                            });
                        }
                    }
                } catch (err) {
                    console.error('Quiz submission error:', err);
                }
            });
        }

        if (retryBtn) {
            retryBtn.addEventListener('click', function () {
                notesSection?.classList.remove('hidden');
                if (quizFail) quizFail.style.display = 'none';
                quizForm.querySelectorAll('input[type="radio"]').forEach(r => r.checked = false);
                document.querySelectorAll('.option-wrapper').forEach(el => {
                    el.style.background = 'none';
                    el.style.border = 'none';
                    el.style.padding = '0';
                });
                if (quizSection) {
                    window.scrollTo({ top: quizSection.offsetTop - 40, behavior: 'smooth' });
                }
            });
        }

        // Notes Auto-save
        const notesTextarea = document.querySelector('#notes-section textarea');
        const saveIndicator = document.getElementById('save-indicator');
        const saveNotesBtn = document.getElementById('save-notes-btn');
        const mainEl = document.querySelector('main[data-module]');

        async function saveNotes() {
            if (!notesTextarea || !mainEl) return;
            const moduleNumber = mainEl.dataset.module;
            try {
                await fetch(`/module/${moduleNumber}/notes`, {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ notes: notesTextarea.value })
                });
                if (saveIndicator) {
                    saveIndicator.style.opacity = '1';
                    setTimeout(() => { saveIndicator.style.opacity = '0'; }, 2000);
                }
            } catch (err) {
                console.error('Notes save error:', err);
            }
        }

        if (notesTextarea) notesTextarea.addEventListener('blur', saveNotes);
        if (saveNotesBtn) saveNotesBtn.addEventListener('click', saveNotes);

        const monologues = window.MODULE_MONOLOGUES || [];

        const genBtn = document.getElementById('generate-monologue-btn');
        const monoDisplay = document.getElementById('monologue-display');
        const monoTitle = document.getElementById('monologue-title');
        const monoText = document.getElementById('monologue-text');
        const emotionContainer = document.getElementById('emotion-container');
        const emotion1 = document.getElementById('emotion-1');
        const emotion2 = document.getElementById('emotion-2');

        if (genBtn) {
            genBtn.addEventListener('click', function () {
                const random = monologues[Math.floor(Math.random() * monologues.length)];
                if (monoDisplay) {
                    monoTitle.textContent = random.title;
                    monoText.textContent = random.text;

                    if (random.emotion_1 && random.emotion_2 && emotionContainer && emotion1 && emotion2) {
                        emotion1.textContent = random.emotion_1;
                        emotion2.textContent = random.emotion_2;
                        emotionContainer.style.display = 'block';
                    } else if (emotionContainer) {
                        emotionContainer.style.display = 'none';
                    }

                    monoDisplay.style.display = 'block';
                    this.textContent = 'GET ANOTHER ONE';
                }
            });
        }
    });

})();

