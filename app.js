function isValidURL(input) {
  try {
      new URL(input);
      return true;
  } catch {
      return false;
  }
}

function extractDomain(input) {
  try {
      const parsedUrl = new URL(input);
      let domain = parsedUrl.hostname.toLowerCase();
      if (domain.startsWith("www.")) domain = domain.substring(4);
      return domain;
  } catch {
      return "";
  }
}

async function analyzeInput(inputType, inputText) {
  const resultDiv = document.getElementById("result");
  resultDiv.textContent = "Analyzing...";
  resultDiv.className = "";

  try {
      const response = await fetch("http://127.0.0.1:5000/predict", {
          method: "POST",
          headers: {
              "Content-Type": "application/json",
          },
          body: JSON.stringify({ text: inputText }),
      });

      const result = await response.json();

      if (result.error) {
          resultDiv.textContent = `Error: ${result.error}`;
          resultDiv.classList.add("error");
      } else {
          resultDiv.innerHTML = `🔍 The text is <span class="${result.prediction.toLowerCase()}">${result.prediction}</span> with a confidence of ${result.confidence}%.`;
          resultDiv.classList.add(result.prediction.toLowerCase());
      }
  } catch (error) {
      resultDiv.textContent = "❌ Failed to analyze input.";
      resultDiv.classList.add("error");
  }
}

document.getElementById("analyzeButton").addEventListener("click", () => {
  const inputType = document.getElementById("inputType").value;
  const inputField = document.getElementById("inputField");
  const resultDiv = document.getElementById("result");

  resultDiv.textContent = "";
  resultDiv.className = "";

  const inputText = inputField.value.trim();
  if (!inputText) {
      alert("Please enter a value.");
      return;
  }

  if (inputType === "Website URL") {
      if (!isValidURL(inputText)) {
          resultDiv.textContent = "⚠️ Invalid URL format!";
          resultDiv.classList.add("warning");
          return;
      }

      const domain = extractDomain(inputText);
      if (!domain) {
          resultDiv.textContent = "⚠️ Unable to extract domain from URL!";
          resultDiv.classList.add("warning");
          return;
      }

      // Expanded list of common legitimate domains
      const commonLegitimateDomains = [
          "google.com", "facebook.com", "paypal.com", "amazon.com",
          "microsoft.com", "apple.com", "github.com", "linkedin.com",
          "canva.com", "twitter.com", "instagram.com", "edu", "gov",
          "ac.in", "iitm.ac.in"
      ];

      // Check if the domain or its parent domain is legitimate
      const isLegitimate = commonLegitimateDomains.some(
          legitDomain => domain === legitDomain || domain.endsWith(`.${legitDomain}`)
      );

      if (isLegitimate) {
          resultDiv.innerHTML = `🔍 The URL is <span class="legitimate">Legitimate</span>.`;
          resultDiv.classList.add("legitimate");
          return;
      }

      resultDiv.innerHTML = `🔍 The URL is <span class="phishing">Phishing</span> because it is not a known legitimate domain.`;
      resultDiv.classList.add("phishing");
      return;
  }

  // For other input types, directly analyze the input
  analyzeInput(inputType, inputText);
});