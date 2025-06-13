import streamlit as st
from auth import *
from blog import *
from blog import create_comments_table

# ----- Init -----
st.set_page_config(page_title="My Blog", layout="wide")
create_user_table()
create_blog_table()
create_comments_table()

# ----- Sidebar Navigation -----
menu = ["Login", "Sign Up"]
if 'logged_in' in st.session_state and st.session_state['logged_in']:
    menu = ["Create Post", "View Posts", "Logout"]

choice = st.sidebar.selectbox("Navigation", menu)

# ----- Login -----
if choice == "Login":
    st.title("🔐 Login to Your Blog")
    username = st.text_input("Username")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if login_user(username, hash_password(password)):
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.success(f"Welcome, {username}!")
            st.rerun()
        else:
            st.error("Incorrect username or password")

# ----- Sign Up -----
elif choice == "Sign Up":
    st.title("📝 Create Account")
    new_user = st.text_input("New Username")
    new_password = st.text_input("New Password", type='password')
    if st.button("Sign Up"):
        add_user(new_user, hash_password(new_password))
        st.success("Account created!")

# ----- Logout -----
elif choice == "Logout":
    st.session_state['logged_in'] = False
    st.session_state['username'] = ""
    st.rerun()

# ----- Create Post -----
elif choice == "Create Post":
    st.title("✍️ Create New Blog Post")
    title = st.text_input("Title")
    content = st.text_area("Write your post here...", height=200)
    category = st.selectbox("Category", ["Tech", "Lifestyle", "Education", "Other"])

    if st.button("Publish"):
        if title and content:
            add_blog_post(title, content, category, st.session_state['username'])
            st.success("✅ Post published!")
        else:
            st.warning("Please fill all fields.")

# ----- View Posts -----
elif choice == "View Posts":
    st.title("📰 All Blog Posts")

    categories = ["All", "Tech", "Lifestyle", "Education", "Other"]
    selected_category = st.selectbox("📚 Filter by Category", categories)

    if selected_category == "All":
        posts = get_all_posts()
    else:
        posts = get_posts_by_category(selected_category)

    if posts:
        for post in posts:
            st.subheader(post[0])
            st.caption(f"By {post[3]} | {post[4]} | Category: {post[2]}")
            st.write(post[1])
            st.markdown("---")

            # Show comments
            st.markdown("**💬 Comments:**")
            comments = get_comments_for_post(post[0])
            if comments:
                for commenter, text, time in comments:
                    st.info(f"{commenter} ({time}) said:\n{text}")
            else:
                st.write("No comments yet.")

            # Comment input (only if logged in)
            if 'logged_in' in st.session_state and st.session_state['logged_in']:
                with st.form(f"comment_form_{post[0]}"):
                    comment_text = st.text_area("Add a comment", key=post[0])
                    submit = st.form_submit_button("Post Comment")
                    if submit and comment_text.strip():
                        add_comment(post[0], st.session_state['username'], comment_text.strip())
                        st.success("Comment added!")
                        st.rerun()

            st.markdown("----")
    else:
        st.info("No blog posts found.")
