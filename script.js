
const form = document.getElementById("registrationForm");

form.addEventListener("submit", function(event) {
    event.preventDefault();

    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const message = document.getElementById("message");

    message.style.color = "red";

    if (name.length < 2) {
        message.textContent = "Please enter a valid name.";
        return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        message.textContent = "Please enter a valid email address.";
        return;
    }

    if (!/^[6-9]\d{9}$/.test(phone)) {
        message.textContent = "Enter a valid 10-digit Indian phone number.";
        return;
    }

    if (password.length < 8) {
        message.textContent = "Password must contain at least 8 characters.";
        return;
    }

    if (!/[A-Z]/.test(password) ||
        !/[a-z]/.test(password) ||
        !/[0-9]/.test(password)) {
        message.textContent = "Password must contain uppercase, lowercase and a number.";
        return;
    }

    if (password !== confirmPassword) {
        message.textContent = "Passwords do not match.";
        return;
    }

    message.style.color = "green";
    message.textContent = "Registration form validated successfully! Backend integration is pending.";

    form.reset();
});
