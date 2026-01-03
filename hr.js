async function createEmployee() {
  const token = localStorage.getItem("token");

  const res = await apiRequest(
    "/hr/create-employee",
    "POST",
    { name: "Demo User", email: "demo@test.com" },
    token
  );

  document.getElementById("output").innerText =
    "Employee Login ID: " + res.loginId;
}
