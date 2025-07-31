// waterEvent.js
let eventSource = null
let listeners = []

export function initWaterStream() {
  if (eventSource) return // already connected

  eventSource = new EventSource('http://localhost:8000/api/water-stream')
  eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data)
    if (data.type === 'water') {
      // Notify all listeners
      listeners.forEach(fn => fn(data.data.waterLevel))
    }
  }
}

export function onWaterLevelUpdate(callback) {
  listeners.push(callback)
}

export function stopWaterStream() {
  if (eventSource) {
    eventSource.close()
    eventSource = null
  }
  listeners = []
}
