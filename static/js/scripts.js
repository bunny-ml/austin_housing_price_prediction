document.getElementById('predictionForm').addEventListener('submit', async function(event) {
    event.preventDefault();

    const bedrooms = document.getElementById('bedrooms').value;
    const stories = document.getElementById('stories').value;
    const spa = document.getElementById('spa').value;
    const view = document.getElementById('view').value;
    const garage = document.getElementById('garage').value;

    const response = await fetch('/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ bedrooms, stories, spa, view, garage })
    });

    const predictions = await response.json();

    document.getElementById('predictions').innerHTML = `
        <h3>Predicted Prices:</h3>
        <p>KNN Prediction: $${predictions["KNN Prediction"].toFixed(2)}</p>
        <p>Linear Regression Prediction: $${predictions["Linear Regression Prediction"].toFixed(2)}</p>
        <p>Random Forest Prediction: $${predictions["Random Forest Prediction"].toFixed(2)}</p>
    `;
});
