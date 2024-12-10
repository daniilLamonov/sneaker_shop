document.addEventListener("DOMContentLoaded", () => {
    // Добавление товара в корзину
    const cartCount = document.getElementById("cart-count");
    const cartItems = document.getElementById("cart-items");
    const totalPriceElement = document.getElementById("total-price");

    // Хранение корзины в localStorage
    let cart = JSON.parse(localStorage.getItem("cart")) || [];

    const updateCartUI = () => {
        cartCount.textContent = cart.length;
        totalPriceElement.textContent = cart.reduce((total, item) => total + item.price, 0).toFixed(2);

        cartItems.innerHTML = cart.map(item => `
            <li>${item.name} - $${item.price}</li>
        `).join('');
    };

    // Добавление товара в корзину
    if (document.getElementById("add-to-cart")) {
        document.getElementById("add-to-cart").addEventListener("click", () => {
            const product = { name: "Sneaker 1", price: 120.00 };
            cart.push(product);
            localStorage.setItem("cart", JSON.stringify(cart));
            updateCartUI();
        });
    }

    // Обновление UI при загрузке страницы
    updateCartUI();
});
