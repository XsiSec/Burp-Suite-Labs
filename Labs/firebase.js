import { initializeApp } from 'firebase/app'
import { getAuth } from 'firebase/auth'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
    apiKey: "AIzaSyA8Nh6FYteW6cthMgFokujwmSva05s4Oq0",
    authDomain: "nextjs-test13.firebaseapp.com",
    projectId: "nextjs-test13",
    storageBucket: "nextjs-test13.appspot.com",
    messagingSenderId: "984323725321",
    appId: "1:984323725321:web:237a821f759a2b62bbc0d8"
}

const app = initializeApp(firebaseConfig)


export const auth = getAuth(app)
export const db = getFirestore(app)