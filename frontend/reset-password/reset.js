const resetForm = document.getElementById("resetForm");
const message = document.getElementById("message");
const resetButton = document.getElementById("resetButton");

// Get UID and token from the reset URL
const params = new URLSearchParams(window.location.search);

const uid = params.get("uid");
const token = params.get("token");

if (!uid || !token) {
    message.textContent = "Invalid or incomplete password reset link.";
    message.style.color = "red";
    resetButton.disabled = true;
}

resetForm.addEventListener("submit", async function (event) {
    event.preventDefault();

    const newPassword = document.getElementById("newPassword").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    message.textContent = "";

    if (newPassword !== confirmPassword) {
        message.textContent = "Passwords do not match.";
        message.style.color = "red";
        return;
    }

    if (newPassword.length < 8) {
        message.textContent = "Password must contain at least 8 characters.";
        message.style.color = "red";
        return;
    }

    try {
        resetButton.disabled = true;
        resetButton.textContent = "Resetting...";

        const response = await fetch(
            "http://127.0.0.1:8000/api/auth/reset-password/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    uid: uid,
                    token: token,
                    new_password: newPassword
                })
            }
        );

        const data = await response.json();

        if (response.ok) {
            message.textContent =
                data.message || "Password reset successfully!";

            message.style.color = "green";

            resetForm.reset();

            setTimeout(() => {
                window.location.href = "../login/login.html";
            }, 2000);

        } else {
            message.textContent =
                data.error || data.message ||
                Object.values(data).flat().join(" ");

            message.style.color = "red";
        }

    } catch (error) {
        message.textContent =
            "Unable to connect to the server. Please try again.";

        message.style.color = "red";

        console.error(error);

    } finally {
        resetButton.disabled = false;
        resetButton.textContent = "Reset Password";
    }
});