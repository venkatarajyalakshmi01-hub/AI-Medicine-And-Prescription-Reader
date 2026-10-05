// ===============================
// 🌐 LANGUAGE + THEME SETTINGS
// ===============================

let currentLanguage = localStorage.getItem("language") || "en";
let currentTheme = localStorage.getItem("theme") || "light";

// Voice list
let availableVoices = [];


// ===============================
// 🌙 APPLY THEME
// ===============================

function applyTheme() {

    if (currentTheme === "dark") {
        document.body.classList.add("dark-mode");
    } else {
        document.body.classList.remove("dark-mode");
    }

    const themeSelect = document.getElementById("themeSelect");

    if (themeSelect) {
        themeSelect.value = currentTheme;
    }
}


// ===============================
// 🌙 CHANGE THEME
// ===============================

function changeTheme(theme) {

    currentTheme = theme;

    localStorage.setItem("theme", theme);

    applyTheme();
}


// ===============================
// 🌐 TRANSLATIONS
// ===============================

const translations = {

    en: {

        home: "Home",
        dashboard: "Dashboard",
        prescription: "Prescription",
        medicines: "Medicines",
        reminders: "Reminders",
        history: "History",
        logout: "Logout",

        language: "Language",
        theme: "Theme",
        light: "Light",
        dark: "Dark",

        medicine: "Medicine",
        time: "Time",
        instructions: "Instructions",
        status: "Status",

        taken: "✓ Taken",
        missed: "✗ Missed",

        setReminder: "Set New Reminder",
        savedReminders: "Saved Reminders",

        reminderTitle: "💊 Medicine Reminder",

        reminderMessage:
            "It is time to take your medicine.",

        close: "Close",

        speak: "🔊 Speak Again",

        noHistory:
            "No medicine history available yet."
    },


    te: {

        home: "హోమ్",
        dashboard: "డాష్‌బోర్డ్",
        prescription: "ప్రిస్క్రిప్షన్",
        medicines: "మందులు",
        reminders: "రిమైండర్లు",
        history: "చరిత్ర",
        logout: "లాగ్ అవుట్",

        language: "భాష",
        theme: "థీమ్",
        light: "లైట్",
        dark: "డార్క్",

        medicine: "మందు",
        time: "సమయం",
        instructions: "సూచనలు",
        status: "స్థితి",

        taken: "✓ తీసుకున్నారు",
        missed: "✗ మిస్ అయ్యింది",

        setReminder: "కొత్త రిమైండర్ సెట్ చేయండి",
        savedReminders: "సేవ్ చేసిన రిమైండర్లు",

        reminderTitle: "💊 మందు రిమైండర్",

        reminderMessage:
            "మీ మందు తీసుకునే సమయం వచ్చింది.",

        close: "మూసివేయి",

        speak: "🔊 మళ్లీ వినండి",

        noHistory:
            "ఇంకా మందుల చరిత్ర అందుబాటులో లేదు."
    },


    hi: {

        home: "होम",
        dashboard: "डैशबोर्ड",
        prescription: "प्रिस्क्रिप्शन",
        medicines: "दवाइयाँ",
        reminders: "रिमाइंडर",
        history: "इतिहास",
        logout: "लॉग आउट",

        language: "भाषा",
        theme: "थीम",
        light: "लाइट",
        dark: "डार्क",

        medicine: "दवा",
        time: "समय",
        instructions: "निर्देश",
        status: "स्थिति",

        taken: "✓ ली गई",
        missed: "✗ छूट गई",

        setReminder: "नया रिमाइंडर सेट करें",
        savedReminders: "सेव किए गए रिमाइंडर",

        reminderTitle: "💊 दवा रिमाइंडर",

        reminderMessage:
            "आपकी दवा लेने का समय हो गया है।",

        close: "बंद करें",

        speak: "🔊 फिर से सुनें",

        noHistory:
            "अभी तक दवा का इतिहास उपलब्ध नहीं है।"
    },


    ta: {

        home: "முகப்பு",
        dashboard: "டாஷ்போர்டு",
        prescription: "மருத்துவ சீட்டு",
        medicines: "மருந்துகள்",
        reminders: "நினைவூட்டல்கள்",
        history: "வரலாறு",
        logout: "வெளியேறு",

        language: "மொழி",
        theme: "தீம்",
        light: "லைட்",
        dark: "டார்க்",

        medicine: "மருந்து",
        time: "நேரம்",
        instructions: "வழிமுறைகள்",
        status: "நிலை",

        taken: "✓ எடுத்துக்கொண்டது",
        missed: "✗ தவறியது",

        setReminder: "புதிய நினைவூட்டலை அமைக்கவும்",
        savedReminders: "சேமிக்கப்பட்ட நினைவூட்டல்கள்",

        reminderTitle: "💊 மருந்து நினைவூட்டல்",

        reminderMessage:
            "உங்கள் மருந்தை எடுத்துக்கொள்ளும் நேரம் வந்துவிட்டது.",

        close: "மூடு",

        speak: "🔊 மீண்டும் கேட்கவும்",

        noHistory:
            "மருந்து வரலாறு இன்னும் இல்லை."
    },


    kn: {

        home: "ಮುಖಪುಟ",
        dashboard: "ಡ್ಯಾಶ್‌ಬೋರ್ಡ್",
        prescription: "ಪ್ರಿಸ್ಕ್ರಿಪ್ಷನ್",
        medicines: "ಔಷಧಿಗಳು",
        reminders: "ಜ್ಞಾಪನೆಗಳು",
        history: "ಇತಿಹಾಸ",
        logout: "ಲಾಗ್ ಔಟ್",

        language: "ಭಾಷೆ",
        theme: "ಥೀಮ್",
        light: "ಲೈಟ್",
        dark: "ಡಾರ್ಕ್",

        medicine: "ಔಷಧಿ",
        time: "ಸಮಯ",
        instructions: "ಸೂಚನೆಗಳು",
        status: "ಸ್ಥಿತಿ",

        taken: "✓ ತೆಗೆದುಕೊಂಡಿದೆ",
        missed: "✗ ತಪ್ಪಿದೆ",

        setReminder: "ಹೊಸ ಜ್ಞಾಪನೆ ಹೊಂದಿಸಿ",
        savedReminders: "ಉಳಿಸಿದ ಜ್ಞಾಪನೆಗಳು",

        reminderTitle: "💊 ಔಷಧಿ ಜ್ಞಾಪನೆ",

        reminderMessage:
            "ನಿಮ್ಮ ಔಷಧಿ ತೆಗೆದುಕೊಳ್ಳುವ ಸಮಯ ಬಂದಿದೆ.",

        close: "ಮುಚ್ಚಿ",

        speak: "🔊 ಮತ್ತೆ ಕೇಳಿ",

        noHistory:
            "ಇನ್ನೂ ಔಷಧಿ ಇತಿಹಾಸ ಲಭ್ಯವಿಲ್ಲ."
    }
};


