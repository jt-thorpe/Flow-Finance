async function handleRegister(event) {
    event.preventDefault();

    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // TODO: Extract and improve validation logic
    if (!email && !password) {
        alert("Please provide your email and password.");
        return;
    }

    // Send the data to app.py via POST request
    const response = await fetch('/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password })
    });

    const result = await response.json();

    if (result.success) {
        window.location.href = result.redirect;
    } else {
        alert(result.message);
    }
}