const API_URL = "http://127.0.0.1:8000/api/symptoms/";

// Get JWT access token.
// Make sure one of these keys matches your existing login.js.
function getAccessToken() {
    return (
        localStorage.getItem("access") ||
        localStorage.getItem("access_token") ||
        localStorage.getItem("accessToken")
    );
}
const symptomList = document.getElementById("symptomList");
const searchInput = document.getElementById("searchInput");
const selectedSymptomsDiv = document.getElementById("selectedSymptoms");
const errorMessage = document.getElementById("errorMessage");
const successMessage = document.getElementById("successMessage");
const submitButton = document.getElementById("submitButton");
let availableSymptoms = [];
let selectedSymptoms = new Map();

// 1. Load available symptoms
async function loadSymptoms(search = "") {
    try {
        const response = await fetch(
            `${API_URL}?search=${encodeURIComponent(search)}`
        );
        if (!response.ok) {
            throw new Error("Unable to load symptoms.");
        }
        availableSymptoms = await response.json();
        displaySymptoms();
    }
    catch (error) {
        symptomList.textContent = error.message;
    }
}

// 2. Display symptoms
function displaySymptoms() {
    symptomList.innerHTML = "";
    if (availableSymptoms.length === 0) {
        symptomList.textContent = "No matching symptoms found.";
        return;
    }
    availableSymptoms.forEach(symptom => {
        const label = document.createElement("label");
        label.className = "symptom-item";
        const checkbox = document.createElement("input");
        checkbox.type = "checkbox";
        checkbox.checked = selectedSymptoms.has(symptom.id);
        checkbox.addEventListener("change", () => {
            if (checkbox.checked) {
                selectedSymptoms.set(symptom.id, symptom);
            } else {
                selectedSymptoms.delete(symptom.id);
            }
            displaySelectedSymptoms();
        });
        const text = document.createTextNode(symptom.symptom_name);
        label.appendChild(checkbox);
        label.appendChild(text);
        symptomList.appendChild(label);
    });
}

// 3. Display selected symptoms
function displaySelectedSymptoms() {
    selectedSymptomsDiv.innerHTML = "";
    if (selectedSymptoms.size === 0) {
        selectedSymptomsDiv.textContent = "No symptoms selected.";
        return;
    }
    selectedSymptoms.forEach(symptom => {
        const item = document.createElement("div");
        item.className = "selected-item";
        const name = document.createElement("span");
        name.textContent = symptom.symptom_name;
        const removeButton = document.createElement("button");
        removeButton.textContent = "×";
        removeButton.className = "remove-button";
        removeButton.addEventListener("click", () => {
            selectedSymptoms.delete(symptom.id);
            displaySelectedSymptoms();
            displaySymptoms();
        });
        item.appendChild(name);
        item.appendChild(removeButton);
        selectedSymptomsDiv.appendChild(item);
    });
}
// 4. Search symptoms
searchInput.addEventListener("input", () => {
    loadSymptoms(searchInput.value);
});

// 5. Submit selected symptoms
async function submitSymptoms() {
    errorMessage.textContent = "";
    successMessage.textContent = "";

    // Frontend validation
    if (selectedSymptoms.size === 0) {
        errorMessage.textContent =
            "Please select at least one symptom.";
        return;
    }
    const token = getAccessToken();
    if (!token) {
        errorMessage.textContent =
            "Please log in before submitting symptoms.";
        return;
    }
    const symptomIds = Array.from(selectedSymptoms.keys());
    submitButton.disabled = true;
    try {
        const response = await fetch(
            `${API_URL}select/`,
            {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                },
                body: JSON.stringify({
                    symptoms: symptomIds
                })
            }
        );
        const data = await response.json();
        if (!response.ok) {
            const errors = data.errors || data;
            throw new Error(JSON.stringify(errors));
        }
        successMessage.textContent =
            `Symptoms submitted successfully! Assessment ID: ${data.assessment_id}`;
        selectedSymptoms.clear();
        displaySelectedSymptoms();
        displaySymptoms();
    }
    catch (error) {
        errorMessage.textContent = error.message;
    }
    finally {
        submitButton.disabled = false;
    }
}

// 6. Retrieve previous assessments
async function loadAssessments() {
    const token = getAccessToken();
    if (!token) {
        errorMessage.textContent = "Please log in first.";
        return;
    }
    try {
        const response = await fetch(
            `${API_URL}my-assessments/`,
            {
                headers: {
                    "Authorization": `Bearer ${token}`
                }
            }
        );
        const data = await response.json();
        if (!response.ok) {
            throw new Error("Unable to retrieve assessments.");
        }
        const historyList = document.getElementById("historyList");
        historyList.innerHTML = "";
        if (data.length === 0) {
            historyList.textContent = "No previous assessments found.";
            return;
        }
        data.forEach(assessment => {
            const item = document.createElement("div");
            item.className = "history-item";
            const names = assessment.selected_symptoms
                .map(symptom => symptom.symptom_name)
                .join(", ");
            const heading = document.createElement("h3");
            heading.textContent = `Assessment #${assessment.id}`;
            const symptoms = document.createElement("p");
            symptoms.textContent = `Symptoms: ${names}`;
            const date = document.createElement("p");
            date.textContent =
                `Date: ${new Date(assessment.assessment_date).toLocaleString()}`;
            item.appendChild(heading);
            item.appendChild(symptoms);
            item.appendChild(date);
            historyList.appendChild(item);
        });
    }
    catch (error) {
        errorMessage.textContent = error.message;
    }
}
// Event listeners
submitButton.addEventListener("click", submitSymptoms);
document.getElementById("historyButton")
    .addEventListener("click", loadAssessments);
// Initial loading
loadSymptoms();