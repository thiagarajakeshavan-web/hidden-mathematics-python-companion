# V2C16-CASE01: மூன்று கட்டமைப்புக் கூறுகள் [Architecture Blocks]

வெளியீடு [Release] 0.1.0; தொகுதி 2, அத்தியாயம் 16. இது செயற்கைக் கற்றல் உள்ளீடு [Synthetic Teaching Fixture].

## நிரல் என்ன செய்கிறது [Program Behaviour]

இங்கே CNN கணக்கு ஒரு பரிமாண குறுக்குத் தொடர்பு [Cross-correlation]; வடிகட்டி [Kernel] தலைகீழாக்கப்படுவதில்லை. மீள்நுழைவு வலையமைப்பு [RNN] முந்தைய மறை நிலையை [Hidden State] பயன்படுத்துகிறது. LSTM வாயில் வெளியீடுகள் [Gate Outputs] நேரடியாக வழங்கப்பட்டவை; இந்தப் பயிற்சியில் அவை கற்றுக்கொள்ளப்படுவதில்லை.

## முடிவைப் புரிந்துகொள்ளுதல் [Result Interpretation]

குறுக்குத் தொடர்பு [Cross-correlation] [-1,-2,1] ஆகவும் LSTM செல் நிலை [Cell State] 0.7 ஆகவும் வருகிறது. 0.75^10 மற்றும் 0.99^10 ஆகியவை நிலையான வாயிலின் நேரடி நினைவுப் பாதையை [Direct Carry Path] மட்டுமே காட்டுகின்றன; முழுச் சாய்வைக் [Full Gradient] காட்டவில்லை.

## இயக்குதல் [Run]

துணைத்தொகுப்பின் முதன்மைக் கோப்புறையிலிருந்து [Companion Root]:

    python run_cases.py --chapter 16 --verify

fixture.json கோப்பில் உள்ளீடுகள் [Inputs] உள்ளன. expected.json கோப்பில் உண்மையில் இயக்கிப் பதிவு செய்த வெளியீடு [Recorded Output] உள்ளது. src/volume2_companion/chapter16.py கோப்பில் கணிப்புமுறை [Algorithm] உள்ளது. tests/test_companion.py கோப்பில் அலகுச் சோதனைகள் [Unit Tests] உள்ளன. முதன்மை README_TA.md கோப்பில் நிறுவல் வழிகாட்டி [Setup Guide] உள்ளது.

உள்ளீட்டை [Input] மாற்றும் முன் நகலை [Copy] வைத்துக்கொள்ளவும். அலகுகளையும் [Units] கருதுகோள்களையும் [Assumptions] கவனிக்கவும். எதிர்பார்க்கப்பட்ட கோப்பை [Expected File] மாற்றுவது மட்டும் சரியான கணக்கீட்டிற்கான சான்று அல்ல. இணையம் [Network], கட்டண API [Paid API], அணுகல் சாவி [Credential] அல்லது மாதிரி பதிவிறக்கம் [Model Download] தேவையில்லை.
