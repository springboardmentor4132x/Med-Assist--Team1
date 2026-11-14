const form = document.getElementById("loginForm");
const password = document.getElementById("password");
const togglePassword = document.getElementById("togglePassword");
const message = document.getElementById("message");

// Show or hide password
togglePassword.addEventListener("click", function () {
    if (password.type === "password") {
        password.type = "text";
        togglePassword.textContent = "Hide";
    } else {
        password.type = "password";
        togglePassword.textContent = "Show";
    }
});
// Login using Django API
form.addEventListener("submit",async function (event) {
    event.preventDefault();
    const email = document.getElementById("email").value.trim();
    const enteredPassword = password.value;
    message.style.color = "red";
    message.textContent = "Logging in...";
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/auth/login/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    email: email,
                    password: enteredPassword
                })
            }
        );
        const data = await response.json();
        if (!response.ok) {
            message.textContent =
                data.error || data.detail || "Login failed.";
            return;
        }
        // Store JWT tokens
        localStorage.setItem("access_token", data.tokens.access);
        localStorage.setItem("refresh_token", data.tokens.refresh);
        // Store user information
        localStorage.setItem("user", JSON.stringify(data.user));
        message.style.color = "green";
        message.textContent = "Login successful! Welcome, " +
            data.user.username + "!";
        console.log("Logged-in user:", data.user);
    } catch (error) {
        console.error("Login error:", error);
        message.textContent =
            "Unable to connect to the server. Please try again.";
    }
});

async function refreshAccessToken() {
    const refreshToken = localStorage.getItem("refresh_token");
    if (!refreshToken) {
        console.log("No refresh token found. Please log in.");
        return false;
    }
    try {
        const response = await fetch(
            "http://127.0.0.1:8000/api/auth/token/refresh/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    refresh: refreshToken
                })
            }
        );
        const data = await response.json();
        if (!response.ok) {
            console.log("Refresh token expired. Please log in again.");
            localStorage.removeItem("access_token");
            localStorage.removeItem("refresh_token");
            localStorage.removeItem("user");
            return false;
        }
        localStorage.setItem("access_token", data.access);
        console.log("Access token refreshed successfully!");
        return true;
    } catch (error) {
        console.error("Token refresh error:", error);
        return false;
    }
}

async function authenticatedFetch(url, options = {}) {
    let accessToken = localStorage.getItem("access_token");
    // First API request
    let response = await fetch(url, {
        ...options,
        headers: {
            ...options.headers,
            "Authorization": `Bearer ${accessToken}`
        }
    });
    // If access token expired
    if (response.status === 401) {
        const refreshed = await refreshAccessToken();
        if (!refreshed) {
            logoutUser();
            return response;
        }
        // Get the newly generated access token
        accessToken = localStorage.getItem("access_token");
        // Retry the original request
        response = await fetch(url, {
            ...options,
            headers: {
                ...options.headers,
                "Authorization": `Bearer ${accessToken}`
            }
        });
    }
    return response;
}
async function logoutUser() {

    const accessToken = localStorage.getItem("access_token");
    const refreshToken = localStorage.getItem("refresh_token");

    if (!accessToken || !refreshToken) {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");

        window.location.href = "login.html";
        return;
    }
    try{
        const response = await fetch(
            "http://127.0.0.1:8000/api/auth/logout/",
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${accessToken}`
                },
                body: JSON.stringify({
                    refresh: refreshToken
                })
            }
        );

        const data = await response.json();

        if (!response.ok) {
            console.error("Logout error:", data);
        } else {
            console.log(data.message);
        }

    } catch (error) {
        console.error("Logout request failed:", error);

    } finally {
        localStorage.removeItem("access_token");
        localStorage.removeItem("refresh_token");
        localStorage.removeItem("user");

        window.location.href = "login.html";
    }
}