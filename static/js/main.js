document.addEventListener('DOMContentLoaded', () => {
    // Mobile menu toggle
    const btn = document.getElementById('mobile-menu-btn');
    const menu = document.getElementById('mobile-menu');
    const menuIcon = document.getElementById('menu-icon');
    const closeIcon = document.getElementById('close-icon');

    if (btn && menu) {
        btn.addEventListener('click', () => {
            menu.classList.toggle('hidden');
            menuIcon.classList.toggle('hidden');
            closeIcon.classList.toggle('hidden');
        });
    }
});

// Desktop dropdown toggle
function fecharTodosDropdowns() {
    document.querySelectorAll('.lw-nav__dropdown').forEach(d => {
        d.classList.remove('open');
        const btn = d.querySelector('button[aria-haspopup="true"]');
        if (btn) btn.setAttribute('aria-expanded', 'false');
    });
}

function toggleDropdown(button) {
    const dropdown = button.closest('.lw-nav__dropdown');
    const isOpen = dropdown.classList.contains('open');

    fecharTodosDropdowns();

    if (!isOpen) {
        dropdown.classList.add('open');
        button.setAttribute('aria-expanded', 'true');
    }
}

// Close dropdowns when clicking outside
document.addEventListener('click', (e) => {
    if (!e.target.closest('.lw-nav__dropdown')) {
        fecharTodosDropdowns();
    }
});

// Close dropdowns on Escape
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        fecharTodosDropdowns();
    }
});

// Copia o valor de um input/textarea para a área de transferência
function copiarTexto(id, botao) {
    const el = document.getElementById(id);
    if (!el || !el.value) return;

    const marcarCopiado = () => {
        if (!botao) return;
        const original = botao.textContent;
        botao.textContent = 'Copiado!';
        setTimeout(() => { botao.textContent = original; }, 1500);
    };

    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(el.value).then(marcarCopiado).catch(() => {
            el.select();
            document.execCommand('copy');
            marcarCopiado();
        });
    } else {
        el.select();
        document.execCommand('copy');
        marcarCopiado();
    }
}
