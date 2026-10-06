# V2C21-CASE01: வரம்புள்ள முகவர் செயல்முறை [Bounded Agent Workflow]

வெளியீடு [Release] 0.1.0; தொகுதி 2, அத்தியாயம் 21. இது செயற்கைக் கற்றல் உள்ளீடு [Synthetic Teaching Fixture].

## நிரல் என்ன செய்கிறது [Program Behaviour]

read_catalogue, read_labels, calculate_total என்ற மூன்று போலி கருவிகள் [Mock Tools] மட்டுமே இயக்கப்படுகின்றன. பொருள் பட்டியல் உரை [Catalogue Text] தரவாக [Data] மட்டுமே வைக்கப்படுகிறது. நம்பகமான செயல்முறை [Trusted Workflow] கருவியைத் தேர்ந்தெடுக்கிறது; அழைப்பு எண்ணிக்கை [Call Count] வரம்புக்குள் இருக்க வேண்டும். வாங்கும் கருவி [Purchase Tool] இல்லை.

## முடிவைப் புரிந்துகொள்ளுதல் [Result Interpretation]

செயற்கைப் பொருள் செலவு A$31.50 மற்றும் விநியோகக் கட்டணம் [Delivery Fee] A$5.00 சேர்ந்து A$36.50. தீர்க்கப்படாத குறுக்குத் தொடர்புச் சான்று [Cross-contact Evidence] இருந்தால் செயல்முறை தடுக்கப்படுகிறது. இது பெரிய மொழி மாதிரி முகவர் சோதனை [LLM Agent Benchmark] அல்ல.

## இயக்குதல் [Run]

துணைத்தொகுப்பின் முதன்மைக் கோப்புறையிலிருந்து [Companion Root]:

    python run_cases.py --chapter 21 --verify

fixture.json கோப்பில் உள்ளீடுகள் [Inputs] உள்ளன. expected.json கோப்பில் உண்மையில் இயக்கிப் பதிவு செய்த வெளியீடு [Recorded Output] உள்ளது. src/volume2_companion/chapter21.py கோப்பில் கணிப்புமுறை [Algorithm] உள்ளது. tests/test_companion.py கோப்பில் அலகுச் சோதனைகள் [Unit Tests] உள்ளன. முதன்மை README_TA.md கோப்பில் நிறுவல் வழிகாட்டி [Setup Guide] உள்ளது.

உள்ளீட்டை [Input] மாற்றும் முன் நகலை [Copy] வைத்துக்கொள்ளவும். அலகுகளையும் [Units] கருதுகோள்களையும் [Assumptions] கவனிக்கவும். எதிர்பார்க்கப்பட்ட கோப்பை [Expected File] மாற்றுவது மட்டும் சரியான கணக்கீட்டிற்கான சான்று அல்ல. இணையம் [Network], கட்டண API [Paid API], அணுகல் சாவி [Credential] அல்லது மாதிரி பதிவிறக்கம் [Model Download] தேவையில்லை.
