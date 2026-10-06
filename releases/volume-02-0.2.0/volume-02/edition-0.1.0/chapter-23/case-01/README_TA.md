# V2C23-CASE01: மதிப்பீடும் உறுதியின்மையும் [Evaluation and Uncertainty]

வெளியீடு [Release] 0.1.0; தொகுதி 2, அத்தியாயம் 23. இது செயற்கைக் கற்றல் உள்ளீடு [Synthetic Teaching Fixture].

## நிரல் என்ன செய்கிறது [Program Behaviour]

supported=1 என்பது செயற்கை மனிதச் சான்று ஆதரவு குறியீடு [Evidence-support Label]. flagged_unsupported=1 என்பது ஆதரவில்லாததைச் சுட்டும் கணிப்பு [Prediction]. இணை மீள்மாதிரியாக்கம் [Paired Bootstrap] ஒரே கோரிக்கை குறியீடுகளை [Request Indices] இரு முறைகளுக்கும் பயன்படுத்துகிறது.

## முடிவைப் புரிந்துகொள்ளுதல் [Result Interpretation]

ஆதரவு விகிதம் [Faithfulness] 0.7; வில்சன் நம்பக இடைவெளி [Wilson Confidence Interval] சுமார் [0.396778,0.892209]. பிரையர் மதிப்பு [Brier Score] 0.175 இருந்தும் ஒற்றைப் பிரிவு ECE [One-bin ECE] பூஜ்யமாக வட்டமிடப்படுகிறது. இந்தச் சிறிய செயற்கை மாதிரி [Synthetic Sample] உண்மையையோ செயல்பாட்டுப் பாதுகாப்பையோ உறுதி செய்யாது.

## இயக்குதல் [Run]

துணைத்தொகுப்பின் முதன்மைக் கோப்புறையிலிருந்து [Companion Root]:

    python run_cases.py --chapter 23 --verify

fixture.json கோப்பில் உள்ளீடுகள் [Inputs] உள்ளன. expected.json கோப்பில் உண்மையில் இயக்கிப் பதிவு செய்த வெளியீடு [Recorded Output] உள்ளது. src/volume2_companion/chapter23.py கோப்பில் கணிப்புமுறை [Algorithm] உள்ளது. tests/test_companion.py கோப்பில் அலகுச் சோதனைகள் [Unit Tests] உள்ளன. முதன்மை README_TA.md கோப்பில் நிறுவல் வழிகாட்டி [Setup Guide] உள்ளது.

உள்ளீட்டை [Input] மாற்றும் முன் நகலை [Copy] வைத்துக்கொள்ளவும். அலகுகளையும் [Units] கருதுகோள்களையும் [Assumptions] கவனிக்கவும். எதிர்பார்க்கப்பட்ட கோப்பை [Expected File] மாற்றுவது மட்டும் சரியான கணக்கீட்டிற்கான சான்று அல்ல. இணையம் [Network], கட்டண API [Paid API], அணுகல் சாவி [Credential] அல்லது மாதிரி பதிவிறக்கம் [Model Download] தேவையில்லை.
