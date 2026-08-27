from components.icons import render_html

TEXTE_MENTION = (
    "ORIENT'IA constitue un outil d'aide à l'orientation. Ses recommandations ne remplacent "
    "ni l'avis d'un conseiller pédagogique ni une décision officielle d'admission."
)


def render_mention_banner():
    render_html(
        f"""
        <div class="mention-banner">
            <span class="material-symbols-outlined">verified</span>
            <span>{TEXTE_MENTION}</span>
        </div>
        """
    )


def render_footer():
    render_html(
        """
        <div class="app-footer">
            <strong>ORIENT'IA</strong> — Institut Supérieur Polytechnique de Madagascar (ISPM)
        </div>
        """
    )
