(function() {
  "use strict"; // Start of use strict

  function initParallax() {

    if (!('requestAnimationFrame' in window)) return;
    if (/Mobile|Android/.test(navigator.userAgent)) return;

    var parallaxItems = document.querySelectorAll('[data-bss-parallax]');

    if (!parallaxItems.length) return;

    var defaultSpeed = 0.5;
    var visible = [];
    var scheduled;

    window.addEventListener('scroll', scroll);
    window.addEventListener('resize', scroll);

    scroll();

    function scroll() {

      visible.length = 0;

      for (var i = 0; i < parallaxItems.length; i++) {
        var rect = parallaxItems[i].getBoundingClientRect();
        var speed = parseFloat(parallaxItems[i].getAttribute('data-bss-parallax-speed'), 10) || defaultSpeed;

        if (rect.bottom > 0 && rect.top < window.innerHeight) {
          visible.push({
            speed: speed,
            node: parallaxItems[i]
          });
        }

      }

      cancelAnimationFrame(scheduled);

      if (visible.length) {
        scheduled = requestAnimationFrame(update);
      }

    }

    function update() {

      for (var i = 0; i < visible.length; i++) {
        var node = visible[i].node;
        var speed = visible[i].speed;

        node.style.transform = 'translate3d(0, ' + (-window.scrollY * speed) + 'px, 0)';
      }

    }
  }

  initParallax();
})(); // End of use strict


function editNote(noteId) {
  // Get the elements by their IDs
  const noteContent = document.getElementById('note-content-' + noteId);
  const noteTextarea = document.getElementById('note-textarea-' + noteId);
  const saveForm = document.getElementById('save-form-' + noteId);
  const editButton = document.getElementById('edit-note-' + noteId);

  // Add debugging logs to check if elements exist
  console.log(noteContent, noteTextarea, saveForm);

  if (noteContent && noteTextarea && saveForm) {
      noteContent.classList.add('d-none'); // Hide the note content
      noteTextarea.classList.remove('d-none'); // Show the textarea
      saveForm.classList.remove('d-none'); // Show Save/Cancel buttons
      editButton.classList.add('d-none');
  } else {
      console.error("One or more elements not found for noteId:", noteId);
  }
}

function cancelEdit(noteId) {
  const noteContent = document.getElementById('note-content-' + noteId);
  const noteTextarea = document.getElementById('note-textarea-' + noteId);
  const saveForm = document.getElementById('save-form-' + noteId);
  const editButton = document.getElementById('edit-note-' + noteId);

  // Add debugging logs to check if elements exist
  console.log(noteContent, noteTextarea, saveForm);

  if (noteContent && noteTextarea && saveForm) {
      noteContent.classList.remove('d-none'); // Show the note content
      noteTextarea.classList.add('d-none'); // Hide the textarea
      saveForm.classList.add('d-none'); // Hide Save/Cancel buttons
      editButton.classList.remove('d-none');
  } else {
      console.error("One or more elements not found for noteId:", noteId);
  }
}

function saveNote(noteId) {
  // Get the visible textarea where the user edited the note
  const noteTextarea = document.getElementById('note-textarea-' + noteId);
  const dateInput = document.getElementById('date-input-' + noteId);

  // Get the hidden textarea inside the form that will be submitted
  const textareaForm = document.getElementById('textarea-form-' + noteId);

  // Transfer the content from the visible textarea to the hidden textarea
  if (noteTextarea && textareaForm && dateInput) {
      textareaForm.value = noteTextarea.value;  // Copy edited content

      document.getElementById('save-form-' + noteId).submit();  // Submit the form

  } else {
      console.error("Textarea or form not found for noteId:", noteId);
  }
}
