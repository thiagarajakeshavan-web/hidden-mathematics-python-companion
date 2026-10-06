# V2C24-CASE01: செயல்திறன் கணக்கீடுகள் [Efficiency Calculations]

வெளியீடு [Release] 0.1.0; தொகுதி 2, அத்தியாயம் 24. இது செயற்கைக் கற்றல் உள்ளீடு [Synthetic Teaching Fixture].

## நிரல் என்ன செய்கிறது [Program Behaviour]

சமச்சீர் int8 அளவாக்கம் [Symmetric Quantization] max(abs(weights))/127 அளவைப் பயன்படுத்துகிறது. வெட்டுக் குறியீடு [Pruning Mask] மற்றும் வெட்டப்பட்ட எடைகள் [Pruned Weights] வெளியிடப்படுகின்றன. அறிவு வடித்தல் [Distillation] மூன்று வகை மதிப்புகளை [Categorical Logits] மட்டுமே 20 படிகளில் கற்பிக்கிறது. சாய்வு [Gradient] மைய வேறுபாட்டால் [Central Difference] சரிபார்க்கப்படுகிறது.

## முடிவைப் புரிந்துகொள்ளுதல் [Result Interpretation]

மாணவர் KL [Student KL] 0.0227302548 இலிருந்து சுமார் 0.0002191048 ஆகக் குறைகிறது. கற்பனை KV தற்காலிக நினைவகம் [KV Cache] 50,331,648 bytes அல்லது 48 MiB. உண்மையான GPU வேகம் [Speed] அல்லது முழு LLM சுருக்கம் [Compression] அளவிடப்படவில்லை.

## இயக்குதல் [Run]

துணைத்தொகுப்பின் முதன்மைக் கோப்புறையிலிருந்து [Companion Root]:

    python run_cases.py --chapter 24 --verify

fixture.json கோப்பில் உள்ளீடுகள் [Inputs] உள்ளன. expected.json கோப்பில் உண்மையில் இயக்கிப் பதிவு செய்த வெளியீடு [Recorded Output] உள்ளது. src/volume2_companion/chapter24.py கோப்பில் கணிப்புமுறை [Algorithm] உள்ளது. tests/test_companion.py கோப்பில் அலகுச் சோதனைகள் [Unit Tests] உள்ளன. முதன்மை README_TA.md கோப்பில் நிறுவல் வழிகாட்டி [Setup Guide] உள்ளது.

உள்ளீட்டை [Input] மாற்றும் முன் நகலை [Copy] வைத்துக்கொள்ளவும். அலகுகளையும் [Units] கருதுகோள்களையும் [Assumptions] கவனிக்கவும். எதிர்பார்க்கப்பட்ட கோப்பை [Expected File] மாற்றுவது மட்டும் சரியான கணக்கீட்டிற்கான சான்று அல்ல. இணையம் [Network], கட்டண API [Paid API], அணுகல் சாவி [Credential] அல்லது மாதிரி பதிவிறக்கம் [Model Download] தேவையில்லை.
