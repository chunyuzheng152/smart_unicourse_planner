// When the backend is ready, replace localStorage with API requests.
// Suggested
// GET /api/me
// POST /api/login
// POST /api/signup
// POST /api/user/settings
// POST /api/logout

function getInitials(name) {
  if (!name) {
    return "U";
  }

  const words = name.trim().split(" ");

  if (words.length === 1) {
    return words[0].charAt(0).toUpperCase();
  }

  return (words[0].charAt(0) + words[1].charAt(0)).toUpperCase();
}

function updateNavbarAvatar() {
  const navAvatar = document.getElementById("navAvatar");

  if (!navAvatar) {
    return;
  }

  // TODO
  // Replace the localStorage data below with user data from GET /api/me.
  // Expected response example:
  // {
  //   "username": "alice bob",
  //   "avatar_url": "/static/uploads/avatars/user_1.png"
  // }

  const savedName = localStorage.getItem("username") || "User";
  const savedAvatar = localStorage.getItem("avatarImage");

  if (savedAvatar) {
    navAvatar.textContent = "";
    navAvatar.style.backgroundImage = `url(${savedAvatar})`;
    navAvatar.style.backgroundSize = "cover";
    navAvatar.style.backgroundPosition = "center";
  } else {
    navAvatar.textContent = getInitials(savedName);
    navAvatar.style.backgroundImage = "none";
  }
}

document.addEventListener("DOMContentLoaded", updateNavbarAvatar);