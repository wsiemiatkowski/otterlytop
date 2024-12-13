import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO

# Page setup
st.title("Otterly Amazing Coffee Tier List of Greatness 2024")

st.markdown(
    """
    <style>
        .header {
            font-size: 24px;
            font-weight: bold;
            color: #6a0dad;
        }
        .subheader {
            font-size: 18px;
            color: #4b0082;
        }
        .rules {
            margin-top: 20px;
            padding: 15px;
            background-color: #f9f9f9;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }
        .kinky {
            font-style: italic;
            color: #ff4500;
        }
        .spacer {
            margin: 20px 0;
        }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="header">Greetings, Fellow Cultists of Otters and NPR!</div>', unsafe_allow_html=True)

st.markdown(
    """
    As a fun little bonding activity (<span class="kinky">kinky</span>), we'd like to offer you this fun tier list.  
    For each of the tiers, please input between **1 and 5 coffees**.  
    You will be able to save the results for sharing!
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)

st.markdown(
    """
    <div style="text-align: center;">
        <img src="https://i.pinimg.com/originals/f1/99/92/f19992618d0a8caae5e468e758825a02.gif" 
            alt="Sea Otter" style="width: 300px; border-radius: 10px;">
    </div>
    """,
    unsafe_allow_html=True
)

user_name = st.text_input("What's your name?", "")

st.markdown(
    """
    <div class="rules">
        <strong>Rules of Categories:</strong>
        <ul>
            <li><strong>S:</strong> Your absolute favorites.</li>
            <li><strong>A:</strong> The best quality coffees of the year. They can overlap with the S category, but they are all about quality, not just subjective thoughts.</li>
            <li><strong>B:</strong> Truly great - coffees that you found to be just a tier below the best - something truly exceptional.</li>
            <li><strong>C:</strong> Great beans that almost made it to the categories above.</li>
            <li><strong>D:</strong> Honorable mentions - whatever you desire on the chart that you can't place anywhere else.</li>
            <li><strong>E:</strong> Best value! Choose something you fell in love with at a lower price.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

categories = ['S', 'A', 'B', 'C', 'D', 'E']
coffee_preferences = {}

st.markdown('<div class="spacer"></div>', unsafe_allow_html=True)
st.subheader("Input your top 5 for each category:")

for category in categories:
    st.write(f"### {category}")
    coffee_preferences[category] = []
    for i in range(1, 6):
        coffee = st.text_input(f"{category} - Rank #{i}", key=f"{category}_{i}")
        coffee_preferences[category].append(coffee)


def render_table_as_image(df, color, filename="tier_list.png"):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('off')

    table = ax.table(cellText=df.values, colLabels=df.columns, loc='center', cellLoc='center',
                     colColours=[color] * len(df.columns))

    table.auto_set_font_size(False)
    table.set_fontsize(14)
    table.scale(2.0, 2.0)
    plt.tight_layout()

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.1)
    buf.seek(0)
    return buf


def render_full_tier_list(coffee_preferences, user_name):
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.axis('off')

    pastel_colors = [
        "#FFB3BA",  # Light Pink
        "#FFDFBA",  # Light Peach
        "#FFFFBA",  # Light Yellow
        "#BAFFB3",  # Light Green
        "#BAE1FF",  # Light Blue
        "#D8BFD8",  # Thistle (Light Purple)
    ]

    row_height = 1 / 3
    column_width = 1 / 2

    y_offset = 1.0
    for idx, category in enumerate(categories):
        coffees = [c.strip() for c in coffee_preferences[category] if c.strip()]
        coffee_df = pd.DataFrame(coffees, columns=[f"{category} Coffees"])

        if coffees:
            color = pastel_colors[idx]
            ax.table(cellText=coffee_df.values, colLabels=coffee_df.columns, loc='center', cellLoc='center',
                     colColours=[color] * len(coffee_df.columns),
                     bbox=[(idx % 2) * column_width, y_offset - row_height, column_width, row_height])

        if idx % 2 == 1:
            y_offset -= row_height

    ax.text(0.5, 1.05, f"{user_name}'s Amazing Coffee Year of 2024", ha='center', va='center', fontsize=20,
            fontweight='bold', color='#6a0dad')

    buf = BytesIO()
    plt.savefig(buf, format="png", bbox_inches="tight", pad_inches=0.1)
    buf.seek(0)
    return buf


if st.button("Generate Tier List"):
    if all(any(c.strip() for c in coffee_preferences[cat]) for cat in categories):
        col1, col2 = st.columns(2)

        with col1:
            for idx, category in enumerate(categories[:3]):
                coffees = [c.strip() for c in coffee_preferences[category] if c.strip()]
                coffee_df = pd.DataFrame(coffees, columns=[f"{category} Coffees"])
                st.subheader(f"{category} Tier")
                st.dataframe(coffee_df)

        with col2:
            for idx, category in enumerate(categories[3:]):
                coffees = [c.strip() for c in coffee_preferences[category] if c.strip()]
                coffee_df = pd.DataFrame(coffees, columns=[f"{category} Coffees"])
                st.subheader(f"{category} Tier")
                st.dataframe(coffee_df)


        img_buf = render_full_tier_list(coffee_preferences, user_name)
        st.download_button(
            label="Download Full Tier List as Image",
            data=img_buf,
            file_name=f"{user_name}_coffee_tier_list_2024.png",
            mime="image/png"
        )
    else:
        st.error("Please fill in at least one coffee for each category.")
