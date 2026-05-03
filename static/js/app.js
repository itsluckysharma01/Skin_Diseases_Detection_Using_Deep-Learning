(function () {
  const dropzone = document.getElementById("dropzone");
  const fileInput = document.getElementById("file-input");
  const previewRow = document.getElementById("preview-row");
  const previewImg = document.getElementById("preview-img");
  const btnAnalyze = document.getElementById("btn-analyze");
  const btnClear = document.getElementById("btn-clear");
  const btnOpenCamera = document.getElementById("btn-open-camera");
  const btnCapture = document.getElementById("btn-capture");
  const btnCloseCamera = document.getElementById("btn-close-camera");
  const cameraWrap = document.getElementById("camera-wrap");
  const cameraVideo = document.getElementById("camera-video");
  const cameraCanvas = document.getElementById("camera-canvas");
  const statusEl = document.getElementById("status");
  const resultsEl = document.getElementById("results");
  const topCard = document.getElementById("top-card");
  const recommendCard = document.getElementById("recommend-card");
  const rankList = document.getElementById("rank-list");
  const disclaimerEl = document.getElementById("disclaimer");
  const disclaimerHiEl = document.getElementById("disclaimer-hi");

  let currentFile = null;
  let mediaStream = null;

  function setStatus(text, kind) {
    statusEl.textContent = text || "";
    statusEl.className = "status" + (kind ? " " + kind : "");
  }

  function showResults(data) {
    resultsEl.classList.remove("hidden");
    const top = data.top_prediction;
    topCard.innerHTML =
      '<p class="label"></p><p class="label-hi"></p><p class="conf"></p>';
    topCard.querySelector(".label").textContent = top.label;
    topCard.querySelector(".label-hi").textContent = "Hindi: " + (top.label_hi || top.label);
    topCard.querySelector(".conf").textContent =
      (top.confidence * 100).toFixed(2) + "% confidence";
    recommendCard.textContent = "Recommendation: " + (top.recommendation || "Consult dermatologist.");

    rankList.innerHTML = "";
    data.top_k.forEach((row) => {
      const li = document.createElement("li");
      const name = document.createElement("span");
      name.className = "name";
      name.textContent = row.rank + ". " + row.label + " | " + (row.label_hi || row.label);
      const pct = document.createElement("span");
      pct.className = "pct";
      pct.textContent = (row.confidence * 100).toFixed(1) + "%";
      li.appendChild(name);
      li.appendChild(pct);
      rankList.appendChild(li);
    });

    disclaimerEl.textContent = data.disclaimer || "";
    disclaimerHiEl.textContent = data.disclaimer_hi || "";
  }

  function resetResults() {
    resultsEl.classList.add("hidden");
    topCard.innerHTML = "";
    recommendCard.innerHTML = "";
    rankList.innerHTML = "";
    disclaimerEl.textContent = "";
    disclaimerHiEl.textContent = "";
  }

  function onFile(file) {
    if (!file || !file.type.startsWith("image/")) {
      setStatus("Please choose an image file.", "error");
      return;
    }
    currentFile = file;
    const url = URL.createObjectURL(file);
    previewImg.onload = function () {
      URL.revokeObjectURL(url);
    };
    previewImg.src = url;
    previewRow.classList.remove("hidden");
    btnAnalyze.disabled = false;
    resetResults();
    setStatus("Ready to analyze.");
  }

  async function openCamera() {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setStatus("Camera is not supported in this browser.", "error");
      return;
    }
    try {
      mediaStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "environment" },
        audio: false,
      });
      cameraVideo.srcObject = mediaStream;
      cameraWrap.classList.remove("hidden");
      btnCapture.classList.remove("hidden");
      btnCloseCamera.classList.remove("hidden");
      setStatus("Camera ready. Click Capture Photo.");
    } catch (err) {
      setStatus("Could not open camera: " + err.message, "error");
    }
  }

  function closeCamera() {
    if (mediaStream) {
      mediaStream.getTracks().forEach((t) => t.stop());
      mediaStream = null;
    }
    cameraVideo.srcObject = null;
    cameraWrap.classList.add("hidden");
    btnCapture.classList.add("hidden");
    btnCloseCamera.classList.add("hidden");
  }

  function captureFromCamera() {
    if (!mediaStream) return;
    const w = cameraVideo.videoWidth || 640;
    const h = cameraVideo.videoHeight || 480;
    cameraCanvas.width = w;
    cameraCanvas.height = h;
    const ctx = cameraCanvas.getContext("2d");
    ctx.drawImage(cameraVideo, 0, 0, w, h);
    cameraCanvas.toBlob(
      (blob) => {
        if (!blob) {
          setStatus("Capture failed.", "error");
          return;
        }
        const file = new File([blob], "camera-photo.jpg", { type: "image/jpeg" });
        onFile(file);
        closeCamera();
      },
      "image/jpeg",
      0.95
    );
  }

  dropzone.addEventListener("click", () => fileInput.click());
  dropzone.addEventListener("keydown", (e) => {
    if (e.key === "Enter" || e.key === " ") {
      e.preventDefault();
      fileInput.click();
    }
  });

  ["dragenter", "dragover"].forEach((ev) => {
    dropzone.addEventListener(ev, (e) => {
      e.preventDefault();
      dropzone.style.borderColor = "var(--accent)";
    });
  });
  ["dragleave", "drop"].forEach((ev) => {
    dropzone.addEventListener(ev, (e) => {
      e.preventDefault();
      dropzone.style.borderColor = "";
    });
  });
  dropzone.addEventListener("drop", (e) => {
    const f = e.dataTransfer.files[0];
    onFile(f);
  });

  fileInput.addEventListener("change", () => {
    const f = fileInput.files[0];
    onFile(f);
  });
  btnOpenCamera.addEventListener("click", openCamera);
  btnCapture.addEventListener("click", captureFromCamera);
  btnCloseCamera.addEventListener("click", closeCamera);

  btnClear.addEventListener("click", () => {
    currentFile = null;
    fileInput.value = "";
    previewRow.classList.add("hidden");
    previewImg.removeAttribute("src");
    btnAnalyze.disabled = true;
    closeCamera();
    resetResults();
    setStatus("");
  });

  btnAnalyze.addEventListener("click", async () => {
    if (!currentFile) return;
    const fd = new FormData();
    fd.append("image", currentFile, currentFile.name);

    btnAnalyze.disabled = true;
    setStatus("Running model… first load can take a few seconds.", "loading");

    try {
      const res = await fetch("/api/predict", {
        method: "POST",
        body: fd,
      });
      const data = await res.json();
      if (!res.ok) {
        setStatus(data.error || "Request failed.", "error");
        btnAnalyze.disabled = false;
        return;
      }
      showResults(data);
      setStatus("Done.");
    } catch (err) {
      setStatus("Network error: " + err.message, "error");
    }
    btnAnalyze.disabled = false;
  });
})();
