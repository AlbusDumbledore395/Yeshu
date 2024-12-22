document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('uploadBtn').addEventListener('click', function() {
        // Get the file and graph type from the user
        var fileInput = document.getElementById('fileInput');
        var graphType = document.getElementById('graphType').value;
        var file = fileInput.files[0];

        // Check if the file and graph type are selected
        if (!file) {
            alert("Please select a file.");
            return;
        }

        if (!graphType) {
            alert("Please select a graph type.");
            return;
        }

        // Create FormData to send the file and graph type to the server
        var formData = new FormData();
        formData.append('file', file);
        formData.append('graphType', graphType);

        // Show a loading spinner
        var spinner = document.createElement('div');
        spinner.classList.add('spinner');
        document.getElementById('graphPreview').innerHTML = '';  // Clear previous content
        document.getElementById('graphPreview').appendChild(spinner);

        // Make a POST request to upload the file and graph type
        fetch('http://127.0.0.1:5000/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to generate graph');
            }
            return response.blob();  // Expecting an image (graph) as response
        })
        .then(blob => {
            // Create an image element to display the graph
            var img = document.createElement('img');
            img.src = URL.createObjectURL(blob);
            
            // Display the graph preview
            document.getElementById('graphPreview').innerHTML = '';  // Clear the spinner
            document.getElementById('graphPreview').appendChild(img);  // Add the new graph preview

            // Optionally, add a download link for the image
            var downloadLink = document.createElement('a');
            downloadLink.href = img.src;
            downloadLink.download = 'graph.png';  // You can change this to a specific name or format
            downloadLink.textContent = 'Download Graph';
            downloadLink.style.display = 'block';
            downloadLink.style.marginTop = '15px';
            document.getElementById('graphPreview').appendChild(downloadLink);  // Add download link
        })
        .catch(error => {
            // Handle any errors during the fetch process
            console.error('Error:', error);
            alert("Error uploading the file. Please try again.");
        });
    });
});
