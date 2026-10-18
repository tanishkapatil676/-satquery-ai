import streamlit as st
import requests
import json

st.set_page_config(
    page_title="SatQuery AI Dashboard",
    page_icon="🛰️",
    layout="wide"
)

st.title("🛰️ SatQuery AI: Geospatial Intelligence Platform")
st.markdown("Translate natural language queries into multispectral satellite dataset processing and analytics.")

# Sidebar Configuration
st.sidebar.header("Configuration")
backend_url = st.sidebar.text_input("FastAPI Backend URL", value="http://localhost:8000")

# Main Navigation Tabs
tab1, tab2, tab3 = st.tabs(["💬 Natural Language Query", "🔍 Raster Inspector", "📊 System Health"])

with tab1:
    st.header("Natural Language Spatial Query")
    query_text = st.text_area(
        "Enter your spatial query:",
        placeholder="e.g., Analyze NDVI over agricultural zone and detect vegetation health anomalies."
    )
    raster_path_input = st.text_input("Target Raster File Path", value="data/raw/sample_band.tif")
    
    if st.button("Run Spatial Query", type="primary"):
        if not query_text:
            st.warning("Please enter a query.")
        else:
            payload = {
                "query": query_text,
                "raster_path": raster_path_input
            }
            try:
                response = requests.post(f"{backend_url}/api/v1/query", json=payload)
                if response.status_code == 200:
                    st.success("Query successfully processed!")
                    st.json(response.json())
                else:
                    st.error(f"Error {response.status_code}: {response.text}")
            except requests.exceptions.ConnectionError:
                st.error(f"Could not connect to FastAPI backend at {backend_url}. Ensure the server is running!")

with tab2:
    st.header("Raster Metadata Inspector")
    inspect_path = st.text_input("GeoTIFF Path to Inspect", value="data/raw/sample_band.tif")
    
    if st.button("Inspect Raster"):
        payload = {"file_path": inspect_path}
        try:
            response = requests.post(f"{backend_url}/api/v1/raster/inspect", json=payload)
            if response.status_code == 200:
                st.success("Raster metadata retrieved successfully!")
                st.json(response.json())
            else:
                st.error(f"Error {response.status_code}: {response.text}")
        except requests.exceptions.ConnectionError:
            st.error(f"Could not connect to FastAPI backend at {backend_url}.")

with tab3:
    st.header("System Health & Status")
    if st.button("Check Backend Health"):
        try:
            response = requests.get(f"{backend_url}/health")
            if response.status_code == 200:
                st.success("Backend is fully operational!")
                st.json(response.json())
            else:
                st.error(f"Health check failed with status {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("Backend is unreachable.")
