const API_BASE = "http://localhost:5000/api";

// Kiểm tra kết nối API
async function checkAPIStatus() {
  try {
    const response = await fetch(`${API_BASE}/health`);
    const data = await response.json();

    if (response.ok && data.model_loaded) {
      updateStatus("API đã kết nối", "connected");
    } else if (response.ok) {
      updateStatus("API kết nối nhưng mô hình chưa sẵn sàng", "error");
    } else {
      updateStatus("Lỗi kết nối API", "error");
    }
  } catch (error) {
    updateStatus("Không thể kết nối API", "error");
    console.error("API Error:", error);
  }
}

function updateStatus(text, status) {
  const statusText = document.getElementById("statusText");
  const statusDot = document.getElementById("statusDot");

  statusText.textContent = text;
  statusDot.className = `status-dot ${status}`;
}

// Tab Switching
function switchTab(tabName) {
  // Hide all tabs
  document.querySelectorAll(".tab-content").forEach((tab) => {
    tab.classList.remove("active");
  });
  document.querySelectorAll(".tab-button").forEach((btn) => {
    btn.classList.remove("active");
  });

  // Show selected tab
  document.getElementById(tabName).classList.add("active");
  event.target.classList.add("active");
}

// Alert System
function showAlert(message, type = "info") {
  const alert = document.getElementById("alert");
  alert.textContent = message;
  alert.className = `alert show ${type}`;

  setTimeout(() => {
    alert.classList.remove("show");
  }, 5000);
}

// Single Message Prediction
async function predictSingle() {
  const text = document.getElementById("messageInput").value.trim();

  if (!text) {
    showAlert("Vui lòng nhập nội dung tin nhắn", "error");
    return;
  }

  showLoading("singleLoading", true);

  try {
    const response = await fetch(`${API_BASE}/predict`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ text }),
    });

    const data = await response.json();

    if (response.ok) {
      displaySingleResult(data);
      showAlert("Phân tích thành công!", "success");
    } else {
      showAlert(data.message || "Lỗi phân tích", "error");
    }
  } catch (error) {
    showAlert("Lỗi: " + error.message, "error");
  } finally {
    showLoading("singleLoading", false);
  }
}

function displaySingleResult(data) {
  const resultsDiv = document.getElementById("singleResults");
  const isSpam = data.label === "Spam";
  const cardClass = isSpam ? "spam" : "ham";
  const badgeEmoji = isSpam ? "⚠️" : "✅";

  const html = `
                <div class="result-card ${cardClass}">
                    <div class="result-header">
                        <h3>${badgeEmoji} ${data.label}</h3>
                        <span class="badge ${cardClass}">${data.label}</span>
                    </div>
                    <div class="result-text">"${data.text}"</div>
                    <div class="confidence">
                        Độ tin cậy: ${(data.confidence * 100).toFixed(2)}%
                    </div>
                    <div class="progress-bar">
                        <div class="progress-fill ${cardClass}" style="width: ${data.confidence * 100}%"></div>
                    </div>
                </div>
            `;

  resultsDiv.innerHTML = html;
  resultsDiv.classList.add("show");
}

// File Upload
function handleDragOver(event) {
  event.preventDefault();
  document.getElementById("dropZone").classList.add("dragover");
}

function handleDragLeave(event) {
  document.getElementById("dropZone").classList.remove("dragover");
}

function handleDrop(event) {
  event.preventDefault();
  document.getElementById("dropZone").classList.remove("dragover");

  const files = event.dataTransfer.files;
  if (files.length > 0) {
    document.getElementById("fileInput").files = files;
    handleFileSelect({ target: { files } });
  }
}

function handleFileSelect(event) {
  const file = event.target.files[0];

  if (!file) return;

  if (!file.name.endsWith(".txt")) {
    showAlert("Chỉ hỗ trợ file .txt", "error");
    return;
  }

  if (file.size > 10 * 1024 * 1024) {
    // 10MB
    showAlert("File quá lớn (tối đa 10MB)", "error");
    return;
  }

  document.getElementById("fileName").textContent =
    `📄 ${file.name} (${(file.size / 1024).toFixed(2)} KB)`;
  document.getElementById("uploadBtn").disabled = false;
}

function clearFile() {
  document.getElementById("fileInput").value = "";
  document.getElementById("fileName").textContent = "";
  document.getElementById("uploadBtn").disabled = true;
  document.getElementById("fileResults").classList.remove("show");
}

