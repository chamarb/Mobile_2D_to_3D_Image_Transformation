import dash
from dash import html, dcc, Output, Input
import dash_bootstrap_components as dbc
import os
import json
import base64
import plotly.graph_objs as go

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.FLATLY])
app.title = "PFE Dashboard - Image Description & 3D"

# Directory for processed images and 3D models
PROCESSED_IMAGES_DIR = "/Users/chamarb/Downloads/PFE_Projects/pfe_dashboard/assets/"

# Utility to encode image as base64
def encode_image(image_path):
    with open(image_path, 'rb') as f:
        encoded = base64.b64encode(f.read()).decode()
    return encoded

# Load all image names available
def get_available_image_names():
    return list(set(f.split("_")[0] for f in os.listdir(PROCESSED_IMAGES_DIR) if f.endswith(".json")))

# Layout Tabs
tabs = dcc.Tabs(id="tabs", value="overview", children=[
    dcc.Tab(label="🏠 Overview", value="overview"),
    dcc.Tab(label="🧠 Model Showcase", value="models"),
    dcc.Tab(label="🧊 3D Preview", value="preview3d"),
    dcc.Tab(label="📐 Architecture", value="architecture"),
    dcc.Tab(label="📊 Comparison", value="comparison"),
    dcc.Tab(label="🔚 Conclusion", value="conclusion"),
])

# Page Content
content = html.Div(id="tab-content")

# Define Layout
app.layout = dbc.Container([
    html.H1("PFE Project Dashboard", className="text-center mt-4 mb-4"),
    tabs,
    content
], fluid=True)

