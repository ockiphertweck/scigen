import streamlit as st
from streamlit_elements import elements, mui, html

# Function to show the floating panel


def show_floating_panel():
    with elements("floating-panel"):
        html.div(
            style={
                "position": "fixed",
                "top": "50%",
                "left": "50%",
                "transform": "translate(-50%, -50%)",
                "backgroundColor": "white",
                "padding": "20px",
                "border": "1px solid #ccc",
                "borderRadius": "8px",
                "zIndex": 1000,
            },
            children=[
                mui.Button("Regenerate", variant="contained", color="primary"),
                mui.Button("Add Section", variant="contained",
                           color="secondary"),
            ]
        )

# Main Streamlit app


def main():
    st.title("Markdown with Hover Button")

    markdown_content = """
    # Sample Markdown
    This is an example of markdown content.
    
    ## Section 1
    Content of section 1.
    
    ## Section 2
    Content of section 2.
    """.replace('\n', '<br>')  # Replace newlines with <br> for HTML

    # Custom HTML and CSS for the hover effect and floating panel
    custom_html = f"""
    <div class="markdown-content">
        {markdown_content}
    </div>
    <style>
        .markdown-content {{
            position: relative;
            padding-right: 50px;
        }}
        .hover-button {{
            display: none;
            position: absolute;
            right: 10px;
            top: 10px;
            cursor: pointer;
            background-color: #007bff;
            color: white;
            border: none;
            padding: 5px 10px;
            border-radius: 5px;
        }}
        .markdown-content:hover .hover-button {{
            display: block;
        }}
    </style>
    <script>
        document.addEventListener("DOMContentLoaded", function() {{
            const button = document.querySelector('.hover-button');
            button.addEventListener('click', function() {{
                const panel = document.querySelector('.floating-panel');
                if (panel) {{
                    panel.style.display = 'block';
                }}
            }});
        }});
    </script>
    <button class="hover-button">Options</button>
    """

    st.write(custom_html, unsafe_allow_html=True)

    # Place the floating panel here to be displayed when the button is clicked
    show_floating_panel()


if __name__ == "__main__":
    main()
