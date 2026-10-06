# V2C25-CASE01: எச்சரிக்கையான கொள்கைச் சரிபார்ப்பு [Conservative Policy Check]

வெளியீடு [Release] 0.1.0; தொகுதி 2, அத்தியாயம் 25. இது செயற்கைக் கற்றல் உள்ளீடு [Synthetic Teaching Fixture].

## நிரல் என்ன செய்கிறது [Program Behaviour]

read_catalogue செயலும் நம்பகமான அனுமதி [Trusted Authorization], பங்கு அனுமதி [Role Permission], அளவுரு சரிபார்ப்பு [Argument Validation] ஆகியவையும் இருந்தால் மட்டுமே அனுமதி கிடைக்கும். முக்கியத் தரவு ஏற்றுமதி [Sensitive Export] தடுக்கப்படுகிறது. நிராகரிப்புக் காரணங்கள் [Denial Reasons] வெளியிடப்படுகின்றன.

## முடிவைப் புரிந்துகொள்ளுதல் [Result Interpretation]

கற்பனைக் குழு A-வின் TPR 0.8, FPR 0.2; குழு B-வின் TPR 0.6, FPR 0.1. இந்த வேறுபாடு [Gap] காரணத்தையோ சரியான நியாயத் தீர்வையோ [Fairness Remedy] தனியாகச் சொல்லாது. குறுகிய மின்னஞ்சல் மறைப்பு [Email Redaction] முழுமையான தனிப்பட்ட தகவல் பாதுகாப்பு [PII Protection] அல்ல.

## இயக்குதல் [Run]

துணைத்தொகுப்பின் முதன்மைக் கோப்புறையிலிருந்து [Companion Root]:

    python run_cases.py --chapter 25 --verify

fixture.json கோப்பில் உள்ளீடுகள் [Inputs] உள்ளன. expected.json கோப்பில் உண்மையில் இயக்கிப் பதிவு செய்த வெளியீடு [Recorded Output] உள்ளது. src/volume2_companion/chapter25.py கோப்பில் கணிப்புமுறை [Algorithm] உள்ளது. tests/test_companion.py கோப்பில் அலகுச் சோதனைகள் [Unit Tests] உள்ளன. முதன்மை README_TA.md கோப்பில் நிறுவல் வழிகாட்டி [Setup Guide] உள்ளது.

உள்ளீட்டை [Input] மாற்றும் முன் நகலை [Copy] வைத்துக்கொள்ளவும். அலகுகளையும் [Units] கருதுகோள்களையும் [Assumptions] கவனிக்கவும். எதிர்பார்க்கப்பட்ட கோப்பை [Expected File] மாற்றுவது மட்டும் சரியான கணக்கீட்டிற்கான சான்று அல்ல. இணையம் [Network], கட்டண API [Paid API], அணுகல் சாவி [Credential] அல்லது மாதிரி பதிவிறக்கம் [Model Download] தேவையில்லை.
