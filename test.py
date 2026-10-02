import streamlit as st

col1, col2 = st.columns(2)

with col1:
    st.pills("Lang", ["🇹🇷 TR", "🇬🇧 EN"], default="🇹🇷 TR")

with col2:
    html_code = """
    <style>
    .custom-info-pill {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border: 1px solid rgba(250, 250, 250, 0.2);
        border-radius: 1rem;
        padding: 0.25rem 0.75rem;
        font-size: 14px;
        color: rgba(250, 250, 250, 0.8);
        background-color: transparent;
        cursor: help;
        position: relative;
        white-space: nowrap;
        height: 33px;
        font-family: "Source Sans Pro", sans-serif;
    }
    .custom-info-pill:hover {
        border-color: rgba(250, 250, 250, 0.5);
        color: rgba(250, 250, 250, 1);
    }
    .custom-info-pill .tooltiptext {
        visibility: hidden;
        width: 320px;
        background-color: #262730;
        color: #fff;
        text-align: left;
        border-radius: 0.5rem;
        padding: 12px;
        position: absolute;
        z-index: 999999;
        top: 130%;
        left: 50%;
        transform: translateX(-50%);
        opacity: 0;
        transition: opacity 0.2s;
        font-weight: normal;
        font-size: 14px;
        border: 1px solid rgba(250, 250, 250, 0.2);
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
        white-space: normal;
        line-height: 1.4;
    }
    .custom-info-pill:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
    </style>
    <div class="custom-info-pill">
        ❓ Bilgi
        <span class="tooltiptext">Bu bir test metnidir ve tooltip içinde görünmelidir. Taşıp taşmadığını test ediyoruz.</span>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)
