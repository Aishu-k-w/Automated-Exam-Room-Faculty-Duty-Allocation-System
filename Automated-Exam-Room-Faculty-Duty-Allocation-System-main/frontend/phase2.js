const banner = document.getElementById('banner');
const submitBtn = document.getElementById('submit-btn');
const spinner = document.getElementById('spinner');

function showBanner(message, type) {
    banner.innerHTML = `<div class='banner banner-${type}'>${message}</div>`;
}
function clearBanner() {
    banner.innerHTML = '';
}

document.getElementById('phase2-form').onsubmit = async function(e) {
    e.preventDefault();
    clearBanner();
    submitBtn.disabled = true;
    spinner.style.display = 'inline-block';
    document.getElementById('download-phase2').style.display = 'none';
    const formData = new FormData(this);
    try {
        const res = await fetch('http://localhost:5000/allocate', {
            method: 'POST',
            body: formData
        });
        const data = await res.json();
        if (res.ok) {
            showBanner('Faculty allocation completed!', 'success');
            document.getElementById('download-phase2').style.display = 'block';
            document.getElementById('download-phase2').href = 'http://localhost:5000/download/phase2';
            document.getElementById('summary-banner').style.display = 'block';
            document.getElementById('summary-text').textContent = 'Faculty allocated successfully.';
        } else {
            showBanner('Error: ' + data.error, 'error');
        }
    } catch (error) {
        showBanner('Error: ' + error.message, 'error');
    }
    submitBtn.disabled = false;
    spinner.style.display = 'none';
};

document.getElementById('to-phase1').onclick = function() {
    window.location.href = 'phase1.html';
}; 