# Callback to handle tab content based on selection
@app.callback(Output("tab-content", "children"), Input("tabs", "value"))
def render_content(tab):
    if tab == "overview":
        return html.Div([
            html.H3("📌 Project Overview: AI-Powered Image Understanding & 3D Visualization", style={"textAlign": "center", "fontWeight": "bold"}),
            
            html.Div([
                html.P("👩‍💻 Author: Chaimae Rouineb", style={"fontSize": "18px", "fontStyle": "italic"}),
                html.P("🛠️ Tech Stack: Flutter • FastAPI • HuggingFace (PaLI-Gemma3B) • SAM • Gaussian Splatting • Three.js", style={"fontSize": "16px"}),
            ], style={"textAlign": "center", "marginBottom": "20px"}),
            
            html.Hr(style={"borderColor": "#E1E1E1"}),

            html.H4("🌟 What This Project Does", style={"color": "#333", "fontWeight": "bold"}),
            html.P("This end-to-end solution turns 2D images into semantically rich textual descriptions and 3D interactive visualizations.", style={"fontSize": "16px", "lineHeight": "1.6em"}),
            
            html.Ul([
                html.Li("🔍 AI-driven image understanding with multi-modal models"),
                html.Li("✂️ Background removal and object segmentation"),
                html.Li("🔁 3D reconstruction and rendering (in development)"),
            ], style={"fontSize": "16px", "lineHeight": "1.8em"}),

            html.Hr(style={"borderColor": "#E1E1E1"}),

            html.H4("🧠 The Brains Behind the System: AI Models Used", style={"color": "#333", "fontWeight": "bold"}),

            html.H5("🔬 AI Model Focus: PaLI-Gemma3B", style={"fontSize": "18px", "fontWeight": "bold", "marginTop": "15px"}),
            html.P("The **PaLI-Gemma3B** model, developed by Google, bridges the gap between image and text. It is fine-tuned for generating highly detailed and coherent descriptions based on input images. Unlike traditional models, PaLI-Gemma3B excels at understanding complex visual semantics and articulating them in natural language, making it ideal for applications requiring high-level image interpretation.", style={"fontSize": "16px", "lineHeight": "1.6em"}),

            html.Ul([
                html.Li("⚙️ **PaLI-Gemma3B**: A state-of-the-art model for generating textual descriptions from images."),
                html.Li("💡 Generates natural, human-readable text based on visual content."),
                html.Li("🔍 Enhances image recognition accuracy for real-time systems."),
            ], style={"fontSize": "16px", "lineHeight": "1.8em"}),
            
            html.A("🔗 Source: PaLI-Gemma3B on HuggingFace", href="https://huggingface.co/google/paligemma-3b-pt-448", target="_blank", style={"fontSize": "16px", "color": "#1f77b4", "textDecoration": "underline"}),

            html.Br(), html.Br(),

            html.H5("🔹 SAM (Segment Anything Model) – Meta AI", style={"fontSize": "18px", "fontWeight": "bold", "marginTop": "15px"}),
            html.P("SAM is used to perform background removal and extract object masks before applying captioning and 3D reconstruction. It’s essential for isolating the object of interest.", style={"fontSize": "16px", "lineHeight": "1.6em"}),
            
            html.Ul([
                html.Li("✂️ High-precision object segmentation"),
                html.Li("🖼️ Mask generation for Gaussian Splatting"),
                html.Li("🎯 Improves 3D and captioning accuracy"),
            ], style={"fontSize": "16px", "lineHeight": "1.8em"}),

            html.A("🔗 Source: Segment Anything (SAM) GitHub", href="https://github.com/facebookresearch/segment-anything", target="_blank", style={"fontSize": "16px", "color": "#1f77b4", "textDecoration": "underline"}),

            html.Br(), html.Br(),

            html.H5("🔹 Gaussian Splatting – 3D Reconstruction Technique", style={"fontSize": "18px", "fontWeight": "bold", "marginTop": "15px"}),
            html.P("Gaussian Splatting transforms segmented images into dynamic point-based 3D representations. This technique is still under development but will enable volume estimation and immersive object interaction.", style={"fontSize": "16px", "lineHeight": "1.6em"}),

            html.Ul([
                html.Li("🧊 Converts 2D masks into dense 3D splats"),
                html.Li("📐 Supports potential volume estimation"),
                html.Li("🌐 Rendered in-browser using Three.js"),
            ], style={"fontSize": "16px", "lineHeight": "1.8em"}),

            html.A("🔗 Gaussian Splatting Blog by HuggingFace", href="https://huggingface.co/blog/gaussian-splatting", target="_blank", style={"fontSize": "16px", "color": "#1f77b4", "textDecoration": "underline"}),

            html.Hr(style={"borderColor": "#E1E1E1"}),

            html.H4("📈 Quick Stats", style={"color": "#333", "fontWeight": "bold"}),
            html.Ul([
                html.Li("🖼️ Number of demo images processed: 36"),
                html.Li("⚙️ Backend Inference: FastAPI + HuggingFace Transformers"),
                html.Li("📱 Frontend: Flutter (Mobile App) + Dash (Dashboard)"),
            ], style={"fontSize": "16px", "lineHeight": "1.8em"}),

            html.Hr(style={"borderColor": "#E1E1E1"}),

            html.H4("🚀 Project Goals", style={"color": "#333", "fontWeight": "bold"}),
            html.P("✅ Build an intelligent pipeline for image understanding and 3D reconstruction.", style={"fontSize": "16px", "lineHeight": "1.6em"}),
            html.P("🔄 Optimize model performance on mobile devices.", style={"fontSize": "16px", "lineHeight": "1.6em"}),
            html.P("🔬 Enable object measurement (e.g., volume) using 3D representation.", style={"fontSize": "16px", "lineHeight": "1.6em"}),
        ], style={"padding": "30px", "lineHeight": "1.8em", "backgroundColor": "#f9f9f9", "borderRadius": "8px"})


    
    elif tab == "models":

        import json

        def load_description(file_path):
            with open(file_path, "r") as f:
                data = json.load(f)
            return data.get("description", "")

        # Load the descriptions
        laptop_description = load_description("assets/demo_laptop_object_description.json")
        chair_description = load_description("assets/demo_chair_object_description.json")

        return html.Div([
            html.H4("🧠 AI Model Showcase: Image Descriptions with PaLI-Gemma2"),
            html.P("This section shows the original image, the background-removed version, and the generated image descriptions."),

            html.H5("💻 Example: Laptop"),
            html.Div([
                html.Img(src="assets/demo_laptop.jpg", style={"width": "45%"}),
                html.Img(src="assets/demo_laptop_background_removed.jpg", style={"width": "45%", "marginLeft": "5%"})
            ]),
            html.P(f"🧠 PaLI-Gemma2: {laptop_description}"),

            html.H5("🪑 Example: Chair"),
            html.Div([
                html.Img(src="assets/demo_chair.jpg", style={"width": "45%"}),
                html.Img(src="assets/demo_chair_background_removed.jpg", style={"width": "45%", "marginLeft": "5%"})
            ]),
            html.P(f"🧠 PaLI-Gemma2: {chair_description}")
        ], style={"padding": "30px"})


    elif tab == "preview3d":
        image_models = [
            {"label": "Chair", "value": "chair"},
            {"label": "Laptop", "value": "laptop"}
        ]

        return html.Div([
            html.H4("🧊 3D Visualization: Gaussian Splatting Results"),
            html.P("Select an object to view the segmented image and its 3D model (.ply)."),
            dcc.Dropdown(
                id="model-selector",
                options=image_models,
                placeholder="Select an object..."
            ),
            html.Div(id="model-display-section")
        ])

    
    elif tab == "architecture":
        return html.Div([
            html.H4("📐 System Architecture Overview"),
            html.Img(src="/assets/architecture.png", style={"width": "80%"}),
            html.P("This diagram shows the interaction between Flutter, FastAPI, and models (PaLI-Gemma2, SmolVLM2, SAM, Gaussian Splatting).")
        ])

    elif tab == "comparison":
        return html.Div([
            html.H4("📊 Comparative Analysis of Vision-Language Models"),
            dcc.Graph(
                figure=go.Figure([
                    go.Bar(name='Model Size (GB)', x=['SmolVLM2', 'PaLI-Gemma2'], y=[2.2, 10]),
                    go.Bar(name='VRAM Needed (GB)', x=['SmolVLM2', 'PaLI-Gemma2'], y=[8, 40]),
                    go.Bar(name='Inference Speed (s/img)', x=['SmolVLM2', 'PaLI-Gemma2'], y=[2, 7])
                ]).update_layout(
                    barmode='group',
                    title='Comparison of SmolVLM2 vs PaLI-Gemma2 Models',
                    xaxis_title='Model',
                    yaxis_title='Metric Value',
                    legend_title='Metric'
                )
            )
        ])
    
    elif tab == "conclusion":
        return html.Div([
            html.H4("🔚 Project Conclusion & Future Outlook"),
            html.P("✅ End-to-end system from image input to AI-driven description."),
            html.P("⚙️ Gaussian Splatting 3D + volume estimation under active development."),
            html.P("🚀 Next steps: Optimize for mobile, real-time inference, better UX.")
        ])

