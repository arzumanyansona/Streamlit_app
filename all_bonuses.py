import pandas as pd
import streamlit as st
import plotly.express as px
from streamlit_plotly_events import plotly_events

# --- Loaders ---
def load_data():
    return pd.read_csv("all_data.csv")
    )

def load_freespin_data():
    return pd.read_csv("freespin_per_game_data.csv")
    )

def get_clicked_index(event_data):
    if not event_data:
        return None
    return event_data[0].get('pointIndex') or event_data[0].get('pointNumber')

# --- Main ---
def show_all_bonuses():
    # ===============================
    # Part 1: Bonus Inefficiency Analysis
    # ===============================
    data = load_data()
    
    negative_ngrs = data[data['CasinoNGR_EUR_no_jpot_total'] < 0].copy()
    positive_GGR = negative_ngrs[negative_ngrs['CasinoGGR_EUR_no_jpot_total'] >= 0]

    bonuses_features = [
        'CasinoWageringCost_EUR_total', 'FreespinCost_EUR_total',
        'HarmonyFreespin_EUR_total', 'LuckyWheelCost_EUR_total',
        'CasinoCashback_EUR_total', 'CasinoCorrection_EUR_total',
        'LoyaltyCost_EUR_total'
    ]

    st.title("Bonus Inefficiency Analysis")

    summary = negative_ngrs[bonuses_features].sum().sort_values(ascending=False).reset_index()
    summary.columns = ['BonusFeature', 'Total(EUR)']

    col1, col2 = st.columns([3, 3])

    with col1:
        st.write("Summary of bonuses:")
        st.dataframe(summary)

        fig = px.pie(
            summary,
            values="Total(EUR)",
            names="BonusFeature",
            title="Bonuses Distribution",
            width=500,
            height=500
        )
        fig.update_traces(textposition='inside', textinfo='percent')
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        option = st.selectbox(
            "Select client group to analyze:",
            ("Negative NGR Clients", "Negative NGR with Positive GGR Clients")
        )

        option_1 = st.selectbox(
            "Select bonus feature to analyze:",
            bonuses_features
        )

        bonus_name_clean = option_1.replace('_EUR_total', '')

        if option == "Negative NGR Clients":
            new_col = 'CasinoNGR_EUR_no_jpot_total_new'
            negative_ngrs[new_col] = negative_ngrs['CasinoNGR_EUR_no_jpot_total'] + negative_ngrs[option_1]
            new_data = negative_ngrs[negative_ngrs[new_col] < 0]

            st.write(f"Negative NGR clients count: {negative_ngrs.shape[0]}")
            st.markdown("<br>", unsafe_allow_html=True) 
            st.write(f"Negative NGR clients count after removing bonus '{bonus_name_clean}': {new_data.shape[0]}")

        else:
            new_col = 'CasinoNGR_EUR_no_jpot_total_new'
            positive_GGR[new_col] = positive_GGR['CasinoNGR_EUR_no_jpot_total'] + positive_GGR[option_1]
            new_data = positive_GGR[positive_GGR[new_col] < 0]

            st.write(f"Negative NGR with positive GGR clients count: {positive_GGR.shape[0]}")
            st.markdown("<br>", unsafe_allow_html=True)  
            st.write(f"Negative NGR clients count after removing bonus '{bonus_name_clean}': {new_data.shape[0]}")

    # ===============================
    # Part 2: Freespin per Game Analysis
    # ===============================
    st.markdown("---")
    st.header("Freespin Per Game Analysis")

    free_data = load_freespin_data()

    free_negative_ngrs = free_data[free_data['CasinoNGR_EUR_no_jpot_total'] < 0].copy()
    free_positive_GGR = free_negative_ngrs[free_negative_ngrs['CasinoGGR_EUR_no_jpot_total'] >= 0]

    # Example: only numeric freespin-related columns
    freespin_features = ['EGT FreeSpin_Cost_EUR', 'FreeSpin SayYo_Cost_EUR',
       'FreeSpin_0 Evoplay_Cost_EUR', 'FreeSpin_0 Playtech_Cost_EUR',
       'FreeSpin_0 Popok_Cost_EUR', 'FreeSpin_0 TopGame_Cost_EUR',
       'FreeSpin_Cost_EUR', 'GoldenChipWin_Cost_EUR',
       'PatePlay Freespin_Cost_EUR']

    free_summary = free_data[freespin_features].sum().sort_values(ascending=False).reset_index()
    free_summary.columns = ['FreespinFeature', 'Total(EUR)']

    col3, col4 = st.columns([3, 3])

    with col3:
        st.write("Summary of freespin usage:")
        st.dataframe(free_summary)

        fig2 = px.pie(
            free_summary,
            values="Total(EUR)",
            names="FreespinFeature",
            title="Freespin Distribution",
            width= 500,
            height= 500
        )
        fig2.update_traces(textposition='inside', textinfo='percent')
        st.plotly_chart(fig2, use_container_width=True)

    with col4:
        option_fs = st.selectbox(
            "Select client group to analyze (freespin data):",
            ("Negative NGR Clients", "Negative NGR with Positive GGR Clients")
        )

        option_fs_feature = st.selectbox(
            "Select freespin feature to analyze:",
            freespin_features
        )

        fs_name_clean = option_fs_feature.replace('_EUR_total', '')

        if option_fs == "Negative NGR Clients":
            new_col_fs = 'CasinoNGR_EUR_no_jpot_total_new'
            free_negative_ngrs[new_col_fs] = free_negative_ngrs['CasinoNGR_EUR_no_jpot_total'] + free_negative_ngrs[option_fs_feature]
            new_data_fs = free_negative_ngrs[free_negative_ngrs[new_col_fs] < 0]

            st.write(f"Negative NGR clients count: {free_negative_ngrs.shape[0]}")
            st.markdown("<br>", unsafe_allow_html=True) 
            st.write(f"Negative NGR clients count after removing '{fs_name_clean}': {new_data_fs.shape[0]}")

        else:
            new_col_fs = 'CasinoNGR_EUR_no_jpot_total_new'
            free_positive_GGR[new_col_fs] = free_positive_GGR['CasinoNGR_EUR_no_jpot_total'] + free_positive_GGR[option_fs_feature]
            new_data_fs = free_positive_GGR[free_positive_GGR[new_col_fs] < 0]

            st.write(f"Negative NGR with positive GGR clients count: {free_positive_GGR.shape[0]}")
            st.markdown("<br>", unsafe_allow_html=True)  
            st.write(f"Negative NGR clients count after removing '{fs_name_clean}': {new_data_fs.shape[0]}")

if __name__ == "__main__":
    show_all_bonuses()
