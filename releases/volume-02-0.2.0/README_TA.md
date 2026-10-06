# தொகுதி 2: பைதான் துணைத்தொகுப்பு [Python Companion]

நூல்: The Hidden Mathematics of Machine Learning and Large Language Models
தொகுதி: 2 / 2
ஆசிரியர்: Keshavan Thiagaraja
ஆசிரியர் பார்வைக்கான வெளியீடு [Author-review Release]: 0.2.0

15–26 அத்தியாயங்களுக்கான பதினான்கு சிறிய பயிற்சிகள் [Labs] இங்கே உள்ளன. ஆங்கில மற்றும் தமிழ் நூல்களுக்கு ஒரே நிரல் [Code] பயன்படுத்தப்படுகிறது. ஒவ்வொரு பயிற்சியின் அடையாளமும் [Case ID] இரு நூல்களிலும் ஒன்றாக இருக்கும்.

இவை செயற்கைத் தரவுகளைக் [Synthetic Data] கொண்ட கற்றல் எடுத்துக்காட்டுகள். இவை செயல்பாட்டிலுள்ள SHOP SMART AI சேவைகளோ, முன்பயிற்சி பெற்ற பெரிய மொழி மாதிரிகளோ [Pretrained Large Language Models], உண்மையான கடை இணைப்புகளோ [Retailer Integrations] அல்ல. கணக்கு [Account], அணுகல் சாவி [API Key], வரைகலைச் செயலி [GPU], மாதிரி பதிவிறக்கம் [Model Download] அல்லது உண்மையான வாடிக்கையாளர் தரவு [Customer Data] தேவையில்லை. தேவையான மென்பொருள் ஏற்கெனவே இருந்தால், அனைத்து பயிற்சிகளையும் இணையமின்றி [Offline] இயக்கலாம்.

## தொடங்குவது எப்படி [Setup]

இந்த வெளியீடு [Release] Linux x86_64 சூழலில் CPython 3.12.14 மற்றும் NumPy 2.3.5 கொண்டு சோதிக்கப்பட்டது. மற்ற இயக்க முறைமைகள் [Operating Systems] அல்லது பதிப்புகள் [Versions] இந்த வெளியீட்டில் சோதிக்கப்படவில்லை.

1. ZIP கோப்பைப் பிரித்தெடுக்கவும் [Extract]. README.md மற்றும் run_cases.py உள்ள கோப்புறையைத் [Folder] திறக்கவும்.
2. அக்கோப்புறையில் முனையத்தைத் [Terminal] திறக்கவும்.
3. Python மற்றும் குறிப்பிட்ட NumPy பதிப்பு [Version] ஏற்கெனவே இருந்தால், கீழே உள்ள இயக்கக் கட்டளைகளுக்குச் [Run Commands] செல்லலாம்.
4. தனிச் சூழல் [Virtual Environment] தேவைப்பட்டால், நம்பகமான Python நிறுவலைப் பயன்படுத்தவும். NumPy நிறுவுவதற்கு மட்டும் இணையம் தேவைப்படலாம். ஏற்கெனவே நம்பகமான உள்ளூர் நிறுவல் கோப்பு [Wheel] இருந்தால் இணையம் தேவையில்லை.

Linux, macOS அல்லது Windows WSL Ubuntu:

    python3 -m venv .venv
    source .venv/bin/activate
    python -m pip install -r requirements.lock

Windows PowerShell:

    py -3.12 -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.lock

Windows-இல் கீழே வரும் python என்பதற்குப் பதிலாக .\.venv\Scripts\python.exe என்பதைப் பயன்படுத்தவும். இதற்காக PowerShell இயக்கக் கொள்கையை [Execution Policy] மாற்ற வேண்டியதில்லை. தெரியாத இணைப்பிலிருந்து மென்பொருள் நிறுவ வேண்டாம். கடவுச்சொல் [Password] அல்லது அணுகல் சாவியை [Access Token] இந்தத் துணைத்தொகுப்பில் சேர்க்க வேண்டாம்.

## இயக்குதல் மற்றும் சரிபார்த்தல் [Run and Verify]

பதினான்கு பயிற்சிகளையும் இயக்கி, பதிவு செய்யப்பட்ட முடிவுகளுடன் [Recorded Results] ஒப்பிட:

    python run_cases.py --verify

முடிவுகளைப் புதிய கோப்பில் [File] சேமிக்க:

    python run_cases.py --verify --output my_results.json

17ஆம் அத்தியாயத்தை மட்டும் இயக்க:

    python run_cases.py --chapter 17 --verify

அனைத்து அலகுச் சோதனைகளையும் [Unit Tests] இயக்க:

    python -m unittest discover -s tests -v

