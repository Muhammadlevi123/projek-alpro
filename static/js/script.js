document.addEventListener("DOMContentLoaded", () => {
    const currentPath = window.location.pathname;
    const menuItems = document.querySelectorAll(".sidebar ul li a");

    menuItems.forEach(item => {
        if (item.getAttribute("href") === currentPath) {
            item.classList.add("active");
        }
    });
});
