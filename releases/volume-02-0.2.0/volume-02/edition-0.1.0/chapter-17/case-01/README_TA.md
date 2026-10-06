# V2C17-CASE01: காரணவழிக் கவனம் [Causal Attention]

வெளியீடு [Release] 0.1.0; தொகுதி 2, அத்தியாயம் 17. இது செயற்கைக் கற்றல் உள்ளீடு [Synthetic Teaching Fixture].

## நிரல் என்ன செய்கிறது [Program Behaviour]

Q மற்றும் K இரண்டிலும் இரண்டு அம்சங்கள் [Features] இருப்பதால் புள்ளிப் பெருக்கல் [Dot Product] sqrt(2) ஆல் வகுக்கப்படுகிறது. காரணவழி மறைப்பு [Causal Mask] தற்போதைய இடத்தையும் முந்தைய இடங்களையும் மட்டுமே அனுமதிக்கிறது. ஒவ்வொரு கவன வரிசையின் [Attention Row] எடைகள் [Weights] சேர்ந்து ஒன்று ஆகின்றன.

## முடிவைப் புரிந்துகொள்ளுதல் [Result Interpretation]

முதல் வெளியீடு [Output] [2,0]. இரண்டாவது வெளியீடு [Output] சுமார் [0.6604769013,2.6790461973]. எதிர்கால மதிப்பு திசையனை [Future Value Vector] மாற்றினாலும் முதல் வெளியீடு மாறாது. கவன எடைகள் [Attention Weights] உண்மைக்கான சான்றோ முழுமையான விளக்கமோ அல்ல.

## இயக்குதல் [Run]

துணைத்தொகுப்பின் முதன்மைக் கோப்புறையிலிருந்து [Companion Root]:

    python run_cases.py --chapter 17 --verify

fixture.json கோப்பில் உள்ளீடுகள் [Inputs] உள்ளன. expected.json கோப்பில் உண்மையில் இயக்கிப் பதிவு செய்த வெளியீடு [Recorded Output] உள்ளது. src/volume2_companion/chapter17.py கோப்பில் கணிப்புமுறை [Algorithm] உள்ளது. tests/test_companion.py கோப்பில் அலகுச் சோதனைகள் [Unit Tests] உள்ளன. முதன்மை README_TA.md கோப்பில் நிறுவல் வழிகாட்டி [Setup Guide] உள்ளது.

உள்ளீட்டை [Input] மாற்றும் முன் நகலை [Copy] வைத்துக்கொள்ளவும். அலகுகளையும் [Units] கருதுகோள்களையும் [Assumptions] கவனிக்கவும். எதிர்பார்க்கப்பட்ட கோப்பை [Expected File] மாற்றுவது மட்டும் சரியான கணக்கீட்டிற்கான சான்று அல்ல. இணையம் [Network], கட்டண API [Paid API], அணுகல் சாவி [Credential] அல்லது மாதிரி பதிவிறக்கம் [Model Download] தேவையில்லை.
