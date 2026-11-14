const form = document.getElementById("registrationForm");

form.addEventListener("submit", async function(event) {
    event.preventDefault();
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const phone = document.getElementById("phone").value.trim();
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;
    const message = document.getElementById("message");
    const submitButton = form.querySelector("button[type='submit']");

    message.style.color = "red";
    // Frontend validation
    if (name.split(/\s+/).length < 2) {
        message.textContent = "Please enter your full name.";
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
        message.textContent =
            "Password must contain uppercase, lowercase and a number.";
        return;
    }
    if (password !== confirmPassword) {
        message.textContent = "Passwords do not match.";
        return;
    }
    // Send registration details to Django
    message.style.color = "blue";
    message.textContent = "Creating your account...";
    submitButton.disabled = true;
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/auth/register/",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    full_name: name,
                    email: email,
                    phone: phone,
                    password: password,
                    confirm_password: confirmPassword
                })
            }
        );
        const data = await response.json();
        if (!response.ok) {
            message.style.color = "red";
            message.textContent = Array.isArray(data.error)
                ? data.error.join(" ")
                : data.error || "Registration failed.";
            return;
        }
        message.style.color = "green";
        message.textContent = data.message;
        form.reset();
    } catch (error) {
        console.error("Registration error:", error);
        message.style.color = "red";
        message.textContent =
            "Unable to connect to the server. Please try again.";
    } finally {
        submitButton.disabled = false;
    }
});