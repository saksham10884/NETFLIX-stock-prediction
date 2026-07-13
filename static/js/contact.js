document.getElementById("contactForm").addEventListener("submit", async function(e) {
    e.preventDefault();

    const name = document.getElementById("name").value;
    const email = document.getElementById("email").value;
    const subject = document.getElementById("subject").value;
    const message = document.getElementById("message").value;

    if (!name || !email || !message) {
        document.getElementById("responseMsg").innerText = "Please fill all required fields!";
        return;
    }

    try {
        const response = await fetch("http://localhost:5000/contact", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ name, email, subject, message })
        });

        const data = await response.json();

        document.getElementById("responseMsg").innerText = data.message;
        document.getElementById("contactForm").reset();

    } catch (error) {
        document.getElementById("responseMsg").innerText = "Error sending message!";
    }
});