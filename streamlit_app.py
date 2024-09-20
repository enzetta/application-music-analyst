import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# Custom CSS for consistent styling
st.markdown(
    """
    <style>
    body {
        background-color: #f5f5f5;
        font-family: 'Arial', sans-serif;
    }
    h1 {
        color: #C3979F;
        text-align: center;
    }
    h2 {
        color: #fff;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Witty Title
st.title("Musik liebende Analytikerin sucht Bühne bei Sony Music 🎸📊")

# Introduction
st.write("""
Willkommen zu meinem interaktiven Sony Music Analytics Dashboard! Als eventuell angehende Praktikantin für das Analytics-Team 
im Bereich Streaming & Social Media habe ich dieses Dashboard erstellt, um meine Fähigkeiten in Datenanalyse und 
Visualisierung sowie mein Verständnis der Musikindustrie zu demonstrieren. Lasst uns gemeinsam einige 
Schlüsselkennzahlen für eine Auswahl von Sony Music Künstler und Künstlerinnen erkunden! 

(Disclaimer: die Zahlen sind fiktiv)
""")


# Sample data for Sony Music artists with human-readable names
@st.cache_data
def load_data():
    data = {
        "Künstler": [
            "Anfisa Letyago", "Avaion", "Fritz Kalkbrenner",
            "Jean Michel Jarre", "Purple Disco Machine "
        ],
        "Streams - Spotify": [
            2500000000,
            3000000000,
            4500000000,
            5500000000,
            6000000000,
        ],
        "Streams - Apple Music": [
            800000000,
            1000000000,
            1500000000,
            2000000000,
            2500000000,
        ],
        "Streams - YouTube": [
            1500000000,
            2500000000,
            3500000000,
            2000000000,
            3000000000,
        ],
        "Streams - Amazon Music": [
            300000000,
            400000000,
            600000000,
            800000000,
            1000000000,
        ],
        "Follower - Instagram":
        [4000000, 12000000, 24000000, 47000000, 51000000],
        "Follower - TikTok": [6000000, 30000000, 25000000, 15000000, 2000000],
        "Vinyl-Verkäufe": [50000, 75000, 100000, 300000, 500000],
        "Engagement-Rate": [0.05, 0.08, 0.06, 0.04, 0.03],
        "Durchschnittlicher Ticketpreis (€)": [45, 60, 55, 80, 120],
    }

    # Generate monthly data for 2024
    months = [
        "Jan 2024",
        "Feb 2024",
        "Mar 2024",
        "Apr 2024",
        "Mai 2024",
        "Jun 2024",
        "Jul 2024",
        "Aug 2024",
    ]
    monthly_data = {}
    for artist in data["Künstler"]:
        artist_data = {
            "Monat": months,
            "Streams - Spotify": [
                int(
                    np.random.normal(
                        data["Streams - Spotify"][data["Künstler"].index(artist)] / 12,
                        1e7,
                    )
                )
                for _ in range(8)
            ],
            "Streams - Apple Music": [
                int(
                    np.random.normal(
                        data["Streams - Apple Music"][data["Künstler"].index(artist)]
                        / 8,
                        5e6,
                    )
                )
                for _ in range(8)
            ],
            "Streams - YouTube": [
                int(
                    np.random.normal(
                        data["Streams - YouTube"][data["Künstler"].index(artist)] / 8,
                        8e6,
                    )
                )
                for _ in range(8)
            ],
            "Streams - Amazon Music": [
                int(
                    np.random.normal(
                        data["Streams - Amazon Music"][data["Künstler"].index(artist)]
                        / 8,
                        3e6,
                    )
                )
                for _ in range(8)
            ],
        }
        artist_data["Gesamtstreams"] = [
            sum(x)
            for x in zip(
                artist_data["Streams - Spotify"],
                artist_data["Streams - Apple Music"],
                artist_data["Streams - YouTube"],
                artist_data["Streams - Amazon Music"],
            )
        ]

        # Calculate revenue (assuming €0.004 per stream)
        for platform in ["Spotify", "Apple Music", "YouTube", "Amazon Music"]:
            artist_data[f"Umsatz - {platform}"] = [
                x * 0.004 for x in artist_data[f"Streams - {platform}"]
            ]
        artist_data["Gesamtumsatz"] = [
            sum(x)
            for x in zip(
                artist_data["Umsatz - Spotify"],
                artist_data["Umsatz - Apple Music"],
                artist_data["Umsatz - YouTube"],
                artist_data["Umsatz - Amazon Music"],
            )
        ]

        monthly_data[artist] = pd.DataFrame(artist_data)

    # Generate country data for EU5
    countries = ["Deutschland", "Frankreich", "Grossbritannien", "Italien", "Spanien"]
    country_data = {}
    for artist in data["Künstler"]:
        country_data[artist] = pd.DataFrame(
            {
                "Land": countries,
                "Umsatz": [int(np.random.normal(1e6, 2e5)) for _ in range(5)],
            }
        )

    return pd.DataFrame(data), monthly_data, country_data


df, monthly_data, country_data = load_data()


# Formatting functions
def format_compact(value):
    if value >= 1_000_000_000:
        return f"{value/1_000_000_000:.1f}Mrd"
    elif value >= 1_000_000:
        return f"{value/1_000_000:.1f}M"
    elif value >= 1_000:
        return f"{value/1_000:.1f}k"
    else:
        return f"{value:.0f}"


def format_percent(value):
    return f"{value:.1%}"


def format_currency(value):
    return f"{value:.0f} €"


# Artist selection
selected_artist = st.selectbox("Wähle einen Künstler zur Analyse:", df["Künstler"])
artist_data = df[df["Künstler"] == selected_artist].iloc[0]

# Section 1: Artist Overview
st.header("1. Künstlerübersicht")

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Streams - Spotify", format_compact(artist_data["Streams - Spotify"]))
with col2:
    st.metric(
        "Follower - Instagram", format_compact(artist_data["Follower - Instagram"])
    )
with col3:
    st.metric("Follower - TikTok", format_compact(artist_data["Follower - TikTok"]))

# Section 2: Streaming Platform Comparison
st.header("2. Vergleich der Streaming-Plattformen")

streaming_platforms = ["Spotify", "Apple Music", "YouTube", "Amazon Music"]
streaming_data = [
    artist_data[f"Streams - {platform}"] for platform in streaming_platforms
]

fig = go.Figure(
    data=[
        go.Bar(
            x=streaming_platforms,
            y=streaming_data,
            text=[format_compact(val) for val in streaming_data],
        )
    ]
)
fig.update_layout(
    title=f"Streams auf verschiedenen Plattformen - {selected_artist}",
    xaxis_title="Plattform",
    yaxis_title="Streams",
)
fig.update_traces(textposition="outside")
st.plotly_chart(fig)

st.write(
    f"""
Diese Grafik zeigt die Performance von {selected_artist} auf verschiedenen Streaming-Plattformen. 
Wir können sehen, dass {'Spotify' if artist_data['Streams - Spotify'] == max(streaming_data) else 'eine andere Plattform'} 
die meisten Streams für diesen Künstler generiert. Diese Erkenntnisse können helfen, plattformspezifische 
Promotion-Strategien für {selected_artist} zu entwickeln.
"""
)

# Section 3: Social Media Engagement
st.header("3. Social Media Engagement")

fig = px.scatter(
    df,
    x="Follower - Instagram",
    y="Follower - TikTok",
    size="Engagement-Rate",
    hover_name="Künstler",
    size_max=60,
    color="Künstler",
)
fig.update_layout(
    title="Social Media Follower vs. Engagement-Rate",
    xaxis_title="Instagram Follower",
    yaxis_title="TikTok Follower",
)
fig.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>Instagram Follower: %{x:,.0f}<br>TikTok Follower: %{y:,.0f}<br>Engagement-Rate: %{marker.size:.2%}"
)
fig.update_xaxes(tickformat=".2s")
fig.update_yaxes(tickformat=".2s")
st.plotly_chart(fig)

st.write(
    f"""
Diese Bubble-Chart visualisiert die Beziehung zwischen der Follower-Anzahl eines Künstlers auf Instagram 
und TikTok, wobei die Grösse der Blase die Engagement-Rate darstellt. {selected_artist} hat 
{format_compact(artist_data['Follower - Instagram'])} Instagram-Follower und {format_compact(artist_data['Follower - TikTok'])} 
TikTok-Follower mit einer Engagement-Rate von {format_percent(artist_data['Engagement-Rate'])}. 
Diese Daten können helfen, die Social-Media-Strategie für {selected_artist} zu optimieren.
"""
)

# Section 4: Vinyl Sales Analysis
st.header("4. Analyse der Vinyl-Verkäufe")

fig = px.pie(
    df, values="Vinyl-Verkäufe", names="Künstler", title="Anteil der Vinyl-Verkäufe"
)
fig.update_traces(
    textposition="inside",
    textinfo="percent+label",
    hovertemplate="%{label}: %{value:,.0f} Verkäufe",
)
st.plotly_chart(fig)

st.write(
    f"""
Die Wiederbelebung von Vinyl ist ein bedeutender Trend in der Musikindustrie. Diese Grafik zeigt die Verteilung 
der Vinyl-Verkäufe unter unseren ausgewählten Künstlern. {selected_artist} hat {format_compact(artist_data['Vinyl-Verkäufe'])} 
Vinyl-Verkäufe. {'Dies deutet auf ein starkes Interesse der Fans an physischen Medien hin.' if artist_data['Vinyl-Verkäufe'] > df['Vinyl-Verkäufe'].mean() else 'Hier könnte Potenzial für spezielle Vinyl-Editionen oder gezielte Promotion-Aktionen liegen.'}
"""
)

# Section 5: Artist Performance Score
st.header("5. Künstler-Performance-Score")

df["Performance_Score"] = (
    df["Streams - Spotify"] / 1e9 * 0.25
    + df["Streams - Apple Music"] / 1e9 * 0.15
    + df["Streams - YouTube"] / 1e9 * 0.1
    + df["Streams - Amazon Music"] / 1e9 * 0.1
    + df["Follower - Instagram"] / 1e6 * 0.15
    + df["Follower - TikTok"] / 1e6 * 0.15
    + df["Vinyl-Verkäufe"] / 1e5 * 0.05
    + df["Engagement-Rate"] * 100 * 0.05
)

fig = px.bar(
    df.sort_values("Performance_Score", ascending=False),
    x="Künstler",
    y="Performance_Score",
    title="Gesamt-Performance-Score der Künstler",
)
fig.update_traces(hovertemplate="%{y:.2f}")
st.plotly_chart(fig)

st.write(
    f"""
Der 'Performance-Score' berücksichtigt alle betrachteten Metriken, gewichtet nach ihrer relativen Bedeutung 
in der heutigen Musikindustrie. {selected_artist} hat einen Performance-Score von 
{df[df['Künstler'] == selected_artist]['Performance_Score'].values[0]:.2f}. 
{'Dies deutet auf eine starke Gesamtperformance hin.' if df[df['Künstler'] == selected_artist]['Performance_Score'].values[0] > df['Performance_Score'].mean() else 'Hier könnte es Raum für Verbesserungen in bestimmten Bereichen geben.'}

Die Gewichtungen für jede Metrik sind:
- Spotify Streams: 25%
- Apple Music Streams: 15%
- YouTube Streams: 10%
- Amazon Music Streams: 10%
- Instagram Follower: 15%
- TikTok Follower: 15%
- Vinyl-Verkäufe: 5%
- Engagement-Rate: 5%
"""
)

# Section 6: Ticket Price vs. Engagement Rate
st.header("6. Ticketpreis vs. Engagement-Rate")

fig = px.scatter(
    df,
    x="Durchschnittlicher Ticketpreis (€)",
    y="Engagement-Rate",
    size="Streams - Spotify",
    hover_name="Künstler",
    color="Künstler",
)
fig.update_layout(
    title="Durchschnittlicher Ticketpreis vs. Engagement-Rate",
    xaxis_title="Durchschnittlicher Ticketpreis (€)",
    yaxis_title="Engagement-Rate",
)
fig.update_traces(
    hovertemplate="<b>%{hovertext}</b><br>Ticketpreis: %{x} €<br>Engagement-Rate: %{y:.2%}<br>Spotify Streams: %{marker.size:,.0f}"
)
fig.update_yaxes(tickformat=".1%")
st.plotly_chart(fig)

st.write(
    f"""
Diese Scatter-Plot zeigt die Beziehung zwischen dem durchschnittlichen Ticketpreis und der Engagement-Rate der Künstler, 
wobei die Größe der Punkte die Anzahl der Spotify-Streams darstellt. {selected_artist} hat einen durchschnittlichen 
Ticketpreis von {format_currency(artist_data['Durchschnittlicher Ticketpreis (€)'])} und eine Engagement-Rate von 
{format_percent(artist_data['Engagement-Rate'])}. {'Dies deutet auf eine gute Balance zwischen Ticketpreis und Fan-Engagement hin.' if artist_data['Engagement-Rate'] > df['Engagement-Rate'].mean() else 'Hier könnte es Potenzial geben, das Fan-Engagement zu steigern oder die Preisgestaltung zu überdenken.'}
"""
)

# New Section: Monthly Metrics for 2024
st.header("7. Monatliche Metriken für 2024")

artist_monthly_data = monthly_data[selected_artist]

st.write(f"Monatliche Streams und Umsätze für {selected_artist} im Jahr 2024:")
st.dataframe(
    artist_monthly_data.style.format(
        {
            "Streams - Spotify": "{:,.0f}",
            "Streams - Apple Music": "{:,.0f}",
            "Streams - YouTube": "{:,.0f}",
            "Streams - Amazon Music": "{:,.0f}",
            "Gesamtstreams": "{:,.0f}",
            "Umsatz - Spotify": "{:,.2f} €",
            "Umsatz - Apple Music": "{:,.2f} €",
            "Umsatz - YouTube": "{:,.2f} €",
            "Umsatz - Amazon Music": "{:,.2f} €",
            "Gesamtumsatz": "{:,.2f} €",
        }
    )
)

# Visualize monthly total streams and revenue
fig = go.Figure()
fig.add_trace(
    go.Bar(
        x=artist_monthly_data["Monat"],
        y=artist_monthly_data["Gesamtstreams"],
        name="Gesamtstreams",
    )
)
fig.add_trace(
    go.Scatter(
        x=artist_monthly_data["Monat"],
        y=artist_monthly_data["Gesamtumsatz"],
        name="Gesamtumsatz",
        yaxis="y2",
    )
)
fig.update_layout(
    title=f"Monatliche Gesamtstreams und Umsatz für {selected_artist} (2024)",
    yaxis=dict(title="Gesamtstreams"),
    yaxis2=dict(title="Gesamtumsatz", overlaying="y", side="right"),
)
st.plotly_chart(fig)

# New Section: Revenue by Country (EU5)
st.header("8. Umsatz nach Land (EU5)")

artist_country_data = country_data[selected_artist]

st.write(f"Umsatzverteilung für {selected_artist} in den EU5-Ländern:")
st.dataframe(artist_country_data.style.format({"Umsatz": "{:,.2f} €"}))

# Visualize country revenue
fig = px.pie(
    artist_country_data,
    values="Umsatz",
    names="Land",
    title=f"Umsatzverteilung für {selected_artist} in EU5",
)
st.plotly_chart(fig)

# Conclusion
st.header("Fazit")
st.write("""
Dieses Dashboard demonstriert meine Fähigkeit, Daten in der Musikindustrie zu analysieren und zu visualisieren. 
Durch die Untersuchung verschiedener Metriken auf unterschiedlichen Plattformen können wertvolle Einblicke in die 
Performance von Musikschaffenden und das Fan-Engagement gewinnen. Diese Erkenntnisse können strategische Entscheidungen in 
Bereichen wie:

1. Plattformspezifische Promotionsstrategien
2. Social-Media-Content-Planung zur Steigerung des Engagements
3. Identifizierung von Möglichkeiten für Special-Edition-Veröffentlichungen
4. Zuweisung von Marketing-Ressourcen basierend auf der Gesamtperformance der Künstler
5. Optimierung der Preisgestaltung für Konzerte und Events

erleichtern und mit Daten fundieren.

Als Teil des Analytics-Teams für Streaming & Social Media bei Sony Music würde ich mich freuen, noch tiefer in diese 
Analysen einzutauchen, weitere Datenpunkte einzubeziehen und umsetzbare Erkenntnisse zu gewinnen, um den Erfolg der 
Musikschaffenden voranzutreiben. Ich bin besonders daran interessiert zu erforschen, wie prädiktive Analysen genutzt werden können, 
um aufkommende Trends vorherzusagen und vielversprechende neue Künstler und Künstlerinnen zu identifizieren, zu fördern und deren Erfolge für Sony Music sichtbar zu machen.

Vielen Dank, dass ihr meine Bewerbung in Betracht ziehen. Ich freue mich auf die Möglichkeit, zu besprechen, wie meine 
Fähigkeiten und meine Leidenschaft für datengesteuerte Entscheidungsfindung zum anhaltenden Erfolg von Sony Music im 
digitalen Zeitalter beitragen können und darauf von eurem Team noch einiges lernen zu können.

Danke für eure Zeit und eure Neugierde bis hierher gelesen zu haben.
""")

# Add a personal touch
st.markdown(
    """
    <style>
    .sidebar-content {
        padding-top: 50px;  /* Adjust this value to control the space */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.markdown('<div class="sidebar-content"></div>',
                    unsafe_allow_html=True)

# Add a call-to-action
st.sidebar.info("""
Ich freue mich darauf, meine Fähigkeiten und Leidenschaft in das Sony Music Team einzubringen und neue spannende Themen kennenzulernen.
Was mich weiter bewegt und motiviert findet ihr in meinem [Motivationsschreiben](https://drive.google.com/file/d/1b6a7Fz3WCf4H1W7l0Ym7LEd__7upXNOv/view?usp=drive_link).
""")


# Sidebar introduction text
st.sidebar.write("""
**Über mich:**

Ich bin Sophie, Daten-Enthusiastin mit einem sozialwissenschaftlichen und quantitativen Hintergrund sowie mehrjähriger Erfahrung in der Musik-, Förder- und Eventbranche in Berlin. 

Weitere Details zu meinem Werdegang findet ihr in meinem [Lebenslauf](https://drive.google.com/file/d/1sj3mElOWp6-S9xoXpubWNZ0Cy7eZkU5Z/view?usp=sharing).
Ich freue mich darauf, meine analytischen Fähigkeiten, Branchenkenntnisse und meine inherente Leidenschaft für die Branche bei Sony Music einbringen zu können!
""")

# Add contact information
st.sidebar.write("""
**Kontakt:**
- A: Schlimmbergstr. 65, 8802 Kilchberg
- E: sophie.c.philipp@gmail.com
- M: +41 76 366 4845
- [LinkedIn](https://www.linkedin.com/in/sophie-philipp-now) 
- [GitHub](https://github.com/enzetta) 
""")

# Add skills section
st.sidebar.write("""
**Kernkompetenzen:**
- Datenanalyse und Visualisierung
- Python (Pandas, Numpy, Plotly, Streamlit)
- SQL, RStudio, Bereitschaft mehr Tools und Technologien zu lernen
- Event- und Salesmanagement 
- Musikindustrie-Kenntnisse
- Projektmanagement
- Kreatives Problemlösen
""")

# Add education section
st.sidebar.write("""
**Ausbildung:**
- Cand. B.A. Sozialwissenschaften, quant. Schwerpunkt, Humboldt Universität zu Berlin
- Diverse Zertifikate in Data Science, Inferenz Statistik, Excel
- Ersthelferin
""")
