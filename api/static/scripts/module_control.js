// module_control.js
document.addEventListener('DOMContentLoaded', (event) => {
  let selectedButton = null;

  document.querySelectorAll('.module-button').forEach(button => {
      button.addEventListener('click', () => {
          if (selectedButton) {
              selectedButton.classList.remove('btn-glow');
          }
          button.classList.add('btn-glow');
          selectedButton = button;
      });
  });

  document.getElementById('hook-form').addEventListener('submit', function(event) {
      event.preventDefault();
      if (selectedButton) {
          const hookId = document.getElementById('hook_id').value;
          const selectedModuleName = selectedButton.getAttribute('data-module');
          const actionUrl = '/admin/attacks/command';
          const formData = new FormData();
          formData.append('hook_id', hookId);
          formData.append('command', selectedModuleName);
          fetch(actionUrl, {
              method: 'POST',
              body: formData
          })
          .then(response => {
              if (!response.ok) {
                  throw new Error('Network response was not ok');
              }
              return response.json();
          })
          .then(data => {
              console.log(data); // Optionally, handle response data
          })
          .catch(error => {
              console.error('There was a problem with the fetch operation:', error);
          });
      } else {
          alert('Please select a module before submitting.');
      }
  });
});
