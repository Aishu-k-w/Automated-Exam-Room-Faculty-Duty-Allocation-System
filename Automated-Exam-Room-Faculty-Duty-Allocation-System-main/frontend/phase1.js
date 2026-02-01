const banner = document.getElementById('banner');
const submitBtn = document.getElementById('submit-btn');
const spinner = document.getElementById('spinner');

function showBanner(message, type) {
    banner.innerHTML = `<div class='banner banner-${type}'>${message}</div>`;
}
function clearBanner() {
    banner.innerHTML = '';
}

document.getElementById('phase1-form').onsubmit = async function(e) {
    e.preventDefault();
    clearBanner();
    submitBtn.disabled = true;
    spinner.style.display = 'inline-block';
    document.getElementById('download-phase1').style.display = 'none';
    const formData = new FormData(this);
    try {
        const res = await fetch('http://localhost:5000/upload', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        if (res.ok) {
            showBanner('Allocation completed successfully!', 'success');
            document.getElementById('download-phase1').style.display = 'block';
            document.getElementById('download-phase1').href = 'http://localhost:5000/download/phase1';
            document.getElementById('summary-banner').style.display = 'block';
            document.getElementById('summary-text').textContent = '120 students allocated to 5 rooms.';
        } else {
            showBanner('Error: ' + data.error, 'error');
        }
    } catch (error) {
        showBanner('Error: ' + error.message, 'error');
    }
    submitBtn.disabled = false;
    spinner.style.display = 'none';
};

document.getElementById('to-phase2').onclick = function() {
    window.location.href = 'phase2.html';
}; 