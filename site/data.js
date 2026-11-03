window.SURVEYCOACH_DEMO = {
 "disclaimer": "Sample data: two made-up surveys. SurveyCoach never reads or changes anything in RedJade; you copy the fixes and apply them yourself.",
 "disclaimer_short": "Sample data. SurveyCoach never reads or edits RedJade; you copy fixes yourself.",
 "surveys": [
  {
   "id": "boxer-briefs",
   "title": "Member's Mark Boxer Briefs Feedback Survey",
   "blurb": "A deliberately flawed sample. Shows what a review catches and how it explains each fix.",
   "review": {
    "survey_title": "Member's Mark Boxer Briefs Feedback Survey",
    "content_hash": "912f055f4103cff763ddb10e52ab44ea20e4ea0532fac87d555f29fc097d3d4e",
    "rubric_version": "v2",
    "scorecard": {
     "score": 83.13,
     "provisional": true,
     "unchecked_points": 54,
     "by_dimension": {
      "D1": {
       "name": "First impression",
       "earned": 9.0,
       "possible": 11
      },
      "D2": {
       "name": "Respect for members' time",
       "earned": 12.0,
       "possible": 13
      },
      "D3": {
       "name": "Clear questions",
       "earned": 7.82,
       "possible": 10
      },
      "D4": {
       "name": "Fair and complete answers",
       "earned": 6.0,
       "possible": 9
      },
      "D5": {
       "name": "Neutral questions",
       "earned": 7.0,
       "possible": 7
      },
      "D6": {
       "name": "Built for the phone",
       "earned": 7.8100000000000005,
       "possible": 11
      },
      "D7": {
       "name": "Images that work on a phone",
       "earned": 8.5,
       "possible": 13
      },
      "D8": {
       "name": "Engaging experience",
       "earned": 12.0,
       "possible": 13
      },
      "D9": {
       "name": "Community voice and tone",
       "earned": 6.0,
       "possible": 6
      },
      "D10": {
       "name": "Closing the loop",
       "earned": 7.0,
       "possible": 7
      }
     },
     "open_blockers": [
      "B7"
     ],
     "kept_blockers": [],
     "pending_blockers": [
      "B1",
      "B2",
      "B6"
     ],
     "readiness": "needs_work",
     "strengths": [
      "Length fits the survey type",
      "Format variety that fits the content",
      "Not a wall of agree/disagree"
     ]
    },
    "findings": [
     {
      "criterion_id": "B7",
      "severity": "must_fix",
      "headline": "Image didn't load: Relaxed fit",
      "evidence": "The image \"Relaxed fit\" failed to load.",
      "explanation": "Fix or replace the image so members can see what they're judging.",
      "member_impact": "Members guess when they can't see, and the answers are meaningless.",
      "page_id": "p7",
      "question_id": "q7",
      "element_id": "img3",
      "current_text": null,
      "suggested_text": null,
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "1.4",
      "severity": "worth_improving",
      "headline": "Intro says 3 min but it takes about 4 and skips the reward",
      "evidence": "The intro promises 3 minutes; we estimate about 4.3. The intro doesn't mention the reward.",
      "explanation": "Say the true time and what members get, so they can decide to start. The suggested intro does both.",
      "member_impact": "Members decide whether to start from the time and reward; a wrong time breaks trust.",
      "page_id": "p0",
      "question_id": null,
      "element_id": null,
      "current_text": "Welcome to the Boxer Briefs Survey! This takes about 3 minutes.",
      "suggested_text": "Welcome to the Boxer Briefs Survey! This takes about 4 minutes. [Say what members get for finishing.]",
      "highlight": "about 3 minutes",
      "source": "auto"
     },
     {
      "criterion_id": "2.4",
      "severity": "worth_improving",
      "headline": "Required typing question; make it optional",
      "evidence": "Tell us what else you would like to share?",
      "explanation": "Make this answer optional, or replace it with answer choices.",
      "member_impact": "Typing on a phone is work, and required typing makes members quit.",
      "page_id": null,
      "question_id": "q10",
      "element_id": null,
      "current_text": "Tell us what else you would like to share?",
      "suggested_text": null,
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "3.2",
      "severity": "worth_improving",
      "headline": "\"aforementioned\" is not everyday language",
      "evidence": "\"aforementioned\" in: Please indicate your level of agreement with each of the following statements about the...",
      "explanation": "Use everyday words a member would use at the kitchen table.",
      "member_impact": "Jargon makes members guess or skip.",
      "page_id": null,
      "question_id": "q3",
      "element_id": null,
      "current_text": "Please indicate your level of agreement with each of the following statements about the aforementioned boxer briefs.",
      "suggested_text": "Please indicate your level of agreement with each of the following statements about the boxer briefs.",
      "highlight": "aforementioned",
      "source": "auto"
     },
     {
      "criterion_id": "3.3",
      "severity": "worth_improving",
      "headline": "Missing \"Select all that apply\"",
      "evidence": "Which of these matter to you?",
      "explanation": "Add \"Select all that apply\" to the question.",
      "member_impact": "Members can't tell whether they may pick more than one answer.",
      "page_id": null,
      "question_id": "q6",
      "element_id": null,
      "current_text": "Which of these matter to you?",
      "suggested_text": "Which of these matter to you? Select all that apply.",
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "4.2",
      "severity": "worth_improving",
      "headline": "Answer ranges overlap: 1 to 5 years, 5 to 10 years",
      "evidence": "\"1 to 5 years\" and \"5 to 10 years\" overlap.",
      "explanation": "Make the ranges share no numbers, for example 1 to 4 and 5 to 10.",
      "member_impact": "A member at the shared number can't tell which answer is theirs.",
      "page_id": null,
      "question_id": "q2",
      "element_id": null,
      "current_text": "1 to 5 years",
      "suggested_text": "1 to 4 years",
      "highlight": "1 to 5 years",
      "source": "auto"
     },
     {
      "criterion_id": "4.4",
      "severity": "worth_improving",
      "headline": "Scale has no label on one end",
      "evidence": "How likely are you to recommend them?",
      "explanation": "Both ends of the scale should be labeled so every member reads it the same way.",
      "member_impact": "Unlabeled or lopsided scales push members toward certain answers.",
      "page_id": null,
      "question_id": "q11",
      "element_id": null,
      "current_text": "Not at all likely ... (no label)",
      "suggested_text": "Not at all likely ... Extremely likely",
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "6.1",
      "severity": "worth_improving",
      "headline": "2 answers below the fold on a phone",
      "evidence": "2 answers below the fold on a phone.",
      "explanation": "Trim or group the answers so the question and its first answers show without scrolling.",
      "member_impact": "Long questions push the answers off the first screen.",
      "page_id": null,
      "question_id": "q6",
      "element_id": null,
      "current_text": null,
      "suggested_text": null,
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "6.2",
      "severity": "worth_improving",
      "headline": "Dropdown with only 4 choices",
      "evidence": "A dropdown with only 4 choices.",
      "explanation": "Use buttons instead; they take one tap, not two.",
      "member_impact": "Long or crowded answers are hard to read and tap on a phone.",
      "page_id": null,
      "question_id": "q5",
      "element_id": null,
      "current_text": null,
      "suggested_text": null,
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "6.2",
      "severity": "worth_improving",
      "headline": "9 answer choices; cut to 8",
      "evidence": "9 answer choices.",
      "explanation": "Group, alphabetize, or trim to 8 or fewer.",
      "member_impact": "Long or crowded answers are hard to read and tap on a phone.",
      "page_id": null,
      "question_id": "q6",
      "element_id": null,
      "current_text": null,
      "suggested_text": null,
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "6.3",
      "severity": "worth_improving",
      "headline": "Grid has 7 rows; split it",
      "evidence": "A grid with 7 rows.",
      "explanation": "Split it into separate questions of 5 rows or fewer.",
      "member_impact": "Wide grids and long scales force sideways scrolling and mis-taps.",
      "page_id": null,
      "question_id": "q3",
      "element_id": null,
      "current_text": null,
      "suggested_text": null,
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "6.3",
      "severity": "worth_improving",
      "headline": "11-point scale is hard to tap",
      "evidence": "A 11-point scale.",
      "explanation": "Use 7 points or fewer; a 0 to 10 scale is hard to tap.",
      "member_impact": "Wide grids and long scales force sideways scrolling and mis-taps.",
      "page_id": null,
      "question_id": "q11",
      "element_id": null,
      "current_text": null,
      "suggested_text": null,
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "6.4",
      "severity": "worth_improving",
      "headline": "\"Click\" is a desktop word",
      "evidence": "\"Click\" is a desktop word.",
      "explanation": "Say \"tap\" and avoid \"left\" or \"right\".",
      "member_impact": "Members on a phone can't click, hover, or drag.",
      "page_id": null,
      "question_id": "q7",
      "element_id": null,
      "current_text": "Click the one you like best.",
      "suggested_text": "Tap the one you like best.",
      "highlight": "Click",
      "source": "auto"
     },
     {
      "criterion_id": "7.2",
      "severity": "worth_improving",
      "headline": "Wide image makes the product small",
      "evidence": "A wide image (1.78 wide for every 1 tall).",
      "explanation": "Crop it to 4:5 (portrait) so the product fills the phone width instead of shrinking to a strip.",
      "member_impact": "At phone width, a wide image makes the product tiny and awkward.",
      "page_id": "p1",
      "question_id": "q1",
      "element_id": "img1",
      "current_text": null,
      "suggested_text": null,
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "7.3",
      "severity": "worth_improving",
      "headline": "Image is too small to show full width",
      "evidence": "400 px wide, shown full width.",
      "explanation": "Use the original file, at least 750 px wide. Never upscale a small one.",
      "member_impact": "Soft or stretched images make products look cheap and hard to judge.",
      "page_id": "p7",
      "question_id": "q7",
      "element_id": "img2",
      "current_text": null,
      "suggested_text": null,
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "7.6",
      "severity": "worth_improving",
      "headline": "Image file is heavy (650 KB)",
      "evidence": "650 KB image.",
      "explanation": "Compress it to under about 500 KB.",
      "member_impact": "Heavy images are slow on cellular, and members using screen readers lose context.",
      "page_id": "p1",
      "question_id": "q1",
      "element_id": "img1",
      "current_text": null,
      "suggested_text": null,
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "7.6",
      "severity": "worth_improving",
      "headline": "Image has no alt text",
      "evidence": "An image has no alt text.",
      "explanation": "Add a short description for screen readers.",
      "member_impact": "Heavy images are slow on cellular, and members using screen readers lose context.",
      "page_id": "p1",
      "question_id": "q1",
      "element_id": "img1",
      "current_text": null,
      "suggested_text": null,
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "8.6",
      "severity": "worth_improving",
      "headline": "No optional comment box near the end",
      "evidence": "No optional comment box near the end.",
      "explanation": "Add one optional question: Anything else you'd like the product team to know?",
      "member_impact": "Members who have something to say feel heard when they get the chance.",
      "page_id": "p11",
      "question_id": null,
      "element_id": null,
      "current_text": null,
      "suggested_text": "Anything else you'd like the product team to know? (optional)",
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "9.1",
      "severity": "worth_improving",
      "headline": "Emoji in a question",
      "evidence": "How much did you LOVE the fit? \ud83e\ude72",
      "explanation": "Remove emoji from questions.",
      "member_impact": "Emoji belong in the intro only.",
      "page_id": null,
      "question_id": "q4",
      "element_id": null,
      "current_text": "How much did you LOVE the fit? \ud83e\ude72",
      "suggested_text": "How much did you LOVE the fit?",
      "highlight": null,
      "source": "auto"
     },
     {
      "criterion_id": "9.2",
      "severity": "worth_improving",
      "headline": "ALL CAPS reads as shouting",
      "evidence": "How much did you LOVE the fit? \ud83e\ude72",
      "explanation": "Write it in normal capitalization; avoid ALL CAPS for emphasis.",
      "member_impact": "Consistent, friendly wording builds trust in every survey.",
      "page_id": null,
      "question_id": "q4",
      "element_id": null,
      "current_text": "How much did you LOVE the fit? \ud83e\ude72",
      "suggested_text": null,
      "highlight": "LOVE",
      "source": "auto"
     }
    ],
    "unchecked": [
     "Inviting, specific title in sentence case",
     "What we're exploring and why this member was asked",
     "Co-creator framing",
     "Don't ask what we already know",
     "No repeats, smooth flow",
     "One idea per question",
     "Grammar and spelling",
     "Consistent terms",
     "Every member can find their answer",
     "A way out when needed",
     "No leading or loaded words",
     "No right answer framing",
     "No anchoring",
     "The right image is there",
     "The product is the hero",
     "Easy, on-topic opener",
     "An insider moment",
     "Only relevant questions",
     "A good energy curve",
     "Warm and human",
     "A genuine thank-you",
     "Impact reminder"
    ],
    "est_minutes": 4.3,
    "promised_minutes": 3.0
   },
   "timeline": [
    {
     "page_id": "p0",
     "seconds": 5
    },
    {
     "page_id": "p1",
     "seconds": 18
    },
    {
     "page_id": "p2",
     "seconds": 30
    },
    {
     "page_id": "p3",
     "seconds": 67
    },
    {
     "page_id": "p4",
     "seconds": 78
    },
    {
     "page_id": "p5",
     "seconds": 88
    },
    {
     "page_id": "p6",
     "seconds": 105
    },
    {
     "page_id": "p7",
     "seconds": 120
    },
    {
     "page_id": "p8",
     "seconds": 162
    },
    {
     "page_id": "p9",
     "seconds": 205
    },
    {
     "page_id": "p10",
     "seconds": 249
    },
    {
     "page_id": "p11",
     "seconds": 257
    },
    {
     "page_id": "p12",
     "seconds": 259
    }
   ],
   "total_seconds": 259,
   "snapshot": {
    "title": "Member's Mark Boxer Briefs Feedback Survey",
    "source_url": "fixture://boxer-briefs",
    "pages": [
     {
      "id": "p0",
      "position": 0,
      "kind": "intro",
      "intro_text": "Welcome to the Boxer Briefs Survey! This takes about 3 minutes."
     },
     {
      "id": "p1",
      "position": 1,
      "kind": "question",
      "questions": [
       {
        "id": "q1",
        "text": "Which Member's Mark Boxer Briefs did you buy?",
        "kind": "single_choice",
        "options": [
         {
          "id": "q1-0",
          "label": "Navy 3-pack"
         },
         {
          "id": "q1-1",
          "label": "Black 3-pack"
         },
         {
          "id": "q1-2",
          "label": "Grey 6-pack"
         }
        ],
        "media": [
         {
          "element_id": "img1",
          "natural_w": 1600,
          "natural_h": 900,
          "rendered_w": 349,
          "rendered_h": 196,
          "bytes": 650000
         }
        ]
       }
      ]
     },
     {
      "id": "p2",
      "position": 2,
      "kind": "question",
      "questions": [
       {
        "id": "q2",
        "text": "How long have you owned them?",
        "kind": "single_choice",
        "options": [
         {
          "id": "q2-0",
          "label": "Under 1 year"
         },
         {
          "id": "q2-1",
          "label": "1 to 5 years"
         },
         {
          "id": "q2-2",
          "label": "5 to 10 years"
         },
         {
          "id": "q2-3",
          "label": "Over 10 years"
         }
        ]
       }
      ]
     },
     {
      "id": "p3",
      "position": 3,
      "kind": "question",
      "questions": [
       {
        "id": "q3",
        "text": "Please indicate your level of agreement with each of the following statements about the aforementioned boxer briefs.",
        "kind": "grid_single",
        "rows": [
         "Statement 1",
         "Statement 2",
         "Statement 3",
         "Statement 4",
         "Statement 5",
         "Statement 6",
         "Statement 7"
        ],
        "scale": {
         "points": 5,
         "low_label": "Strongly disagree",
         "high_label": "Strongly agree"
        }
       }
      ]
     },
     {
      "id": "p4",
      "position": 4,
      "kind": "question",
      "questions": [
       {
        "id": "q4",
        "text": "How much did you LOVE the fit? \ud83e\ude72",
        "kind": "single_choice",
        "options": [
         {
          "id": "q4-0",
          "label": "Not at all"
         },
         {
          "id": "q4-1",
          "label": "A little"
         },
         {
          "id": "q4-2",
          "label": "Somewhat"
         },
         {
          "id": "q4-3",
          "label": "Very much"
         }
        ]
       }
      ]
     },
     {
      "id": "p5",
      "position": 5,
      "kind": "question",
      "questions": [
       {
        "id": "q5",
        "text": "Where do you usually shop for underwear?",
        "kind": "dropdown",
        "options": [
         {
          "id": "q5-0",
          "label": "Sam's Club"
         },
         {
          "id": "q5-1",
          "label": "Walmart"
         },
         {
          "id": "q5-2",
          "label": "Target"
         },
         {
          "id": "q5-3",
          "label": "Online"
         }
        ]
       }
      ]
     },
     {
      "id": "p6",
      "position": 6,
      "kind": "question",
      "questions": [
       {
        "id": "q6",
        "text": "Which of these matter to you?",
        "kind": "multi_choice",
        "options": [
         {
          "id": "q6-0",
          "label": "Fit"
         },
         {
          "id": "q6-1",
          "label": "Comfort"
         },
         {
          "id": "q6-2",
          "label": "Price"
         },
         {
          "id": "q6-3",
          "label": "Fabric"
         },
         {
          "id": "q6-4",
          "label": "Waistband"
         },
         {
          "id": "q6-5",
          "label": "Durability"
         },
         {
          "id": "q6-6",
          "label": "Color"
         },
         {
          "id": "q6-7",
          "label": "Pack size"
         },
         {
          "id": "q6-8",
          "label": "Brand"
         }
        ],
        "options_below_fold": 2,
        "fits_one_screen": false
       }
      ]
     },
     {
      "id": "p7",
      "position": 7,
      "kind": "question",
      "questions": [
       {
        "id": "q7",
        "text": "Click the one you like best.",
        "kind": "single_choice",
        "options": [
         {
          "id": "q7-0",
          "label": "Classic"
         },
         {
          "id": "q7-1",
          "label": "Athletic"
         },
         {
          "id": "q7-2",
          "label": "Relaxed"
         }
        ],
        "media": [
         {
          "element_id": "img2",
          "alt": "Briefs",
          "natural_w": 400,
          "natural_h": 400,
          "rendered_w": 349,
          "rendered_h": 349,
          "bytes": 40000
         },
         {
          "element_id": "img3",
          "alt": "Relaxed fit",
          "loaded": false
         }
        ]
       }
      ]
     },
     {
      "id": "p8",
      "position": 8,
      "kind": "question",
      "questions": [
       {
        "id": "q8",
        "text": "Why did you choose them?",
        "kind": "text_long"
       }
      ]
     },
     {
      "id": "p9",
      "position": 9,
      "kind": "question",
      "questions": [
       {
        "id": "q9",
        "text": "What would you change?",
        "kind": "text_long"
       }
      ]
     },
     {
      "id": "p10",
      "position": 10,
      "kind": "question",
      "questions": [
       {
        "id": "q10",
        "text": "Tell us what else you would like to share?",
        "kind": "text_long"
       }
      ]
     },
     {
      "id": "p11",
      "position": 11,
      "kind": "question",
      "questions": [
       {
        "id": "q11",
        "text": "How likely are you to recommend them?",
        "kind": "rating",
        "scale": {
         "points": 11,
         "low_label": "Not at all likely"
        }
       }
      ]
     },
     {
      "id": "p12",
      "position": 12,
      "kind": "thank_you",
      "text": "Survey complete."
     }
    ]
   }
  },
  {
   "id": "coffee-pods",
   "title": "Help pick our next coffee pod flavor",
   "blurb": "A clean sample. It still cannot be called Ready to launch, because the AI step has not run.",
   "review": {
    "survey_title": "Help pick our next coffee pod flavor",
    "content_hash": "6a6b2fb38a084511c9b4a9c9844785717ebfef6f8f514de6956d22486fc62dbf",
    "rubric_version": "v2",
    "scorecard": {
     "score": 100.0,
     "provisional": true,
     "unchecked_points": 54,
     "by_dimension": {
      "D1": {
       "name": "First impression",
       "earned": 11.0,
       "possible": 11
      },
      "D2": {
       "name": "Respect for members' time",
       "earned": 13.0,
       "possible": 13
      },
      "D3": {
       "name": "Clear questions",
       "earned": 10.0,
       "possible": 10
      },
      "D4": {
       "name": "Fair and complete answers",
       "earned": 9.0,
       "possible": 9
      },
      "D5": {
       "name": "Neutral questions",
       "earned": 7.0,
       "possible": 7
      },
      "D6": {
       "name": "Built for the phone",
       "earned": 11.0,
       "possible": 11
      },
      "D7": {
       "name": "Images that work on a phone",
       "earned": 13.0,
       "possible": 13
      },
      "D8": {
       "name": "Engaging experience",
       "earned": 13.0,
       "possible": 13
      },
      "D9": {
       "name": "Community voice and tone",
       "earned": 6.0,
       "possible": 6
      },
      "D10": {
       "name": "Closing the loop",
       "earned": 7.0,
       "possible": 7
      }
     },
     "open_blockers": [],
     "kept_blockers": [],
     "pending_blockers": [
      "B1",
      "B2",
      "B6"
     ],
     "readiness": "almost_ready",
     "strengths": [
      "Length fits the survey type",
      "Fits on one screen",
      "Phone-friendly shape"
     ]
    },
    "findings": [],
    "unchecked": [
     "Inviting, specific title in sentence case",
     "What we're exploring and why this member was asked",
     "Co-creator framing",
     "Don't ask what we already know",
     "No repeats, smooth flow",
     "One idea per question",
     "Grammar and spelling",
     "Consistent terms",
     "Every member can find their answer",
     "A way out when needed",
     "No leading or loaded words",
     "No right answer framing",
     "No anchoring",
     "The right image is there",
     "The product is the hero",
     "Easy, on-topic opener",
     "An insider moment",
     "Only relevant questions",
     "A good energy curve",
     "Warm and human",
     "A genuine thank-you",
     "Impact reminder"
    ],
    "est_minutes": 1.6,
    "promised_minutes": 2.0
   },
   "timeline": [
    {
     "page_id": "p0",
     "seconds": 6
    },
    {
     "page_id": "p1",
     "seconds": 24
    },
    {
     "page_id": "p2",
     "seconds": 35
    },
    {
     "page_id": "p3",
     "seconds": 47
    },
    {
     "page_id": "p4",
     "seconds": 91
    },
    {
     "page_id": "p5",
     "seconds": 96
    }
   ],
   "total_seconds": 96,
   "snapshot": {
    "title": "Help pick our next coffee pod flavor",
    "source_url": "fixture://coffee",
    "pages": [
     {
      "id": "p0",
      "position": 0,
      "kind": "intro",
      "intro_text": "Thanks for helping shape Member's Mark! This takes about 2 minutes and you'll earn points."
     },
     {
      "id": "p1",
      "position": 1,
      "kind": "question",
      "questions": [
       {
        "id": "q1",
        "text": "Which flavor would you try first?",
        "kind": "image_choice",
        "options": [
         {
          "id": "q1-0",
          "label": "Hazelnut",
          "media": {
           "alt": "Hazelnut",
           "natural_w": 1000,
           "natural_h": 1000,
           "rendered_w": 170,
           "rendered_h": 170,
           "bytes": 90000
          }
         },
         {
          "id": "q1-1",
          "label": "Caramel",
          "media": {
           "alt": "Caramel",
           "natural_w": 1000,
           "natural_h": 1000,
           "rendered_w": 170,
           "rendered_h": 170,
           "bytes": 90000
          }
         },
         {
          "id": "q1-2",
          "label": "Vanilla",
          "media": {
           "alt": "Vanilla",
           "natural_w": 1000,
           "natural_h": 1000,
           "rendered_w": 170,
           "rendered_h": 170,
           "bytes": 90000
          }
         }
        ]
       }
      ]
     },
     {
      "id": "p2",
      "position": 2,
      "kind": "question",
      "questions": [
       {
        "id": "q2",
        "text": "How often do you make coffee at home?",
        "kind": "single_choice",
        "options": [
         {
          "id": "q2-0",
          "label": "Every day"
         },
         {
          "id": "q2-1",
          "label": "A few times a week"
         },
         {
          "id": "q2-2",
          "label": "Rarely"
         }
        ]
       }
      ]
     },
     {
      "id": "p3",
      "position": 3,
      "kind": "question",
      "questions": [
       {
        "id": "q3",
        "text": "Which of these do you buy? Select all that apply.",
        "kind": "multi_choice",
        "options": [
         {
          "id": "q3-0",
          "label": "Pods"
         },
         {
          "id": "q3-1",
          "label": "Whole bean"
         },
         {
          "id": "q3-2",
          "label": "Ground"
         }
        ]
       }
      ]
     },
     {
      "id": "p4",
      "position": 4,
      "kind": "question",
      "questions": [
       {
        "id": "q4",
        "text": "Anything else you'd like the product team to know?",
        "kind": "text_long",
        "required": false
       }
      ]
     },
     {
      "id": "p5",
      "position": 5,
      "kind": "thank_you",
      "text": "Thanks! Your feedback will help shape the next Member's Mark coffee pods."
     }
    ]
   }
  }
 ],
 "dimensions": {
  "D1": "First impression",
  "D2": "Respect for members' time",
  "D3": "Clear questions",
  "D4": "Fair and complete answers",
  "D5": "Neutral questions",
  "D6": "Built for the phone",
  "D7": "Images that work on a phone",
  "D8": "Engaging experience",
  "D9": "Community voice and tone",
  "D10": "Closing the loop"
 },
 "criteria": {
  "1.1": {
   "title": "Inviting, specific title in sentence case",
   "dimension": "D1",
   "points": 2
  },
  "1.2": {
   "title": "What we're exploring and why this member was asked",
   "dimension": "D1",
   "points": 3
  },
  "1.3": {
   "title": "Co-creator framing",
   "dimension": "D1",
   "points": 4
  },
  "1.4": {
   "title": "Honest time estimate and the reward are stated",
   "dimension": "D1",
   "points": 2
  },
  "2.1": {
   "title": "Length fits the survey type",
   "dimension": "D2",
   "points": 5
  },
  "2.2": {
   "title": "Qualifying questions come first",
   "dimension": "D2",
   "points": 3
  },
  "2.3": {
   "title": "Don't ask what we already know",
   "dimension": "D2",
   "points": 2
  },
  "2.4": {
   "title": "Light typing load",
   "dimension": "D2",
   "points": 2
  },
  "2.5": {
   "title": "No repeats, smooth flow",
   "dimension": "D2",
   "points": 1
  },
  "3.1": {
   "title": "One idea per question",
   "dimension": "D3",
   "points": 3
  },
  "3.2": {
   "title": "Plain words",
   "dimension": "D3",
   "points": 2
  },
  "3.3": {
   "title": "Clear instructions and context",
   "dimension": "D3",
   "points": 2
  },
  "3.4": {
   "title": "Grammar and spelling",
   "dimension": "D3",
   "points": 2
  },
  "3.5": {
   "title": "Consistent terms",
   "dimension": "D3",
   "points": 1
  },
  "4.1": {
   "title": "Every member can find their answer",
   "dimension": "D4",
   "points": 3
  },
  "4.2": {
   "title": "No overlapping choices",
   "dimension": "D4",
   "points": 2
  },
  "4.3": {
   "title": "A way out when needed",
   "dimension": "D4",
   "points": 2
  },
  "4.4": {
   "title": "Honest scales",
   "dimension": "D4",
   "points": 2
  },
  "5.1": {
   "title": "No leading or loaded words",
   "dimension": "D5",
   "points": 3
  },
  "5.2": {
   "title": "No right answer framing",
   "dimension": "D5",
   "points": 2
  },
  "5.3": {
   "title": "No anchoring",
   "dimension": "D5",
   "points": 1
  },
  "5.4": {
   "title": "Not a wall of agree/disagree",
   "dimension": "D5",
   "points": 1
  },
  "6.1": {
   "title": "Fits on one screen",
   "dimension": "D6",
   "points": 3
  },
  "6.2": {
   "title": "Short, tappable answer choices",
   "dimension": "D6",
   "points": 2
  },
  "6.3": {
   "title": "Small grids, short scales",
   "dimension": "D6",
   "points": 2
  },
  "6.4": {
   "title": "Thumb-friendly",
   "dimension": "D6",
   "points": 2
  },
  "6.5": {
   "title": "Stays put and renders cleanly",
   "dimension": "D6",
   "points": 2
  },
  "7.1": {
   "title": "The right image is there",
   "dimension": "D7",
   "points": 2
  },
  "7.2": {
   "title": "Phone-friendly shape",
   "dimension": "D7",
   "points": 3
  },
  "7.3": {
   "title": "Sharp and high resolution",
   "dimension": "D7",
   "points": 2
  },
  "7.4": {
   "title": "The product is the hero",
   "dimension": "D7",
   "points": 2
  },
  "7.5": {
   "title": "Fair image choices",
   "dimension": "D7",
   "points": 2
  },
  "7.6": {
   "title": "Readable, light, and accessible",
   "dimension": "D7",
   "points": 2
  },
  "8.1": {
   "title": "Easy, on-topic opener",
   "dimension": "D8",
   "points": 2
  },
  "8.2": {
   "title": "Format variety that fits the content",
   "dimension": "D8",
   "points": 2
  },
  "8.3": {
   "title": "An insider moment",
   "dimension": "D8",
   "points": 4
  },
  "8.4": {
   "title": "Only relevant questions",
   "dimension": "D8",
   "points": 2
  },
  "8.5": {
   "title": "A good energy curve",
   "dimension": "D8",
   "points": 2
  },
  "8.6": {
   "title": "Room to speak freely",
   "dimension": "D8",
   "points": 1
  },
  "9.1": {
   "title": "Warm and human",
   "dimension": "D9",
   "points": 4
  },
  "9.2": {
   "title": "Follows the content standards",
   "dimension": "D9",
   "points": 2
  },
  "10.1": {
   "title": "A genuine thank-you",
   "dimension": "D10",
   "points": 4
  },
  "10.2": {
   "title": "Reward confirmed (inactive)",
   "dimension": "D10",
   "points": 0
  },
  "10.3": {
   "title": "Impact reminder",
   "dimension": "D10",
   "points": 3
  },
  "10.4": {
   "title": "What happens next (inactive until Q4 2026)",
   "dimension": "D10",
   "points": 0
  },
  "10.5": {
   "title": "How was this survey (inactive)",
   "dimension": "D10",
   "points": 0
  },
  "B1": {
   "title": "Leading question on the main research topic",
   "dimension": "blocker",
   "points": 0
  },
  "B2": {
   "title": "No valid answer",
   "dimension": "blocker",
   "points": 0
  },
  "B3": {
   "title": "Late screen-out",
   "dimension": "blocker",
   "points": 0
  },
  "B4": {
   "title": "No intro page",
   "dimension": "blocker",
   "points": 0
  },
  "B5": {
   "title": "Broken time promise",
   "dimension": "blocker",
   "points": 0
  },
  "B6": {
   "title": "Asks for personal details it does not need",
   "dimension": "blocker",
   "points": 0
  },
  "B7": {
   "title": "Members can't see what they're asked to judge",
   "dimension": "blocker",
   "points": 0
  }
 }
};
