// import { initializeApp } from "firebase/app";
// import {
//     getAuth,
//     GoogleAuthProvider,
//     signInWithPopup,
//     RecaptchaVerifier,
//     signInWithPhoneNumber
// } from "firebase/auth";
// import {
//     getFirestore,
//     collection,
//     addDoc,
//     getDocs,
//     query,
//     orderBy,
//     limit,
//     doc,
//     setDoc,
//     Timestamp,
//     serverTimestamp,
//     getDoc,
//     updateDoc,
//     deleteDoc,
//     where
// } from "firebase/firestore";

// // ✅ Production Firebase config via environment variables
// const firebaseConfig = {
//     apiKey: import.meta.env.VITE_API_KEY,
//     authDomain: import.meta.env.VITE_AUTH_DOMAIN,
//     projectId: import.meta.env.VITE_PROJECT_ID,
//     storageBucket: import.meta.env.VITE_STORAGE_BUCKET,
//     messagingSenderId: import.meta.env.VITE_MESSAGING_SENDER_ID,
//     appId: import.meta.env.VITE_APP_ID
// };

// // ✅ Initialize Firebase app (only once)
// const app = initializeApp(firebaseConfig);

// // ✅ Initialize services
// const auth = getAuth(app);
// const db = getFirestore(app);
// const googleProvider = new GoogleAuthProvider();

// // ✅ Export Firebase modules for use across your app
// export {
//     auth,
//     db,
//     googleProvider,
//     getAuth,
//     signInWithPopup,
//     RecaptchaVerifier,
//     signInWithPhoneNumber,
//     // Firestore helpers
//     collection,
//     addDoc,
//     getDocs,
//     query,
//     orderBy,
//     limit,
//     doc,
//     setDoc,
//     Timestamp,
//     serverTimestamp,
//     getDoc,
//     updateDoc,
//     deleteDoc,
//     where
// };
// src/firebase.js
import { initializeApp } from "firebase/app";
import {
  getAuth,
  GoogleAuthProvider,
  signInWithPopup,
  RecaptchaVerifier,
  signInWithPhoneNumber
} from "firebase/auth";
import {
  getFirestore,
  collection,
  addDoc,
  getDocs,
  query,
  orderBy,
  limit,
  doc,
  setDoc,
  Timestamp,
  serverTimestamp,
  getDoc,
  updateDoc,
  deleteDoc,
  where
} from "firebase/firestore";

// ✅ Firebase config
const firebaseConfig = {
  apiKey: import.meta.env.VITE_API_KEY,
  authDomain: import.meta.env.VITE_AUTH_DOMAIN,
  projectId: import.meta.env.VITE_PROJECT_ID,
  storageBucket: import.meta.env.VITE_STORAGE_BUCKET,
  messagingSenderId: import.meta.env.VITE_MESSAGING_SENDER_ID,
  appId: import.meta.env.VITE_APP_ID
};

// ✅ Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);
const googleProvider = new GoogleAuthProvider();

// ✅ Export ONLY initialized instances
export {
  auth,
  db,
  googleProvider,
  signInWithPopup,
  RecaptchaVerifier,
  signInWithPhoneNumber,
  // Firestore helpers
  collection,
  addDoc,
  getDocs,
  query,
  orderBy,
  limit,
  doc,
  setDoc,
  Timestamp,
  serverTimestamp,
  getDoc,
  updateDoc,
  deleteDoc,
  where
};