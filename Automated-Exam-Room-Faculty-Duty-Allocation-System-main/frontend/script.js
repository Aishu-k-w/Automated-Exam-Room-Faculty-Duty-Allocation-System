document.getElementById('phase1-form').onsubmit = async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    try {
        const res = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        if (res.ok) {
            alert('Allocation completed successfully! Click the download link below to get the result.');
            document.getElementById('download-link').style.display = 'block';
            document.getElementById('download-link').href = 'http://localhost:5000/download';
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
};

document.getElementById('phase2-form').onsubmit = async function(e) {
    e.preventDefault();
    const formData = new FormData(this);
    try {
        const res = await fetch('http://localhost:5000/allocate', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        if (res.ok) {
            alert('Faculty allocation completed! Click the download link below to get the result.');
            document.getElementById('download-link').style.display = 'block';
            document.getElementById('download-link').href = 'http://localhost:5000/download';
        } else {
            alert('Error: ' + data.error);
        }
    } catch (error) {
        alert('Error: ' + error.message);
    }
}; 