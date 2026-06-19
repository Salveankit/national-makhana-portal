const form = document.getElementById("login-form");
if (form) {
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const payload = {
      email: formData.get("email"),
      password: formData.get("password"),
    };
    const res = await fetch("/api/v1/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
    const message = document.getElementById("message");
    if (!res.ok) {
      message.textContent = "Login failed";
      return;
    }
    const data = await res.json();
    localStorage.setItem("nmb_token", data.access_token);
    window.location.href = data.role === "beneficiary" ? "/beneficiary" : "/dashboard";
  });
}
