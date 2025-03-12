const themeToggle = document.getElementById("theme-toggle");
const body = document.body;

// Check local storage for theme preference and apply it
if (localStorage.getItem("dark-mode") === "enabled") {
    body.classList.add("dark-mode");
    themeToggle.textContent = "☀"; // Sun icon for light mode
}

// Event listener for theme toggle button
themeToggle.addEventListener("click", () => {
    body.classList.toggle("dark-mode");

    // Update button icon and save preference in local storage
    if (body.classList.contains("dark-mode")) {
        themeToggle.textContent = "☀"; // Light mode icon
        localStorage.setItem("dark-mode", "enabled");
    } else {
        themeToggle.textContent = "🌙"; // Dark mode icon
        localStorage.setItem("dark-mode", "disabled");
    }
});