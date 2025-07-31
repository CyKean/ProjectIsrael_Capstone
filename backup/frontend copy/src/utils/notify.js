export function sendPushNotification(title, message) {
    if ('Notification' in window && Notification.permission === 'granted') {
      new Notification(title, {
        body: message,
        icon: '/icons/water-icon.png' // optional, add your own icon path
      })
    }
  }
  