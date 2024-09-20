async function handleLogin(event) {
    event.preventDefault();  // Prevent form from submitting normally

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Simple validation
    if (!email && !password) {
        alert("Please provide your email and password.");
        return;
    }

    // Send the data to the backend via POST request
    const response = await fetch('/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();

    // Check response from server
    if (result.success) {
        window.location.href = '/dashboard';  // Redirect on successful login
    } else {
        alert(result.message);  // Show error message on failure
    }
}