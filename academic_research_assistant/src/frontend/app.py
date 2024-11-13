# src/frontend/app.py
import streamlit as st
import requests
from datetime import datetime, timedelta

def main():
    st.title("Academic Research Paper Assistant")
    
    # Sidebar for topic search
    with st.sidebar:
        st.header("Search Papers")
        topic = st.text_input("Enter research topic")
        if st.button("Search"):
            if topic:
                with st.spinner("Searching papers..."):
                    response = requests.post(
                        "http://localhost:8000/search",
                        json={"topic": topic}
                    )
                    if response.status_code == 200:
                        st.session_state.papers = response.json()["papers"]
                        st.success("Papers found!")
    
    # Main content area
    if "papers" in st.session_state:
        st.header("Research Papers")
        
        # Display papers in a timeline
        papers = st.session_state.papers
        selected_papers = []
        
        for paper in papers:
            col1, col2 = st.columns([1, 4])
            with col1:
                selected = st.checkbox("Select", key=paper["id"])
                if selected:
                    selected_papers.append(paper["id"])
            
            with col2:
                st.markdown(f"### {paper['title']}")
                st.markdown(f"**Published:** {paper['published_date']}")
                st.markdown(f"**Authors:** {', '.join(paper['authors'])}")
                with st.expander("Abstract"):
                    st.write(paper["abstract"])
        
        # Q&A Section
        st.header("Ask Questions")
        question = st.text_input("Enter your question about the selected papers")
        if st.button("Get Answer") and question and selected_papers:
            with st.spinner("Generating answer..."):
                response = requests.post(
                    "http://localhost:8000/answer",
                    json={"question": question, "paper_ids": selected_papers}
                )
                if response.status_code == 200:
                    st.write(response.json()["answer"])
        
        # Summary and Future Directions
        if selected_papers:
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("Generate Summary"):
                    with st.spinner("Generating summary..."):
                        response = requests.post(
                            "http://localhost:8000/summarize",
                            json=selected_papers
                        )
                        if response.status_code == 200:
                            st.write(response.json()["summary"])
            
            with col2:
                if st.button("Generate Future Directions"):
                    with st.spinner("Generating future directions..."):
                        response = requests.post(
                            "http://localhost:8000/future-directions",
                            json=selected_papers
                        )
                        if response.status_code == 200:
                            st.write(response.json()["future_directions"])

if __name__ == "__main__":
    main()
    