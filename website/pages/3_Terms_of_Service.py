"""
Terms of Service page for PsychAI / FrAInd.ly
"""

import streamlit as st

st.set_page_config(
    page_title="Terms of Service — FrAInd.ly",
    page_icon="🧠",
    layout="centered",
)

st.markdown("""<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
.stApp { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
#MainMenu, footer { visibility: hidden; }
.stDeployButton { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }
[data-testid="stHeader"] { display: none !important; }
.main .block-container {
    max-width: 720px !important;
    margin: 0 auto;
    padding: 2rem 1.5rem 4rem !important;
}
.back-link {
    display: inline-flex; align-items: center; gap: 0.4rem;
    color: #71717a; font-size: 0.85rem; text-decoration: none;
    margin-bottom: 1.5rem; transition: color 0.2s;
}
.back-link:hover { color: #a1a1aa; }
.tos-title {
    font-size: 2rem; font-weight: 700; color: #fafafa;
    margin-bottom: 0.25rem;
}
.tos-updated {
    font-size: 0.82rem; color: #52525b; margin-bottom: 2.5rem;
}
.tos h3 {
    font-size: 1.1rem; font-weight: 600; color: #e4e4e7;
    margin: 2rem 0 0.5rem;
}
.tos p, .tos li {
    font-size: 0.92rem; color: #a1a1aa; line-height: 1.75;
}
.tos ul { padding-left: 1.25rem; }
.tos li { margin-bottom: 0.35rem; }
.tos strong { color: #d4d4d8; }
</style>""", unsafe_allow_html=True)

st.markdown("""
    <a href="/" target="_self" class="back-link">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none"
             stroke="currentColor" stroke-width="2" stroke-linecap="round">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
        </svg>
        Back to home
    </a>
""", unsafe_allow_html=True)

st.markdown("""
<div class="tos-title">Terms of Service</div>
<div class="tos-updated">Last updated: March 2026</div>

<div class="tos">

<p>By using FrAInd.ly ("the Service"), you acknowledge and agree to the following terms.
Please read them carefully before using the platform.</p>

<h3>1. Nature of the Service</h3>
<p>FrAInd.ly is an <strong>AI-powered conversational tool</strong> designed to provide
general emotional support and coping strategies for young adults. It is
<strong>not a licensed therapist, counselor, psychologist, or medical professional</strong>.
The Service does not provide therapy, clinical diagnoses, medical advice,
or treatment of any kind.</p>

<h3>2. No Professional Relationship</h3>
<p>Use of the Service does not establish a therapist-client, doctor-patient,
or any other professional relationship. The AI's responses are generated from
patterns in training data and should not be treated as professional guidance.</p>

<h3>3. Not a Substitute for Professional Help</h3>
<p>The Service is intended to complement — <strong>never replace</strong> — professional
mental health care, human connection, or social support. If you are
experiencing a mental health crisis, suicidal thoughts, or any medical
emergency, please:</p>
<ul>
    <li>Call <strong>988</strong> (Suicide &amp; Crisis Lifeline)</li>
    <li>Text <strong>HOME</strong> to <strong>741741</strong> (Crisis Text Line)</li>
    <li>Call <strong>911</strong> or your local emergency services</li>
    <li>Reach out to a trusted adult, counselor, or healthcare provider</li>
</ul>

<h3>4. No Diagnoses or Prescriptions</h3>
<p>The Service will never diagnose conditions, prescribe medication, or
recommend specific treatments. Any information provided is general in
nature and not tailored to your individual clinical needs.</p>

<h3>5. Limitation of Liability</h3>
<p>The Service is provided <strong>"as is"</strong> without warranties of any kind,
express or implied. FrAInd.ly, its creators, and contributors shall not be
held liable for any damages, harm, or adverse outcomes arising from
the use of or reliance on the Service, including but not limited to
emotional distress, delayed treatment, or decisions made based on
AI-generated responses.</p>

<h3>6. Privacy &amp; Data</h3>
<p>We store conversation data to maintain chat history within your account.
Your data is encrypted in transit and stored securely. We do not sell or
share your personal information with third parties. You may request
deletion of your data at any time by contacting us.</p>

<h3>7. Appropriate Use</h3>
<p>You agree not to use the Service to:</p>
<ul>
    <li>Seek emergency medical or psychiatric care (call 911 or 988 instead)</li>
    <li>Generate harmful, abusive, or illegal content</li>
    <li>Misrepresent AI responses as professional medical or legal advice</li>
    <li>Attempt to extract or reverse-engineer the underlying model</li>
</ul>

<h3>8. Age Requirement</h3>
<p>The Service is intended for users aged <strong>13 and older</strong>. Users under
18 are encouraged to use the Service with the awareness of a
parent or guardian.</p>

<h3>9. Changes to Terms</h3>
<p>We reserve the right to update these terms at any time. Continued use
of the Service after changes constitutes acceptance of the revised terms.</p>

<h3>10. Contact</h3>
<p>For questions about these terms or to request data deletion, please
reach out through the contact information provided on our platform.</p>

</div>
""", unsafe_allow_html=True)
