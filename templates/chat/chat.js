async function loadMessages() {
    const response = await fetch('/api/messages?limit=50');
    const messages = await response.json();

    const container = document.getElementById('messages');
    container.innerHTML = '';

    messages.forEach(m => {
        const div = document.createElement('div');
        div.className = 'message';
        div.innerHTML = `<strong>${m.nickname}:</strong> ${m.message}`;
        container.appendChild(div);
    });
}

loadMessages();
setInterval(loadMessages, 2000);