// ===============================
// 🌐 APPLY LANGUAGE
// ===============================

function applyLanguage() {

    const language =
        translations[currentLanguage];

    if (!language) {
        return;
    }

    document
        .querySelectorAll("[data-i18n]")
        .forEach(element => {

            const key =
                element.getAttribute("data-i18n");

            if (language[key]) {

                element.textContent =
                    language[key];

            }

        });


    const languageSelect =
        document.getElementById(
            "languageSelect"
        );

    if (languageSelect) {

        languageSelect.value =
            currentLanguage;

    }
}


// ===============================
// 🌐 CHANGE LANGUAGE
// ===============================

function changeLanguage(language) {

    currentLanguage = language;

    localStorage.setItem(
        "language",
        language
    );

    applyLanguage();

    console.log(
        "Language changed to:",
        currentLanguage
    );
}


// ===============================
// 🔊 GET VOICE LANGUAGE
// ===============================

function getVoiceLanguage() {

    if (currentLanguage === "te") {
        return "te-IN";
    }

    if (currentLanguage === "hi") {
        return "hi-IN";
    }

    if (currentLanguage === "ta") {
        return "ta-IN";
    }

    if (currentLanguage === "kn") {
        return "kn-IN";
    }

    return "en-IN";
}


// ===============================
// 🔊 LOAD BROWSER VOICES
// ===============================

function loadVoices() {

    availableVoices =
        window.speechSynthesis.getVoices();

    console.log(
        "Available voices:",
        availableVoices.map(voice => ({
            name: voice.name,
            language: voice.lang
        }))
    );
}


// Browser voices load
if ("speechSynthesis" in window) {

    loadVoices();

    window.speechSynthesis.onvoiceschanged =
        function () {

            loadVoices();

        };
}


// ===============================
// 🔊 FIND BEST VOICE
// ===============================

function getBestVoice(language) {

    if (!availableVoices.length) {

        availableVoices =
            window.speechSynthesis.getVoices();

    }


    console.log(
        "Requested language:",
        language
    );


    console.log(
        "Available voices:",
        availableVoices.map(voice => ({
            name: voice.name,
            language: voice.lang
        }))
    );


    // -------------------------------
    // Exact language match
    // -------------------------------

    let voice =
        availableVoices.find(v =>
            v.lang.toLowerCase() ===
            language.toLowerCase()
        );


    // -------------------------------
    // Same base language
    // -------------------------------

    if (!voice) {

        const baseLanguage =
            language
                .split("-")[0]
                .toLowerCase();


        voice =
            availableVoices.find(v =>
                v.lang
                    .toLowerCase()
                    .startsWith(baseLanguage)
            );

    }


    console.log(
        "Selected voice:",
        voice
            ? voice.name + " (" + voice.lang + ")"
            : "NO VOICE FOUND"
    );


    // IMPORTANT:
    // No English fallback here.
    return voice || null;
}


