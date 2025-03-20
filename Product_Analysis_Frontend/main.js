document.addEventListener("DOMContentLoaded", function () {
    const analyzeButton = document.querySelector(".analyze-btn");

    analyzeButton.addEventListener("click", async function () {
        // Get the product URL and type from the input fields
        const productUrl = document.getElementById("input-url").value.trim();
        const productType = document.getElementById("input-type").value;

        if (!productUrl) {
            alert("Please enter a product URL");
            return;
        }

        // Validate the URL
        try {
            new URL(productUrl);
        } catch (e) {
            alert("Please enter a valid URL");
            return;
        }

        console.log("Fetching reviews for:", productUrl); // Debugging log

        // API URL
        const apiUrl = "http://localhost:5000/Fetch_Product_reviews";
        // const requestUrl = `${apiUrl}?url=${encodeURIComponent(productUrl)}&type=multiple`;
        const requestUrl = `${apiUrl}?url=${encodeURIComponent(productUrl)}&type=${productType}`;

        try {
            const response = await fetch(requestUrl);

            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }

            const data = await response.json();
            console.log("API Response:", data);

            // Save the JSON response to a file
            saveJSONToFile(data, 'review.json');
        } catch (error) {
            console.error("Error calling API:", error);
            alert(`An error occurred: ${error.message}`);
        }
    });

    function saveJSONToFile(jsonData, filename) {
        const jsonString = JSON.stringify(jsonData, null, 2); // Convert JSON object to string
        const blob = new Blob([jsonString], { type: 'application/json' }); // Create a Blob object
        const url = URL.createObjectURL(blob); // Create a URL for the Blob
        const a = document.createElement('a'); // Create an anchor element
        a.href = url;
        a.download = filename; // Set the download attribute with the filename
        document.body.appendChild(a); // Append the anchor to the body
        a.click(); // Programmatically click the anchor to trigger the download
        document.body.removeChild(a); // Remove the anchor from the document
        URL.revokeObjectURL(url); // Release the object URL
    }
});
