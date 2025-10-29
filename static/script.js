const sendOtpBtn = document.getElementById("send-otp-btn");
const verifyOtpBtn = document.getElementById("verify-otp-btn");
const emailInput = document.getElementById("email");
const otpInput = document.getElementById("otp");
const loginSection = document.getElementById("login-section");
const otpSection = document.getElementById("otp-section");
const chatSection = document.getElementById("chat-section");
const chatBox = document.getElementById("chat-box");
const chatForm = document.getElementById("chat-form");
const messageInput = document.getElementById("message-input");
const fileInput = document.getElementById("file-input");

sendOtpBtn.onclick = async () => {
  const email = emailInput.value.trim();
  if (!email || !email.includes("@")) {
    alert("Enter a valid email");
    return;
  }

  sendOtpBtn.disabled = true;
  const res = await fetch("/send_otp", {
    method: "POST",
    body: new URLSearchParams({ email }),
  });
  const data = await res.json();
  alert(data.message);
  sendOtpBtn.disabled = false;

  if (data.status === "success") {
    loginSection.style.display = "none";
    otpSection.style.display = "block";
  }
};

verifyOtpBtn.onclick = async () => {
  const otp = otpInput.value.trim();
  if (otp.length !== 6) {
    alert("Enter 6 digit OTP");
    return;
  }

  verifyOtpBtn.disabled = true;
  const res = await fetch("/verify_otp", {
    method: "POST",
    body: new URLSearchParams({ otp }),
  });
  const data = await res.json();
  verifyOtpBtn.disabled = false;

  if (data.status === "success") {
    otpSection.style.display = "none";
    chatSection.style.display = "block";
  } else {
    alert(data.message || "Invalid OTP");
  }
};

chatForm.onsubmit = async (e) => {
  e.preventDefault();
  const message = messageInput.value.trim();
  if (!message && fileInput.files.length === 0) return;

  if (message) appendMessage("You", message, "user-message");
  messageInput.value = "";

  const formData = new FormData();
  formData.append("message", message);
  if (fileInput.files.length > 0) {
    formData.append("file", fileInput.files[0]);
  }

  try {
    const res = await fetch("/chat", {
      method: "POST",
      body: formData,
    });

    const data = await res.json();
    appendMessage("Bot", data.response, "bot-message");
  } catch (error) {
    appendMessage("Bot", "Error sending message.", "bot-message");
  }

  fileInput.value = ""; // clear after upload completes
};

function appendMessage(sender, text, className) {
  const msgDiv = document.createElement("div");
  msgDiv.classList.add("message", className);
  msgDiv.innerText = `${sender}: ${text}`;
  chatBox.appendChild(msgDiv);
  chatBox.scrollTop = chatBox.scrollHeight;
}
