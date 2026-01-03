const employees = [
  { name: "Jainam Oswal", status: "Present", email: "jainam@test.com", loginId: "EMP001" },
  { name: "Rahul Verma", status: "On Leave", email: "rahul@test.com", loginId: "EMP002" },
  { name: "Anita Sharma", status: "Absent", email: "anita@test.com", loginId: "EMP003" }
];

function showTab(tab) {
  document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
  event.target.classList.add("active");

  if (tab === "employees") loadEmployees();
  if (tab === "attendance") loadAttendance();
  if (tab === "timeoff") loadTimeOff();
}

function loadEmployees() {
  let html = `<h2>Employees</h2><div class="grid">`;

  employees.forEach((e, i) => {
    html += `
      <div class="card" onclick="viewEmployee(${i})">
        <h3>${e.name}</h3>
        <p>Status: ${e.status}</p>
      </div>
    `;
  });

  html += `</div>`;
  document.getElementById("content").innerHTML = html;
}

function viewEmployee(index) {
  const e = employees[index];
  document.getElementById("content").innerHTML = `
    <h2>Employee Details</h2>
    <div class="card">
      <p><b>Name:</b> ${e.name}</p>
      <p><b>Email:</b> ${e.email}</p>
      <p><b>Login ID:</b> ${e.loginId}</p>
      <p><b>Status:</b> ${e.status}</p>
    </div>
    <button onclick="loadEmployees()">← Back</button>
  `;
}

function loadAttendance() {
  document.getElementById("content").innerHTML = `
    <h2>Attendance</h2>
    <div class="card">Attendance list view (as per PDF) – coming next</div>
  `;
}

function loadTimeOff() {
  document.getElementById("content").innerHTML = `
    <h2>Time Off</h2>
    <div class="card">Leave approvals & allocation (as per PDF) – coming next</div>
  `;
}

function logout() {
  alert("Logout");
}

loadEmployees(); // DEFAULT TAB
