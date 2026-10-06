> 1.2.0 இணைப்பு: கீழே உள்ள பழைய அமைப்பு வழிகாட்டி [Setup Guide] தொடர்ந்து பொருந்தும். புதிய எடுத்துக்காட்டுகளுக்கு [தமிழ் வழிகாட்டியை](shopsmart_scenarios/README_TA.md) படித்து `python run_additions.py` இயக்கவும். முழுச் சோதனைத் தொகுப்பில் [Full Test Suite] இப்போது 178 சோதனைகள் உள்ளன. வெளியீடு [Publication] இன்னும் நிலுவையில் உள்ளது.

# தமிழில் விரைவுத் தொடக்க வழிகாட்டி [Quickstart Guide]

இந்தத் துணைத்தொகுப்பை [Companion] உங்கள் கணினியில் இயக்கலாம். நூலை வாங்கியிருக்க வேண்டிய நிபந்தனையின்றி, அனைவருக்கும் பொதுவான நிரல் அணுகலை [Public Code Access] வழங்க ஆசிரியர் முடிவு செய்துள்ளார். தொலைநிலைக் களஞ்சியத்தின் [Remote Repository] வெளியீடு உறுதிசெய்யப்பட்டுள்ளதா என்பதை இந்தச் சுருக்கப்பட்ட கோப்பு [ZIP File] தனியாகச் சான்றளிக்காது. இப்போது வழங்கப்படுவது ஆசிரியரின் ஆய்வுப் பதிப்பு [Author Review Version]. ஆங்கிலப் பதிப்புக்கும் தமிழ்ப் பதிப்புக்கும் ஒரே பைத்தான் மூலநிரல் [Python Source Code] பயன்படுத்தப்படுகிறது.

## 1. தயாராகுங்கள்

பைத்தான் [Python] 3.12 தேவை. பதிவு செய்யப்பட்ட சோதனைகள் [Tests], பைத்தான் [Python] 3.12.14 சூழலில் [Environment] நடைபெற்றன. அதிகாரப்பூர்வ தளம்: https://www.python.org/downloads/ . சுருக்கப்பட்ட கோப்பை [ZIP File] நீங்கள் எழுத அனுமதியுள்ள கோப்புறையில் [Folder] பிரித்தெடுக்கவும். `requirements.txt` உள்ள `volume1_code` கோப்புறையில் [Folder] முனையத்தை [Terminal] திறக்கவும்.

கீழுள்ள கட்டளைகள் [Commands], இந்தப் பணிக்கான தனி மெய்நிகர் சூழலை [Virtual Environment] உருவாக்கும். கணினியின் பொதுப் பைத்தான் நிறுவலை [System Python Installation], கட்டளைச் சூழல் அமைப்பை [Shell Configuration], அல்லது நிரல் இயக்க அனுமதிக் கொள்கையை [Execution Policy] மாற்றத் தேவையில்லை. நிர்வாகி [Administrator] அல்லது `root` ஆக இயக்க வேண்டாம். உங்கள் இயக்க முறைமைக்கு [Operating System] ஏற்ற ஒரு பகுதியை மட்டும் பின்பற்றவும்.

## 2. Windows PowerShell

