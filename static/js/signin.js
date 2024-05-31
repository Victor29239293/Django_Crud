document.addEventListener('DOMContentLoaded', function () {
    const password = document.getElementById('id_password');
    const icon = document.querySelector('#id-icon-password');

    icon.addEventListener('click', event => {
        event.preventDefault();
        if (password.type === 'password') {
            password.type = 'text';
            icon.classList.remove('bi-eye-fill');
            icon.classList.add('bi-eye-slash-fill');
        } else {
            password.type = 'password';
            icon.classList.add('bi-eye-fill');
            icon.classList.remove('bi-eye-slash-fill');
        }
    });
});