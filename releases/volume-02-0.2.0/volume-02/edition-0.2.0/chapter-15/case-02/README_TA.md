# V2C15-CASE02: தழுவும் உகப்பாக்கி [Adaptive optimiser] கணக்கீடு

இந்த வழக்கு ஒரே வழங்கப்பட்ட சாய்வுகளை [Supplied gradients] 2, பின்னர் −1 என AdaGrad, மையப்படுத்தப்படாத RMSProp [Uncentred RMSProp], Adam ஆகியவற்றிற்கு வழங்குகிறது. மூன்று வலைகளைப் [Networks] பயிற்றுவிப்பதோ செயல்திறன் வெற்றியாளரை [Performance winner] நிறுவுவதோ இல்லை. எல்லா முறைகளிலும் தொடக்க அளவுரு [Initial parameter] 0, குவிப்பிகள் [Accumulators] 0, கற்றல் வீதம் [Learning rate] 0.1, எப்சிலான் [Epsilon] 1e-8. RMSProp-இல் beta2=0.9; Adam-இல் beta1=beta2=0.9. இவை தெளிவான கணக்கீட்டிற்கான மதிப்புகள்; பரிந்துரைக்கப்படும் இயல்புநிலைகள் [Defaults] அல்ல.

எல்லாப் பகுதிகளிலும் [Denominators] வர்க்கமூலத்திற்குப் [Square root] பிறகே எப்சிலான் [Epsilon] சேர்க்கப்படுகிறது. AdaGrad எல்லாச் சாய்வு வர்க்கங்களையும் [Squared gradients] குவிக்கிறது. RMSProp அடுக்கியல் எடையிட்ட சராசரியை [Exponentially weighted average] பயன்படுத்துகிறது; மையப்படுத்தல் [Centring], உந்தம் [Momentum], சார்புத் திருத்தம் [Bias correction] இல்லை. Adam குறியுள்ள மற்றும் வர்க்க நகரும் சராசரிகளை [Moving averages] இணைத்து 1−beta1^t, 1−beta2^t ஆகியவற்றால் வகுக்கிறது. எடைத் தேய்வு [Weight decay], சாய்வு வெட்டுதல் [Gradient clipping], அட்டவணை [Schedule], AMSGrad, AdamW இல்லை.

இரண்டாம் அளவுரு மதிப்புகள் [Parameter values]: AdaGrad −0.05527864015000421; RMSProp −0.16878580703585389; Adam −0.1270604029857565. சாய்வு [Gradient] எதிர்மறையான பின்னரும் Adam-இன் குறியுள்ள முதல் திருப்புத்திறன் [Signed first moment] நேர்மறையாக இருப்பதால் எதிர்மறைத் திசையில் நகர்கிறது. சிறிய அளவுரு [Parameter] சிறந்த முடிவு எனக் கருதாமல், இடைநிலைப் பகுதிகளையும் [Intermediate denominators] குறியுள்ள மாற்றங்களையும் பாருங்கள்.

எப்சிலானை [Epsilon] 0.25-ஆக மாற்றி அதன் இடத்தைக் கையால் சரிபாருங்கள்; இரண்டாம் சாய்வை [Gradient] பூஜ்ஜியமாக மாற்றி நினைவில் உள்ள உந்தத்தை [Momentum] பாருங்கள். புதிய அலகுச் சோதனைகள் [Unit tests] தனியான அளவிச் சூத்திரங்களால் [Scalar formulas] விடைகளை வருவிக்கின்றன. தனி ஆய்வாளர் சோதனைகள் [Reviewer tests] 60 இலக்க Decimal கணக்கீட்டையும் பலவகைச் சாய்வு வரிசையையும் [Mixed-gradient sweep] பயன்படுத்துகின்றன. பூஜ்ஜிய/முடிவுறாத கட்டுப்பாடுகள் [Nonfinite controls], செல்லாத தேய்வுக் காரணிகள் [Decay factors], பூஜ்ஜியச் சாய்வுகள் [Zero gradients] சோதிக்கப்படுகின்றன.

செயலாக்கம் [Implementation] src/volume2_companion/chapter15_optimizers.py-இல் உள்ளது. இது முடிவுறும் அளவிச் சாய்வு வரிசையை [Finite scalar-gradient sequence] ஏற்று, ஒவ்வொரு அழைப்பிலும் புதிய தடத்தை [Trace] தொடங்குகிறது. இது திசையன் உகப்பாக்கிப் பொருள் [Vector optimiser object], சேமிப்புநிலை அமைப்பு [Checkpoint system], தானியக்க வகையிடல் பயிற்சிச் சுற்று [Automatic-differentiation training loop] அல்ல. உண்மையான உகப்பாக்கம் [Optimisation] ஒவ்வொரு முறையின் தற்போதைய அளவுருக்களில் [Parameters] சாய்வுகளை [Gradients] மீண்டும் கணக்கிடுவதால், பிந்தைய சாய்வுகள் [Gradients] எல்லா முறைகளுக்கும் ஒரேபோல் இருக்க வேண்டியதில்லை.

இணைப்புத் தொகுப்பு மூலக் கோப்புறையிலிருந்து [Companion root]:

    python run_cases.py --chapter 15 --case 2 --verify

அல்லது எந்தக் கோப்புறையிலிருந்தும் [Folder] இவ்வழக்கின் run.py-ஐ இயக்கலாம். மாற்றத்திற்கு முன் fixture.json-ஐப் பாதுகாக்கவும். expected.json இயக்கப்பட்ட வெளியீட்டைப் [Executed output] பதிவு செய்கிறது; அதை மாற்றுவது தனியான சரிபார்ப்பு [Independent verification] அல்ல. இணையம் [Network], பதிவிறக்கங்கள் [Downloads], அணுகல் சாவிகள் [API keys], சான்றுகள் [Credentials] பயன்படுத்தப்படுவதில்லை.