// ===============================
// 🔊 SPEAK MEDICINE REMINDER
// ===============================

function speakReminder(medicine, instructions) {

    if (!("speechSynthesis" in window)) {

        alert(
            "Voice is not supported in this browser."
        );

        return;
    }


    const synth =
        window.speechSynthesis;


    // Stop previous speech
    synth.cancel();


    // Get selected language
    const language =
        getVoiceLanguage();


    // Find matching voice
    const localVoice =
        getBestVoice(language);


    console.log(
        "Speaking language:",
        language
    );


    console.log(
        "Speaking voice:",
        localVoice
            ? localVoice.name +
              " (" +
              localVoice.lang +
              ")"
            : "NO MATCHING VOICE"
    );


    // -------------------------------
    // Reminder message
    // -------------------------------

    let reminderText = "";


    if (currentLanguage === "te") {

        reminderText =
            "మందు తీసుకునే సమయం వచ్చింది.";

    }

    else if (currentLanguage === "hi") {

        reminderText =
            "दवा लेने का समय है।";

    }

    else if (currentLanguage === "ta") {

        reminderText =
            "மருந்து எடுத்துக்கொள்ளும் நேரம் இது.";

    }

    else if (currentLanguage === "kn") {

        reminderText =
            "ಔಷಧಿ ತೆಗೆದುಕೊಳ್ಳುವ ಸಮಯ ಬಂದಿದೆ.";

    }

    else {

        reminderText =
            "It is time to take your medicine.";

    }


    // -------------------------------
    // Reminder speech
    // -------------------------------

    const reminderSpeech =
        new SpeechSynthesisUtterance(
            reminderText
        );


    reminderSpeech.lang =
        language;


    reminderSpeech.rate = 0.7;

    reminderSpeech.pitch = 1;

    reminderSpeech.volume = 1;


    if (localVoice) {

        reminderSpeech.voice =
            localVoice;

    }


    // -------------------------------
    // Medicine name
    // -------------------------------

    const medicineSpeech =
        new SpeechSynthesisUtterance(
            medicine || ""
        );


    medicineSpeech.lang =
        "en-IN";


    medicineSpeech.rate =
        0.7;


    medicineSpeech.pitch =
        1;


    medicineSpeech.volume =
        1;


    const englishVoice =
        getBestVoice("en-IN");


    if (englishVoice) {

        medicineSpeech.voice =
            englishVoice;

    }


    // -------------------------------
    // Instructions
    // -------------------------------

    let instructionSpeech =
        null;


    if (
        instructions &&
        instructions.trim() !== ""
    ) {

        let instructionText = "";


        if (currentLanguage === "te") {

            instructionText =
                "సూచనలు. " +
                instructions;

        }

        else if (currentLanguage === "hi") {

            instructionText =
                "निर्देश। " +
                instructions;

        }

        else if (currentLanguage === "ta") {

            instructionText =
                "வழிமுறைகள். " +
                instructions;

        }

        else if (currentLanguage === "kn") {

            instructionText =
                "ಸೂಚನೆಗಳು. " +
                instructions;

        }

        else {

            instructionText =
                "Instructions. " +
                instructions;

        }


        instructionSpeech =
            new SpeechSynthesisUtterance(
                instructionText
            );


        instructionSpeech.lang =
            language;


        instructionSpeech.rate =
            0.7;


        instructionSpeech.pitch =
            1;


        instructionSpeech.volume =
            1;


        if (localVoice) {

            instructionSpeech.voice =
                localVoice;

        }

    }


    // -------------------------------
    // Speech sequence
    // -------------------------------

    reminderSpeech.onend =
        function () {

            synth.speak(
                medicineSpeech
            );

        };


    medicineSpeech.onend =
        function () {

            if (instructionSpeech) {

                synth.speak(
                    instructionSpeech
                );

            }

        };


    // Start speech
    setTimeout(
        function () {

            synth.resume();

            synth.speak(
                reminderSpeech
            );

        },
        200
    );
}



// ===============================
// 🌙 PAGE LOAD
// ===============================

document.addEventListener(
    "DOMContentLoaded",
    function () {

        applyTheme();

        applyLanguage();

    }
);