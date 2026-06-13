import streamlit as st
from agent import analyse

st.set_page_config(
    page_title="Crypto Intelligence Agent",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Crypto Intelligence Agent")
st.caption("Enter a coin ticker or name to generate a live research report.")

# Input
coin_input = st.text_input(
    label="Cryptocurrency",
    placeholder="e.g. ETH, BTC, SOL, BNB",
    max_chars=20
)

analyse_button = st.button("Analyse", type="primary")

if analyse_button:
    if not coin_input.strip():
        st.warning("Please enter a coin ticker or name.")
    else:
        with st.spinner(f"Analysing {coin_input.upper()}..."):
            result = analyse(coin_input)

        if "error" in result:
            st.error(result["error"])
        else:
            # Header metrics
            st.subheader(f"{result['name']} ({result['coin']})")
            col1, col2, col3 = st.columns(3)
            col1.metric("Mark Price", f"${result['mark_price']:,.2f}")
            col2.metric("Funding Rate", f"{result['funding_rate']:.4f}%")
            col3.metric("Open Interest", f"{result['open_interest']:,.0f}")

            st.divider()

            # Report
            st.markdown("### 📝 Research Report")
            st.markdown(result["report"])

            st.divider()

            # News
            st.markdown("### 📰 Recent News")
            for article in result["news"]:
                st.markdown(f"**[{article['title']}]({article['url']})**")
                st.caption(f"{article['source']} · {article['published'][:10]}")
                if article["description"]:
                    st.write(article["description"])
                st.write("")

            # Retrieved knowledge
            with st.expander("📚 Retrieved Knowledge (from research documents)"):
                for chunk in result["knowledge"]:
                    st.markdown(f"- {chunk}")
