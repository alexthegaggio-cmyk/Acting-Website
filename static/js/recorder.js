const recordPanel = document.getElementById('record-panel')
const recordDot = document.getElementById('record-dot')
const recordLabel = document.getElementById('record-label')
const previewArea = document.getElementById('video-preview')
const previewVideo = document.getElementById('preview-video')
let mediaRecorder, recordedChunks = [], isRecording = false

if (recordPanel) {
  recordPanel.addEventListener('click', async () => {
    if (!isRecording) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        mediaRecorder = new MediaRecorder(stream)
        recordedChunks = []
        mediaRecorder.ondataavailable = e => { if (e.data.size > 0) recordedChunks.push(e.data) }
        mediaRecorder.onstop = () => {
          const blob = new Blob(recordedChunks, { type: 'video/webm' })
          window.recordedBlob = blob
          previewVideo.src = URL.createObjectURL(blob)
          previewVideo.style.display = 'block'
          previewArea.style.display = 'block'
        }
        mediaRecorder.start()
        isRecording = true
        recordDot.style.background = '#8B3A3A'
        recordDot.style.animation = 'pulse 1s ease infinite'
        recordLabel.textContent = 'RECORDING... CLICK TO STOP'
      } catch (err) { console.error('MediaRecorder error:', err) }
    } else {
      mediaRecorder.stop()
      mediaRecorder.stream.getTracks().forEach(t => t.stop())
      isRecording = false
      recordDot.style.background = 'var(--charcoal)'
      recordDot.style.animation = 'none'
      recordLabel.textContent = 'RECORD IN BROWSER'
    }
  })
}

const submitForm = document.getElementById('submission-form') || document.querySelector('form[action*="submit"]')
if (submitForm) {
  submitForm.addEventListener('submit', e => {
    // Only intercept if we have a recorded blob
    if (window.recordedBlob) {
      e.preventDefault()

      // Show the coaching overlay
      const overlay = document.getElementById('submission-overlay')
      if (overlay) overlay.style.display = 'flex'

      const fd = new FormData(submitForm)
      fd.append('video', window.recordedBlob, 'recording.webm')

      const btn = submitForm.querySelector('button[type="submit"]')
      if (btn) {
        btn.textContent = 'UPLOADING...'
        btn.disabled = true
      }

      fetch(submitForm.action, { method: 'POST', body: fd })
        .then(async r => {
          if (r.ok) {
            if (r.redirected) {
              window.location = r.url
            } else {
              window.location.reload()
            }
          } else {
            const errText = await r.text()
            throw new Error(`Server returned ${r.status}: ${errText}`)
          }
        })
        .catch(err => {
          console.error('Upload error:', err)
          if (overlay) overlay.style.display = 'none'
          if (btn) {
            btn.textContent = 'RETRY SUBMISSION'
            btn.disabled = false
          }
          alert('Submission failed: ' + err.message)
        })
    }
  })
}
