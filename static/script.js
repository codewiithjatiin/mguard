// DARK/LIGHT MODE TOGGLE
document.addEventListener('DOMContentLoaded', function () {
    const modeSwitch = document.getElementById('modeSwitch');
    modeSwitch.addEventListener('click', function () {
        document.body.classList.toggle('light-mode');
        if (document.body.classList.contains('light-mode')) {
            modeSwitch.textContent = 'Dark Mode';
        } else {
            modeSwitch.textContent = 'Light Mode';
        }
    });

    // TYPING EFFECT
    const typingText = document.querySelector('.typing-text');
    if (typingText) {
        const fullText = typingText.getAttribute('data-text');
        let index = 0;
        function typeChar() {
            if (index < fullText.length) {
                typingText.textContent += fullText.charAt(index);
                index++;
                setTimeout(typeChar, 100);
            }
        }
        typeChar();
    }

    // GLOW ON FOCUS FOR INPUTS
    const inputs = document.querySelectorAll('.input-box');
    inputs.forEach(input => {
        input.addEventListener('focus', () => {
            input.style.boxShadow = '0 0 15px #00ff99, 0 0 30px #00ff99';
        });
        input.addEventListener('blur', () => {
            input.style.boxShadow = 'none';
        });
    });

    // LOGIN FORM SUBMISSION EFFECT
    const loginForm = document.querySelector('form');
    if (loginForm) {
        loginForm.addEventListener('submit', (e) => {
            const btn = loginForm.querySelector('.btn');
            btn.textContent = 'Authenticating...';
            btn.disabled = true;
            btn.style.opacity = '0.6';
        });
    }
});
