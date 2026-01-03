async function login() {
  const role = document.getElementById("role").value;
  const email = document.getElementById("email").value;
  const password = document.getElementById("password").value;

  if (!role || !email || !password) {
    document.getElementById("msg").innerText = "All fields required";
    return;
  }

  const data = await apiRequest("/auth/login", "POST", {
    email,
    password
  });

  if (!data.token) {
    document.getElementById("msg").innerText = "Invalid credentials";
    return;
  }

  localStorage.setItem("token", data.token);
  localStorage.setItem("role", role);

  if (role === "HR") {
    window.location.href = "hr.html";
  } else {
    window.location.href = "employee.html";
  }
}