# Helper function to load image, description and 3D model
def load_processed_results(image_name):
    img_path = os.path.join(PROCESSED_IMAGES_DIR, f"{image_name}_background_removed.jpg")
    json_path = os.path.join(PROCESSED_IMAGES_DIR, f"{image_name}_object_description.json")

    if not os.path.exists(img_path) or not os.path.exists(json_path):
        return html.P("⚠️ Selected image data not found.")

    with open(json_path, "r") as f:
        desc_data = json.load(f)

    return html.Div([
        html.Img(src=f"data:image/jpeg;base64,{encode_image(img_path)}", style={"maxWidth": "50%", "marginBottom": "20px"}),
        html.P(f"📄 Description (SmolVLM2): {desc_data.get('smolvlm2', 'N/A')}"),
        html.P(f"📄 Description (PaLI-Gemma2): {desc_data.get('pali_gemma2', 'N/A')}"),
        html.Hr(),
        html.Iframe(
            src=f"http://localhost:8000/viewer?image={image_name}",
            style={"width": "100%", "height": "500px", "border": "1px solid #ccc", "borderRadius": "10px"}
        )
    ])

# Callback to load image + 3D model dynamically
@app.callback(
    Output("image-display-section", "children"),
    Input("image-selector", "value")
)
def update_image_preview(selected_image):
    if not selected_image:
        return html.P("ℹ️ Please select an image to preview.")
    return load_processed_results(selected_image)
    
@app.callback(
    Output("model-display-section", "children"),
    Input("model-selector", "value")
)
def display_model(selected_model):
    if selected_model == "chair":
        return html.Iframe(src="/assets/viewer_chair.html", width="100%", height="600")
    elif selected_model == "laptop":
        return html.Iframe(src="/assets/viewer_laptop.html", width="100%", height="600")
    return html.Div("Please select an object to preview.")

# Run the Dash app
if __name__ == '__main__':
    app.run(debug=True)
