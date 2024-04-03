from services.text_splitter import Splitter, SplitterOptions, split_text
import streamlit as st
import pandas as pd

st.title('Text File Processor')

# Corrected slider ranges and default values
chunk_size = st.sidebar.slider('Chunk Size', min_value=1, max_value=5000, value=500, key='chunk_size')
chunk_overlap = st.sidebar.slider('Chunk Overlap', min_value=0, max_value=1000, value=100, key='chunk_overlap')

splitter_type = st.sidebar.selectbox('Text Splitter Type', list(Splitter), format_func=lambda x: x.value)

uploaded_file = st.file_uploader("Choose a text file", type="txt")
if uploaded_file is not None:
    # Use the cache key mechanism to differentiate processing based on slider values
    cache_key = f"{uploaded_file.name}_{chunk_size}_{chunk_overlap}_{splitter_type}"
    st.write(f"Cache Key: {cache_key}")
    chunks = []
    # Check if we need to process the file (or if this exact processing was already done)
    if 'chunks' not in st.session_state or 'cache_key' not in st.session_state or st.session_state['cache_key'] != cache_key:
        # New processing is needed: update the cache key and process
        print("new")
        st.session_state['cache_key'] = cache_key
        st.session_state['chunks'] = []  # Initialize the 'chunks' key in session state
        text_data = str(uploaded_file.getvalue(), 'utf-8')  # Use getvalue() for consistent behavior

        # Process the text based on user inputs
        chunks, references = split_text(text_data,splitter=splitter_type, splitter_options=SplitterOptions(chunk_size, chunk_overlap))
        print(len(chunks))
        # Store processed chunks in session state to avoid re-processing on reruns that don't change inputs
        st.session_state['chunks'] = chunks
    else:
        # Retrieve previously processed chunks from session state
        chunks = st.session_state['chunks']

    # Display the number of chunks
    st.write(f"Number of Chunks: {len(chunks)}")

    # Create a DataFrame to hold the chunks
    df_chunks = pd.DataFrame(chunks, columns=['Text Chunk'])

    # Display the DataFrame as a table
    st.table(df_chunks)
