
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


// fetch('/get_account_statement_openai')
// .then(response => response.blob())
// .then(blob => {
//   const url = window.URL.createObjectURL(blob);
//   const a = document.createElement('a');
//   a.href = url;
//   a.download = 'account_statement.csv';
//   document.body.appendChild(a);
//   a.click();
//   URL.revokeObjectURL(url);
// })
// .catch(error => console.error('Error downloading CSV:', error));
socket.on('server_data_event', function(data) {
  // Handle received data from server
  console.log('Received data from server:', data);
  get_account_statement_openai(data);
});
function get_account_statement_openai(data) {
  // Make an AJAX request to the server
  var xhr = new XMLHttpRequest();
  console.log('start date:', data.data.start_date);
  console.log('end date:', data.data.end_date);
  var startDate = data.data.start_date;
  var endDate = data.data.end_date;
  xhr.open('GET', '/account_statement?start=' + startDate + '&end=' + endDate);
  xhr.responseType = 'blob'; // Set the response type to blob
  console.log('Error:', xhr.status);
  xhr.onload = function() {
    if (xhr.status === 200) {
      // Create a URL object from the response blob
      var url = URL.createObjectURL(xhr.response);

      // Create a temporary link element
      var link = document.createElement('a');
      link.href = url;
      link.download = 'account_statement.csv'; // Specify the desired filename

      // Programmatically trigger the click event on the link element
      link.click();

      // Clean up the URL object
      URL.revokeObjectURL(url);
    } else {
      console.log('Error:', xhr.status);
    }
  };

  xhr.send();
}