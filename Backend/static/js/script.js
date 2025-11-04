function openModal() {
  document.getElementById('loginModal').style.display = 'block';
}

function closeModal() {
  document.getElementById('loginModal').style.display = 'none';
}

// Optional: Close login modal when clicked outside
window.onclick = function(event) {
  const modal = document.getElementById('loginModal');
  if (modal && event.target === modal) {
    modal.style.display = "none";
  }
}; 