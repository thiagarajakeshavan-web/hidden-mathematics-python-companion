# V2C20-CASE01: மீட்டெடுப்பும் தகுதியும் [Retrieval and Eligibility]

வெளியீடு [Release] 0.1.0; தொகுதி 2, அத்தியாயம் 20. இது செயற்கைக் கற்றல் உள்ளீடு [Synthetic Teaching Fixture].

## நிரல் என்ன செய்கிறது [Program Behaviour]

திசையனின் [Vector] மூன்று கூறுகள் vegan, dinner, powder என்ற சொற்களைக் குறிக்கின்றன. இவை கற்றுக்கொண்ட பொதிவுகள் [Learned Embeddings] அல்ல. அனுமதியற்ற மற்றும் பழைய பதிவுகள் [Unauthorized and Stale Records] மதிப்பெண் [Score] கணக்கிடும் முன்பே நீக்கப்படுகின்றன. கட்டுப்பாட்டுச் சான்று [Restriction Evidence] தனியாகச் சரிபார்க்கப்படுகிறது.

## முடிவைப் புரிந்துகொள்ளுதல் [Result Interpretation]

D1 ஒற்றுமையில் [Cosine Similarity] முதலிடம் பெற்றாலும் அதன் சான்று [Evidence] தெரியாததால் தடுக்கப்படுகிறது. D2 மதிப்பு 0.7071067812; அது செயற்கை மனித ஆய்விற்கான தேர்வு [Review Candidate] மட்டுமே. எந்த மதிப்பெண்ணும் [Score] ஒவ்வாமைப் பாதுகாப்பை [Allergen Safety] உறுதி செய்யாது.

## இயக்குதல் [Run]

துணைத்தொகுப்பின் முதன்மைக் கோப்புறையிலிருந்து [Companion Root]:

    python run_cases.py --chapter 20 --verify

fixture.json கோப்பில் உள்ளீடுகள் [Inputs] உள்ளன. expected.json கோப்பில் உண்மையில் இயக்கிப் பதிவு செய்த வெளியீடு [Recorded Output] உள்ளது. src/volume2_companion/chapter20.py கோப்பில் கணிப்புமுறை [Algorithm] உள்ளது. tests/test_companion.py கோப்பில் அலகுச் சோதனைகள் [Unit Tests] உள்ளன. முதன்மை README_TA.md கோப்பில் நிறுவல் வழிகாட்டி [Setup Guide] உள்ளது.

உள்ளீட்டை [Input] மாற்றும் முன் நகலை [Copy] வைத்துக்கொள்ளவும். அலகுகளையும் [Units] கருதுகோள்களையும் [Assumptions] கவனிக்கவும். எதிர்பார்க்கப்பட்ட கோப்பை [Expected File] மாற்றுவது மட்டும் சரியான கணக்கீட்டிற்கான சான்று அல்ல. இணையம் [Network], கட்டண API [Paid API], அணுகல் சாவி [Credential] அல்லது மாதிரி பதிவிறக்கம் [Model Download] தேவையில்லை.
