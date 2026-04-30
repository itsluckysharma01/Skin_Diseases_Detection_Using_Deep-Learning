const diseaseDataElement = document.getElementById("disease-data");
let diseaseData = [];

try {
  diseaseData = JSON.parse(diseaseDataElement?.textContent || "[]");
  if (!Array.isArray(diseaseData)) {
    diseaseData = [];
  }
} catch (error) {
  diseaseData = [];
}

const tabButtons = document.querySelectorAll(".tab-btn");
const tabPanels = {
  upload: document.getElementById("upload-panel"),
  camera: document.getElementById("camera-panel"),
};

const form = document.getElementById("predict-form");
const imageInput = document.getElementById("image-input");
const loading = document.getElementById("loading");

const resultEmpty = document.getElementById("result-empty");
const resultContent = document.getElementById("result-content");
const predictedName = document.getElementById("predicted-name");
const predictedConfidence = document.getElementById("predicted-confidence");
const predictedSummary = document.getElementById("predicted-summary");
const topPredictions = document.getElementById("top-predictions");
const urgency = document.getElementById("urgency");
const specialist = document.getElementById("specialist");
const actions = document.getElementById("recommended-actions");
const signs = document.getElementById("common-signs");
const triggers = document.getElementById("possible-triggers");
const resultDisclaimer = document.getElementById("result-disclaimer");

const diseaseSearch = document.getElementById("disease-search");
const diseaseList = document.getElementById("disease-list");

const video = document.getElementById("camera-video");
const canvas = document.getElementById("camera-canvas");
const startCameraButton = document.getElementById("start-camera");
const captureButton = document.getElementById("capture-camera");
const stopCameraButton = document.getElementById("stop-camera");

let cameraStream = null;

function setActiveTab(tab) {
  tabButtons.forEach((button) => {
    button.classList.toggle("active", button.dataset.tab === tab);
  });

  Object.keys(tabPanels).forEach((key) => {
    tabPanels[key].classList.toggle("active", key === tab);
  });
}

function createListItems(items) {
  const fragment = document.createDocumentFragment();
  items.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = item;
    fragment.appendChild(li);
  });
  return fragment;
}

function renderPrediction(result) {
  const primary = result.predicted;
  const details = primary.details || {};

  predictedName.textContent = primary.class_name;
  predictedConfidence.textContent = `Confidence: ${primary.probability}%`;
  predictedSummary.textContent = details.clinical_summary || "";

  topPredictions.innerHTML = "";
  result.top_predictions.forEach((item) => {
    const li = document.createElement("li");
    li.textContent = `${item.class_name} - ${item.probability}%`;
    topPredictions.appendChild(li);
  });

  urgency.textContent = `Urgency: ${details.urgency || "Not specified"}`;
  specialist.textContent = `Recommended specialist: ${details.specialist || "Dermatologist"}`;

  actions.innerHTML = "";
  signs.innerHTML = "";
  triggers.innerHTML = "";

  actions.appendChild(createListItems(details.recommended_actions || []));
  signs.appendChild(createListItems(details.common_signs || []));
  triggers.appendChild(createListItems(details.possible_triggers || []));

  resultDisclaimer.textContent = result.disclaimer || "";

  resultEmpty.classList.add("hidden");
  resultContent.classList.remove("hidden");
}

async function runPredictionWithFormData(formData) {
  loading.classList.remove("hidden");

  try {
    const response = await fetch("/api/predict", {
      method: "POST",
      body: formData,
    });
    const payload = await response.json();

    if (!payload.ok) {
      alert(payload.error || "Prediction failed.");
      return;
    }

    renderPrediction(payload.result);
  } catch (error) {
    alert("Unable to connect to prediction service.");
  } finally {
    loading.classList.add("hidden");
  }
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  if (!imageInput.files.length) {
    alert("Please select an image first.");
    return;
  }

  const formData = new FormData();
  formData.append("image", imageInput.files[0]);
  await runPredictionWithFormData(formData);
});

