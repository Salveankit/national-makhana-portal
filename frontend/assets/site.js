const NMB_LANGUAGE_KEY = "nmb_portal_language";

const translations = {
  common: {
    en: {
      utility: {
        gov: "Government of India",
        skip: "Skip to main content",
        screenReader: "Screen Reader Access",
        status: "System Status",
        login: "Secure Login",
        home: "Home",
      },
      masthead: {
        gov: "Government of India",
        title: "National Makhana Board Portal",
        department: "Department of Agriculture & Farmers Welfare",
      },
      actions: {
        login: "Service Login",
        beneficiary: "Beneficiary Services",
      },
      nav: {
        home: "Home",
        services: "Services",
        schemes: "Schemes",
        updates: "Updates",
        helpdesk: "Helpdesk",
        dashboard: "Officer Console",
        login: "Login",
      },
      footer: {
        portal: "National Makhana Board Portal",
        department: "Department of Agriculture & Farmers Welfare",
        gov: "Government of India",
        summary:
          "Integrated digital access for beneficiary registration, application services, field verification, and board review.",
        publicPages: "Public Pages",
        access: "Service Access",
        support: "Support",
        rights: "© 2026 National Makhana Board. All rights reserved.",
        updated: "Last Updated: 18 June 2026",
        ownership:
          "Content owned by the Department of Agriculture & Farmers Welfare, Government of India.",
      },
      loginPage: {
        error: "Login failed",
      },
    },
    hi: {
      utility: {
        gov: "भारत सरकार",
        skip: "मुख्य सामग्री पर जाएं",
        screenReader: "स्क्रीन रीडर सुविधा",
        status: "सिस्टम स्थिति",
        login: "सुरक्षित लॉगिन",
        home: "होम",
      },
      masthead: {
        gov: "भारत सरकार",
        title: "राष्ट्रीय मखाना बोर्ड पोर्टल",
        department: "कृषि एवं किसान कल्याण विभाग",
      },
      actions: {
        login: "सेवा लॉगिन",
        beneficiary: "लाभार्थी सेवाएं",
      },
      nav: {
        home: "होम",
        services: "सेवाएं",
        schemes: "योजनाएं",
        updates: "अपडेट",
        helpdesk: "सहायता केंद्र",
        dashboard: "अधिकारी कंसोल",
        login: "लॉगिन",
      },
      footer: {
        portal: "राष्ट्रीय मखाना बोर्ड पोर्टल",
        department: "कृषि एवं किसान कल्याण विभाग",
        gov: "भारत सरकार",
        summary:
          "लाभार्थी पंजीकरण, आवेदन सेवाओं, फील्ड सत्यापन और बोर्ड समीक्षा के लिए एकीकृत डिजिटल पहुंच।",
        publicPages: "सार्वजनिक पृष्ठ",
        access: "सेवा पहुंच",
        support: "सहायता",
        rights: "© 2026 राष्ट्रीय मखाना बोर्ड। सर्वाधिकार सुरक्षित।",
        updated: "अंतिम अद्यतन: 18 जून 2026",
        ownership: "सामग्री का स्वामित्व कृषि एवं किसान कल्याण विभाग, भारत सरकार के पास है।",
      },
      loginPage: {
        error: "लॉगिन असफल रहा",
      },
    },
  },
  home: {
    en: {
      metaTitle: "National Makhana Board Portal",
      badge: "National Agriculture Service Platform",
      notice:
        "Official portal for beneficiary services, field verification, state review, approval monitoring, and scheme administration for the makhana sector.",
      heroEyebrow: "National Makhana Board Digital Services",
      heroTitle:
        "Single-window access for registration, application tracking, field verification, and board-level review.",
      heroBody:
        "Access beneficiary services, service updates, scheme information, and secure officer workflows through one formal portal.",
      heroLogin: "Open Secure Login",
      heroBeneficiary: "Open Beneficiary Workspace",
      statOneTitle: "10 States",
      statOneBody: "States covered under the board programme",
      statTwoTitle: "Single Window",
      statTwoBody: "Farmer registration, application, and status tracking",
      statThreeTitle: "Multi-Level Workflow",
      statThreeBody: "State review, inspection, and board approval",
      serviceHeading: "Service Areas",
      cardOneTitle: "Beneficiary Services",
      cardOneBody:
        "Farmer registration, identity verification, application submission, and status visibility.",
      cardTwoTitle: "Officer Operations",
      cardTwoBody:
        "Application review, clarification handling, inspection assignment, recommendation, and approval.",
      cardThreeTitle: "Planning and Monitoring",
      cardThreeBody:
        "Annual Action Plans, budget visibility, district updates, and national monitoring support.",
      cardFourTitle: "Inspection Support",
      cardFourBody:
        "Field verification, geotagged site reporting, and inspection-based validation.",
      supportBody:
        "Guidance for registration, login, application tracking, and public service access is available through the helpdesk.",
      supportAction: "Open Helpdesk",
    },
    hi: {
      metaTitle: "राष्ट्रीय मखाना बोर्ड पोर्टल",
      badge: "राष्ट्रीय कृषि सेवा मंच",
      notice:
        "मखाना क्षेत्र के लिए लाभार्थी सेवाओं, फील्ड सत्यापन, राज्य समीक्षा, स्वीकृति निगरानी और योजना प्रशासन का आधिकारिक पोर्टल।",
      heroEyebrow: "राष्ट्रीय मखाना बोर्ड डिजिटल सेवाएं",
      heroTitle:
        "पंजीकरण, आवेदन ट्रैकिंग, फील्ड सत्यापन और बोर्ड स्तर की समीक्षा के लिए सिंगल-विंडो पहुंच।",
      heroBody:
        "एक औपचारिक पोर्टल के माध्यम से लाभार्थी सेवाएं, सेवा अपडेट, योजना जानकारी और सुरक्षित अधिकारी कार्यप्रवाह प्राप्त करें।",
      heroLogin: "सुरक्षित लॉगिन खोलें",
      heroBeneficiary: "लाभार्थी कार्यक्षेत्र खोलें",
      statOneTitle: "10 राज्य",
      statOneBody: "बोर्ड कार्यक्रम के अंतर्गत कवर किए गए राज्य",
      statTwoTitle: "सिंगल विंडो",
      statTwoBody: "किसान पंजीकरण, आवेदन और स्थिति ट्रैकिंग",
      statThreeTitle: "बहु-स्तरीय कार्यप्रवाह",
      statThreeBody: "राज्य समीक्षा, निरीक्षण और बोर्ड स्वीकृति",
      serviceHeading: "सेवा क्षेत्र",
      cardOneTitle: "लाभार्थी सेवाएं",
      cardOneBody:
        "किसान पंजीकरण, पहचान सत्यापन, आवेदन जमा करना और स्थिति की दृश्यता।",
      cardTwoTitle: "अधिकारी संचालन",
      cardTwoBody:
        "आवेदन समीक्षा, स्पष्टीकरण प्रबंधन, निरीक्षण आवंटन, अनुशंसा और स्वीकृति।",
      cardThreeTitle: "योजना एवं निगरानी",
      cardThreeBody:
        "वार्षिक कार्ययोजना, बजट दृश्यता, जिला अपडेट और राष्ट्रीय निगरानी समर्थन।",
      cardFourTitle: "निरीक्षण सहायता",
      cardFourBody:
        "फील्ड सत्यापन, जियोटैग्ड साइट रिपोर्टिंग और निरीक्षण-आधारित वैधीकरण।",
      supportBody:
        "पंजीकरण, लॉगिन, आवेदन ट्रैकिंग और सार्वजनिक सेवा पहुंच के लिए मार्गदर्शन सहायता केंद्र के माध्यम से उपलब्ध है।",
      supportAction: "सहायता केंद्र खोलें",
    },
  },
  login: {
    en: {
      metaTitle: "NMB Service Login",
      badge: "Protected Service Gateway",
      loginNoticeTitle: "Secure entry for beneficiaries and officers",
      loginNoticeBody:
        "Login is available here as the primary service entry point for beneficiary services, inspection workflows, and officer actions.",
      loginNoticeAction: "Go to Login Form",
      loginEyebrow: "Government Service Gateway",
      loginTitle: "Login to NMB Digital Services",
      loginHint:
        "Use authorized credentials to access beneficiary, inspection, state workflow, or board-level operational services.",
      roleOneTitle: "NMB Admin",
      roleOneBody: "National visibility, audit logs, and final decision actions.",
      roleTwoTitle: "State Officer",
      roleTwoBody: "Application review, clarifications, inspections, and recommendations.",
      roleThreeTitle: "Inspector",
      roleThreeBody: "Inspection completion with geo-tagged field verification.",
      roleFourTitle: "Beneficiary",
      roleFourBody: "Profile management, application filing, and status tracking.",
      authEyebrow: "Authentication",
      signIn: "Sign in",
      email: "Email",
      password: "Password",
      submit: "Continue to Services",
      demoUsers:
        "Demo users: `nmb.admin@example.com`, `bihar.officer@example.com`, `inspector@example.com`, `farmer@example.com`.",
      footer:
        "Secure access point for National Makhana Board beneficiary services and officer operations.",
    },
    hi: {
      metaTitle: "एनएमबी सेवा लॉगिन",
      badge: "सुरक्षित सेवा प्रवेश द्वार",
      loginNoticeTitle: "लाभार्थियों और अधिकारियों के लिए सुरक्षित प्रवेश",
      loginNoticeBody:
        "लाभार्थी सेवाओं, निरीक्षण कार्यप्रवाह और अधिकारी कार्यों के लिए लॉगिन यहां प्राथमिक सेवा प्रवेश बिंदु के रूप में उपलब्ध है।",
      loginNoticeAction: "लॉगिन फॉर्म पर जाएं",
      loginEyebrow: "सरकारी सेवा प्रवेश द्वार",
      loginTitle: "एनएमबी डिजिटल सेवाओं में लॉगिन करें",
      loginHint:
        "लाभार्थी, निरीक्षण, राज्य कार्यप्रवाह या बोर्ड स्तर की परिचालन सेवाओं तक पहुंच के लिए अधिकृत क्रेडेंशियल का उपयोग करें।",
      roleOneTitle: "एनएमबी प्रशासक",
      roleOneBody: "राष्ट्रीय दृश्यता, ऑडिट लॉग और अंतिम निर्णय कार्रवाई।",
      roleTwoTitle: "राज्य अधिकारी",
      roleTwoBody: "आवेदन समीक्षा, स्पष्टीकरण, निरीक्षण और अनुशंसाएं।",
      roleThreeTitle: "निरीक्षक",
      roleThreeBody: "जियोटैग्ड फील्ड सत्यापन के साथ निरीक्षण पूर्ण करना।",
      roleFourTitle: "लाभार्थी",
      roleFourBody: "प्रोफाइल प्रबंधन, आवेदन दाखिल करना और स्थिति ट्रैकिंग।",
      authEyebrow: "प्रमाणीकरण",
      signIn: "साइन इन करें",
      email: "ईमेल",
      password: "पासवर्ड",
      submit: "सेवाओं पर आगे बढ़ें",
      demoUsers:
        "डेमो उपयोगकर्ता: `nmb.admin@example.com`, `bihar.officer@example.com`, `inspector@example.com`, `farmer@example.com`.",
      footer: "राष्ट्रीय मखाना बोर्ड की लाभार्थी सेवाओं और अधिकारी संचालन के लिए सुरक्षित प्रवेश बिंदु।",
    },
  },
  services: {
    en: {
      metaTitle: "NMB Services",
      badge: "Public Service Directory",
      notice:
        "Service modules are organized for beneficiaries, state implementing agencies, inspection teams, and board administrators.",
      heading: "Digital Service Catalogue",
      lead: "Service areas are arranged to help users find the right function quickly.",
      serviceOneTag: "Citizen Service",
      serviceOneTitle: "Beneficiary Registration",
      serviceOneBody:
        "Farmer profile creation with location hierarchy, cultivation details, and identity-linked service access.",
      serviceOneAction: "Open Workspace",
      serviceTwoTag: "Citizen Service",
      serviceTwoTitle: "Application Submission",
      serviceTwoBody:
        "Scheme support application with document metadata, geotag inputs, and acknowledgement-based filing.",
      serviceThreeTag: "Citizen Service",
      serviceThreeTitle: "Status Tracking",
      serviceThreeBody:
        "Beneficiaries can view stage progression, clarifications, inspections, and final decision visibility.",
      serviceFourTag: "State Operations",
      serviceFourTitle: "Review and Recommendation",
      serviceFourBody:
        "State officers process applications, raise clarifications, assign field visits, and recommend eligible cases.",
      serviceFiveTag: "Inspection",
      serviceFiveTitle: "Field Verification",
      serviceFiveBody:
        "Inspectors complete on-ground verification with site details, coordinates, photographs, and remarks.",
      serviceSixTag: "Board Operations",
      serviceSixTitle: "Approval and Monitoring",
      serviceSixBody:
        "National-level users review recommendations, approve or return applications, and monitor implementation progress.",
      groupsHeading: "User Groups and Access Pathways",
      groupsLead:
        "Services are grouped according to the needs of beneficiaries, inspectors, officers, and administrators.",
      groupOneTitle: "Beneficiaries",
      groupOneBody:
        "Profile management, identity verification, application submission, and application status tracking.",
      groupTwoTitle: "State Officers",
      groupTwoBody:
        "Scrutiny, query management, inspection assignment, recommendation, and state-level progress review.",
      groupThreeTitle: "Inspectors",
      groupThreeBody:
        "Field verification closure, geotagging, observations, and supporting photo-record capture.",
      groupFourTitle: "NMB Administrators",
      groupFourBody:
        "Final approval, planning oversight, utilization visibility, service readiness review, and monitoring access.",
      supportBody:
        "Use the services directory to identify the correct service path for beneficiaries, inspection teams, and officers.",
      supportAction: "Open Helpdesk",
    },
    hi: {
      metaTitle: "एनएमबी सेवाएं",
      badge: "सार्वजनिक सेवा निर्देशिका",
      notice:
        "सेवा मॉड्यूल लाभार्थियों, राज्य कार्यान्वयन एजेंसियों, निरीक्षण टीमों और बोर्ड प्रशासकों के लिए व्यवस्थित किए गए हैं।",
      heading: "डिजिटल सेवा कैटलॉग",
      lead: "सेवा क्षेत्रों को इस प्रकार व्यवस्थित किया गया है कि उपयोगकर्ता सही कार्य को शीघ्रता से खोज सकें।",
      serviceOneTag: "नागरिक सेवा",
      serviceOneTitle: "लाभार्थी पंजीकरण",
      serviceOneBody:
        "स्थान पदानुक्रम, खेती विवरण और पहचान-आधारित सेवा पहुंच के साथ किसान प्रोफाइल निर्माण।",
      serviceOneAction: "कार्यस्थान खोलें",
      serviceTwoTag: "नागरिक सेवा",
      serviceTwoTitle: "आवेदन जमा करना",
      serviceTwoBody:
        "दस्तावेज़ मेटाडेटा, जियोटैग इनपुट और स्वीकृति-आधारित दाखिले के साथ योजना सहायता आवेदन।",
      serviceThreeTag: "नागरिक सेवा",
      serviceThreeTitle: "स्थिति ट्रैकिंग",
      serviceThreeBody:
        "लाभार्थी चरण प्रगति, स्पष्टीकरण, निरीक्षण और अंतिम निर्णय की स्थिति देख सकते हैं।",
      serviceFourTag: "राज्य संचालन",
      serviceFourTitle: "समीक्षा और अनुशंसा",
      serviceFourBody:
        "राज्य अधिकारी आवेदन संसाधित करते हैं, स्पष्टीकरण उठाते हैं, फील्ड विजिट सौंपते हैं और पात्र मामलों की अनुशंसा करते हैं।",
      serviceFiveTag: "निरीक्षण",
      serviceFiveTitle: "फील्ड सत्यापन",
      serviceFiveBody:
        "निरीक्षक स्थल विवरण, निर्देशांक, फोटो और टिप्पणियों के साथ जमीनी सत्यापन पूरा करते हैं।",
      serviceSixTag: "बोर्ड संचालन",
      serviceSixTitle: "स्वीकृति और निगरानी",
      serviceSixBody:
        "राष्ट्रीय स्तर के उपयोगकर्ता अनुशंसाओं की समीक्षा करते हैं, आवेदनों को स्वीकृत या वापस करते हैं और कार्यान्वयन प्रगति की निगरानी करते हैं।",
      groupsHeading: "उपयोगकर्ता समूह और पहुंच मार्ग",
      groupsLead:
        "सेवाओं को लाभार्थियों, निरीक्षकों, अधिकारियों और प्रशासकों की आवश्यकताओं के अनुसार समूहित किया गया है।",
      groupOneTitle: "लाभार्थी",
      groupOneBody:
        "प्रोफाइल प्रबंधन, पहचान सत्यापन, आवेदन जमा करना और आवेदन स्थिति ट्रैकिंग।",
      groupTwoTitle: "राज्य अधिकारी",
      groupTwoBody:
        "समीक्षा, प्रश्न प्रबंधन, निरीक्षण आवंटन, अनुशंसा और राज्य स्तरीय प्रगति समीक्षा।",
      groupThreeTitle: "निरीक्षक",
      groupThreeBody:
        "फील्ड सत्यापन समापन, जियोटैगिंग, अवलोकन और सहायक फोटो रिकॉर्ड कैप्चर।",
      groupFourTitle: "एनएमबी प्रशासक",
      groupFourBody:
        "अंतिम स्वीकृति, योजना पर्यवेक्षण, उपयोग दृश्यता, सेवा तत्परता समीक्षा और निगरानी पहुंच।",
      supportBody:
        "लाभार्थियों, निरीक्षण टीमों और अधिकारियों के लिए सही सेवा मार्ग पहचानने हेतु सेवाओं की निर्देशिका का उपयोग करें।",
      supportAction: "सहायता केंद्र खोलें",
    },
  },
  schemes: {
    en: {
      metaTitle: "NMB Schemes and Support Areas",
      badge: "Scheme Overview",
      notice:
        "Support areas shown below reflect the major areas of assistance covered by the portal.",
      heading: "Priority Support Areas",
      lead:
        "These categories help users understand how cultivation, processing, verification, and planning support can be administered.",
      cardOneTitle: "Makhana Cultivation Support",
      cardOneBody:
        "Coverage for cultivation expansion, farmer targeting, pond and field-based activity support, and production-linked assistance.",
      cardTwoTitle: "Nursery and Input Support",
      cardTwoBody:
        "Input readiness, cluster support, and local enabling measures required for productive cultivation cycles.",
      cardThreeTitle: "Processing and Value Addition",
      cardThreeBody:
        "Post-harvest handling, grading, drying, storage, and local infrastructure needed for value realization.",
      cardFourTitle: "Training and Extension",
      cardFourBody:
        "Capacity building for farmers, field-level guidance, and awareness support across implementing regions.",
      cardFiveTitle: "Inspection and Verification",
      cardFiveBody:
        "Structured verification checks to support transparent review, geotagged field visits, and decision confidence.",
      cardSixTitle: "State Planning and Monitoring",
      cardSixBody:
        "Annual Action Plans, district-level target tracking, and utilization visibility for implementation review.",
      supportBody:
        "Scheme information pages provide an overview of intervention areas, while service submission continues through secure portal access.",
      supportAction: "View Services",
    },
    hi: {
      metaTitle: "एनएमबी योजनाएं और सहायता क्षेत्र",
      badge: "योजना अवलोकन",
      notice:
        "नीचे दर्शाए गए सहायता क्षेत्र पोर्टल द्वारा कवर किए गए प्रमुख सहायता क्षेत्रों को दर्शाते हैं।",
      heading: "प्राथमिक सहायता क्षेत्र",
      lead:
        "ये श्रेणियां उपयोगकर्ताओं को समझने में मदद करती हैं कि खेती, प्रसंस्करण, सत्यापन और योजना समर्थन का प्रशासन कैसे किया जा सकता है।",
      cardOneTitle: "मखाना खेती सहायता",
      cardOneBody:
        "खेती विस्तार, किसान लक्ष्यीकरण, तालाब और खेत-आधारित गतिविधि समर्थन तथा उत्पादन-आधारित सहायता के लिए कवरेज।",
      cardTwoTitle: "नर्सरी और इनपुट सहायता",
      cardTwoBody:
        "उत्पादक खेती चक्रों के लिए आवश्यक इनपुट तत्परता, क्लस्टर समर्थन और स्थानीय सक्षम उपाय।",
      cardThreeTitle: "प्रसंस्करण और मूल्य संवर्धन",
      cardThreeBody:
        "फसल कटाई के बाद प्रबंधन, ग्रेडिंग, सुखाना, भंडारण और मूल्य प्राप्ति के लिए आवश्यक स्थानीय अवसंरचना।",
      cardFourTitle: "प्रशिक्षण और विस्तार",
      cardFourBody:
        "किसानों के लिए क्षमता निर्माण, फील्ड-स्तरीय मार्गदर्शन और कार्यान्वयन क्षेत्रों में जागरूकता समर्थन।",
      cardFiveTitle: "निरीक्षण और सत्यापन",
      cardFiveBody:
        "पारदर्शी समीक्षा, जियोटैग्ड फील्ड विजिट और निर्णय विश्वास को समर्थन देने के लिए संरचित सत्यापन जांच।",
      cardSixTitle: "राज्य योजना और निगरानी",
      cardSixBody:
        "कार्यान्वयन समीक्षा के लिए वार्षिक कार्ययोजना, जिला-स्तरीय लक्ष्य ट्रैकिंग और उपयोग दृश्यता।",
      supportBody:
        "योजना जानकारी पृष्ठ हस्तक्षेप क्षेत्रों का अवलोकन प्रदान करते हैं, जबकि सेवा जमा करना सुरक्षित पोर्टल पहुंच के माध्यम से जारी रहता है।",
      supportAction: "सेवाएं देखें",
    },
  },
  updates: {
    en: {
      metaTitle: "NMB Updates and Circulars",
      badge: "Public Notices",
      notice:
        "This page is intended for circulars, advisories, system notices, and service-related announcements.",
      heading: "Latest Notices",
      lead:
        "Illustrative notice blocks are presented in a formal structure that can later be linked to actual notifications and circular records.",
      noticeOne:
        "Beneficiary services are available for registration, application submission, and workflow status visibility through the portal.",
      noticeTwo:
        "State review, inspection assignment, recommendation handling, and approval review are supported in the officer console.",
      noticeThree:
        "Annual Action Plan submission, budget visibility, field reporting, and monitoring support are available through the portal.",
      noticeFour:
        "Notification services, identity verification, and benefit-transfer readiness are included within the portal scope.",
      supportBody:
        "Updates, notices, and circulars should be read with the related service instructions available through the portal helpdesk.",
      supportAction: "Open Helpdesk",
    },
    hi: {
      metaTitle: "एनएमबी अपडेट और परिपत्र",
      badge: "सार्वजनिक सूचनाएं",
      notice:
        "यह पृष्ठ परिपत्र, परामर्श, सिस्टम सूचनाएं और सेवा-संबंधी घोषणाओं के लिए है।",
      heading: "नवीनतम सूचनाएं",
      lead:
        "उदाहरणात्मक सूचना ब्लॉक औपचारिक संरचना में प्रस्तुत किए गए हैं जिन्हें बाद में वास्तविक अधिसूचनाओं और परिपत्र अभिलेखों से जोड़ा जा सकता है।",
      noticeOne:
        "लाभार्थी सेवाएं पंजीकरण, आवेदन जमा करने और पोर्टल के माध्यम से कार्यप्रवाह स्थिति दृश्यता के लिए उपलब्ध हैं।",
      noticeTwo:
        "राज्य समीक्षा, निरीक्षण आवंटन, अनुशंसा प्रबंधन और स्वीकृति समीक्षा अधिकारी कंसोल में समर्थित हैं।",
      noticeThree:
        "वार्षिक कार्ययोजना जमा करना, बजट दृश्यता, फील्ड रिपोर्टिंग और निगरानी समर्थन पोर्टल के माध्यम से उपलब्ध हैं।",
      noticeFour:
        "अधिसूचना सेवाएं, पहचान सत्यापन और लाभ अंतरण तत्परता पोर्टल के दायरे में शामिल हैं।",
      supportBody:
        "अपडेट, सूचनाएं और परिपत्रों को पोर्टल सहायता केंद्र में उपलब्ध संबंधित सेवा निर्देशों के साथ पढ़ा जाना चाहिए।",
      supportAction: "सहायता केंद्र खोलें",
    },
  },
  helpdesk: {
    en: {
      metaTitle: "NMB Helpdesk",
      badge: "User Assistance",
      notice:
        "Use the helpdesk section to find the correct service page, secure login, or officer access point.",
      heading: "Quick Assistance",
      lead:
        "Support guidance is grouped by user need so that public users do not need to interpret internal process terminology.",
      cardOneTitle: "Registration Support",
      cardOneBody:
        "Use the beneficiary workspace to create or update a farmer profile and maintain service eligibility details.",
      cardOneAction: "Open Beneficiary Workspace",
      cardTwoTitle: "Application Status Support",
      cardTwoBody:
        "Beneficiaries can track current application stage, clarifications, field verification, and decision progress after login.",
      cardThreeTitle: "Officer Access Support",
      cardThreeBody:
        "Authorized officers can move to the monitoring console for review, planning, budget tracking, and approvals.",
      cardThreeAction: "Open Officer Console",
      cardFourTitle: "Login Assistance",
      cardFourBody:
        "Use the secure login page to access services for beneficiaries, state officers, inspectors, and administrators.",
      cardFourAction: "Open Secure Login",
      supportBody:
        "Choose Beneficiary Services, Secure Login, or Officer Console according to your role and the service you need to access.",
      supportAction: "Open Secure Login",
    },
    hi: {
      metaTitle: "एनएमबी सहायता केंद्र",
      badge: "उपयोगकर्ता सहायता",
      notice:
        "सही सेवा पृष्ठ, सुरक्षित लॉगिन या अधिकारी पहुंच बिंदु खोजने के लिए सहायता केंद्र अनुभाग का उपयोग करें।",
      heading: "त्वरित सहायता",
      lead:
        "सहायता मार्गदर्शन को उपयोगकर्ता की आवश्यकता के अनुसार समूहित किया गया है ताकि सार्वजनिक उपयोगकर्ताओं को आंतरिक प्रक्रिया शब्दावली समझने की आवश्यकता न हो।",
      cardOneTitle: "पंजीकरण सहायता",
      cardOneBody:
        "किसान प्रोफाइल बनाने या अद्यतन करने और सेवा पात्रता विवरण बनाए रखने के लिए लाभार्थी कार्यक्षेत्र का उपयोग करें।",
      cardOneAction: "लाभार्थी कार्यक्षेत्र खोलें",
      cardTwoTitle: "आवेदन स्थिति सहायता",
      cardTwoBody:
        "लाभार्थी लॉगिन के बाद वर्तमान आवेदन चरण, स्पष्टीकरण, फील्ड सत्यापन और निर्णय प्रगति को ट्रैक कर सकते हैं।",
      cardThreeTitle: "अधिकारी पहुंच सहायता",
      cardThreeBody:
        "अधिकृत अधिकारी समीक्षा, योजना, बजट ट्रैकिंग और स्वीकृतियों के लिए मॉनिटरिंग कंसोल पर जा सकते हैं।",
      cardThreeAction: "अधिकारी कंसोल खोलें",
      cardFourTitle: "लॉगिन सहायता",
      cardFourBody:
        "लाभार्थियों, राज्य अधिकारियों, निरीक्षकों और प्रशासकों के लिए सेवाओं तक पहुंच हेतु सुरक्षित लॉगिन पृष्ठ का उपयोग करें।",
      cardFourAction: "सुरक्षित लॉगिन खोलें",
      supportBody:
        "अपनी भूमिका और आवश्यक सेवा के अनुसार लाभार्थी सेवाएं, सुरक्षित लॉगिन या अधिकारी कंसोल चुनें।",
      supportAction: "सुरक्षित लॉगिन खोलें",
    },
  },
};

