
// Configuration: Update this URL after deploying the backend
const API_URL = "http://127.0.0.1:8000"; 

async function generateEmail() {
    const url = document.getElementById('url').value;
    const tone = document.getElementById('tone').value;
    const cta = document.getElementById('cta').value;
    
    const generateBtn = document.getElementById('generateBtn');
    const loadingDiv = document.getElementById('loading');
    const resultDiv = document.getElementById('result');
    const emailContent = document.getElementById('emailContent');

    if (!url) {
        alert("Please enter a URL");
        return;
    }

    // UI State: Loading
    generateBtn.disabled = true;
    loadingDiv.classList.remove('hidden');
    resultDiv.classList.add('hidden');

    try {
        const response = await fetch(`${API_URL}/generate_email`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ url, tone, cta })
        });

        const data = await response.json();

        if (data.error) {
            alert("Error: " + data.error);
        } else if (data.emails && data.emails.length > 0) {
            // Success: Show the first email
            emailContent.textContent = data.emails[0];
            resultDiv.classList.remove('hidden');
        } else {
            alert("No text found or generation failed.");
        }
    } catch (error) {
        alert("Network Error: " + error.message + "\nMake sure the Backend is running!");
    } finally {
        // UI State: Reset
        generateBtn.disabled = false;
        loadingDiv.classList.add('hidden');
    }
}

function copyToClipboard() {
    const emailText = document.getElementById('emailContent').textContent;
    navigator.clipboard.writeText(emailText).then(() => {
        alert("Copied to clipboard!");
    });
}
