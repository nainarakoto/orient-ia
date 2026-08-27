import base64
import textwrap
from pathlib import Path

ASSETS_DIR = Path(__file__).resolve().parent.parent / "assets" / "logos"

ORIENT_IA_LOGO_SVG = """
<svg width="44" height="44" viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg">
    <path d="M22 3 L40 13 V31 L22 41 L4 31 V13 Z" fill="#1F6D3C"/>
    <path d="M22 3 L40 13 L22 23 L4 13 Z" fill="#2E8B4E"/>
    <path d="M15 22 L20 27 L30 15" fill="none" stroke="#FFFFFF" stroke-width="2.6"
          stroke-linecap="round" stroke-linejoin="round"/>
</svg>
"""

ISPM_LOGO_SVG = """
<svg width="44" height="44" viewBox="0 0 44 44" xmlns="http://www.w3.org/2000/svg">
    <circle cx="22" cy="22" r="20" fill="#FFFFFF" stroke="#1F6D3C" stroke-width="2"/>
    <text x="22" y="26" text-anchor="middle" font-family="Sora, sans-serif" font-size="11"
          font-weight="700" fill="#1F6D3C">ISPM</text>
</svg>
"""


def _logo_fichier(nom_fichier):
    chemin = ASSETS_DIR / nom_fichier
    if chemin.exists():
        encodee = base64.b64encode(chemin.read_bytes()).decode()
        extension = chemin.suffix.lstrip(".")
        return f'<img src="data:image/{extension};base64,{encodee}" class="logo-image" />'
    return None


def get_orient_ia_logo():
    return _logo_fichier("orient-ia.png") or ORIENT_IA_LOGO_SVG


def get_ispm_logo():
    return _logo_fichier("logo_ispm.png") or ISPM_LOGO_SVG


def render_html(html):
    """Affiche un bloc HTML multi-lignes sans jamais le laisser passer pour un bloc
    de code Markdown (bug connu de Streamlit quand le texte est indenté).
    Toujours utiliser cette fonction plutôt que st.markdown(..., unsafe_allow_html=True)
    pour du HTML sur plusieurs lignes."""
    import streamlit as st

    st.markdown(textwrap.dedent(html).strip(), unsafe_allow_html=True)


def inject_global_head():
    import streamlit as st

    st.markdown(
        textwrap.dedent(
            """
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined" />
            <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" />
            """
        ).strip(),
        unsafe_allow_html=True,
    )
