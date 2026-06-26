import streamlit as st
import langcodes
import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import DetectorFactory, LangDetectException, detect
from nltk.tokenize import TreebankWordDetokenizer, wordpunct_tokenize
from spellchecker import SpellChecker
DetectorFactory.seed = 0
MIN_INPUT_LENGTH = 3
SPELL_LANGS = {
 "en", "es", "fr", "pt", "de",
 "ru", "ar", "eu", "lv", "nl"
 }

TARGET_LANGS = {
"Vietnamese": "vi",
"English": "en",
"French": "fr",
"Japanese": "ja",
"Chinese": "zh-CN",
"Korean": "ko",
"Spanish": "es",
"German": "de",
}
EXAMPLES_T = [
"Every morning, I drink a cup of coffee.",
"Bonjour, comment allez-vous?",
"Xin chao, hom nay troi dep qua.",
]

EXAMPLES_S = [
"Yesturday, I recieveed a mesage from my freind.",
"Definately a great oppurtunity.",
"Je voudraiis allerr au marchee.",
]
@st.cache_resource(show_spinner=False)
def get_spellchecker(code):
    return SpellChecker(language=code)


def language_name(code):
    try:
        return langcodes.Language.get(code).display_name()
    except Exception:
        return code or "Unknow"
def detect_language(raw):
    try:
        return detect(raw)
    except LangDetectException:
        return None

languages = detect_language("hello how arre you")
print(language_name(languages))



def fix_typos(text, code):
    spell = get_spellchecker(code)
    tokens = wordpunct_tokenize(text)
    fixed = []
    for token in tokens:
        if token.isalpha() and len(token) > 1:
            suggestion = spell.correction(token.lower()) or token
            suggestion = suggestion.title() if token.istitle() else suggestion
            suggestion = suggestion.upper() if token.isupper() else suggestion
            fixed.append(suggestion)
        else:
            fixed.append(token)
    return TreebankWordDetokenizer().detokenize(fixed), fixed != tokens  #trả về tuple 2 text(nối cái list đó lại thành câu ) và changed(True, nếu có đổi false nếu ko)



def run_translation(text, target_code):
    raw = text.strip()

    if len(raw) < MIN_INPUT_LENGTH:
        return {
            "ok": False,
            "error": f"Nhập tối thiểu {MIN_INPUT_LENGTH} ký tự."
        }

    source = detect_language(raw)

    if source is None:
        return {
            "ok": False,
            "error": "Không nhận diện được ngôn ngữ."
        }

    if source == target_code:
        return {
            "ok": True,
            "source": language_name(source),
            "target": language_name(target_code),
            "translated": raw,
            "note": "Câu đã ở ngôn ngữ đích, không cần dịch."
        }

    try:
        translated = GoogleTranslator(
            source=source,
            target=target_code
        ).translate(raw)

        return {
            "ok": True,
            "source": language_name(source),
            "target": language_name(target_code),
            "translated": translated
        }

    except Exception as e:
        return {
            "ok": False,
            "error": f"Lỗi dịch: {e}"
        }
    return {
        "ok": True,
        "source": language_name(source),
        "target": language_name(target_code),
        "translated": translated,
}


def run_spellcheck(text):
    raw = text.strip()

    if len(raw) < MIN_INPUT_LENGTH:
        return {
            "ok": False,
            "error": f"Nhập tối thiểu {MIN_INPUT_LENGTH} ký tự."
        }

    code = detect_language(raw)

    if code is None:
        return {
            "ok": False,
            "error": "Không nhận diện được ngôn ngữ."
        }

    if code not in SPELL_LANGS:
        return {
            "ok": False,
            "error": f"pyspellchecker chưa hỗ trợ {language_name(code)} ({code}).",
        }

    fixed, changed = fix_typos(raw, code)

    return {
        "ok": True,
        "language": language_name(code),
        "fixed": fixed,
        "changed": changed,
    }

st.set_page_config(page_title="NLP Pipeline Demo", layout="centered")
st.title("Streamlit NLP Pipeline Demo")
st.caption("Hai ứng dụng: Dịch văn bản- Sửa lỗi chính tả")
tab_t, tab_s = st.tabs(["Dịch văn bản", "Sửa lỗi chính tả"])


with tab_t:
    st.session_state.setdefault("res_t",None)
    with st.expander("Example"):
        for ex in EXAMPLES_T:
            st.markdown(f"-{ex}")
    with st.form("form_translate"):
        text_t = st.text_area(
            "Câu cần dịch",
            height = 90,
            placeholder= "Nhập câu ở bất kì ngôn ngữ nào"
        )
        targeted = st.selectbox("Dịch sang",list(TARGET_LANGS.keys()))
        submitted_t = st.form_submit_button("Dịch",type ="primary")
    if submitted_t:
        st.session_state.res_t = run_translation(text_t,TARGET_LANGS[targeted])
    clear = st.button("Clear")
    res = st.session_state.res_t
    if res:
        if res["ok"]:
            st.caption(f"Nguồn: {res['source']}-> Đích: {res['target']}")
            st.write(res["translated"])
            if res.get("note"):
                st.info(res["note"])
        else:
            st.warning(res["error"])

with tab_s:
    st.session_state.setdefault("res_s", None)

    with st.expander("Ví dụ"):
        for ex in EXAMPLES_S:
            st.markdown(f"- {ex}")

    st.caption(f"Hỗ Trợ: {', '.join(sorted(SPELL_LANGS))}")

    with st.form("form_spell"):
        text_s = st.text_area(
            "Câu cần kiểm tra",
            height=90,
            placeholder="Nhập câu để kiểm tra chính tả..."
        )

        submitted_s = st.form_submit_button(
            "Kiểm tra",
            type="primary"
        )

    if submitted_s:
        st.session_state.res_s = run_spellcheck(text_s)

    res = st.session_state.res_s

    if res:
        if res["ok"]:
            st.caption(f"Ngôn ngữ: {res['language']}")
            st.write(res["fixed"])
            st.caption(
                "Có sửa lỗi chính tả"
                if res["changed"]
                else "Không phát hiện lỗi"
            )
        else:
            st.warning(res["error"])