startCameraButton.addEventListener("click", async () => {
  try {
    cameraStream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: "environment" },
      audio: false,
    });
    video.srcObject = cameraStream;
  } catch (error) {
    alert("Camera access was denied or not available.");
  }
});

stopCameraButton.addEventListener("click", () => {
  if (!cameraStream) {
    return;
  }
  cameraStream.getTracks().forEach((track) => track.stop());
  cameraStream = null;
  video.srcObject = null;
});

captureButton.addEventListener("click", async () => {
  if (!cameraStream) {
    alert("Start camera first.");
    return;
  }

  const width = video.videoWidth || 640;
  const height = video.videoHeight || 480;

  canvas.width = width;
  canvas.height = height;

  const ctx = canvas.getContext("2d");
  ctx.drawImage(video, 0, 0, width, height);

  const blob = await new Promise((resolve) =>
    canvas.toBlob(resolve, "image/jpeg", 0.95),
  );
  if (!blob) {
    alert("Could not capture camera frame.");
    return;
  }

  const formData = new FormData();
  formData.append("image", blob, "camera-capture.jpg");
  await runPredictionWithFormData(formData);
});

tabButtons.forEach((button) => {
  button.addEventListener("click", () => setActiveTab(button.dataset.tab));
});

function createDiseaseCard(item) {
  const wrapper = document.createElement("article");
  wrapper.className = "disease-item";

  const head = document.createElement("button");
  head.className = "disease-head";
  head.type = "button";
  head.textContent = `${item.index + 1}. ${item.name}`;

  const body = document.createElement("div");
  body.className = "disease-body";

  const details = item.details || {};

  const summary = document.createElement("p");
  summary.textContent = details.clinical_summary || "";

  const urgencyLine = document.createElement("p");
  urgencyLine.innerHTML = `<strong>Urgency:</strong> ${details.urgency || "N/A"}`;

  const specialistLine = document.createElement("p");
  specialistLine.innerHTML = `<strong>Specialist:</strong> ${details.specialist || "Dermatologist"}`;

  const signsTitle = document.createElement("p");
  signsTitle.innerHTML = "<strong>Common signs</strong>";
  const signsList = document.createElement("ul");
  (details.common_signs || []).forEach((entry) => {
    const li = document.createElement("li");
    li.textContent = entry;
    signsList.appendChild(li);
  });

  const actionsTitle = document.createElement("p");
  actionsTitle.innerHTML = "<strong>Recommended actions</strong>";
  const actionsList = document.createElement("ul");
  (details.recommended_actions || []).forEach((entry) => {
    const li = document.createElement("li");
    li.textContent = entry;
    actionsList.appendChild(li);
  });

  body.appendChild(summary);
  body.appendChild(urgencyLine);
  body.appendChild(specialistLine);
  body.appendChild(signsTitle);
  body.appendChild(signsList);
  body.appendChild(actionsTitle);
  body.appendChild(actionsList);

  head.addEventListener("click", () => {
    wrapper.classList.toggle("open");
  });

  wrapper.appendChild(head);
  wrapper.appendChild(body);

  return wrapper;
}

function renderDiseaseList(filterValue = "") {
  const query = filterValue.trim().toLowerCase();
  diseaseList.innerHTML = "";

  const filtered = diseaseData.filter((item) => {
    if (!query) {
      return true;
    }
    const source =
      `${item.name} ${item.details?.clinical_summary || ""}`.toLowerCase();
    return source.includes(query);
  });

  if (!filtered.length) {
    diseaseList.innerHTML = '<p class="muted">No matching class found.</p>';
    return;
  }

  const fragment = document.createDocumentFragment();
  filtered.forEach((item) => fragment.appendChild(createDiseaseCard(item)));
  diseaseList.appendChild(fragment);
}

diseaseSearch.addEventListener("input", () => {
  renderDiseaseList(diseaseSearch.value);
});

renderDiseaseList();
setActiveTab("upload");