கட்டளைகளை [Commands] மாற்றாமல் ஒவ்வொன்றாக இயக்கவும்:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe run_all.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -v
```

முதல் அத்தியாயத்தை மட்டும் இயக்க:

```powershell
.\.venv\Scripts\python.exe V1C01\lab.py
```

மெய்நிகர் சூழலை [Virtual Environment] தனியாகச் செயல்படுத்தவோ, நிரல் இயக்க அனுமதிக் கொள்கையை [Execution Policy] மாற்றவோ தேவையில்லை. `py -3.12` கிடைக்கவில்லை என்றால், பைத்தான் [Python] 3.12 நிறுவப்பட்டுள்ளதா என்பதை முதலில் சரிபார்க்கவும்.

## 3. Linux அல்லது macOS முனையம் [Terminal]

```sh
python3.12 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python run_all.py
.venv/bin/python -m unittest discover -s tests -v
```

முதல் அத்தியாயத்தை மட்டும் இயக்க:

```sh
.venv/bin/python V1C01/lab.py
```

`python3.12` அல்லது மெய்நிகர் சூழல் ஆதரவு [Virtual Environment Support] இல்லாவிட்டால், உங்கள் இயக்க முறைமைக்கான [Operating System] நம்பகமான அதிகாரப்பூர்வ வழியில் நிறுவவும். `sudo pip` பயன்படுத்தவோ, கணினியின் பொதுப் பைத்தான் மொழிபெயர்ப்பியை [System Python Interpreter] மாற்றவோ வேண்டாம்.

## 4. முடிவுகளைப் படியுங்கள்

ஒவ்வொரு அத்தியாயத்தின் கணக்கீட்டு முடிவுகளும் [Results], `V1C01/results.json` முதல் `V1C13/results.json` வரையிலான கோப்புகளில் [Files] இருக்கும். அவற்றை உரைத் தொகுப்பியில் [Text Editor] திறக்கலாம். முழுச் சோதனை இயக்கத்தின் [Test Run] இறுதியில் `Ran 120 tests` மற்றும் `OK` வர வேண்டும். இயக்க நேரமும் [Runtime], கடைசி சில தசம இலக்கங்களும் கணினிக்கேற்ப மாறலாம்.

சேர்க்கப்பட்ட `test_report.txt`, உண்மையில் நடைபெற்ற Linux சோதனை இயக்கத்தின் [Test Run] பதிவாகும். அது உங்கள் கணினியில் நிறுவல் [Installation] வெற்றியடைந்ததைச் சான்றளிக்காது. Windows மற்றும் macOS கட்டளைகள் [Commands] வழங்கப்பட்டுள்ளன; அந்த இயக்க முறைமைகளில் [Operating Systems] இப்பதிப்பு சோதிக்கப்படவில்லை. புதிதாக உருவாக்கப்பட்ட சுத்தமான சூழலில் [Clean Environment] சார்புத் தொகுப்புகளை [Dependencies] நிறுவிச் சோதிக்கவும் இல்லை.

## 5. புரிந்துகொண்டு மாற்றுங்கள்

முதலில் நூலின் கணித விளக்கத்தைப் படியுங்கள். பின்னர் அத்தியாயக் குறியீட்டை [Chapter Identifier] பொருத்திப் பாருங்கள். எடுத்துக்காட்டாக, `V1C01-CASE01` என்பது முதல் அத்தியாயத்தின் முதன்மை எடுத்துக்காட்டு [Primary Case]. `V1Cxx-LAB01` என்பது கூடுதல் ஆய்வுப் பயிற்சி [Additional Experiment].

மாற்றப்படாத ஒரு நகலைப் பாதுகாக்கவும். வேறு நகலில் ஒரு அளவுருவை [Parameter] மட்டும் மாற்றி மீண்டும் இயக்கவும். வழங்கப்பட்ட அனைத்தும் செயற்கைத் தரவுகள் [Synthetic Data]. அவற்றிலிருந்து உண்மையான நிறுவனச் செயல்திறனை [Business Performance] ஊகிக்க வேண்டாம்.

ஏழாம் அத்தியாயத்தில் முறைப்படுத்தல் வலிமை [Regularization Strength], சரிபார்ப்புத் தொகுப்பை [Validation Set] வைத்துத் தேர்ந்தெடுக்கப்படுகிறது. இறுதிச் சோதனைத் தொகுப்பை [Test Set] அந்தத் தேர்வுக்குப் பயன்படுத்த வேண்டாம். எட்டாம் அத்தியாயத்தில் எதிர்காலத் தகவல் கசிவு [Temporal Leakage] வேண்டுமென்றே காட்டப்படுகிறது; அதனால் கிடைக்கும் மிக உயர்ந்த மதிப்பெண்ணைச் செல்லுபடியான மதிப்பீடாக [Valid Evaluation] கருத வேண்டாம்.

சார்புத் தொகுப்புகளின் நிறுவலுக்கு [Dependency Installation] இணைய இணைப்பு [Internet Connection] தேவை. அதற்குப் பிறகு ஆய்வுப் பயிற்சிகள் [Labs] தரவைப் பதிவிறக்கம் [Download] செய்யவோ, வெளியில் அனுப்பவோ தேவையில்லை.

## 6. விரிவாக்கப்பட்ட அத்தியாயங்கள் 9–13

`1.1.0-author-review` பதிப்பில் [Version], மொத்தம் பதின்மூன்று ஆய்வுப் பயிற்சிகள் [Labs] உள்ளன. முதல் எட்டு அத்தியாயங்களின் நிரல்களும் [Code], பழைய 55 சோதனைகளும் [Tests] மாற்றப்படவில்லை. புதிய அத்தியாயங்களுக்கு மேலும் 46 சோதனைகள் [Tests] சேர்க்கப்பட்டுள்ளன. இவற்றுடன் கீழே விளக்கப்படும் ShopSmart எடுத்துக்காட்டுகளுக்கு 19 சோதனைகள் [Tests] சேர்க்கப்பட்டு, மொத்தம் 120 சோதனைகள் [Tests] உள்ளன.

- `V1C09`: மேற்பார்வைக் கற்றல் [Supervised Learning], மேற்பார்வையற்ற கற்றல் [Unsupervised Learning], சுயமேற்பார்வைக் கற்றல் [Self-Supervised Learning], வலுவூட்டல் கற்றல் [Reinforcement Learning] ஆகியவற்றின் சிறிய கணித எடுத்துக்காட்டுகள்
- `V1C10`: நேரியல் பின்னடைவு [Linear Regression], லாஜிஸ்டிக் பின்னடைவு [Logistic Regression], ஒதுக்கிவைத்த சோதனைத் தொகுப்பு [Held-out Test Set] மற்றும் அடிப்படை ஒப்பீடு [Baseline Comparison]
- `V1C11`: எளிய பேய்ஸ் [Naive Bayes], k அருகமை அண்டைகள் [k-Nearest Neighbours], ஆதரவுத் திசையன் இயந்திரம் [Support Vector Machine], தனித் தரவில் வாய்ப்பு அளவொத்திசைவு [Probability Calibration]
- `V1C12`: முடிவு மரம் [Decision Tree], சீரற்ற காடு [Random Forest], சாய்வு வலுப்படுத்தல் [Gradient Boosting], சரிபார்ப்புத் தொகுப்பு [Validation Set] வழி மாதிரித் தேர்வு [Model Selection]
- `V1C13`: குழுவாக்கம் [Clustering], முதன்மைக் கூறுப் பகுப்பாய்வு [Principal Component Analysis], பயிற்சித் தரவில் மட்டும் மாற்றத்தைப் பொருத்துதல் [Training-only Transform Fitting]

அத்தியாயம் 14 நூலில் ஒரு குறுகிய முன்னோட்டம் மட்டுமே; அதற்குத் தனி நிரல் ஆய்வுப் பயிற்சி [Code Lab] இல்லை. நூலின் அடுத்த தொகுதியில் அத்தியாயங்கள் 15–26 இடம்பெறும். பைத்தான் மூலநிரல் [Python Source Code] அனைத்தும் நூல்களுக்கு வெளியே இந்தத் துணைத்தொகுப்பில் [Companion] இருக்கும்.

பதினொன்றாம் அத்தியாயத்தை மட்டும் இயக்க, Linux அல்லது macOS முனையத்தில் [Terminal]:

```sh
.venv/bin/python V1C11/lab.py
.venv/bin/python -m unittest discover -s tests -p test_classical_labs.py -k V1C11 -v
```

Windows PowerShell கட்டளைகள் [Commands]:

```powershell
.\.venv\Scripts\python.exe V1C11\lab.py
.\.venv\Scripts\python.exe -m unittest discover -s tests -p test_classical_labs.py -k V1C11 -v
```

பதினொன்றாம் அத்தியாயத்தில் பயிற்சித் தொகுப்பு [Training Set], அளவொத்திசைவுத் தொகுப்பு [Calibration Set], இறுதிச் சோதனைத் தொகுப்பு [Test Set] ஆகியவை தனித்தனியாக உள்ளன. ஆதரவு வெக்டர் இயந்திரத்தின் [Support Vector Machine] மதிப்பெண்ணுக்கு [Score] சாதாரண சிக்மாய்டு சார்பை [Sigmoid Function] பயன்படுத்துவது மட்டும் வாய்ப்பு அளவொத்திசைவாக [Probability Calibration] கருதப்படவில்லை; அளவொத்திசைவியின் [Calibrator] அளவுருக்கள் [Parameters] தனித் தரவிலிருந்து கற்கப்படுகின்றன.

பன்னிரண்டாம் அத்தியாயத்தில் மாதிரிக் குடும்பம் [Model Family], சரிபார்ப்புத் தொகுப்பின் [Validation Set] இழப்புச் சார்பால் [Loss] தேர்ந்தெடுக்கப்படுகிறது. இறுதிச் சோதனை முடிவை [Test Result] பார்த்து அந்தத் தேர்வு மாற்றப்படுவதில்லை. பதின்மூன்றாம் அத்தியாயத்தில் அளவுமாற்றமும் [Scaling], முதன்மைக் கூறுப் பகுப்பாய்வும் [Principal Component Analysis] பயிற்சித் தரவில் [Training Data] மட்டுமே பொருத்தப்படுகின்றன.

ShopSmart என்பது இங்கு முன்மொழியப்பட்ட நுகர்வோர் மற்றும் வணிகச் சூழல் [Proposed B2C/B2B Scenario]. இந்தச் செயற்கைத் தரவு [Synthetic Data] ஆய்வுகள் [Experiments], உண்மையில் இயங்கும் உணவுத் திட்டமிடல் [Meal Planning], ஒவ்வாமைப் பாதுகாப்பு [Allergen Safety], பல்கடைப் பொருள் கூடை [Multi-store Basket] அல்லது விநியோக ஒருங்கிணைப்பு [Delivery Integration] அமைப்பைச் சோதித்ததாகப் பொருளல்ல.

மாற்றுவதற்கு முன் கோப்புத் தொகுப்பின் முழுமையை [Package Integrity] சரிபார்க்க, உங்கள் மெய்நிகர் சூழலின் [Virtual Environment] பைத்தான் [Python] மூலம் `verify_manifest.py` இயக்கவும். திட்டமிட்ட கோப்பு மாற்றங்கள் [File Changes] அல்லது மீள்கணக்கீடுகள் [Recalculations] சரிபார்ப்புத் தொகை வேறுபாட்டை [Checksum Mismatch] ஏற்படுத்தலாம்; மாற்றப்படாத வெளியீட்டு நகலை [Release Copy] வைத்திருங்கள்.

## 7. கூடுதல் ShopSmart கணித எடுத்துக்காட்டுகள்

முழு இயக்கத்தில் [Full Run], `shopsmart_examples/basket_results.json` மற்றும் `shopsmart_examples/forecast_results.json` ஆகியவையும் உருவாகும். முதல் கோப்பு [File], அத்தியாயம் 5-இன் `V1C05-CASE02` பொருள் கூடை ஒப்பீட்டுக்கான [Basket Comparison] முடிவுகளை வழங்குகிறது. இரண்டாவது கோப்பு [File], அத்தியாயம் 10-இன் `V1C10-CASE02` விலை முன்னறிவிப்பையும் [Price Forecast], இப்போது வாங்குவதா அல்லது காத்திருப்பதா என்ற எதிர்பார்க்கப்பட்ட செலவு ஒப்பீட்டையும் [Expected-cost Comparison] காட்டுகிறது.

முதல் எடுத்துக்காட்டின் 27 ஒதுக்கீடுகளில் [Assignments], அனைத்து கட்டணங்களுடனான [Fees] மிகக் குறைந்த செயற்கைச் செலவு [Synthetic Cost] Coles மட்டும் பயன்படுத்தும் A$33 ஆகும். ஒவ்வொரு பொருளையும் தனித்தனியாக மலிவான கடையிலிருந்து எடுத்தால், ஒருங்கிணைந்த கூடை [Consolidated Basket] மொத்தம் A$35 ஆகிறது. இரண்டாவது எடுத்துக்காட்டில், கருதப்பட்ட நிலைகளின் [Assumed Scenarios] எதிர்பார்க்கப்பட்ட எதிர்காலச் செலவு [Expected Future Cost] A$29.20; அறிவிக்கப்பட்ட தாமதச் செலவு [Delay Cost] A$2 சேர்க்கப்பட்டால் A$31.20. இவை உண்மையான சலுகைகளோ [Offers], உறுதிப்படுத்தப்பட்ட சேவைகளோ [Verified Services] அல்ல.

தட்டச்சு [Typed Input], குரல் [Voice Input], பதிவேற்றப்பட்ட பட்டியல் [Uploaded List] ஆகியவற்றை ஒரே உறுதிப்படுத்தப்பட்ட பொருள் பட்டியலாக [Confirmed Structured Basket] மாற்றுவது முன்மொழியப்பட்ட வடிவமைப்பு [Proposed Design] மட்டுமே. இங்கு பேச்சுணர்தல் [Speech Recognition], ஒளியியல் எழுத்துணர்தல் [Optical Character Recognition], நேரடி விலை இணைப்பு [Live Price Integration], பொருள் வாங்குதல் [Purchasing] அல்லது விநியோக ஒருங்கிணைப்பு [Delivery Integration] செயல்படுத்தப்படவில்லை.
