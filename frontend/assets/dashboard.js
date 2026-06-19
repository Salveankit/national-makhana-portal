const token = localStorage.getItem("nmb_token");
const apiBase = window.location.protocol === "file:" ? "http://127.0.0.1:8000" : "";
const pageUrl = (path) => `${apiBase}${path}`;
const defaultFilters = {
  financial_year: "2026-27",
  state_code: "BR",
  district_code: "",
  quarter: "",
};
const activeFilters = {
  ...defaultFilters,
};
const sectionNames = ["overview", "planning", "workflow", "system", "services"];
let currentUser = null;
const notificationChannelConfig = {
  sms: {
    label: "Mobile Number",
    hint: "Enter a 10 digit mobile number for SMS delivery.",
    value: "9876543210",
    inputMode: "tel",
    autocomplete: "tel",
    validator: (value) => /^\d{10}$/.test(value.replace(/\D/g, "")),
    error: "SMS delivery requires a valid 10 digit mobile number.",
  },
  email: {
    label: "Email Address",
    hint: "Enter the recipient email address for email delivery.",
    value: "farmer@example.com",
    inputMode: "email",
    autocomplete: "email",
    validator: (value) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value),
    error: "Email delivery requires a valid email address.",
  },
  whatsapp: {
    label: "WhatsApp Number",
    hint: "Enter the beneficiary WhatsApp-enabled mobile number.",
    value: "9876543210",
    inputMode: "tel",
    autocomplete: "tel",
    validator: (value) => /^\d{10}$/.test(value.replace(/\D/g, "")),
    error: "WhatsApp delivery requires a valid 10 digit mobile number.",
  },
};

async function api(path, options = {}) {
  const headers = {
    "Content-Type": "application/json",
    Authorization: `Bearer ${token}`,
    ...(options.headers || {}),
  };
  const res = await fetch(`${apiBase}${path}`, { ...options, headers });
  if (res.status === 401) {
    localStorage.removeItem("nmb_token");
    window.location.href = pageUrl("/login");
    return null;
  }
  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    return res.json();
  }
  return res.text();
}

function currency(value) {
  return new Intl.NumberFormat("en-IN", { maximumFractionDigits: 0 }).format(value || 0);
}

function integrationName(value) {
  const map = {
    "mock-sms-gateway": "SMS Gateway",
    "mock-email-gateway": "Email Gateway",
    "mock-whatsapp-gateway": "WhatsApp Gateway",
    "mock-aadhaar-vault": "Aadhaar Vault",
    "mock-dbt-switch": "DBT Switch",
  };
  return map[value] || value;
}

function integrationStatus(value) {
  const map = {
    ready_for_live_swap: "Ready for Activation",
    requires_business_credentials: "Pending Credentials",
    mock_mode: "Configured for Demonstration",
    banking_integration_pending: "Pending Banking Integration",
    awaiting_credentials: "Pending Credentials",
    connected: "Connected",
    delivered: "Delivered",
    configured: "Configured",
    logged: "Logged",
  };
  return map[value] || value;
}

function badgeTone(value = "") {
  const normalized = String(value).trim().toLowerCase();
  if (["approved", "connected", "delivered", "ready for activation", "up", "completed", "verified", "logged"].includes(normalized)) {
    return "badge-success";
  }
  if (["returned", "rejected", "down", "failed"].includes(normalized)) {
    return "badge-danger";
  }
  if (["query raised", "pending credentials", "pending banking integration", "awaiting credentials", "clarification raised", "inspection assigned", "configured for demonstration", "configured"].includes(normalized)) {
    return "badge-warning";
  }
  if (["recommended by state", "submitted", "under state review", "inspection completed", "ready", "active"].includes(normalized)) {
    return "badge-info";
  }
  return "badge-default";
}

function setActiveSection(section) {
  const target = sectionNames.includes(section) ? section : "overview";
  document.querySelectorAll("[data-console-section]").forEach((node) => {
    node.classList.toggle("active", node.dataset.consoleSection === target);
  });
  document.querySelectorAll("[data-section-target]").forEach((node) => {
    const isActive = node.dataset.sectionTarget === target;
    node.classList.toggle("active", isActive);
    if (node.classList.contains("sidebar-link") || node.classList.contains("console-tab")) {
      node.setAttribute("aria-current", isActive ? "page" : "false");
    }
  });
  const nextHash = `#${target}`;
  if (window.location.hash !== nextHash) {
    history.replaceState(null, "", nextHash);
  }
}