ஒவ்வொரு பயிற்சிக் கோப்புறையிலும் [Case Folder] fixture.json என்ற செயற்கை உள்ளீடு [Synthetic Input], expected.json என்ற பதிவு செய்யப்பட்ட வெளியீடு [Recorded Output], run.py என்ற இயக்க நுழைவுப்புள்ளி [Entry Point], ஆங்கில மற்றும் தமிழ் வழிகாட்டிகள் உள்ளன. src/volume2_companion கோப்புறையில் பகிரப்பட்ட நிரல் [Shared Code] உள்ளது. reports/TEST_REPORT_0.2.0.md கோப்பில் உண்மையில் செய்யப்பட்ட சோதனைகளும் [Tests] அவற்றின் வரம்புகளும் [Limitations] தரப்பட்டுள்ளன.

மிதவைப் புள்ளிக் கணக்கீட்டால் [Floating-point Arithmetic] 0.7 என்ற எண் 0.7000000000000001 எனத் தோன்றலாம். ஒப்பீட்டில் [Comparison] 1e-9 என்ற சிறிய முழுமையான மற்றும் சார்பு சகிப்புத்தன்மைகள் [Absolute and Relative Tolerances] பயன்படுத்தப்படுகின்றன. உரை [Text], பூலியன் மதிப்புகள் [Booleans], முடிவு அமைப்பு [Result Structure] ஆகியவை துல்லியமாகப் பொருந்த வேண்டும்.

## பயிற்சியைப் புரிந்துகொள்வது [Learning Workflow]

முதலில் மாறாத உள்ளீட்டுடன் [Input] பயிற்சியை இயக்கவும். நூலிலுள்ள ஒரு இடைநிலை முடிவை [Intermediate Result] கையால் கணக்கிட்டு ஒப்பிடவும். உள்ளீட்டை மாற்றும் முன் அதன் நகலை [Copy] வைத்துக்கொள்ளவும். மாற்றிய முடிவு எதிர்பார்ப்புடன் [Expected Result] பொருந்தவில்லை என்றால் காரணத்தைக் கண்டறியவும். சோதனைத் தோல்வியை [Test Failure] மறைப்பதற்காக expected.json கோப்பை மாற்ற வேண்டாம்.

15ஆம் அத்தியாயத்தில் கற்றல் வீதத்தை [Learning Rate] மாற்றிப் பார்க்கலாம். 17ஆம் அத்தியாயத்தில் எதிர்கால மதிப்பை [Future Value] மட்டும் மாற்றி, காரணவழிக் கவனத்தின் [Causal Attention] முதல் வெளியீடு [Output] மாறாதிருப்பதைப் பார்க்கலாம். 22ஆம் அத்தியாயத்தில் கிடைத்த நேரத்தை [Available-at Time] மாற்றி, முடிவெடுக்கும் நேரத்தில் [Decision Time] உண்மையில் அறியப்பட்ட தகவலின் முக்கியத்துவத்தை அறியலாம்.

## பாதுகாப்பும் வரம்புகளும் [Safety and Limitations]

ஒற்றுமை மதிப்பெண் [Similarity Score] உண்மையையோ ஒவ்வாமைப் பாதுகாப்பையோ [Allergen Safety] உறுதி செய்யாது. முழுமையான, தற்போதைய, முரண்பாடற்ற சான்று [Evidence] இருந்தாலும் இந்த எடுத்துக்காட்டில் மனித ஆய்விற்கான தகுதி [Review Eligibility] மட்டுமே கிடைக்கும். சான்று இல்லாமை, பழைய சான்று [Stale Evidence], முரண்பாடு [Conflict], தீர்க்கப்படாத குறுக்குத் தொடர்பு [Cross-contact] ஆகியவை இருந்தால் தானியக்கத் தகுதி [Automatic Eligibility] நிறுத்தப்படுகிறது. நிலக்கடலை [Peanut] மற்றும் மரக்கொட்டை வகைகள் [Tree Nuts] வேறுபட்டவை. இவை கற்பனை வாடிக்கையாளரின் கட்டுப்பாடுகள் [Hypothetical Shopper Constraints]; ஆசிரியரின் உடல்நலத் தகவல் அல்ல.

21ஆம் அத்தியாயம் கட்டுப்படுத்தப்பட்ட நிலைமாற்றச் செயல்முறை [Bounded State Workflow] மட்டுமே. உண்மையான பெரிய மொழி மாதிரி [LLM] அல்லது பல்முகவர் சேவை [Multi-agent Service] இயக்கப்படுவதில்லை. 25ஆம் அத்தியாயத்தின் அதிகாரக் கொடிகள் [Authority Flags] நம்பகமான சோதனை உள்ளீடுகள் [Trusted Test Fixtures]. உண்மையான அமைப்பில் அவை அங்கீகரிக்கப்பட்ட பயன்பாட்டுக் கட்டுப்பாடுகளிலிருந்து [Authenticated Application Controls] வர வேண்டும்; மாதிரி வெளியீடு [Model Output] அல்லது தேடிப் பெறப்பட்ட உரையிலிருந்து [Retrieved Text] வரக்கூடாது.

