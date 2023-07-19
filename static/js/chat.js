
function sendMessage() {
  var messageInput = document.getElementById('message');
  var message = messageInput.value;

  // Display the message in the chat messages
  // var chatMessages = document.getElementById('chat-messages');
  // chatMessages.innerHTML += '<div class="message">' + message + '</div>';

  // // Save the message to the backend (MongoDB) using AJAX
  var xhr = new XMLHttpRequest();
  xhr.open('POST', '/save_message');
  xhr.setRequestHeader('Content-Type', 'application/json');
  addSentMessageToChat(message);
  xhr.onload = function() {
    if (xhr.status === 200) {
      var response = JSON.parse(xhr.responseText);
      var processedMessage = response.output;
      console.log('Processed Message:', response);
      // Display the processed message in the chat messages
      addReceivedMessageToChat(processedMessage);
    }
  };
  xhr.send(JSON.stringify({ message: message }));

  // Clear the input field after sending
  messageInput.value = '';
}

function addSentMessageToChat(message) {
  const chatMessages = document.getElementById('chat-messages');
  const messageElement = document.createElement('li');
  messageElement.innerText = message;
  messageElement.classList.add('sent-message'); // Add the class here
  chatMessages.appendChild(messageElement);
  chatMessages.insertBefore(messageElement, chatMessages.firstChild);
  // return false;
}
function addReceivedMessageToChat(message) {
  const chatMessages = document.getElementById('chat-messages');
  const messageElement = document.createElement('li');
  messageElement.innerText = message;
  messageElement.classList.add('received-message'); // Add the class here
  chatMessages.appendChild(messageElement);
  chatMessages.insertBefore(messageElement, chatMessages.firstChild);
}
function handleKeyPress(event) {
  // Check if the Enter key (key code 13) is pressed
  if (event.keyCode === 13) {
    event.preventDefault(); // Prevent form submission
    sendMessage();
  }
}