import streamlit as st
import pandas as pd

st.title("🎬 Movie Recommendation System")

# ---------------- DATA ----------------
if "movies" not in st.session_state:
    st.session_state.movies = [
        {"id": 1, "title": "Inception", "genre": "Sci-Fi", "year": 2010, "ratings": [], "views": 0},
        {"id": 2, "title": "Avengers", "genre": "Action", "year": 2012, "ratings": [], "views": 0},
        {"id": 3, "title": "Interstellar", "genre": "Sci-Fi", "year": 2014, "ratings": [], "views": 0},
        {"id": 4, "title": "Batman", "genre": "Action", "year": 2008, "ratings": [], "views": 0}
    ]

if "users" not in st.session_state:
    st.session_state.users = {"adil": {"history": [], "ratings": {}}}

# ---------------- LOGIN ----------------
user = st.text_input("Enter Username")
if user not in st.session_state.users:
    st.session_state.users[user] = {"history": [], "ratings": {}}

current_user = st.session_state.users[user]

# ---------------- RATE MOVIE ----------------
st.subheader("Rate a Movie")

movie_titles = [m["title"] for m in st.session_state.movies]
selected_movie = st.selectbox("Select Movie", movie_titles)
rating = st.slider("Rating (1-5)", 1, 5)

if st.button("Submit Rating"):
    for m in st.session_state.movies:
        if m["title"] == selected_movie:
            m["ratings"].append(rating)
            m["views"] += 1
            current_user["history"].append(m)
            current_user["ratings"][m["title"]] = rating
    st.success("Rating submitted!")

# ---------------- SEARCH ----------------
st.subheader("Search Movies")

search_title = st.text_input("Search by Title")
search_genre = st.selectbox("Search by Genre", ["All", "Sci-Fi", "Action"])

results = []
for m in st.session_state.movies:
    if (search_title.lower() in m["title"].lower()) and (search_genre == "All" or m["genre"] == search_genre):
        avg = sum(m["ratings"]) / len(m["ratings"]) if m["ratings"] else 0
        results.append([m["title"], m["genre"], m["year"], round(avg, 2)])

if results:
    df = pd.DataFrame(results, columns=["Title", "Genre", "Year", "Avg Rating"])
    st.dataframe(df)

# ---------------- RECOMMENDATION ----------------
st.subheader("Recommended Movies")

watched_genres = [m["genre"] for m in current_user["history"]]

recs = []
for m in st.session_state.movies:
    if m["genre"] in watched_genres and m not in current_user["history"]:
        avg = sum(m["ratings"]) / len(m["ratings"]) if m["ratings"] else 0
        recs.append((m["title"], avg))

recs.sort(key=lambda x: x[1], reverse=True)

for r in recs[:3]:
    st.write(r[0], "⭐", r[1])

# ---------------- DASHBOARD ----------------
st.subheader("User Dashboard")

# Watch history
history_data = []
for m in current_user["history"]:
    history_data.append([m["title"], m["genre"], m["year"]])

if history_data:
    st.write("Watch History")
    st.table(history_data)

# Trending
st.write("Trending Movies")
trending = sorted(st.session_state.movies, key=lambda x: x["views"], reverse=True)[:3]
for m in trending:
    st.write(m["title"], "- Views:", m["views"])

# Popular Genre
genre_count = {}
for m in st.session_state.movies:
    genre_count[m["genre"]] = genre_count.get(m["genre"], 0) + m["views"]

if genre_count:
    popular = max(genre_count, key=genre_count.get)
    st.write("Most Popular Genre:", popular)

# Chart
chart_data = {m["title"]: (sum(m["ratings"]) / len(m["ratings"]) if m["ratings"] else 0)
              for m in st.session_state.movies}
st.bar_chart(chart_data)

# ---------------- ADMIN ----------------
st.subheader("Admin Panel")

admin_key = st.text_input("Enter Admin Key")

if admin_key == "admin123":
    st.success("Admin Access Granted")

    title = st.text_input("Movie Title")
    genre = st.text_input("Genre")
    year = st.number_input("Year", 1900, 2026)

    if st.button("Add Movie"):
        new_id = len(st.session_state.movies) + 1
        st.session_state.movies.append({"id": new_id, "title": title, "genre": genre, "year": year, "ratings": [], "views": 0})
        st.success("Movie Added")

    st.write("Most Watched Movies")
    for m in trending:
        st.write(m["title"])

    st.write("Top Active Users")
    for u in st.session_state.users:
        count = len(st.session_state.users[u]["history"])
        st.write(u, "-", count)
