import streamlit as st
from components.icons import get_orient_ia_logo, get_ispm_logo, render_html


def render_header(titre, sous_titre=""):
    render_html(
        f"""
        <div class="page-header">
            <div class="app-header-brand">
                <div class="page-header-logo">{get_orient_ia_logo()}</div>
                <div>
                    <div class="page-header-title">{titre}</div>
                    <div class="page-header-subtitle">{sous_titre}</div>
                </div>
            </div>
            <div class="app-header-brand">
                {get_ispm_logo()}
                <div>
                    <div class="app-header-ispm-title">ISPM</div>
                    <div class="app-header-ispm-subtitle">Institut Supérieur Polytechnique<br>de Madagascar</div>
                </div>
            </div>
        </div>
        <hr class="app-header-divider" />
        """
    )


def render_dashboard_header():
    render_html(
        f"""
        <div class="app-header">
            <div class="app-header-brand">
                {get_orient_ia_logo()}
                <div>
                    <div class="app-header-title">ORIENT'IA</div>
                    <div class="app-header-subtitle">Plateforme d'Orientation &amp; Assistant</div>
                </div>
            </div>
            <div class="app-header-brand">
                {get_ispm_logo()}
                <div>
                    <div class="app-header-ispm-title">ISPM</div>
                    <div class="app-header-ispm-subtitle">Institut Supérieur Polytechnique<br>de Madagascar</div>
                </div>
            </div>
        </div>
        <hr class="app-header-divider" />
        """
    )
