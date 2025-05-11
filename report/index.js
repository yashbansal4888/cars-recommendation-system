let signup = document.querySelector(".signup");
let login = document.querySelector(".login");
let slider = document.querySelector(".slider");
let formSection = document.querySelector(".form-section");

signup.addEventListener("click", () => {
    slider.classList.add("moveslider");
    formSection.classList.add("form-section-move");
});

login.addEventListener("click", () => {
    slider.classList.remove("moveslider");
    formSection.classList.remove("form-section-move");
});

// LOGIN
document.querySelector(".login-box .clkbtn").addEventListener("click", async () => {
    const email = document.querySelector(".login-box .email").value.trim();
    const password = document.querySelector(".login-box .password").value;

    if (!email || !password) {
        return alert("Please enter both email and password.");
    }

    try {
        const res = await fetch("http://localhost:5501/api/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        let data;
        try {
            data = await res.json();
        } catch (jsonErr) {
            console.error("Failed to parse JSON from login response:", jsonErr);
            throw new Error("Server returned invalid JSON");
        }

        if (res.ok) {
            alert("Login successful!");
            window.location.href="http://127.0.0.1:5000/"
            console.log("Login Response:", data);
        } else {
            alert(data.msg || "Login failed");
        }
    } catch (err) {
        alert("Error connecting to server");
        console.error("Login Error:", err);
    }
});

// SIGNUP
document.querySelector(".signup-box .clkbtn").addEventListener("click", async () => {
    const name = document.querySelector(".signup-box .name").value.trim();
    const email = document.querySelector(".signup-box .email").value.trim();
    const password = document.querySelectorAll(".signup-box .password")[0].value;
    const confirmPassword = document.querySelectorAll(".signup-box .password")[1].value;

    if (!name || !email || !password || !confirmPassword) {
        return alert("All fields are required.");
    }

    if (password !== confirmPassword) {
        return alert("Passwords do not match!");
    }

    try {
        const res = await fetch("http://localhost:5501/api/auth/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, email, password })
        });

        let data;
        try {
            data = await res.json();
        } catch (jsonErr) {
            console.error("Failed to parse JSON from signup response:", jsonErr);
            throw new Error("Server returned invalid JSON");
        }

        if (res.ok) {
            alert("Signup successful!");
            console.log("Signup Response:", data);
        } else {
            alert(data.msg || "Signup failed");
        }
    } catch (err) {
        alert("Error connecting to server");
        console.error("Signup Error:", err);
    }
});
