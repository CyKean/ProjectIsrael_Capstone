/**
 * Import function triggers from their respective submodules:
 *
 * const {onCall} = require("firebase-functions/v2/https");
 * const {onDocumentWritten} = require("firebase-functions/v2/firestore");
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

// const {onRequest} = require("firebase-functions/v2/https");
// const logger = require("firebase-functions/logger");

// Create and deploy your first functions
// https://firebase.google.com/docs/functions/get-started

// exports.helloWorld = onRequest((request, response) => {
//   logger.info("Hello logs!", {structuredData: true});
//   response.send("Hello from Firebase!");
// });

const { onDocumentCreated } = require('firebase-functions/v2/firestore');
const { initializeApp } = require('firebase-admin/app');
const { getFirestore, FieldValue } = require('firebase-admin/firestore');
const fetch = require('node-fetch'); // npm install node-fetch@2

initializeApp();
const db = getFirestore();

exports.sendCriticalSMS = onDocumentCreated(
  {
    document: 'notifications/{id}',
    region: 'us-central1', // or your preferred region
  },
  async (event) => {
    const snap = event.data;
    if (!snap) return;

    const data = snap.data();

    // Only send if severity is critical
    if (data.severity !== 'critical') return;

    const today = new Date().toISOString().split('T')[0];
    const phoneNumber = data.phone || '+63627080157'; // Default fallback
    const message = data.message || '⚠️ Critical alert from your system.';
    const userKey = `sent:${phoneNumber}:${today}`;

    // Check if already sent today
    const smsRef = db.collection('sms_logs').doc(userKey);
    const doc = await smsRef.get();
    if (doc.exists) {
      console.log('SMS already sent today for', phoneNumber);
      return;
    }

    // Send SMS via Textbelt
    const response = await fetch('https://textbelt.com/text', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        phone: phoneNumber,
        message: message,
        key: 'textbelt', // Replace with your paid key if you upgrade
      }),
    });

    const result = await response.json();
    console.log('Textbelt response:', result);

    if (result.success) {
      await smsRef.set({
        sentAt: FieldValue.serverTimestamp(),
        phone: phoneNumber,
        message,
        status: 'sent',
      });
    } else {
      console.warn('Failed to send SMS:', result);
    }
  }
);
