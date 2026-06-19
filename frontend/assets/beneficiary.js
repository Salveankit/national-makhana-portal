const token = localStorage.getItem("nmb_token");
const headers = {
  "Content-Type": "application/json",
  Authorization: `Bearer ${token}`,
};

async function api(path, options = {}) {
  const res = await fetch(path, { headers, ...options });
  if (res.status === 401) {
    localStorage.removeItem("nmb_token");
    window.location.href = "/login";
    return null;
  }
  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return res.json();
  }
  return { detail: "Unexpected response" };
}

function currency(value) {
  return new Intl.NumberFormat("en-IN", { maximumFractionDigits: 0 }).format(value || 0);
}

function setMessage(id, text, isError = false) {
  const node = document.getElementById(id);
  if (!node) return;
  node.textContent = text;
  node.style.color = isError ? "var(--danger)" : "var(--success)";
}

function renderApplications(apps = []) {
  const root = document.getElementById("application-list");
  root.innerHTML = "";
  if (!apps.length) {
    root.innerHTML = `<div class="metric-card"><strong>No applications yet</strong><small>Create a beneficiary profile and submit your first application to begin workflow tracking.</small></div>`;
    return;
  }

  apps.forEach((app) => {
    const history = (app.status_history || [])
      .map(
        (item) => `
          <div class="status-chip">
            <span>${item.status}</span>
            <strong>${new Date(item.changed_at).toLocaleDateString()}</strong>
          </div>
          <small>${item.remarks}</small>
        `
      )
      .join("");

    const el = document.createElement("div");
    el.className = "metric-card";
    el.innerHTML = `
      <div class="metric-badge">${app.current_status}</div>
      <strong>${app.application_id}</strong>
      <small>${app.scheme_component}</small>
      <small>Requested Amount: Rs ${currency(app.requested_amount)}</small>
      <small>Pond Area: ${app.pond_area_acres} acres</small>
      <div class="status-stack">${history}</div>
    `;
    root.appendChild(el);
  });
}

async function loadProfile() {
  const me = await api("/api/v1/auth/me");
  if (!me) return;
  if (me.role !== "beneficiary") {
    window.location.href = "/dashboard";
    return;
  }
  document.getElementById("beneficiary-meta").textContent = `${me.name} | ${me.email} | ${me.role}`;
  const profile = await api("/api/v1/beneficiary/profile");
  if (!profile || profile.detail) return;
  Object.entries(profile).forEach(([key, value]) => {
    const input = document.querySelector(`#profile-form [name="${key}"]`);
    if (input) input.value = value;
  });
  const aadhaarStatus = document.getElementById("aadhaar-status");
  if (aadhaarStatus) {
    aadhaarStatus.textContent = profile.identity_verified
      ? `Verified: ${profile.aadhaar_masked} | Reference: ${profile.aadhaar_vault_ref || "available"}`
      : "Verification not started.";
  }
}

async function loadApplications() {
  const apps = await api("/api/v1/beneficiary/applications");
  if (!apps || apps.detail) {
    renderApplications([]);
    return;
  }
  renderApplications(apps);
}

document.getElementById("profile-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  const payload = Object.fromEntries(form.entries());
  payload.total_land_acres = Number(payload.total_land_acres);
  payload.makhana_area_acres = Number(payload.makhana_area_acres);
  const data = await api("/api/v1/beneficiary/profile", {
    method: "PUT",
    body: JSON.stringify(payload),
  });
  if (!data || data.detail) {
    setMessage("profile-message", data?.detail || "Profile save failed", true);
    return;
  }
  setMessage("profile-message", "Profile saved successfully.");
  loadProfile();
  loadApplications();
});

document.getElementById("application-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  const payload = {
    scheme_component: form.get("scheme_component"),
    pond_area_acres: Number(form.get("pond_area_acres")),
    requested_amount: Number(form.get("requested_amount")),
    documents: [
      {
        file_name: form.get("file_name"),
        document_type: form.get("document_type"),
      },
    ],
    geo_tag: {
      latitude: Number(form.get("latitude")),
      longitude: Number(form.get("longitude")),
      accuracy: Number(form.get("accuracy")),
    },
  };
  const data = await api("/api/v1/beneficiary/applications", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  if (!data || data.detail) {
    setMessage("application-message", data?.detail || "Application submission failed", true);
    return;
  }
  setMessage("application-message", `Application submitted successfully: ${data.application_id}`);
  loadApplications();
});

document.getElementById("aadhaar-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  const payload = {
    aadhaar_number: form.get("aadhaar_number"),
    consent: form.get("consent") === "true",
  };
  const data = await api("/api/v1/beneficiary/profile/verify-aadhaar", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  if (!data || data.detail) {
    setMessage("aadhaar-message", data?.detail || "Identity verification failed", true);
    return;
  }
  setMessage("aadhaar-message", `Identity verified: ${data.aadhaar_masked}`);
  loadProfile();
});

loadProfile();
loadApplications();