## பொது அணுகல் நிலை [Public Access Status]

நூலை வாங்காதவர்களுக்கும் எதிர்காலத்தில் பொது GitHub அணுகல் [Public GitHub Access] வழங்குவது நோக்கம். கணக்கு அமைத்தலும் வெளியிடுதலும் [Account Setup and Publication] இன்னும் நிலுவையில் உள்ளன. உறுதிப்படுத்தப்பட்ட பொது முகவரி [Verified Public URL] இன்னும் இல்லை. இந்தக் கோப்பால் புதிய மென்பொருள் உரிமம் [Software Licence] வழங்கப்படவில்லை; ஆசிரியரின் உரிம முடிவு [Licence Decision] நிலுவையில் உள்ளது.

## 0.2.0 சேர்க்கைகளும் பாதுகாப்பும் [Additions and Preservation]

இந்த வெளியீட்டில் [Release] 14 வழக்குகளும் [Cases] 287 வெற்றிகரமான அலகுச் சோதனைகளும் [Unit tests] உள்ளன: முந்தைய 226, புதிய பாலப்பகுதி சோதனைகள் [Bridge tests] 45, தனி ஆய்வாளர் கணிதச் சரிபார்ப்புகள் [Reviewer oracles] 16. முந்தைய 12 வழக்குக் கோப்புறைகளும் [Case directories] edition-0.1.0-இல் பைட் அளவிலும் மாறாமல் உள்ளன; புதிய இரண்டு CASE02 வழக்குகள் edition-0.2.0-இல் உள்ளன. முந்தைய 0.1.0 காப்பகமும் [Archive] வரலாற்று இயக்க அறிக்கைகளும் [Historical execution reports] தனியாகப் பாதுகாக்கப்படுகின்றன.

V2C15-CASE02: ஒரே இரண்டு அளவிச் சாய்வுகளை [Scalar gradients] AdaGrad, மையப்படுத்தப்படாத RMSProp [Uncentred RMSProp], சார்பு திருத்திய Adam [Bias-corrected Adam] ஆகியவற்றில் கணக்கிடுகிறது.
V2C16-CASE02: BatchNorm பயிற்சி [Training], உறைந்த புள்ளிவிவர ஊகித்தல் [Frozen-stat inference], LayerNorm அச்சு ஒப்பீடு [Axis comparison] ஆகியவற்றைக் கணக்கிடுகிறது.

இயல்பான இயக்கி [Default runner] எல்லா வழக்குகளையும் [Cases] உள்ளடக்கும். --chapter 15 அல்லது --chapter 16 அந்த அத்தியாயத்தின் இரண்டு வழக்குகளையும் இயக்கும். புதிய வழக்கை [Case] மட்டும் தேர்ந்தெடுக்க:

    python run_cases.py --chapter 15 --case 2 --verify

இயல்பாக்க வழக்கிற்கு [Normalisation case] --chapter 16 --case 2 பயன்படுத்தவும். --case 1 முந்தைய வழக்குகளைத் [Cases] தேர்ந்தெடுக்கும். முந்தைய நேரடி CASE01 நுழைவுப்புள்ளிகள் [Entry points] அதே பொருளைத் தக்கவைக்கின்றன. தனி ஆய்வாளர் சோதனைகள் [Reviewer tests] எதிர்பார்த்த வெளியீட்டுக் கோப்புகளை [Expected output files] படிப்பதில்லை. உண்மையான வெளியீட்டுச் சோதனைகளுக்கு [Release checks] reports/TEST_REPORT_0.2.0.md, reports/release_validation_0.2.0.json பார்க்கவும்.

புதிய பயிற்சிகள் [Labs] அளவி உகப்பாக்கிப் புதுப்பிப்புகளையும் [Scalar optimizer updates] முன்னோக்கு இயல்பாக்கத்தையும் [Forward normalization] மட்டுமே விளக்குகின்றன. புதிய நரம்புவலைப் பயிற்சி ஒப்பீடோ [Neural-training benchmark] உற்பத்திக் கூற்றோ [Production claim] இல்லை. PyTorch ஆவணம் ஒப்பீட்டு மரபுகளை [Comparison conventions] விளக்குகிறது; இத்தொகுப்பு PyTorch-ஐ நிறுவுவதோ இயக்குவதோ இல்லை.
