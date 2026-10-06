# V2C19-CASE01: சீரமைப்பு முறைகள் [Alignment Methods]

வெளியீடு [Release] 0.1.0; தொகுதி 2, அத்தியாயம் 19. இது செயற்கைக் கற்றல் உள்ளீடு [Synthetic Teaching Fixture].

## நிரல் என்ன செய்கிறது [Program Behaviour]

SFT எடுத்துக்காட்டு இரண்டு தேர்வு மதிப்புகளை [Candidate Logits] ஒரு படியில் புதுப்பிக்கிறது. DPO விரும்பிய மற்றும் நிராகரித்த பதில்களின் மடக்கை நிகழ்தகவு வேறுபாட்டை [Log-probability Difference], குறிப்பு கொள்கையுடன் [Reference Policy] ஒப்பிடுகிறது. LoRA கணக்கு W*x + scale*B*A*x; அடிப்படை அணி [Base Matrix] நீக்கப்படுவதில்லை.

## முடிவைப் புரிந்துகொள்ளுதல் [Result Interpretation]

SFT விருப்ப நிகழ்தகவு [Preferred Probability] 0.5498339973 ஆகிறது. DPO இழப்பு [Loss] 0.4557463944. LoRA வெளியீடு [Output] [4.1,10.2]. இந்தச் சிறிய அணியில் அளவுரு சேமிப்பு [Parameter Saving] இல்லை; முழுமையான RLHF பயிற்சியும் [Training] இல்லை.

## இயக்குதல் [Run]

துணைத்தொகுப்பின் முதன்மைக் கோப்புறையிலிருந்து [Companion Root]:

    python run_cases.py --chapter 19 --verify

fixture.json கோப்பில் உள்ளீடுகள் [Inputs] உள்ளன. expected.json கோப்பில் உண்மையில் இயக்கிப் பதிவு செய்த வெளியீடு [Recorded Output] உள்ளது. src/volume2_companion/chapter19.py கோப்பில் கணிப்புமுறை [Algorithm] உள்ளது. tests/test_companion.py கோப்பில் அலகுச் சோதனைகள் [Unit Tests] உள்ளன. முதன்மை README_TA.md கோப்பில் நிறுவல் வழிகாட்டி [Setup Guide] உள்ளது.

உள்ளீட்டை [Input] மாற்றும் முன் நகலை [Copy] வைத்துக்கொள்ளவும். அலகுகளையும் [Units] கருதுகோள்களையும் [Assumptions] கவனிக்கவும். எதிர்பார்க்கப்பட்ட கோப்பை [Expected File] மாற்றுவது மட்டும் சரியான கணக்கீட்டிற்கான சான்று அல்ல. இணையம் [Network], கட்டண API [Paid API], அணுகல் சாவி [Credential] அல்லது மாதிரி பதிவிறக்கம் [Model Download] தேவையில்லை.
