const VALID_USER = "qa.engineer@example.com";
const VALID_PASSWORD = "quality-first";
const CART_KEY = "orbit-qa-cart";

const readCart = () => JSON.parse(localStorage.getItem(CART_KEY) || "[]");
const writeCart = (items) => localStorage.setItem(CART_KEY, JSON.stringify(items));

function updateCartCount() {
  const count = document.querySelector("[data-testid='cart-count']");
  if (count) count.textContent = String(readCart().length);
}

function configureLogin() {
  const form = document.querySelector("[data-testid='login-form']");
  if (!form) return;

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const email = document.querySelector("[data-testid='email']").value.trim();
    const password = document.querySelector("[data-testid='password']").value;
    const error = document.querySelector("[data-testid='login-error']");

    if (email === VALID_USER && password === VALID_PASSWORD) {
      sessionStorage.setItem("orbit-qa-user", email);
      localStorage.removeItem(CART_KEY);
      window.location.assign("inventory.html");
      return;
    }

    error.textContent = "We couldn't sign you in with those credentials.";
  });
}

function configureInventory() {
  const cards = [...document.querySelectorAll("[data-testid='product-card']")];
  if (!cards.length) return;

  updateCartCount();
  cards.forEach((card) => {
    card.querySelector("[data-testid='add-product']").addEventListener("click", () => {
      const cart = readCart();
      cart.push({
        name: card.dataset.productName,
        price: Number(card.dataset.productPrice),
      });
      writeCart(cart);
      updateCartCount();

      const notice = document.querySelector("[data-testid='notice']");
      notice.hidden = false;
      notice.textContent = `${card.dataset.productName} added to cart`;
    });
  });

  document.querySelector("[data-testid='product-search']").addEventListener("input", (event) => {
    const term = event.target.value.toLowerCase();
    cards.forEach((card) => {
      card.hidden = !card.dataset.productName.toLowerCase().includes(term);
    });
  });
}

function configureCart() {
  const list = document.querySelector("[data-testid='cart-list']");
  if (!list) return;

  const cart = readCart();
  if (!cart.length) {
    list.innerHTML = '<p class="empty">Your cart is empty.</p>';
    document.querySelector("[data-testid='checkout-link']").hidden = true;
    return;
  }

  list.innerHTML = cart.map((item) => `
    <article class="cart-item" data-testid="cart-item">
      <strong data-testid="cart-item-name">${item.name}</strong>
      <span>$${item.price.toFixed(2)}</span>
    </article>
  `).join("");
}

function configureCheckout() {
  const form = document.querySelector("[data-testid='checkout-form']");
  if (!form) return;

  form.addEventListener("submit", (event) => {
    event.preventDefault();
    form.hidden = true;
    document.querySelector("[data-testid='success-panel']").hidden = false;
    writeCart([]);
  });
}

configureLogin();
configureInventory();
configureCart();
configureCheckout();