async function predictFile() {
  const file = document.getElementById("fileInput").files[0];

  if (!file) {
    showAlert("Vui lòng chọn file", "error");
    return;
  }

  showLoading("fileLoading", true);

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch(`${API_BASE}/predict-file`, {
      method: "POST",
      body: formData,
    });

    const data = await response.json();

    if (response.ok) {
      displayFileResults(data);
      showAlert(
        `Phân tích ${data.total_messages} tin nhắn thành công!`,
        "success",
      );
    } else {
      showAlert(data.message || "Lỗi phân tích", "error");
    }
  } catch (error) {
    showAlert("Lỗi: " + error.message, "error");
  } finally {
    showLoading("fileLoading", false);
  }
}

function displayFileResults(data) {
  const resultsDiv = document.getElementById("fileResults");

  const statsHtml = `
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">${data.total_messages}</div>
                        <div class="stat-label">Tổng Tin</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" style="color: #ff6b6b;">${data.spam_count}</div>
                        <div class="stat-label">Spam</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" style="color: #51cf66;">${data.ham_count}</div>
                        <div class="stat-label">Ham</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" style="color: #667eea;">${data.spam_percentage}</div>
                        <div class="stat-label">Spam %</div>
                    </div>
                </div>
            `;

  const predictionsHtml = data.predictions
    .map((pred) => {
      const isSpam = pred.label === "Spam";
      const cardClass = isSpam ? "spam" : "ham";
      const badgeEmoji = isSpam ? "⚠️" : "✅";

      return `
                    <div class="result-card ${cardClass}">
                        <div class="result-header">
                            <span class="badge ${cardClass}">${badgeEmoji} ${pred.label}</span>
                            <span class="confidence">${(pred.confidence * 100).toFixed(1)}%</span>
                        </div>
                        <div class="result-text">"${pred.text}"</div>
                        <div class="progress-bar">
                            <div class="progress-fill ${cardClass}" style="width: ${pred.confidence * 100}%"></div>
                        </div>
                    </div>
                `;
    })
    .join("");

  resultsDiv.innerHTML = statsHtml + predictionsHtml;
  resultsDiv.classList.add("show");
}

// Batch Prediction
async function predictBatch() {
  const text = document.getElementById("batchInput").value.trim();

  if (!text) {
    showAlert("Vui lòng nhập danh sách tin nhắn", "error");
    return;
  }

  const texts = text
    .split("\n")
    .map((t) => t.trim())
    .filter((t) => t);

  if (texts.length === 0) {
    showAlert("Danh sách trống", "error");
    return;
  }

  showLoading("batchLoading", true);

  try {
    const response = await fetch(`${API_BASE}/predict-batch`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ texts }),
    });

    const data = await response.json();

    if (response.ok) {
      displayBatchResults(data);
      showAlert(
        `Phân tích ${data.total_messages} tin nhắn thành công!`,
        "success",
      );
    } else {
      showAlert(data.message || "Lỗi phân tích", "error");
    }
  } catch (error) {
    showAlert("Lỗi: " + error.message, "error");
  } finally {
    showLoading("batchLoading", false);
  }
}

function displayBatchResults(data) {
  const resultsDiv = document.getElementById("batchResults");

  const statsHtml = `
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-number">${data.total_messages}</div>
                        <div class="stat-label">Tổng Tin</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" style="color: #ff6b6b;">${data.spam_count}</div>
                        <div class="stat-label">Spam</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" style="color: #51cf66;">${data.ham_count}</div>
                        <div class="stat-label">Ham</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-number" style="color: #667eea;">${data.spam_percentage}</div>
                        <div class="stat-label">Spam %</div>
                    </div>
                </div>
            `;

  const predictionsHtml = data.predictions
    .map((pred) => {
      const isSpam = pred.label === "Spam";
      const cardClass = isSpam ? "spam" : "ham";
      const badgeEmoji = isSpam ? "⚠️" : "✅";

      return `
                    <div class="result-card ${cardClass}">
                        <div class="result-header">
                            <span class="badge ${cardClass}">${badgeEmoji} ${pred.label}</span>
                            <span class="confidence">${(pred.confidence * 100).toFixed(1)}%</span>
                        </div>
                        <div class="result-text">"${pred.text}"</div>
                        <div class="progress-bar">
                            <div class="progress-fill ${cardClass}" style="width: ${pred.confidence * 100}%"></div>
                        </div>
                    </div>
                `;
    })
    .join("");

  resultsDiv.innerHTML = statsHtml + predictionsHtml;
  resultsDiv.classList.add("show");
}

// Helper Functions
function showLoading(id, show) {
  const loadingDiv = document.getElementById(id);
  if (show) {
    loadingDiv.classList.add("show");
  } else {
    loadingDiv.classList.remove("show");
  }
}

// Initialize on page load
document.addEventListener("DOMContentLoaded", () => {
  checkAPIStatus();

  // Check API status every 30 seconds
  setInterval(checkAPIStatus, 30000);
});