function bindSectionNavigation() {
  document.querySelectorAll("[data-section-target]").forEach((node) => {
    node.addEventListener("click", () => {
      setActiveSection(node.dataset.sectionTarget);
      document.querySelector(".content-area")?.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
  const initialSection = window.location.hash.replace("#", "");
  setActiveSection(initialSection || "overview");
  window.addEventListener("hashchange", () => {
    setActiveSection(window.location.hash.replace("#", ""));
  });
}

function setQuarterSlicer(value = "") {
  const hidden = document.getElementById("filter-quarter-input");
  if (hidden) {
    hidden.value = value;
  }
  document.querySelectorAll("[data-quarter-value]").forEach((node) => {
    const isActive = node.dataset.quarterValue === value;
    node.classList.toggle("active", isActive);
    node.setAttribute("aria-pressed", isActive ? "true" : "false");
  });
}

function renderFilterSummary() {
  const root = document.getElementById("filter-summary");
  if (!root) return;
  const tags = [];
  if (activeFilters.financial_year) {
    tags.push(["FY", activeFilters.financial_year]);
  }
  tags.push(["State", activeFilters.state_code || "All states"]);
  tags.push(["District", activeFilters.district_code || "All districts"]);
  tags.push(["Quarter", activeFilters.quarter || "All quarters"]);
  root.innerHTML = tags.map(([label, value]) => `<span class="filter-tag"><strong>${label}</strong>${value}</span>`).join("");
}

function syncFilterForm() {
  const financialYear = document.getElementById("filter-financial-year");
  const stateCode = document.getElementById("filter-state-code");
  const districtCode = document.getElementById("filter-district-code");
  if (financialYear) {
    financialYear.value = activeFilters.financial_year || defaultFilters.financial_year;
  }
  if (stateCode) {
    stateCode.value = activeFilters.state_code || "";
  }
  if (districtCode) {
    districtCode.value = activeFilters.district_code || "";
  }
  setQuarterSlicer(activeFilters.quarter || "");
  renderFilterSummary();
}

function fillFilterSelect(selectId, items, { placeholder, valueKey = "code", labelBuilder }) {
  const select = document.getElementById(selectId);
  if (!select) return;
  const selectedValue = select.value;
  select.innerHTML = "";
  if (placeholder !== undefined) {
    const option = document.createElement("option");
    option.value = "";
    option.textContent = placeholder;
    select.appendChild(option);
  }
  items.forEach((item) => {
    const option = document.createElement("option");
    option.value = item[valueKey];
    option.textContent = labelBuilder(item);
    select.appendChild(option);
  });
  if ([...select.options].some((option) => option.value === selectedValue)) {
    select.value = selectedValue;
  }
}

async function loadDistrictOptions(stateCode, preferredDistrict = activeFilters.district_code) {
  const districtSelect = document.getElementById("filter-district-code");
  if (!districtSelect) return;
  if (!stateCode) {
    fillFilterSelect("filter-district-code", [], { placeholder: "All districts", labelBuilder: (item) => item.name });
    districtSelect.value = "";
    return;
  }
  const districts = (await api(`/api/v1/locations/districts?state_code=${encodeURIComponent(stateCode)}`)) || [];
  fillFilterSelect("filter-district-code", districts, {
    placeholder: "All districts",
    labelBuilder: (item) => `${item.name} (${item.code})`,
  });
  const nextDistrict = districts.some((item) => item.code === preferredDistrict) ? preferredDistrict : "";
  districtSelect.value = nextDistrict;
}

async function hydrateDashboardFilters(me) {
  const stateSelect = document.getElementById("filter-state-code");
  if (!stateSelect) return;
  const states = (await api("/api/v1/locations/states")) || [];
  const scopedStates = me.role === "nmb_admin"
    ? states
    : states.filter((item) => item.code === me.state_code);
  fillFilterSelect("filter-state-code", scopedStates, {
    placeholder: me.role === "nmb_admin" ? "All states" : undefined,
    labelBuilder: (item) => `${item.name} (${item.code})`,
  });
  if (me.role !== "nmb_admin" && me.state_code) {
    activeFilters.state_code = me.state_code;
    stateSelect.disabled = true;
  } else {
    stateSelect.disabled = false;
    if (!scopedStates.some((item) => item.code === activeFilters.state_code)) {
      activeFilters.state_code = "";
    }
  }
  await loadDistrictOptions(activeFilters.state_code, activeFilters.district_code);
  syncFilterForm();
}

function buildQuery(filters = activeFilters) {
  const params = new URLSearchParams();
  Object.entries(filters).forEach(([key, value]) => {
    if (value) params.set(key, value);
  });
  return params.toString() ? `?${params.toString()}` : "";
}

function renderStatusBreakdown(items = {}) {
  const root = document.getElementById("status-breakdown");
  root.innerHTML = "";
  const entries = Object.entries(items);
  if (!entries.length) {
    root.innerHTML = `
      <div class="empty-state">
        <picture>
          <source srcset="assets/images/nmb-workflow-illustration.webp" type="image/webp" />
          <img src="assets/images/nmb-workflow-illustration.png" alt="" />
        </picture>
        <div>
          <strong>No workflow activity yet</strong>
          <small>Application status counts will appear after records enter this scope.</small>
        </div>
      </div>
    `;
    return;
  }
  entries.forEach(([label, count]) => {
    const el = document.createElement("div");
    el.className = "status-chip";
    el.innerHTML = `<span>${label}</span><strong>${count}</strong>`;
    root.appendChild(el);
  });
}

function renderMetricCards(rootId, items, renderer) {
  const root = document.getElementById(rootId);
  root.innerHTML = "";
  if (!items?.length) {
    root.innerHTML = `
      <div class="empty-state">
        <picture>
          <source srcset="assets/images/nmb-workflow-illustration.webp" type="image/webp" />
          <img src="assets/images/nmb-workflow-illustration.png" alt="" />
        </picture>
        <div>
          <strong>No records</strong>
          <small>Nothing is available in the selected dashboard scope.</small>
        </div>
      </div>
    `;
    return;
  }
  items.forEach((item) => {
    const el = document.createElement("div");
    el.className = rootId === "district-cards" || rootId === "state-cards" ? "district-card" : "metric-card";
    el.innerHTML = renderer(item);
    root.appendChild(el);
  });
}

function renderQueue(items = []) {
  const root = document.getElementById("queue-cards");
  root.innerHTML = "";
  if (!items.length) {
    root.innerHTML = `
      <div class="empty-state">
        <picture>
          <source srcset="assets/images/nmb-workflow-illustration.webp" type="image/webp" />
          <img src="assets/images/nmb-workflow-illustration.png" alt="" />
        </picture>
        <div>
          <strong>No applications in queue</strong>
          <small>Current role has no pending workflow items.</small>
        </div>
      </div>
    `;
    return;
  }
  items.forEach((item) => {
    const el = document.createElement("div");
    el.className = "queue-card";
    el.innerHTML = `
      <div class="status-pill ${badgeTone(item.current_status)}">${item.current_status}</div>
      <strong>${item.application_id}</strong>
      <small>${item.scheme_component}</small>
      <small>Requested: Rs ${currency(item.requested_amount)}</small>
    `;
    root.appendChild(el);
  });
}

function renderReport(data) {
  const root = document.getElementById("report-summary");
  if (!data?.summary) {
    root.innerHTML = `<div class="report-tile">Report unavailable.</div>`;
    return;
  }
  const { kpis, filters } = data.summary;
  root.innerHTML = `
    <div class="report-tile"><strong>${data.report_name}</strong><small>Generated: ${new Date(data.generated_at).toLocaleString()}</small></div>
    <div class="report-tile"><strong>${filters.financial_year || "All FY"}</strong><small>Financial year scope</small></div>
    <div class="report-tile"><strong>${kpis.aap_submissions}</strong><small>AAP submissions in scope</small></div>
    <div class="report-tile"><strong>${kpis.farmers}</strong><small>Farmers covered by field data</small></div>
    <div class="report-tile"><strong>Rs ${currency(kpis.utilized_budget)}</strong><small>Budget utilized</small></div>
  `;
}

function renderSystemOverview(data) {
  renderMetricCards("system-services", Object.entries(data?.services || {}), ([name, status]) => `
    <div class="metric-badge ${badgeTone(status)}">${integrationStatus(status)}</div>
    <strong>${name}</strong>
    <small>Status: ${status}</small>
  `);
  renderMetricCards("system-integrations", Object.entries(data?.integrations || {}), ([name, status]) => `
    <div class="metric-badge ${badgeTone(integrationStatus(status))}">${integrationStatus(status)}</div>
    <strong>${name.replaceAll("_", " ")}</strong>
    <small>Integration posture</small>
  `);
  renderMetricCards("system-queues", Object.entries(data?.queue_health || {}), ([name, count]) => `
    <strong>${count}</strong>
    <small>${name.replaceAll("_", " ")}</small>
  `);
}

function renderNotifications(items = []) {
  renderMetricCards("notification-log", items, (item) => `
    <div class="metric-badge ${badgeTone(integrationStatus(item.status))}">${integrationStatus(item.status)}</div>
    <strong>${item.subject}</strong>
    <small>${item.recipient}</small>
    <small>${item.channels.join(", ")}</small>
    <small>${new Date(item.created_at).toLocaleString()}</small>
  `);
}

function renderIntegrationCatalog(items = []) {
  renderMetricCards("integration-catalog", items, (item) => `
    <div class="metric-badge ${badgeTone(integrationStatus(item.status))}">${integrationStatus(item.status)}</div>
    <strong>${integrationName(item.provider_name)}</strong>
    <small>${item.integration_type}</small>
  `);
}

function renderIntegrationLogs(items = []) {
  renderMetricCards("integration-log", items, (item) => `
    <div class="metric-badge ${badgeTone(integrationStatus(item.status))}">${integrationStatus(item.status)}</div>
    <strong>${integrationName(item.provider_name)}</strong>
    <small>${item.integration_type} | ${item.action}</small>
    <small>${new Date(item.created_at).toLocaleString()}</small>
  `);
}

function fillSelect(id, items, labelBuilder, valueKey) {
  const select = document.getElementById(id);
  if (!select) return;
  select.innerHTML = "";
  if (!items.length) {
    const option = document.createElement("option");
    option.value = "";
    option.textContent = "No records available";
    select.appendChild(option);
    return;
  }
  items.forEach((item) => {
    const option = document.createElement("option");
    option.value = item[valueKey];
    option.textContent = labelBuilder(item);
    select.appendChild(option);
  });
}

function formDataToJson(form) {
  const data = Object.fromEntries(new FormData(form).entries());
  for (const [key, value] of Object.entries(data)) {
    if (
      value !== "" &&
      !Number.isNaN(Number(value)) &&
      ["financial_year", "district_code", "state_code", "component_name", "remarks", "decision", "application_id", "inspector_email", "query_text", "aap_id", "budget_id", "quarter", "aadhaar_number", "bank_account_last4", "beneficiary_name", "channel", "recipient", "template_key", "message", "consent"].includes(key) === false
    ) {
      data[key] = Number(value);
    }
  }
  return data;
}

function normalizeNotificationRecipient(channel, value) {
  if (channel === "sms" || channel === "whatsapp") {
    return String(value).replace(/\D/g, "");
  }
  return String(value).trim();
}

function syncNotificationContactField() {
  const channel = document.getElementById("mock-notify-channel")?.value || "sms";
  const config = notificationChannelConfig[channel] || notificationChannelConfig.sms;
  const label = document.getElementById("mock-notify-recipient-label");
  const input = document.getElementById("mock-notify-recipient");
  const hint = document.getElementById("mock-notify-recipient-hint");
  if (label) label.textContent = config.label;
  if (hint) hint.textContent = config.hint;
  if (input) {
    input.inputMode = config.inputMode;
    input.autocomplete = config.autocomplete;
    input.placeholder = config.value;
    input.value = config.value;
  }
}

async function refresh() {
  if (!token) {
    window.location.href = pageUrl("/login");
    return;
  }

  const me = await api("/api/v1/auth/me");
  if (!me) return;
  if (me.role === "beneficiary") {
    window.location.href = pageUrl("/beneficiary");
    return;
  }
  currentUser = me;
  await hydrateDashboardFilters(me);

  document.getElementById("name").textContent = me.name;
  document.getElementById("role").textContent = `${me.role} | ${me.email}`;

  const query = buildQuery(activeFilters);
  const [summary, queue, report, ops, notifications, integrationCatalog, integrationLogs] = await Promise.all([
    api(`/api/v1/dashboard/summary${query}`),
    api("/api/v1/officer/applications"),
    api(`/api/v1/reports/overview${query}`),
    api("/api/v1/system/overview"),
    api("/api/v1/notifications?limit=8"),
    api("/api/v1/integrations/mock/catalog"),
    api("/api/v1/integrations/mock/logs?limit=8"),
  ]);
  const [inspections, aaps, budgets] = await Promise.all([
    api("/api/v1/officer/inspections"),
    api("/api/v1/aap"),
    api("/api/v1/budgets"),
  ]);

  if (!summary) return;

  document.getElementById("kpi-applications").textContent = summary.kpis.applications;
  document.getElementById("kpi-approved").textContent = summary.kpis.approved;
  document.getElementById("kpi-area").textContent = summary.kpis.area_hectares;
  document.getElementById("kpi-production").textContent = summary.kpis.production_mt;
  document.getElementById("kpi-budget").textContent = `Rs ${currency(summary.kpis.allocated_budget)}`;

  renderStatusBreakdown(summary.status_breakdown);
  renderMetricCards("budget-cards", summary.budget_cards, (item) => `
    <strong>${item.component_name}</strong>
    <small>Allocated: Rs ${currency(item.allocated_amount)}</small>
    <small>Released: Rs ${currency(item.released_amount)} | Utilized: Rs ${currency(item.utilized_amount)}</small>
  `);
  renderMetricCards("district-cards", summary.district_cards, (item) => `
    <strong>${item.district_code}</strong>
    <small>${item.financial_year} ${item.quarter}</small>
    <small>Area: ${item.area_hectares} Ha | Production: ${item.production_mt} MT</small>
    <small>Farmers: ${item.farmer_count}</small>
  `);
  renderMetricCards("state-cards", summary.state_cards, (item) => `
    <strong>${item.state_code}</strong>
    <small>Area: ${item.area_hectares} Ha</small>
    <small>Production: ${item.production_mt} MT | Farmers: ${item.farmer_count}</small>
  `);
  renderMetricCards("trend-cards", summary.trend_points, (item) => `
    <strong>${item.quarter}</strong>
    <small>Area: ${item.area_hectares} Ha</small>
    <small>Production: ${item.production_mt} MT | Farmers: ${item.farmer_count}</small>
  `);
  renderMetricCards("aap-cards", summary.aap_cards, (item) => `
    <div class="metric-badge ${badgeTone(item.current_status)}">${item.current_status}</div>
    <strong>${item.aap_id}</strong>
    <small>${item.state_code} | ${item.financial_year}</small>
    <small>Budget requested: Rs ${currency(item.budget_requested)}</small>
  `);
  renderQueue(queue || []);
  renderReport(report);
  renderSystemOverview(ops || {});
  renderNotifications(notifications || []);
  renderIntegrationCatalog(integrationCatalog?.items || []);
  renderIntegrationLogs(integrationLogs || []);
  fillSelect("clarification-application-id", queue || [], (item) => `${item.application_id} | ${item.current_status}`, "application_id");
  fillSelect("inspection-application-id", queue || [], (item) => `${item.application_id} | ${item.current_status}`, "application_id");
  fillSelect("decision-application-id", queue || [], (item) => `${item.application_id} | ${item.current_status}`, "application_id");
  fillSelect("inspection-complete-id", inspections || [], (item) => `${item.inspection_id} | ${item.status}`, "inspection_id");
  fillSelect("aap-review-id", aaps || [], (item) => `${item.aap_id} | ${item.current_status}`, "aap_id");
  fillSelect("budget-utilization-id", budgets || [], (item) => `${item.budget_id} | ${item.component_name}`, "budget_id");
  const batchIds = document.getElementById("batch-application-ids");
  if (batchIds && !batchIds.value.trim()) {
    batchIds.value = (queue || []).slice(0, 3).map((item) => item.application_id).join(", ");
  }
  renderFilterSummary();
}

async function bindForm(id, handler, messageId) {
  const form = document.getElementById(id);
  if (!form) return;
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const result = await handler(form);
    const node = document.getElementById(messageId);
    node.textContent = result.text;
    node.style.color = result.error ? "var(--danger)" : "var(--success)";
    refresh();
  });
}

bindForm("dashboard-filter-form", async (form) => {
  const payload = formDataToJson(form);
  Object.assign(activeFilters, payload);
  await loadDistrictOptions(activeFilters.state_code, activeFilters.district_code);
  syncFilterForm();
  return { text: "Filters applied.", error: false };
}, "filter-message");

bindForm("aap-form", async (form) => {
  const data = await api("/api/v1/aap", { method: "POST", body: JSON.stringify(formDataToJson(form)) });
  return { text: data?.aap_id ? `AAP submitted: ${data.aap_id}` : data?.detail || "Action failed", error: Boolean(data?.detail) };
}, "aap-message");

bindForm("field-data-form", async (form) => {
  const data = await api("/api/v1/field-data", { method: "POST", body: JSON.stringify(formDataToJson(form)) });
  return { text: data?.field_data_id ? `Field record added: ${data.field_data_id}` : data?.detail || "Action failed", error: Boolean(data?.detail) };
}, "field-data-message");

bindForm("budget-form", async (form) => {
  const data = await api("/api/v1/budgets", { method: "POST", body: JSON.stringify(formDataToJson(form)) });
  return { text: data?.budget_id ? `Budget created: ${data.budget_id}` : data?.detail || "Action failed", error: Boolean(data?.detail) };
}, "budget-message");

bindForm("budget-utilization-form", async (form) => {
  const payload = formDataToJson(form);
  const data = await api(`/api/v1/budgets/${payload.budget_id}/utilization`, {
    method: "POST",
    body: JSON.stringify({
      released_amount: payload.released_amount,
      utilized_amount: payload.utilized_amount,
      remarks: payload.remarks,
    }),
  });
  return { text: data?.budget_id ? `Budget updated: ${data.budget_id}` : data?.detail || "Action failed", error: Boolean(data?.detail) };
}, "budget-utilization-message");

bindForm("clarification-form", async (form) => {
  const payload = formDataToJson(form);
  const data = await api(`/api/v1/officer/applications/${payload.application_id}/clarifications`, {
    method: "POST",
    body: JSON.stringify({ query_text: payload.query_text }),
  });
  return { text: data?.clarification_id ? `Clarification raised: ${data.clarification_id}` : data?.detail || "Action failed", error: Boolean(data?.detail) };
}, "clarification-message");

bindForm("inspection-form", async (form) => {
  const payload = formDataToJson(form);
  const data = await api(`/api/v1/officer/applications/${payload.application_id}/inspection/assign`, {
    method: "POST",
    body: JSON.stringify({ inspector_email: payload.inspector_email }),
  });
  return { text: data?.inspection_id ? `Inspection assigned: ${data.inspection_id}` : data?.detail || "Action failed", error: Boolean(data?.detail) };
}, "inspection-message");

bindForm("decision-form", async (form) => {
  const payload = formDataToJson(form);
  if (payload.decision === "recommend") {
    const data = await api(`/api/v1/officer/applications/${payload.application_id}/recommend`, {
      method: "POST",
      body: JSON.stringify({ remarks: payload.remarks }),
    });
    return { text: data?.current_status ? `Application updated: ${data.current_status}` : data?.detail || "Action failed", error: Boolean(data?.detail) };
  }
  const data = await api(`/api/v1/nmb/applications/${payload.application_id}/decision`, {
    method: "POST",
    body: JSON.stringify({ decision: payload.decision, remarks: payload.remarks }),
  });
  return { text: data?.current_status ? `Board decision applied: ${data.current_status}` : data?.detail || "Action failed", error: Boolean(data?.detail) };
}, "decision-message");

bindForm("batch-decision-form", async (form) => {
  const payload = formDataToJson(form);
  const applicationIds = String(payload.application_ids)
    .split(/\s|,|\n/)
    .map((item) => item.trim())
    .filter(Boolean);
  const data = await api("/api/v1/nmb/applications/batch-decision", {
    method: "POST",
    body: JSON.stringify({
      application_ids: applicationIds,
      decision: payload.decision,
      remarks: payload.remarks,
    }),
  });
  return { text: data?.processed?.length ? data.processed.map((item) => `${item.application_id}:${item.status}`).join(", ") : data?.detail || "Action failed", error: Boolean(data?.detail) };
}, "batch-decision-message");

bindForm("inspection-complete-form", async (form) => {
  const payload = formDataToJson(form);
  const data = await api(`/api/v1/officer/inspections/${payload.inspection_id}/complete`, {
    method: "POST",
    body: JSON.stringify({
      remarks: payload.remarks,
      latitude: payload.latitude,
      longitude: payload.longitude,
      accuracy: payload.accuracy,
      photo_name: payload.photo_name,
    }),
  });
  return { text: data?.status ? `Inspection marked ${data.status}` : data?.detail || "Action failed", error: Boolean(data?.detail) };
}, "inspection-complete-message");

bindForm("aap-review-form", async (form) => {
  const payload = formDataToJson(form);
  const data = await api(`/api/v1/aap/${payload.aap_id}/review`, {
    method: "POST",
    body: JSON.stringify({ decision: payload.decision, remarks: payload.remarks }),
  });
  return { text: data?.current_status ? `AAP updated: ${data.current_status}` : data?.detail || "Action failed", error: Boolean(data?.detail) };
}, "aap-review-message");

bindForm("mock-notify-form", async (form) => {
  const payload = formDataToJson(form);
  const config = notificationChannelConfig[payload.channel] || notificationChannelConfig.sms;
  payload.recipient = normalizeNotificationRecipient(payload.channel, payload.recipient);
  if (!config.validator(payload.recipient)) {
    return { text: config.error, error: true };
  }
  const data = await api("/api/v1/integrations/mock/notify", {
    method: "POST",
    body: JSON.stringify(payload),
  });
  return { text: data?.event_id ? `Notification logged: ${data.event_id}` : data?.detail || "Action failed", error: Boolean(data?.detail) };
}, "mock-notify-message");

bindForm("mock-aadhaar-kyc-form", async (form) => {
  const payload = formDataToJson(form);
  const data = await api("/api/v1/integrations/mock/aadhaar-kyc", {
    method: "POST",
    body: JSON.stringify({
      beneficiary_name: payload.beneficiary_name,
      aadhaar_number: payload.aadhaar_number,
      consent: payload.consent === "true",
    }),
  });
  return { text: data?.event_id ? `Mock KYC logged: ${data.event_id}` : data?.detail || "Action failed", error: Boolean(data?.detail) };
}, "mock-aadhaar-message");

bindForm("mock-dbt-form", async (form) => {
  const data = await api("/api/v1/integrations/mock/dbt/disburse", {
    method: "POST",
    body: JSON.stringify(formDataToJson(form)),
  });
  return { text: data?.event_id ? `Mock DBT logged: ${data.event_id}` : data?.detail || "Action failed", error: Boolean(data?.detail) };
}, "mock-dbt-message");

document.getElementById("refresh-report").addEventListener("click", async () => {
  const report = await api(`/api/v1/reports/overview${buildQuery(activeFilters)}`);
  renderReport(report);
});

document.getElementById("export-report").addEventListener("click", async () => {
  const query = buildQuery({ ...activeFilters, format: "csv" });
  const content = await api(`/api/v1/reports/overview${query}`);
  if (!content) return;
  const blob = new Blob([content], { type: "text/csv" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = "makhana-monitoring-snapshot.csv";
  link.click();
  URL.revokeObjectURL(url);
});

document.getElementById("reset-dashboard-filters").addEventListener("click", async () => {
  Object.assign(activeFilters, {
    ...defaultFilters,
    state_code: currentUser?.role === "nmb_admin" ? "" : (currentUser?.state_code || defaultFilters.state_code),
    district_code: "",
    quarter: "",
  });
  await hydrateDashboardFilters(currentUser || { role: "nmb_admin", state_code: "" });
  document.getElementById("filter-message").textContent = "Filters reset to default dashboard scope.";
  refresh();
});

document.querySelectorAll("[data-quarter-value]").forEach((node) => {
  node.addEventListener("click", () => {
    setQuarterSlicer(node.dataset.quarterValue || "");
  });
});

document.getElementById("filter-state-code")?.addEventListener("change", async (event) => {
  await loadDistrictOptions(event.target.value, "");
});

document.getElementById("mock-notify-channel")?.addEventListener("change", syncNotificationContactField);

bindSectionNavigation();
syncNotificationContactField();
refresh();
