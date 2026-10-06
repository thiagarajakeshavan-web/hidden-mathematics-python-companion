# V2C26-CASE01: விலகலும் சேவை வரம்புகளும் [Drift and Service Budgets]

வெளியீடு [Release] 0.1.0; தொகுதி 2, அத்தியாயம் 26. இது செயற்கைக் கற்றல் உள்ளீடு [Synthetic Teaching Fixture].

## நிரல் என்ன செய்கிறது [Program Behaviour]

மொத்த மாறுபாடு [Total Variation] ஒரே வகைப்பிரிவுகளின் பகிர்வுகளை [Distributions] ஒப்பிடுகிறது. கிடைப்புத் திறன் [Availability] செயற்கைக் கோரிக்கை எண்ணிக்கையிலிருந்து [Synthetic Request Counts] கணக்கிடப்படுகிறது. லிட்டில் விதி [Little’s Law] நிலையான அமைப்பையும் [Stable System] ஒரே அளவீட்டு எல்லையையும் [Measurement Boundary] கருதுகிறது.

## முடிவைப் புரிந்துகொள்ளுதல் [Result Interpretation]

மொத்த மாறுபாடு [Total Variation] 0.2. 10,000 கோரிக்கைகளில் [Requests] 30 தோல்விகள் [Failures] இருந்தால் கிடைப்புத் திறன் [Availability] 0.997. அனுமதிக்கப்பட்ட 50 தோல்விகளில் 20 மீதம். சராசரி ஒரேநேரப் பணிகள் [Mean Concurrency] 4. 110 ms மற்றும் 70 ms தாமதங்கள் [Latencies] கருதப்பட்டவை; நேரடியாக அளவிடப்பட்டவை அல்ல.

## இயக்குதல் [Run]

துணைத்தொகுப்பின் முதன்மைக் கோப்புறையிலிருந்து [Companion Root]:

    python run_cases.py --chapter 26 --verify

fixture.json கோப்பில் உள்ளீடுகள் [Inputs] உள்ளன. expected.json கோப்பில் உண்மையில் இயக்கிப் பதிவு செய்த வெளியீடு [Recorded Output] உள்ளது. src/volume2_companion/chapter26.py கோப்பில் கணிப்புமுறை [Algorithm] உள்ளது. tests/test_companion.py கோப்பில் அலகுச் சோதனைகள் [Unit Tests] உள்ளன. முதன்மை README_TA.md கோப்பில் நிறுவல் வழிகாட்டி [Setup Guide] உள்ளது.

உள்ளீட்டை [Input] மாற்றும் முன் நகலை [Copy] வைத்துக்கொள்ளவும். அலகுகளையும் [Units] கருதுகோள்களையும் [Assumptions] கவனிக்கவும். எதிர்பார்க்கப்பட்ட கோப்பை [Expected File] மாற்றுவது மட்டும் சரியான கணக்கீட்டிற்கான சான்று அல்ல. இணையம் [Network], கட்டண API [Paid API], அணுகல் சாவி [Credential] அல்லது மாதிரி பதிவிறக்கம் [Model Download] தேவையில்லை.
