# Provenance Guard: Automated Content Verification & Lifecycle Tracker

**Course:** CodePath AI201  
**Project:** Project 4 — Provenance Guard  
**Status:** Completed (Milestones 1–6)

---

## 📺 Walkthrough Video
[👉 Click here to watch my 2-minute project walkthrough video!](https://youtu.be/3DqiKy8pHkQ)

---

## 🚀 Project Overview & Architecture
Provenance Guard is an independent content tracking and validation backend built using Flask and SQLite. The system protects creative attribution by analyzing incoming text strings, maintaining an unalterable database audit trail, tracking a strict state machine lifecycle (`classified` ➔ `under review`), and deploying IP-based token-bucket rate limiting to secure endpoint availability.

---

## 📊 Detection Signals & Confidence Scoring Philosophy

### Why These Signals?
Our architecture relies on a hybrid detection approach combining **LLM-driven linguistic pattern analysis** (via the Groq API) and a lightweight **stylometric variation metric** calculated locally. 
* **Groq API Signal:** Leverages a high-capacity model to identify systemic probabilistic choices in text structure, semantic uniformness, and stereotypical AI transitional phrasing.
* **Stylometric Signal:** Measures text complexity variation (sentence lengths, token variation, and character-to-word density ratios). True human writing exhibits variable punctuation pacing and uneven length distributions, whereas base AI outputs lean toward balanced distributions.

### Scoring Approach & Real-World Evolution
The system averages the standard probability vector from Groq with the stylometric complexity variance to produce a unified metric between `0.0` (Absolute Human) and `1.0` (Absolute AI). 

*If deploying this for a real-world enterprise production platform*, we would replace the local averaging formula with a specialized random forest classification layer trained on domain-specific user writing samples, and incorporate cryptographic browser/device fingerprinting to track client-side pasting habits.

### Scoring Variation Proof (From Milestone 4 Data)
The scoring pipeline demonstrates clear, meaningful data distribution variance rather than returning a flat baseline constant:
* **High-Confidence Human Case (`Score: 0.170`)**: Triggered by casual, lower-case, highly conversational text (*"ok so i finally tried that new ramen place..."*). The low score reflects high stylometric entropy and minimal predictable text patterns.
* **Lower-Confidence/Unclear Case (`Score: 0.703`)**: Triggered by dense, formal academic text (*"The relationship between monetary policy and asset price..."*). The elevated score reflects uniform sentence patterns that mathematically mimic low-entropy AI generations.

---

## 🏷️ Transparency Label Variants (Written Descriptions)

The system maps scores into three distinct structural text labels exposed to client applications:

1. **High-Confidence Human Variant (`Combined Score < 0.35`)**
   * **Exact Display Text:** `Verified Authentic: This content matches patterns consistent with original human composition and diverse linguistic structure.`
2. **High-Confidence AI Variant (`Combined Score > 0.75`)**
   * **Exact Display Text:** `Generated Content: Analysis indicates a exceptionally high probability of automated algorithmic synthesis. Attribution context recommended.`
3. **Uncertain / Mixed Variant (`0.35 <= Combined Score <= 0.75`)**
   * **Exact Display Text:** `Linguistic Origin Unclear: This text contains a blend of stylistic patterns that prevent definitive automated attribution. Audiences are encouraged to evaluate context independently.`

---

## 📝 Technical Reflection & Known Limitations

### Specific System Weakness
Our system will consistently misclassify **highly polished professional copy, legal briefs, and formal academic prose** written genuinely by humans, marking them as `Linguistic Origin Unclear` or even false-positive AI. 

### Core Reason
This limitation is fundamentally bound to our signals rather than data volume. Academic prose demands strict adherence to uniform structural rhythms, explicit objective transitions (*"Furthermore," "Consequently," "It is important to note"*), and static sentence lengths. Because base LLMs are trained heavily on these exact clean structures to maximize clarity, highly structured human text maps identically to the low-entropy, uniform stylometric profiles our system flags as machine-made.

---

## 🔄 Spec Reflection

* **How the Spec Guided Implementation:** The specification's strict mandate for atomic audit logging forced us to think deeply about database reliability before touching frontend layers. Building the database layout to record immutable markers (`groq_score`, `stylometric_score`, `content_id`) directly alongside incoming payloads guaranteed that subsequent state mutations could never compromise historical auditing tracks.
* **How We Diverged & Why:** The initial layout expected a linear processing loop, but during Milestone 4 testing, we decoupled the `/appeal` endpoint state transition logic into an independent, non-destructive conditional database check. Instead of overwriting or re-running the classification engine (which would pollute original telemetry records), the system overrides the `lifecycle_status` property smoothly while leaving the primary algorithmic provenance flags unmodified.

---

## 🤖 AI Usage Section

1. **Instance 1 (PowerShell Stress-Testing Script Layout)**
   * *What I Directed AI to Do:* Help draft a PowerShell command to execute rapid parallel loop requests against a local Flask endpoint to check for server stability.
   * *What It Produced:* A simple `Invoke-WebRequest` loop block.
   * *What I Revised/Overrode:* The original AI output did not account for how PowerShell's pipeline naturally handles non-200 responses. When the rate limiter began firing back raw `429 Too Many Requests` HTML error data, the pipeline choked. I rewrote the block to wrap the call inside an explicit `try/catch` block that accurately parses `[int]$_.Exception.Response.StatusCode`, transforming a breaking exception into clean log tracking.
2. **Instance 2 (Stylometric Metric Normalization Logic)**
   * *What I Directed AI to Do:* Provide a Python formula to check character-to-word variation and return a clean `0.0` to `1.0` balance value.
   * *What It Produced:* A highly complex function utilizing standard deviation weights across long dictionaries.
   * *What I Revised/Overrode:* The produced function had immense performance overhead and broke when handling small, casual user texts (causing zero-division errors). I discarded the multi-tier statistical library code and rewrote a lightweight string length ratio method containing defensive boundary checks (`if len(words) == 0: return 0.0`) to handle raw terminal testing strings elegantly.

---

## ⏱️ Rate Limiting Evidence (10 requests / min)

Under stress-testing conditions via a rapid PowerShell execution loop, the system successfully throttles traffic, moving from healthy creations (`201 Created`) to rejection states (`429 Too Many Requests`) once the window threshold is crossed.

```text
Request 1 : 201
Request 2 : 201
Request 3 : 201
Request 4 : 201
Request 5 : 201
Request 6 : 201
Request 7 : 201
Request 8 : 201
Request 9 : 201
Request 10 : 201
Request 11 : 429 Too Many Requests (10 per 1 minute)
Request 12 : 429 Too Many Requests (10 per 1 minute)
```

Note: More full examples are found in `rate_limiting_example.txt`, with 429 errors occuring on lines 627 and below, and example queries shown from lines 1-627

---

### 🗄️ Structured Audit Log Sample (GET /log)
The database architecture captures a complete history of the tracking pipeline using a structured schema layout. Below is a sample from the live endpoint showing an anonymous user submission, an AI edge-case test, and an active appeal state change:

```json 
[
  {
    "content_id": "0427b510-d910-4db9-bac0-c1a46be2b652",
    "creator_id": "user_45",
    "timestamp": "2026-06-24T18:53:33.598806Z",
    "text_preview": "ok so i finally tried that new ramen place downtown and hone...",
    "groq_score": 0.21,
    "stylometric_score": 0.09599999999999997,
    "combined_score": 0.1701,
    "assigned_label": "Verified Authentic: This content matches patterns consistent with original human composition and diverse linguistic structure.",
    "lifecycle_status": "under review",
    "creator_reasoning": "This is my personal original creative food blog description written completely from memory."
  },
  {
    "content_id": "1a824261-601f-4ad4-8e9e-9e07400a5989",
    "creator_id": "test_ai",
    "timestamp": "2026-06-24T18:58:59.704630Z",
    "text_preview": "Artificial intelligence represents a transformative paradigm...",
    "groq_score": 0.87,
    "stylometric_score": 0.40888888888888886,
    "combined_score": 0.7086111111111111,
    "assigned_label": "Linguistic Origin Unclear: This text contains a blend of stylistic patterns that prevent definitive automated attribution.",
    "lifecycle_status": "classified",
    "creator_reasoning": ""
  },
  {
    "content_id": "e518fe6b-87e5-4623-b09d-f80eae9cfba8",
    "creator_id": "ratelimit-test",
    "timestamp": "2026-06-24T19:00:01.249712Z",
    "text_preview": "This is a test submission for rate limit testing purposes on...",
    "groq_score": 0.42,
    "stylometric_score": 0.5,
    "combined_score": 0.448,
    "assigned_label": "Linguistic Origin Unclear: This text contains a blend of stylistic patterns that prevent definitive automated attribution.",
    "lifecycle_status": "classified",
    "creator_reasoning": ""
  }
]
```
--- 

### 🛠️ Local Setup Instructions
* **Clone & Environment Setup:**

```Bash
   git clone <your-repo-url>
   cd ai201-project4-provenance-guard
   python -m venv .venv
   source .venv/Scripts/Activate  # PowerShell: .venv\Scripts\Activate.ps1
   pip install -r requirements.txt
```

* **Environment Variables:**
* Create a .env file in the root directory and add your Groq API credentials:

```Plaintext
   GROQ_API_KEY=your_actual_api_key_here
   FLASK_ENV=development
```

* **Run the Server:**

```Bash
   flask run
```