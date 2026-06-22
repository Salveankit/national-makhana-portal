const NMB_LANGUAGE_KEY = "nmb_portal_language";
const NMB_FONT_SCALE_KEY = "nmb_portal_font_scale";
const NMB_CONTRAST_KEY = "nmb_portal_high_contrast";
const CHATBOT_PAGE_SET = new Set(["home", "services", "schemes", "updates", "helpdesk", "login", "beneficiary", "dashboard"]);
const CHATBOT_LOGO_PATH = "/assets/images/chatbot-agent-logo-v2.png";

const translations = {
  common: {
    en: {
      utility: {
        bharat: "भारत सरकार",
        gov: "Government of India",
        ministryShort: "Ministry of Agriculture & Farmers Welfare",
        skip: "Skip to main content",
        screenReader: "Screen Reader Access",
        contrast: "Contrast",
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
        makhana: "Makhana in India",
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
        contact: "Get in Touch",
        address: "Krishi Bhawan, Dr. Rajendra Prasad Road, New Delhi - 110001",
        visitors: "Visitors Count",
        rights: "© 2026 National Makhana Board. All rights reserved.",
        updated: "Last Updated: 20 June 2026",
        ownership:
          "Content owned by the Department of Agriculture & Farmers Welfare, Government of India.",
      },
      loginPage: {
        error: "Login failed",
      },
    },
    hi: {
      utility: {
        bharat: "भारत सरकार",
        gov: "भारत सरकार",
        ministryShort: "कृषि एवं किसान कल्याण मंत्रालय",
        skip: "मुख्य सामग्री पर जाएं",
        screenReader: "स्क्रीन रीडर सुविधा",
        contrast: "कॉन्ट्रास्ट",
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
        makhana: "भारत में मखाना",
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
        contact: "संपर्क करें",
        address: "कृषि भवन, डॉ. राजेन्द्र प्रसाद रोड, नई दिल्ली - 110001",
        visitors: "आगंतुक संख्या",
        rights: "© 2026 राष्ट्रीय मखाना बोर्ड। सर्वाधिकार सुरक्षित।",
        updated: "अंतिम अद्यतन: 20 जून 2026",
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
      searchLabel: "Search portal services",
      searchPlaceholder: "Search here...",
      directoryAction: "Service Directory",
      notice:
        "Official portal for beneficiary services, field verification, state review, approval monitoring, and scheme administration for the makhana sector.",
      heroEyebrow: "National Makhana Board Digital Services",
      heroTitle: "National Makhana Board",
      heroBody:
        "Single-window public access for registration, scheme information, application tracking, field verification, and board-level review.",
      heroLogin: "Secure Officer Login",
      heroBeneficiary: "Open Beneficiary Services",
      heroTagOne: "Beneficiary filing",
      heroTagTwo: "Field verification",
      heroTagThree: "Board monitoring",
      statsHeading: "Programme service summary",
      statOneTitle: "10 States",
      statOneBody: "States covered under the board programme",
      statTwoTitle: "Single Window",
      statTwoBody: "Farmer registration, application, and status tracking",
      statThreeTitle: "Multi-Level Workflow",
      statThreeBody: "State review, inspection, and board approval",
      statFourTitle: "Role-Based Access",
      statFourBody: "Public services and secured officer operations",
      serviceKicker: "Service Entry Points",
      serviceHeading: "Access core services without searching through the portal.",
      serviceLead:
        "Use the correct route for public filing, scheme guidance, secure officer work, and implementation monitoring.",
      cardOneTitle: "Beneficiary Services",
      cardOneBody:
        "Farmer registration, identity verification, application submission, and status visibility.",
      cardOneAction: "Open services",
      cardTwoTitle: "Scheme Information",
      cardTwoBody:
        "Eligibility guidance, scheme components, support categories, and public information.",
      cardTwoAction: "View schemes",
      cardThreeTitle: "Officer Operations",
      cardThreeBody:
        "Review, clarification, inspection assignment, recommendation, and approval workflows.",
      cardThreeAction: "Go to login",
      cardFourTitle: "Planning and Monitoring",
      cardFourBody:
        "Annual Action Plans, budget visibility, district updates, and national monitoring support.",
      cardFourAction: "Open console",
      updatesKicker: "Latest Information",
      updatesHeading: "Notices and service guidance",
      updateOne:
        "Application filing and review status updates are available from the Updates section.",
      updateTwo:
        "Use the service directory to choose the correct public or secure workflow route.",
      updateThree:
        "Use secure login for officer access and beneficiary status support.",
      supportKicker: "Need Assistance?",
      supportHeading: "Service guidance and secure access",
      supportBody:
        "Use the service directory for public routes and secure login for officer and beneficiary account access.",
      supportAction: "Open Services",
    },
    hi: {
      metaTitle: "राष्ट्रीय मखाना बोर्ड पोर्टल",
      badge: "राष्ट्रीय कृषि सेवा मंच",
      searchLabel: "पोर्टल सेवाएं खोजें",
      searchPlaceholder: "यहां खोजें...",
      directoryAction: "सेवा निर्देशिका",
      notice:
        "मखाना क्षेत्र के लिए लाभार्थी सेवाओं, फील्ड सत्यापन, राज्य समीक्षा, स्वीकृति निगरानी और योजना प्रशासन का आधिकारिक पोर्टल।",
      heroEyebrow: "राष्ट्रीय मखाना बोर्ड डिजिटल सेवाएं",
      heroTitle: "राष्ट्रीय मखाना बोर्ड",
      heroBody:
        "पंजीकरण, योजना जानकारी, आवेदन ट्रैकिंग, फील्ड सत्यापन और बोर्ड स्तर की समीक्षा के लिए सिंगल-विंडो सार्वजनिक पहुंच।",
      heroLogin: "सुरक्षित अधिकारी लॉगिन",
      heroBeneficiary: "लाभार्थी सेवाएं खोलें",
      heroTagOne: "लाभार्थी आवेदन",
      heroTagTwo: "फील्ड सत्यापन",
      heroTagThree: "बोर्ड निगरानी",
      statsHeading: "कार्यक्रम सेवा सारांश",
      statOneTitle: "10 राज्य",
      statOneBody: "बोर्ड कार्यक्रम के अंतर्गत कवर किए गए राज्य",
      statTwoTitle: "सिंगल विंडो",
      statTwoBody: "किसान पंजीकरण, आवेदन और स्थिति ट्रैकिंग",
      statThreeTitle: "बहु-स्तरीय कार्यप्रवाह",
      statThreeBody: "राज्य समीक्षा, निरीक्षण और बोर्ड स्वीकृति",
      statFourTitle: "भूमिका आधारित पहुंच",
      statFourBody: "सार्वजनिक सेवाएं और सुरक्षित अधिकारी संचालन",
      serviceKicker: "सेवा प्रवेश बिंदु",
      serviceHeading: "पोर्टल में खोज किए बिना मुख्य सेवाओं तक पहुंचें।",
      serviceLead:
        "सार्वजनिक आवेदन, योजना मार्गदर्शन, सुरक्षित अधिकारी कार्य और कार्यान्वयन निगरानी के लिए सही मार्ग का उपयोग करें।",
      cardOneTitle: "लाभार्थी सेवाएं",
      cardOneBody:
        "किसान पंजीकरण, पहचान सत्यापन, आवेदन जमा करना और स्थिति की दृश्यता।",
      cardOneAction: "सेवाएं खोलें",
      cardTwoTitle: "योजना जानकारी",
      cardTwoBody:
        "पात्रता मार्गदर्शन, योजना घटक, सहायता श्रेणियां और सार्वजनिक जानकारी।",
      cardTwoAction: "योजनाएं देखें",
      cardThreeTitle: "अधिकारी संचालन",
      cardThreeBody:
        "समीक्षा, स्पष्टीकरण, निरीक्षण आवंटन, अनुशंसा और स्वीकृति कार्यप्रवाह।",
      cardThreeAction: "लॉगिन पर जाएं",
      cardFourTitle: "योजना एवं निगरानी",
      cardFourBody:
        "वार्षिक कार्ययोजना, बजट दृश्यता, जिला अपडेट और राष्ट्रीय निगरानी समर्थन।",
      cardFourAction: "कंसोल खोलें",
      updatesKicker: "नवीनतम जानकारी",
      updatesHeading: "सूचनाएं और सेवा मार्गदर्शन",
      updateOne:
        "आवेदन और समीक्षा स्थिति अपडेट, अपडेट अनुभाग में उपलब्ध हैं।",
      updateTwo:
        "सही सार्वजनिक या सुरक्षित कार्यप्रवाह मार्ग चुनने के लिए सेवा निर्देशिका का उपयोग करें।",
      updateThree:
        "अधिकारी पहुंच और लाभार्थी स्थिति सहायता के लिए सुरक्षित लॉगिन का उपयोग करें।",
      supportKicker: "सहायता चाहिए?",
      supportHeading: "सेवा मार्गदर्शन और सुरक्षित पहुंच",
      supportBody:
        "सार्वजनिक मार्गों के लिए सेवा निर्देशिका और अधिकारी तथा लाभार्थी खाता पहुंच के लिए सुरक्षित लॉगिन का उपयोग करें।",
      supportAction: "सेवाएं खोलें",
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
        "Public-facing services begin in the beneficiary workspace. Review, inspection, and approval functions operate through the secure officer environment.",
      heading: "Service Access Directory",
      lead:
        "Find the correct service route for registration, application filing, field verification, officer review, and board-level approval.",
      heroPointOne: "Public filing and tracking through one beneficiary workspace",
      heroPointTwo: "Secure officer route for scrutiny, inspection, and approval",
      heroPointThree: "Helpdesk escalation for unresolved access issues",
      catalogHeading: "Operational Service Catalogue",
      catalogLead:
        "Use search and role-based filters to reach the correct module without scanning the full workflow.",
      filterAll: "All Modules",
      filterPublic: "Beneficiary Services",
      filterSecure: "Officer Workflows",
      searchLabel: "Search services",
      searchPlaceholder: "Search by role, workflow stage, or service name",
      resultsSummaryStatic: "Showing all service modules.",
      resultsSummary: "Showing {count} service modules.",
      resultsEmpty: "No service modules match the current search or filter.",
      resultsAction: "Need secure service access?",
      stageLabel: "Workflow Use",
      entryOneLabel: "Public Access",
      entryOneTitle: "Beneficiary Workspace",
      entryOneBody:
        "Use this route for registration, application submission, and status tracking.",
      entryOneAction: "Open Beneficiary Services",
      entryTwoLabel: "Secure Access",
      entryTwoTitle: "Officer Login",
      entryTwoBody:
        "Use secure login for scrutiny, inspections, approval, and monitoring functions.",
      entryTwoAction: "Open Secure Login",
      visualTitle: "Field support and document review",
      visualBody:
        "Service delivery extends from public registration to document scrutiny, field verification, and assisted resolution at district level.",
      statOneLabel: "Service Modules",
      statOneValue: "6",
      statOneBody: "Registration, filing, tracking, review, field verification, and approval monitoring.",
      statTwoLabel: "Operational Roles",
      statTwoValue: "4",
      statTwoBody: "Beneficiaries, inspectors, state officers, and National Makhana Board administrators.",
      serviceOneTag: "Public Entry",
      serviceOneCode: "Module 01",
      serviceOneTitle: "Beneficiary Registration",
      serviceOneMeta: "Role: Beneficiary · Access: Public workspace",
      serviceOneBody:
        "Farmer profile creation with identity verification, location hierarchy, and cultivation profile setup.",
      serviceOneAction: "Open Workspace",
      serviceOneRoute: "Used before application filing.",
      serviceTwoTag: "Public Entry",
      serviceTwoCode: "Module 02",
      serviceTwoTitle: "Application Submission",
      serviceTwoMeta: "Role: Beneficiary · Access: Public workspace",
      serviceTwoBody:
        "Scheme support filing with document capture, geotag inputs, and acknowledgement-based submission.",
      serviceTwoRoute: "Available inside the beneficiary workspace.",
      serviceThreeTag: "Public Entry",
      serviceThreeCode: "Module 03",
      serviceThreeTitle: "Status Tracking",
      serviceThreeMeta: "Role: Beneficiary · Access: Public workspace",
      serviceThreeBody:
        "Stage-level visibility for scrutiny, clarifications, inspections, recommendation, and final decision status.",
      serviceThreeRoute: "Accessible from the beneficiary workspace dashboard.",
      serviceFourTag: "Secure Workflow",
      serviceFourCode: "Module 04",
      serviceFourTitle: "Review and Recommendation",
      serviceFourMeta: "Role: State officer · Access: Secure login",
      serviceFourBody:
        "Application scrutiny, clarification management, inspection assignment, and eligibility recommendation by state officers.",
      serviceFourRoute: "Operates through the secure officer console.",
      serviceFiveTag: "Secure Workflow",
      serviceFiveCode: "Module 05",
      serviceFiveTitle: "Field Verification",
      serviceFiveMeta: "Role: Inspector · Access: Secure login",
      serviceFiveBody:
        "On-ground verification with field observations, location coordinates, photographs, and inspection remarks.",
      serviceFiveRoute: "Executed within the inspection workflow.",
      serviceSixTag: "Secure Workflow",
      serviceSixCode: "Module 06",
      serviceSixTitle: "Approval and Monitoring",
      serviceSixMeta: "Role: NMB administrator · Access: Secure login",
      serviceSixBody:
        "National-level approval, return decisions, readiness oversight, and implementation monitoring.",
      serviceSixRoute: "Restricted to the board administration environment.",
      groupsHeading: "Access by Role",
      groupsLead: "Use the correct entry point for each operating role.",
      matrixRoleLabel: "Role",
      matrixServiceLabel: "Core Services",
      matrixAccessLabel: "Access Route",
      groupOneTitle: "Beneficiaries",
      groupOneBody: "Registration, application filing, and status tracking.",
      groupOneRoute: "Beneficiary workspace",
      groupTwoTitle: "State Officers",
      groupTwoBody:
        "Scrutiny, clarification handling, inspection assignment, and recommendation.",
      groupTwoRoute: "Secure officer login",
      groupThreeTitle: "Inspectors",
      groupThreeBody:
        "Field verification closure, evidence capture, and inspection remarks.",
      groupThreeRoute: "Secure officer login",
      groupFourTitle: "NMB Administrators",
      groupFourBody:
        "Approval, monitoring, readiness oversight, and implementation review.",
      groupFourRoute: "Secure officer login",
      asideOneHeading: "Before You Proceed",
      asideOneItemOne:
        "Use the beneficiary workspace for public registration, filing, and status-viewing functions.",
      asideOneItemTwo: "Use secure login for scrutiny, inspection, approval, and monitoring actions.",
      asideOneItemThree:
        "Use secure login for role-restricted services and avoid duplicate public submissions.",
      guidanceNoteTitle: "Service route discipline",
      guidanceNoteBody:
        "Public pages should guide users to the correct route quickly. Role-restricted actions should remain inside secure workflows.",
      supportBody:
        "Use the services directory to identify the correct service path for beneficiaries, inspection teams, and officers.",
      supportAction: "Open Secure Login",
    },
    hi: {
      metaTitle: "एनएमबी सेवाएं",
      badge: "सार्वजनिक सेवा निर्देशिका",
      notice:
        "सार्वजनिक सेवाओं की शुरुआत लाभार्थी कार्यस्थान से होती है। समीक्षा, निरीक्षण और स्वीकृति संबंधी कार्य सुरक्षित अधिकारी वातावरण में संचालित होते हैं।",
      heading: "सेवा अभिगम निर्देशिका",
      lead:
        "पंजीकरण, आवेदन दाखिल करने, फील्ड सत्यापन, अधिकारी समीक्षा और बोर्ड-स्तरीय स्वीकृति के लिए सही सेवा मार्ग खोजें।",
      heroPointOne: "सार्वजनिक दाखिला और ट्रैकिंग के लिए एक लाभार्थी कार्यस्थान",
      heroPointTwo: "जांच, निरीक्षण और स्वीकृति के लिए सुरक्षित अधिकारी मार्ग",
      heroPointThree: "अनसुलझे अभिगम मुद्दों के लिए हेल्पडेस्क एस्केलेशन",
      catalogHeading: "संचालन सेवा कैटलॉग",
      catalogLead:
        "पूर्ण कार्यप्रवाह को स्कैन किए बिना सही मॉड्यूल तक पहुंचने के लिए खोज और भूमिका-आधारित फिल्टर का उपयोग करें।",
      filterAll: "सभी मॉड्यूल",
      filterPublic: "लाभार्थी सेवाएं",
      filterSecure: "अधिकारी कार्यप्रवाह",
      searchLabel: "सेवाएं खोजें",
      searchPlaceholder: "भूमिका, कार्यप्रवाह चरण या सेवा नाम से खोजें",
      resultsSummaryStatic: "सभी सेवा मॉड्यूल दिखाए जा रहे हैं।",
      resultsSummary: "{count} सेवा मॉड्यूल दिखाए जा रहे हैं।",
      resultsEmpty: "वर्तमान खोज या फिल्टर से कोई सेवा मॉड्यूल मेल नहीं खाता।",
      resultsAction: "सुरक्षित सेवा पहुंच चाहिए?",
      stageLabel: "कार्यप्रवाह उपयोग",
      entryOneLabel: "सार्वजनिक अभिगम",
      entryOneTitle: "लाभार्थी कार्यस्थान",
      entryOneBody:
        "पंजीकरण, आवेदन जमा करने और स्थिति ट्रैकिंग के लिए इस मार्ग का उपयोग करें।",
      entryOneAction: "लाभार्थी सेवाएं खोलें",
      entryTwoLabel: "सुरक्षित अभिगम",
      entryTwoTitle: "अधिकारी लॉगिन",
      entryTwoBody:
        "जांच, निरीक्षण, स्वीकृति और निगरानी कार्यों के लिए सुरक्षित लॉगिन का उपयोग करें।",
      entryTwoAction: "सुरक्षित लॉगिन खोलें",
      visualTitle: "फील्ड सहायता और दस्तावेज़ समीक्षा",
      visualBody:
        "सेवा वितरण सार्वजनिक पंजीकरण से दस्तावेज़ जांच, फील्ड सत्यापन और जिला स्तर पर सहायता-आधारित समाधान तक विस्तृत है।",
      statOneLabel: "सेवा मॉड्यूल",
      statOneValue: "6",
      statOneBody: "पंजीकरण, दाखिला, ट्रैकिंग, समीक्षा, फील्ड सत्यापन और स्वीकृति निगरानी।",
      statTwoLabel: "संचालन भूमिकाएं",
      statTwoValue: "4",
      statTwoBody: "लाभार्थी, निरीक्षक, राज्य अधिकारी और राष्ट्रीय मखाना बोर्ड प्रशासक।",
      serviceOneTag: "सार्वजनिक प्रवेश",
      serviceOneCode: "मॉड्यूल 01",
      serviceOneTitle: "लाभार्थी पंजीकरण",
      serviceOneMeta: "भूमिका: लाभार्थी · अभिगम: सार्वजनिक कार्यस्थान",
      serviceOneBody:
        "पहचान सत्यापन, स्थान पदानुक्रम और खेती प्रोफाइल सेटअप के साथ किसान प्रोफाइल निर्माण।",
      serviceOneAction: "कार्यस्थान खोलें",
      serviceOneRoute: "आवेदन दाखिल करने से पहले उपयोग किया जाता है।",
      serviceTwoTag: "सार्वजनिक प्रवेश",
      serviceTwoCode: "मॉड्यूल 02",
      serviceTwoTitle: "आवेदन जमा करना",
      serviceTwoMeta: "भूमिका: लाभार्थी · अभिगम: सार्वजनिक कार्यस्थान",
      serviceTwoBody:
        "दस्तावेज़ संकलन, जियोटैग इनपुट और पावती-आधारित जमा के साथ योजना सहायता आवेदन।",
      serviceTwoRoute: "लाभार्थी कार्यस्थान के भीतर उपलब्ध।",
      serviceThreeTag: "सार्वजनिक प्रवेश",
      serviceThreeCode: "मॉड्यूल 03",
      serviceThreeTitle: "स्थिति ट्रैकिंग",
      serviceThreeMeta: "भूमिका: लाभार्थी · अभिगम: सार्वजनिक कार्यस्थान",
      serviceThreeBody:
        "जांच, स्पष्टीकरण, निरीक्षण, अनुशंसा और अंतिम निर्णय की चरण-स्तरीय दृश्यता।",
      serviceThreeRoute: "लाभार्थी कार्यस्थान डैशबोर्ड से उपलब्ध।",
      serviceFourTag: "सुरक्षित कार्यप्रवाह",
      serviceFourCode: "मॉड्यूल 04",
      serviceFourTitle: "समीक्षा और अनुशंसा",
      serviceFourMeta: "भूमिका: राज्य अधिकारी · अभिगम: सुरक्षित लॉगिन",
      serviceFourBody:
        "राज्य अधिकारियों द्वारा आवेदन जांच, स्पष्टीकरण प्रबंधन, निरीक्षण आवंटन और पात्रता अनुशंसा।",
      serviceFourRoute: "सुरक्षित अधिकारी कंसोल के माध्यम से संचालित।",
      serviceFiveTag: "सुरक्षित कार्यप्रवाह",
      serviceFiveCode: "मॉड्यूल 05",
      serviceFiveTitle: "फील्ड सत्यापन",
      serviceFiveMeta: "भूमिका: निरीक्षक · अभिगम: सुरक्षित लॉगिन",
      serviceFiveBody:
        "फील्ड अवलोकन, स्थान निर्देशांक, फोटो और निरीक्षण टिप्पणियों के साथ जमीनी सत्यापन।",
      serviceFiveRoute: "निरीक्षण कार्यप्रवाह के भीतर निष्पादित।",
      serviceSixTag: "सुरक्षित कार्यप्रवाह",
      serviceSixCode: "मॉड्यूल 06",
      serviceSixTitle: "स्वीकृति और निगरानी",
      serviceSixMeta: "भूमिका: एनएमबी प्रशासक · अभिगम: सुरक्षित लॉगिन",
      serviceSixBody:
        "राष्ट्रीय स्तर पर स्वीकृति, वापसी निर्णय, तत्परता पर्यवेक्षण और कार्यान्वयन निगरानी।",
      serviceSixRoute: "बोर्ड प्रशासनिक वातावरण तक सीमित।",
      groupsHeading: "भूमिका के अनुसार अभिगम",
      groupsLead: "प्रत्येक संचालन भूमिका के लिए सही प्रवेश बिंदु का उपयोग करें।",
      matrixRoleLabel: "भूमिका",
      matrixServiceLabel: "मुख्य सेवाएं",
      matrixAccessLabel: "अभिगम मार्ग",
      groupOneTitle: "लाभार्थी",
      groupOneBody: "पंजीकरण, आवेदन दाखिला और स्थिति ट्रैकिंग।",
      groupOneRoute: "लाभार्थी कार्यस्थान",
      groupTwoTitle: "राज्य अधिकारी",
      groupTwoBody:
        "जांच, स्पष्टीकरण प्रबंधन, निरीक्षण आवंटन और अनुशंसा।",
      groupTwoRoute: "सुरक्षित अधिकारी लॉगिन",
      groupThreeTitle: "निरीक्षक",
      groupThreeBody:
        "फील्ड सत्यापन समापन, साक्ष्य संकलन और निरीक्षण टिप्पणियां।",
      groupThreeRoute: "सुरक्षित अधिकारी लॉगिन",
      groupFourTitle: "एनएमबी प्रशासक",
      groupFourBody:
        "स्वीकृति, निगरानी, तत्परता पर्यवेक्षण और कार्यान्वयन समीक्षा।",
      groupFourRoute: "सुरक्षित अधिकारी लॉगिन",
      asideOneHeading: "आगे बढ़ने से पहले",
      asideOneItemOne:
        "सार्वजनिक पंजीकरण, आवेदन दाखिला और स्थिति देखने के लिए लाभार्थी कार्यस्थान का उपयोग करें।",
      asideOneItemTwo:
        "जांच, निरीक्षण, स्वीकृति और निगरानी संबंधी कार्यों के लिए सुरक्षित लॉगिन का उपयोग करें।",
      asideOneItemThree:
        "भूमिका-सीमित सेवाओं के लिए सुरक्षित लॉगिन का उपयोग करें और दोहराव वाले सार्वजनिक सबमिशन से बचें।",
      guidanceNoteTitle: "सेवा मार्ग अनुशासन",
      guidanceNoteBody:
        "सार्वजनिक पृष्ठों को उपयोगकर्ताओं को शीघ्र सही मार्ग तक पहुंचाना चाहिए। भूमिका-सीमित कार्य सुरक्षित कार्यप्रवाह के भीतर ही रहने चाहिए।",
      supportBody:
        "लाभार्थियों, निरीक्षण टीमों और अधिकारियों के लिए सही सेवा मार्ग पहचानने हेतु सेवाओं की निर्देशिका का उपयोग करें।",
      supportAction: "सुरक्षित लॉगिन खोलें",
    },
  },
  schemes: {
    en: {
      metaTitle: "NMB Schemes and Support Areas",
      breadcrumbCurrent: "Schemes",
      badge: "Scheme Overview",
      heading: "Priority Support Areas",
      lead:
        "These categories help users understand how cultivation, processing, verification, and planning support can be administered.",
      primaryAction: "Browse Services",
      secondaryAction: "Secure Login",
      summaryHeading: "Scheme Summary",
      summaryNote:
        "The six support areas work as one connected programme chain, from cultivation readiness through verification and state-level monitoring.",
      lifecycleHeading: "Makhana Development Lifecycle",
      lifecycleLead:
        "The support areas below show how public services connect field activity, processing readiness, oversight, and implementation review.",
      lifecycleOne: "Cultivation",
      lifecycleTwo: "Nursery and Inputs",
      lifecycleThree: "Processing",
      lifecycleFour: "Training and Extension",
      lifecycleFive: "Inspection and Verification",
      lifecycleSix: "State Planning and Monitoring",
      matrixHeading: "Support Coverage Matrix",
      matrixLead:
        "The support structure below groups field assistance, infrastructure needs, and administrative oversight into clear public categories.",
      statOneLabel: "Support Pillars",
      statOneValue: "6",
      statOneBody: "Cultivation, inputs, processing, training, verification, and planning.",
      statTwoLabel: "Delivery Model",
      statTwoValue: "State-led",
      statTwoBody: "State review, inspection evidence, and board-level approval remain linked through the portal.",
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
      guidanceHeading: "How to use this page",
      guidanceLead:
        "Use the support categories below to understand the programme structure before moving into a live service route.",
      guidanceStepOneTitle: "Understand the support category",
      guidanceStepOneBody:
        "Review the category description first so the correct public or secure route is chosen for the next step.",
      guidanceStepTwoTitle: "Open the relevant service",
      guidanceStepTwoBody:
        "Move to the services directory when you are ready to locate the correct beneficiary or officer workflow.",
      guidanceStepThreeTitle: "Use secure login only when required",
      guidanceStepThreeBody:
        "Authenticated actions such as scrutiny, verification, and operational review continue through secure portal access.",
      supportBody:
        "Scheme information pages provide an overview of intervention areas, while service submission continues through secure portal access.",
      supportAction: "View Services",
    },
    hi: {
      metaTitle: "एनएमबी योजनाएं और सहायता क्षेत्र",
      breadcrumbCurrent: "योजनाएं",
      badge: "योजना अवलोकन",
      heading: "प्राथमिक सहायता क्षेत्र",
      lead:
        "ये श्रेणियां उपयोगकर्ताओं को समझने में मदद करती हैं कि खेती, प्रसंस्करण, सत्यापन और योजना समर्थन का प्रशासन कैसे किया जा सकता है।",
      primaryAction: "सेवाएं देखें",
      secondaryAction: "सुरक्षित लॉगिन",
      summaryHeading: "योजना सारांश",
      summaryNote:
        "ये छह सहायता क्षेत्र खेती की तैयारी से लेकर सत्यापन और राज्य-स्तरीय निगरानी तक एक जुड़े हुए कार्यक्रम शृंखला की तरह कार्य करते हैं।",
      lifecycleHeading: "मखाना विकास जीवनचक्र",
      lifecycleLead:
        "नीचे दिए गए सहायता क्षेत्र दिखाते हैं कि सार्वजनिक सेवाएं फील्ड गतिविधि, प्रसंस्करण तत्परता, पर्यवेक्षण और कार्यान्वयन समीक्षा से कैसे जुड़ती हैं।",
      lifecycleOne: "खेती",
      lifecycleTwo: "नर्सरी और इनपुट",
      lifecycleThree: "प्रसंस्करण",
      lifecycleFour: "प्रशिक्षण और विस्तार",
      lifecycleFive: "निरीक्षण और सत्यापन",
      lifecycleSix: "राज्य योजना और निगरानी",
      matrixHeading: "सहायता कवरेज मैट्रिक्स",
      matrixLead:
        "नीचे दी गई संरचना क्षेत्रीय सहायता, अवसंरचना आवश्यकताओं और प्रशासनिक पर्यवेक्षण को स्पष्ट सार्वजनिक श्रेणियों में समूहित करती है।",
      statOneLabel: "सहायता स्तंभ",
      statOneValue: "6",
      statOneBody: "खेती, इनपुट, प्रसंस्करण, प्रशिक्षण, सत्यापन और योजना।",
      statTwoLabel: "कार्यान्वयन मॉडल",
      statTwoValue: "राज्य-नेतृत्व",
      statTwoBody: "राज्य समीक्षा, निरीक्षण साक्ष्य और बोर्ड-स्तरीय स्वीकृति पोर्टल के माध्यम से जुड़े रहते हैं।",
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
      guidanceHeading: "इस पृष्ठ का उपयोग कैसे करें",
      guidanceLead:
        "लाइव सेवा मार्ग में जाने से पहले कार्यक्रम की संरचना समझने हेतु नीचे दिए गए सहायता क्षेत्रों का उपयोग करें।",
      guidanceStepOneTitle: "सहायता श्रेणी को समझें",
      guidanceStepOneBody:
        "अगले चरण के लिए सही सार्वजनिक या सुरक्षित मार्ग चुनने से पहले श्रेणी विवरण को पढ़ें।",
      guidanceStepTwoTitle: "संबंधित सेवा खोलें",
      guidanceStepTwoBody:
        "जब आप सही लाभार्थी या अधिकारी कार्यप्रवाह ढूंढने के लिए तैयार हों, तब सेवा निर्देशिका पर जाएं।",
      guidanceStepThreeTitle: "आवश्यक होने पर ही सुरक्षित लॉगिन का उपयोग करें",
      guidanceStepThreeBody:
        "जांच, सत्यापन और संचालन समीक्षा जैसे प्रमाणित कार्य सुरक्षित पोर्टल पहुंच के माध्यम से जारी रहते हैं।",
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
  chatbot: {
    en: {
      launcherTitle: "Ask NMB",
      launcherSubtitle: "AI chat support",
      launcherAriaLabel: "Open NMB Assistant",
      launcherHint: "Need help? Open NMB Assistant",
      close: "Close chat",
      refresh: "Start new chat",
      title: "NMB Assistant",
      eyebrow: "National Makhana Board",
      headerSubtitle: "Portal guidance, workflow support, and helpdesk direction",
      intro:
        "Ask about services, login, applications, or workflow status.",
      capabilityOne: "Services",
      capabilityTwo: "Applications",
      capabilityThree: "Workflow status",
      placeholder: "Type your question",
      inputHint: "Enter to send. Shift+Enter for a new line.",
      send: "Send",
      sources: "Sources",
      suggested: "Quick prompts",
      minimize: "Minimize",
      maximize: "Maximize",
      restore: "Restore",
      error: "The assistant could not complete the request. Please try again or use the Helpdesk.",
      promptsHome: [
        "What is this portal used for?",
        "Which users are supported here?",
        "How should this portal be understood in a bid setting?",
      ],
      promptsServices: [
        "What service areas are available in the portal?",
        "What can state officers do here?",
        "Where should a farmer go to apply?",
      ],
      promptsSchemes: [
        "What are the main support areas shown under schemes?",
        "Is this only an information website?",
        "How does scheme support connect to workflow?",
      ],
      promptsUpdates: [
        "What kind of notices does this portal support?",
        "What does integration-ready mean in this PoC?",
        "How are updates linked to services?",
      ],
      promptsHelpdesk: [
        "What can I do if I cannot log in?",
        "What does clarification raised mean?",
        "What does inspection assigned mean?",
      ],
      promptsLogin: [
        "Which users can log in here?",
        "What can beneficiaries do after secure login?",
        "What should I do if login fails?",
      ],
      promptsBeneficiary: [
        "What is my current application status?",
        "Do I have any open clarification?",
        "What should I do next in the beneficiary workspace?",
      ],
      promptsDashboard: [
        "What is currently pending in the workflow queue?",
        "Summarize the AAP and budget situation.",
        "What does the service readiness view show?",
      ],
    },
    hi: {
      launcherTitle: "एनएमबी से पूछें",
      launcherSubtitle: "एआई चैट सहायता",
      launcherAriaLabel: "एनएमबी सहायक खोलें",
      launcherHint: "सहायता चाहिए? एनएमबी सहायक खोलें",
      close: "चैट बंद करें",
      refresh: "नई चैट शुरू करें",
      title: "एनएमबी सहायक",
      eyebrow: "राष्ट्रीय मखाना बोर्ड",
      headerSubtitle: "पोर्टल मार्गदर्शन, कार्यप्रवाह सहायता और हेल्पडेस्क दिशा",
      intro:
        "सेवाओं, लॉगिन, आवेदनों या कार्यप्रवाह स्थिति के बारे में पूछें।",
      capabilityOne: "सेवाएं",
      capabilityTwo: "आवेदन",
      capabilityThree: "कार्यप्रवाह स्थिति",
      placeholder: "अपना प्रश्न लिखें",
      inputHint: "भेजने के लिए Enter दबाएं। नई पंक्ति के लिए Shift+Enter दबाएं।",
      send: "भेजें",
      sources: "स्रोत",
      suggested: "त्वरित प्रश्न",
      minimize: "छोटा करें",
      maximize: "बड़ा करें",
      restore: "सामान्य करें",
      error: "सहायक अनुरोध पूरा नहीं कर सका। कृपया पुनः प्रयास करें या सहायता केंद्र का उपयोग करें।",
      promptsHome: [
        "यह पोर्टल किसलिए उपयोग किया जाता है?",
        "यहां किन उपयोगकर्ताओं का समर्थन है?",
        "बिड सेटिंग में इस पोर्टल को कैसे समझा जाए?",
      ],
      promptsServices: [
        "पोर्टल में कौन-कौन सी सेवा क्षेत्र उपलब्ध हैं?",
        "राज्य अधिकारी यहां क्या कर सकते हैं?",
        "किसान आवेदन करने के लिए कहाँ जाए?",
      ],
      promptsSchemes: [
        "योजनाओं के अंतर्गत मुख्य सहायता क्षेत्र क्या हैं?",
        "क्या यह केवल सूचना वेबसाइट है?",
        "योजना सहायता कार्यप्रवाह से कैसे जुड़ती है?",
      ],
      promptsUpdates: [
        "यह पोर्टल किस प्रकार की सूचनाएँ समर्थित करता है?",
        "इस पीओसी में इंटीग्रेशन-रेडी का क्या अर्थ है?",
        "अपडेट सेवाओं से कैसे जुड़ते हैं?",
      ],
      promptsHelpdesk: [
        "यदि मैं लॉगिन नहीं कर पा रहा हूँ तो क्या करूँ?",
        "स्पष्टीकरण उठाया गया का क्या अर्थ है?",
        "निरीक्षण आवंटित का क्या अर्थ है?",
      ],
      promptsLogin: [
        "यहाँ कौन-कौन से उपयोगकर्ता लॉगिन कर सकते हैं?",
        "सुरक्षित लॉगिन के बाद लाभार्थी क्या कर सकते हैं?",
        "यदि लॉगिन विफल हो तो क्या करना चाहिए?",
      ],
      promptsBeneficiary: [
        "मेरे आवेदन की वर्तमान स्थिति क्या है?",
        "क्या मेरे लिए कोई खुला स्पष्टीकरण है?",
        "लाभार्थी कार्यक्षेत्र में मुझे आगे क्या करना चाहिए?",
      ],
      promptsDashboard: [
        "कार्यप्रवाह कतार में अभी क्या लंबित है?",
        "एएपी और बजट की स्थिति का सारांश दें।",
        "सेवा तत्परता दृश्य क्या दिखाता है?",
      ],
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
  const page = document.body.dataset.page || "";
  const source = getPageTranslations(language);
  const directMatch = key.split(".").reduce((value, segment) => value?.[segment], source);
  if (typeof directMatch === "string") {
    return directMatch;
  }

  if (page && key.startsWith(`${page}.`)) {
    const pageKey = key.slice(page.length + 1);
    const pageSource = translations[page]?.[language] || {};
    return pageKey.split(".").reduce((value, segment) => value?.[segment], pageSource);
  }

  return directMatch;
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
  document.querySelectorAll("[data-i18n-placeholder]").forEach((node) => {
    const text = resolveTranslation(language, node.dataset.i18nPlaceholder);
    if (typeof text === "string") {
      node.setAttribute("placeholder", text);
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

function applyFontScale(scale) {
  const nextScale = scale === "small" || scale === "large" ? scale : "normal";
  document.documentElement.classList.toggle("nmb-font-small", nextScale === "small");
  document.documentElement.classList.toggle("nmb-font-large", nextScale === "large");
  document.querySelectorAll("[data-font-scale]").forEach((button) => {
    button.setAttribute("aria-pressed", String(button.dataset.fontScale === nextScale));
  });
  localStorage.setItem(NMB_FONT_SCALE_KEY, nextScale);
}

function applyContrast(isEnabled) {
  document.documentElement.classList.toggle("nmb-high-contrast", Boolean(isEnabled));
  document.querySelectorAll("[data-contrast-toggle]").forEach((button) => {
    button.setAttribute("aria-pressed", String(Boolean(isEnabled)));
  });
  localStorage.setItem(NMB_CONTRAST_KEY, isEnabled ? "true" : "false");
}

function initAccessibilityControls() {
  applyFontScale(localStorage.getItem(NMB_FONT_SCALE_KEY) || "normal");
  applyContrast(localStorage.getItem(NMB_CONTRAST_KEY) === "true");

  document.querySelectorAll("[data-font-scale]").forEach((button) => {
    button.addEventListener("click", () => applyFontScale(button.dataset.fontScale));
  });
  document.querySelectorAll("[data-contrast-toggle]").forEach((button) => {
    button.addEventListener("click", () => {
      applyContrast(!document.documentElement.classList.contains("nmb-high-contrast"));
    });
  });
}

function chatbotCopy(language) {
  return translations.chatbot?.[language] || translations.chatbot?.en;
}

function chatbotPrompts(page, language) {
  const copy = chatbotCopy(language);
  const key = `prompts${page.charAt(0).toUpperCase()}${page.slice(1)}`;
  return copy[key] || copy.promptsHome || [];
}

function createChatbotShell(language, page) {
  const copy = chatbotCopy(language);
  const shell = document.createElement("aside");
  shell.className = "chatbot-shell";
  shell.innerHTML = `
    <button type="button" class="chatbot-toggle" aria-expanded="false" aria-label="${copy.launcherAriaLabel || copy.launcherTitle}" title="${copy.launcherTitle}">
      <span class="chatbot-toggle-ping" aria-hidden="true"></span>
      <span class="chatbot-toggle-icon-wrap" aria-hidden="true">
        <img class="chatbot-toggle-icon" src="${CHATBOT_LOGO_PATH}" alt="" />
      </span>
      <span class="sr-only">${copy.launcherTitle}</span>
    </button>
    <div class="chatbot-toggle-hint" aria-hidden="true">${copy.launcherHint}</div>
    <section class="chatbot-panel" hidden>
      <div class="chatbot-panel-head">
        <div class="chatbot-panel-brand">
          <img class="chatbot-panel-logo" src="${CHATBOT_LOGO_PATH}" alt="" />
          <div class="chatbot-panel-identity">
            <span class="chatbot-panel-eyebrow">${copy.eyebrow}</span>
            <h2>${copy.title}</h2>
            <p class="chatbot-panel-subtitle">${copy.headerSubtitle}</p>
          </div>
        </div>
        <div class="chatbot-panel-controls">
          <button type="button" class="chatbot-control chatbot-control-refresh" data-chatbot-control="refresh" aria-label="${copy.refresh}" title="${copy.refresh}">
            <span class="chatbot-control-icon" aria-hidden="true">↻</span>
            <span class="chatbot-control-label sr-only">${copy.refresh}</span>
          </button>
          <button type="button" class="chatbot-control chatbot-control-close" data-chatbot-control="close" aria-label="${copy.close}" title="${copy.close}">
            <span class="chatbot-control-icon" aria-hidden="true">×</span>
            <span class="chatbot-control-label sr-only">${copy.close}</span>
          </button>
        </div>
      </div>
      <div class="chatbot-intro">
        <p>${copy.intro}</p>
        <div class="chatbot-capability-list" aria-hidden="true">
          <span class="chatbot-capability">${copy.capabilityOne}</span>
          <span class="chatbot-capability">${copy.capabilityTwo}</span>
          <span class="chatbot-capability">${copy.capabilityThree}</span>
        </div>
      </div>
      <div class="chatbot-prompts">
        <strong class="chatbot-prompts-title">${copy.suggested}</strong>
        <div class="chatbot-prompt-list"></div>
      </div>
      <div class="chatbot-thread" role="log" aria-live="polite" aria-relevant="additions text"></div>
      <form class="chatbot-form">
        <label class="sr-only" for="chatbot-message">${copy.placeholder}</label>
        <textarea id="chatbot-message" name="message" rows="3" placeholder="${copy.placeholder}"></textarea>
        <div class="chatbot-form-foot">
          <span class="chatbot-form-hint">${copy.inputHint}</span>
          <button class="button primary chatbot-submit" type="submit" disabled>${copy.send}</button>
        </div>
      </form>
    </section>
  `;
  const promptList = shell.querySelector(".chatbot-prompt-list");
  chatbotPrompts(page, language).forEach((prompt) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "chatbot-prompt";
    button.textContent = prompt;
    promptList.appendChild(button);
  });
  return shell;
}

function setChatbotOpenState(shell, isOpen) {
  const toggle = shell.querySelector(".chatbot-toggle");
  const panel = shell.querySelector(".chatbot-panel");
  const textarea = shell.querySelector(".chatbot-form textarea");
  toggle?.setAttribute("aria-expanded", String(isOpen));
  if (panel) {
    panel.hidden = !isOpen;
  }
  shell.classList.toggle("is-open", isOpen);
  if (isOpen) {
    window.setTimeout(() => textarea?.focus(), 60);
  }
}

function resetChatbotSession(shell) {
  const panel = shell.querySelector(".chatbot-panel");
  const thread = shell.querySelector(".chatbot-thread");
  const form = shell.querySelector(".chatbot-form");
  const textarea = form?.querySelector("textarea");
  panel?.classList.remove("chatbot-has-messages");
  if (thread) {
    thread.innerHTML = "";
  }
  if (textarea) {
    textarea.value = "";
  }
  syncChatbotComposerState(form);
}

function syncChatbotComposerState(form) {
  const textarea = form?.querySelector("textarea");
  const submitButton = form?.querySelector('button[type="submit"]');
  if (!textarea || !submitButton) return;
  submitButton.disabled = textarea.disabled || !textarea.value.trim();
}

function escapeChatHtml(value) {
  return String(value)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

function escapeChatAttribute(value) {
  return escapeChatHtml(value);
}

function normalizeAssistantText(text) {
  return String(text || "")
    .replace(/\r\n/g, "\n")
    .replace(/([^\n])\s+(?=#{1,4}\s+)/g, "$1\n\n")
    .replace(/([^\n])\s+(?=\d+\.\s)/g, "$1\n")
    .replace(/([^\n])\s+(?=(?:-|\*)\s+(?:\*\*)?[A-Za-z])/g, "$1\n")
    .replace(/:\s+(?=(?:-|\*)\s+)/g, ":\n")
    .replace(/([^\n])\s+(?=(?:[A-Z][A-Za-z ]{1,32}:)\s)/g, "$1\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}

function formatInlineChatMarkup(text) {
  return escapeChatHtml(text)
    .replace(/\*\*(.+?)\*\*/g, "<strong>$1</strong>")
    .replace(/`([^`]+)`/g, "<code>$1</code>");
}

function renderPlainChatText(text) {
  const content = escapeChatHtml(text).replace(/\n/g, "<br>");
  return `<p>${content}</p>`;
}

function renderAssistantText(text) {
  const normalized = normalizeAssistantText(text);
  if (!normalized) {
    return renderPlainChatText("");
  }

  const blocks = normalized.split(/\n{2,}/).filter(Boolean);
  const html = [];

  for (const block of blocks) {
    const lines = block
      .split("\n")
      .map((line) => line.trim())
      .filter(Boolean);

    if (!lines.length) continue;

    let index = 0;
    while (index < lines.length) {
      if (/^\d+\.\s+/.test(lines[index])) {
        const items = [];
        while (index < lines.length && /^\d+\.\s+/.test(lines[index])) {
          items.push(lines[index].replace(/^\d+\.\s+/, ""));
          index += 1;
        }
        html.push(`<ol>${items.map((line) => `<li>${formatInlineChatMarkup(line)}</li>`).join("")}</ol>`);
        continue;
      }

      if (/^(?:-|\*)\s+/.test(lines[index])) {
        const items = [];
        while (index < lines.length && /^(?:-|\*)\s+/.test(lines[index])) {
          items.push(lines[index].replace(/^(?:-|\*)\s+/, ""));
          index += 1;
        }
        html.push(`<ul>${items.map((line) => `<li>${formatInlineChatMarkup(line)}</li>`).join("")}</ul>`);
        continue;
      }

      if (/^#{1,4}\s+/.test(lines[index])) {
        const heading = lines[index].replace(/^#{1,4}\s+/, "");
        html.push(`<h4>${formatInlineChatMarkup(heading)}</h4>`);
        index += 1;
        continue;
      }

      if (/^[A-Z][A-Za-z /&()-]{1,40}:$/.test(lines[index])) {
        html.push(`<h4>${formatInlineChatMarkup(lines[index].slice(0, -1))}</h4>`);
        index += 1;
        continue;
      }

      html.push(`<p>${formatInlineChatMarkup(lines[index])}</p>`);
      index += 1;
    }
  }

  return html.join("");
}

function buildSourcesMarkup(copy, sources) {
  if (!sources.length) return "";
  return `<div class="chatbot-sources"><strong>${escapeChatHtml(copy.sources)}</strong><ul>${sources
    .map(
      (item) =>
        `<li><strong>${escapeChatHtml(item.title)}</strong><br /><span>${escapeChatHtml(item.summary || item.category || "")}</span></li>`,
    )
    .join("")}</ul></div>`;
}

function buildActionsMarkup(actions) {
  if (!actions.length) return "";
  return `<div class="chatbot-actions">${actions
    .map((item) => `<a class="button secondary" href="${escapeChatAttribute(item.href)}">${escapeChatHtml(item.label)}</a>`)
    .join("")}</div>`;
}

function renderChatMessage(container, { role, text, sources = [], actions = [] }, language) {
  const copy = chatbotCopy(language);
  const node = document.createElement("article");
  node.className = `chatbot-message ${role}`;
  const bodyMarkup = role === "assistant" ? renderAssistantText(text) : renderPlainChatText(text);
  const sourcesMarkup = buildSourcesMarkup(copy, sources);
  const actionsMarkup = buildActionsMarkup(actions);
  node.innerHTML = `<div class="chatbot-bubble"><div class="chatbot-message-body">${bodyMarkup}</div>${sourcesMarkup}${actionsMarkup}</div>`;
  container.appendChild(node);
  container.scrollTop = container.scrollHeight;
}

function createStreamingAssistantMessage(container) {
  const article = document.createElement("article");
  article.className = "chatbot-message assistant";
  article.innerHTML = `
    <div class="chatbot-bubble chatbot-bubble-streaming">
      <div class="chatbot-message-body chatbot-live-text is-streaming"></div>
      <div class="chatbot-typing" aria-hidden="true">
        <span></span><span></span><span></span>
      </div>
      <div class="chatbot-meta"></div>
    </div>
  `;
  container.appendChild(article);
  container.scrollTop = container.scrollHeight;
  return article;
}

function updateStreamingAssistantMessage(node, { text, sources = [], actions = [], complete = false }, language) {
  const copy = chatbotCopy(language);
  const textNode = node.querySelector(".chatbot-live-text");
  const typingNode = node.querySelector(".chatbot-typing");
  const metaNode = node.querySelector(".chatbot-meta");
  if (!complete) {
    textNode.classList.add("is-streaming");
    textNode.innerHTML = renderAssistantText(text);
    if (!typingNode) {
      const typing = document.createElement("div");
      typing.className = "chatbot-typing";
      typing.setAttribute("aria-hidden", "true");
      typing.innerHTML = "<span></span><span></span><span></span>";
      metaNode.before(typing);
    }
    metaNode.innerHTML = "";
    return;
  }
  textNode.classList.remove("is-streaming");
  textNode.innerHTML = renderAssistantText(text);
  typingNode?.remove();
  const sourcesMarkup = buildSourcesMarkup(copy, sources);
  const actionsMarkup = buildActionsMarkup(actions);
  metaNode.innerHTML = `${sourcesMarkup}${actionsMarkup}`;
}

async function submitChatQuestion({ page, language, message, thread, form, toggle }) {
  thread.closest(".chatbot-panel")?.classList.add("chatbot-has-messages");
  renderChatMessage(thread, { role: "user", text: message }, language);
  const textarea = form.querySelector("textarea");
  const submitButton = form.querySelector('button[type="submit"]');
  textarea.value = "";
  textarea.disabled = true;
  submitButton.disabled = true;
  toggle.disabled = true;
  const assistantNode = createStreamingAssistantMessage(thread);
  let accumulated = "";
  const revealAt = performance.now() + 1000;
  let revealed = false;
  const waitForRevealWindow = async () => {
    const remaining = revealAt - performance.now();
    if (remaining > 0) {
      await new Promise((resolve) => window.setTimeout(resolve, remaining));
    }
  };
  try {
    const token = localStorage.getItem("nmb_token");
    const headers = { "Content-Type": "application/json" };
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
    const response = await fetch("/api/v1/chat/stream", {
      method: "POST",
      headers,
      body: JSON.stringify({ message, page, language }),
    });
    if (!response.ok || !response.body) throw new Error("chat_stream_failed");
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = "";
    let finalSources = [];
    let finalActions = [];
    while (true) {
      const { value, done } = await reader.read();
      if (done) break;
      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";
      for (const line of lines) {
        if (!line.trim()) continue;
        const event = JSON.parse(line);
        if (event.type === "status") {
          assistantNode.dataset.chatMode = event.mode || "";
          assistantNode.dataset.chatFallback = String(Boolean(event.fallback_used));
          if (event.fallback_used) {
            console.warn("[NMB chat] Fallback mode active", event);
          } else {
            console.info("[NMB chat] Azure grounded mode active", event);
          }
        }
        if (event.type === "delta") {
          if (!revealed) {
            await waitForRevealWindow();
            revealed = true;
          } else {
            await new Promise((resolve) => window.setTimeout(resolve, 55));
          }
          accumulated += event.content;
          updateStreamingAssistantMessage(assistantNode, { text: accumulated }, language);
        }
        if (event.type === "complete") {
          finalSources = event.sources || [];
          finalActions = event.suggested_actions || [];
        }
      }
    }
    if (!revealed) {
      await waitForRevealWindow();
    }
    updateStreamingAssistantMessage(
      assistantNode,
      { text: accumulated, sources: finalSources, actions: finalActions, complete: true },
      language,
    );
  } catch (_error) {
    assistantNode.remove();
    renderChatMessage(thread, { role: "assistant", text: chatbotCopy(language).error }, language);
  } finally {
    textarea.disabled = false;
    toggle.disabled = false;
    syncChatbotComposerState(form);
    textarea.focus();
  }
}

function initChatbot() {
  const page = document.body.dataset.page;
  if (!CHATBOT_PAGE_SET.has(page)) return;
  document.querySelector(".chatbot-shell")?.remove();
  const language = getLanguage();
  const shell = createChatbotShell(language, page);
  document.body.appendChild(shell);
  const toggle = shell.querySelector(".chatbot-toggle");
  const panel = shell.querySelector(".chatbot-panel");
  const thread = shell.querySelector(".chatbot-thread");
  const form = shell.querySelector(".chatbot-form");
  const textarea = form.querySelector("textarea");
  const refreshButton = shell.querySelector('[data-chatbot-control="refresh"]');
  const closeButton = shell.querySelector('[data-chatbot-control="close"]');
  toggle.addEventListener("click", () => {
    const isOpen = toggle.getAttribute("aria-expanded") === "true";
    if (isOpen) {
      setChatbotOpenState(shell, false);
      return;
    }
    setChatbotOpenState(shell, true);
  });
  refreshButton?.addEventListener("click", () => {
    resetChatbotSession(shell);
    setChatbotOpenState(shell, true);
  });
  closeButton?.addEventListener("click", () => {
    resetChatbotSession(shell);
    setChatbotOpenState(shell, false);
  });
  shell.querySelectorAll(".chatbot-prompt").forEach((button) => {
    button.addEventListener("click", () => {
      setChatbotOpenState(shell, true);
      submitChatQuestion({ page, language: getLanguage(), message: button.textContent, thread, form, toggle });
    });
  });
  form.addEventListener("submit", (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const message = String(formData.get("message") || "").trim();
    if (!message) return;
    setChatbotOpenState(shell, true);
    submitChatQuestion({ page, language: getLanguage(), message, thread, form, toggle });
  });
  textarea?.addEventListener("keydown", (event) => {
    if (event.key !== "Enter" || event.shiftKey) return;
    event.preventDefault();
    form.requestSubmit();
  });
  textarea?.addEventListener("input", () => {
    syncChatbotComposerState(form);
  });
  syncChatbotComposerState(form);
}

function initLanguageControls() {
  document.querySelectorAll("[data-lang-switch]").forEach((button) => {
    button.addEventListener("click", () => setLanguage(button.dataset.langSwitch));
  });
  window.addEventListener("nmb:languagechange", initChatbot);
  applyTranslations(getLanguage());
}

function initServicesDirectory() {
  if (document.body.dataset.page !== "services") {
    return;
  }

  const filters = Array.from(document.querySelectorAll("[data-service-filter]"));
  const rows = Array.from(document.querySelectorAll("[data-service-group]"));
  const searchInput = document.querySelector("[data-service-search-input]");
  const resultsNode = document.querySelector("[data-service-results]");
  if (!filters.length || !rows.length) {
    return;
  }

  const initialQuery = new URLSearchParams(window.location.search).get("q");
  if (searchInput && initialQuery) {
    searchInput.value = initialQuery;
  }

  const updateResultsSummary = (count) => {
    if (!resultsNode) return;
    const language = getLanguage();
    const key = count === 0 ? "services.resultsEmpty" : "services.resultsSummary";
    const template = resolveTranslation(language, key);
    if (typeof template === "string") {
      resultsNode.textContent = template.replace("{count}", String(count));
    }
  };

  const applyServiceFilter = (group) => {
    const nextGroup = group === "public" || group === "secure" ? group : "all";
    const query = String(searchInput?.value || "").trim().toLowerCase();
    let visibleCount = 0;
    filters.forEach((button) => {
      const isActive = button.dataset.serviceFilter === nextGroup;
      button.classList.toggle("is-active", isActive);
      button.setAttribute("aria-pressed", String(isActive));
    });
    rows.forEach((row) => {
      const matchesGroup = nextGroup === "all" || row.dataset.serviceGroup === nextGroup;
      const haystack = row.textContent.toLowerCase();
      const matchesQuery = !query || haystack.includes(query);
      const shouldShow = matchesGroup && matchesQuery;
      row.hidden = !shouldShow;
      if (shouldShow) {
        visibleCount += 1;
      }
    });
    updateResultsSummary(visibleCount);
  };

  filters.forEach((button) => {
    button.addEventListener("click", () => applyServiceFilter(button.dataset.serviceFilter));
  });

  searchInput?.addEventListener("input", () => {
    const activeFilter =
      filters.find((button) => button.classList.contains("is-active"))?.dataset.serviceFilter || "all";
    applyServiceFilter(activeFilter);
  });

  window.addEventListener("nmb:languagechange", () => {
    const activeFilter =
      filters.find((button) => button.classList.contains("is-active"))?.dataset.serviceFilter || "all";
    window.setTimeout(() => applyServiceFilter(activeFilter), 0);
  });

  applyServiceFilter("all");
}

window.NMBI18n = {
  getLanguage,
  setLanguage,
  translate: (key) => resolveTranslation(getLanguage(), key),
};

if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => {
    initAccessibilityControls();
    initLanguageControls();
    initServicesDirectory();
  }, { once: true });
} else {
  initAccessibilityControls();
  initLanguageControls();
  initServicesDirectory();
}