function getPageTranslations(language) {
  const page = document.body.dataset.page || "";
  return {
    ...translations.common[language],
    ...(translations[page]?.[language] || {}),
  };
}

function resolveTranslation(language, key) {
  const source = getPageTranslations(language);
  return key.split(".").reduce((value, segment) => value?.[segment], source);
}

function updateLanguageButtons(language) {
  document.querySelectorAll("[data-lang-switch]").forEach((button) => {
    const isActive = button.dataset.langSwitch === language;
    button.setAttribute("aria-pressed", String(isActive));
  });
}

function applyTranslations(language) {
  const page = translations[document.body.dataset.page]?.[language];
  if (page?.metaTitle) {
    document.title = page.metaTitle;
  }
  document.documentElement.lang = language === "hi" ? "hi" : "en";
  document.body.classList.toggle("lang-hi", language === "hi");
  document.querySelectorAll("[data-i18n]").forEach((node) => {
    const text = resolveTranslation(language, node.dataset.i18n);
    if (typeof text === "string") {
      node.textContent = text;
    }
  });
  updateLanguageButtons(language);
  window.dispatchEvent(new CustomEvent("nmb:languagechange", { detail: { language } }));
}

function setLanguage(language) {
  const nextLanguage = language === "hi" ? "hi" : "en";
  localStorage.setItem(NMB_LANGUAGE_KEY, nextLanguage);
  applyTranslations(nextLanguage);
}

function getLanguage() {
  return localStorage.getItem(NMB_LANGUAGE_KEY) === "hi" ? "hi" : "en";
}

function initLanguageControls() {
  document.querySelectorAll("[data-lang-switch]").forEach((button) => {
    button.addEventListener("click", () => setLanguage(button.dataset.langSwitch));
  });
  applyTranslations(getLanguage());
}

window.NMBI18n = {
  getLanguage,
  setLanguage,
  translate: (key) => resolveTranslation(getLanguage(), key),
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initLanguageControls, { once: true });
} else {
  initLanguageControls();
}
