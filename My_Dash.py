#!/usr/bin/env python
# coding: utf-8

# In[5]:


import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Load the datasets
alberta_df = pd.read_csv(r"C:\Users\Dell\Desktop\Final project\Alberta_cleaned.csv")
manitoba_df = pd.read_csv(r"C:\Users\Dell\Desktop\Final project\Manitoba_cleaned.csv")
ontario_df = pd.read_csv(r"C:\Users\Dell\Desktop\Final project\Ontario_cleaned.csv")
quebec_df = pd.read_csv(r"C:\Users\Dell\Desktop\Final project\Quebec_cleaned.csv")
vancouver_df = pd.read_csv(r"C:\Users\Dell\Desktop\Final project\Vancouver_cleaned.csv")                         

# Combine datasets into one DataFrame with an additional 'city' column
alberta_df['city'] = 'Alberta'
manitoba_df['city'] = 'Manitoba'
ontario_df['city'] = 'Ontario'
quebec_df['city'] = 'Quebec'
vancouver_df['city'] = 'Vancouver'
df = pd.concat([alberta_df, manitoba_df, ontario_df, quebec_df, vancouver_df])

# Create a dictionary to hold city coordinates for the map
city_coords = {
    'Alberta': (53.9333, -116.5765),
    'Manitoba': (49.8951, -97.1384),
    'Ontario': (51.2538, -85.3232),
    'Quebec': (52.9399, -73.5491),
    'Vancouver': (49.2827, -123.1207)
}

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Restaurant Data Analysis"),
    
    # Dropdown for selecting city
    dcc.Dropdown(
        id='city-dropdown',
        options=[
            {'label': 'All Cities', 'value': 'All'},
            {'label': 'Alberta', 'value': 'Alberta'},
            {'label': 'Manitoba', 'value': 'Manitoba'},
            {'label': 'Ontario', 'value': 'Ontario'},
            {'label': 'Quebec', 'value': 'Quebec'},
            {'label': 'Vancouver', 'value': 'Vancouver'}
        ],
        value='All',
        clearable=False
    ),
    
    # Filter sliders and dropdowns
    dcc.Slider(id='rating-slider', min=0, max=5, step=0.1, value=0, marks={i: str(i) for i in range(6)}, tooltip={"placement": "bottom", "always_visible": True}),
    dcc.Slider(id='reviews-slider', min=0, max=500, step=10, value=0, marks={i: str(i) for i in range(0, 501, 50)}, tooltip={"placement": "bottom", "always_visible": True}),
    
    # Placeholder for graphs (initially empty)
    html.Div(id='graphs-container')
])

# Define the callback to update the graphs and map
@app.callback(
    Output('graphs-container', 'children'),
    [Input('city-dropdown', 'value'),
     Input('rating-slider', 'value'),
     Input('reviews-slider', 'value')]
)
def update_graphs(selected_city, min_rating, min_reviews):
    # Filter data based on selected city
    filtered_df = df[df['city'] == selected_city] if selected_city != 'All' else df
    
    # Apply additional filters
    filtered_df = filtered_df[(filtered_df['rating'] >= min_rating) & (filtered_df['number_of_reviews'] >= min_reviews)]
    
    # Get top 10 results based on rating
    top_10_df = filtered_df.nlargest(10, 'rating')
    
    # Create the figures as before
    fig_rating = px.histogram(filtered_df, x='rating', nbins=10, title='Rating Distribution')
    fig_service = px.histogram(filtered_df, x='service', nbins=10, title='Service Distribution')
    fig_food = px.histogram(filtered_df, x='food', nbins=10, title='Food Distribution')
    fig_ambience = px.histogram(filtered_df, x='ambience', nbins=10, title='Ambience Distribution')
    fig_value = px.histogram(filtered_df, x='value', nbins=10, title='Value Distribution')
    
    # Cuisine type distribution
    cuisine_counts = filtered_df['food_type'].value_counts().reset_index()
    cuisine_counts.columns = ['Cuisine', 'Count']
    fig_cuisine = px.bar(cuisine_counts, x='Cuisine', y='Count', title='Cuisine Types')

    # Map for selected city
    lat, lon = city_coords.get(selected_city, (None, None))
    map_fig = go.Figure()
    if lat and lon:
        map_fig.add_trace(go.Scattergeo(lat=[lat], lon=[lon], text=selected_city, marker=dict(size=12, color='red')))
    map_fig.update_layout(title='Location of Selected City', geo=dict(scope='north america', showland=True))

    # Output the graphs and the map
    return [
        dcc.Graph(figure=map_fig),
        dcc.Graph(figure=fig_rating),
        dcc.Graph(figure=fig_service),
        dcc.Graph(figure=fig_food),
        dcc.Graph(figure=fig_ambience),
        dcc.Graph(figure=fig_value),
        dcc.Graph(figure=fig_cuisine),
        html.H3("Top 10 Restaurants by Rating"),
        dcc.Graph(figure=px.bar(top_10_df, x='rest_name', y='rating', title="Top 10 Restaurants by Rating"))
    ]

if __name__ == '__main__':
    app.run_server(debug=True, port=8061)


# In[6]:


import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# Load the datasets
alberta_df = pd.read_csv(r"C:\Users\Dell\Desktop\Final project\Alberta_cleaned.csv")
manitoba_df = pd.read_csv(r"C:\Users\Dell\Desktop\Final project\Manitoba_cleaned.csv")
ontario_df = pd.read_csv(r"C:\Users\Dell\Desktop\Final project\Ontario_cleaned.csv")
quebec_df = pd.read_csv(r"C:\Users\Dell\Desktop\Final project\Quebec_cleaned.csv")
vancouver_df = pd.read_csv(r"C:\Users\Dell\Desktop\Final project\Vancouver_cleaned.csv")                         

# Combine datasets into one DataFrame with an additional 'city' column
alberta_df['city'] = 'Alberta'
manitoba_df['city'] = 'Manitoba'
ontario_df['city'] = 'Ontario'
quebec_df['city'] = 'Quebec'
vancouver_df['city'] = 'Vancouver'
df = pd.concat([alberta_df, manitoba_df, ontario_df, quebec_df, vancouver_df])

# Create a dictionary to hold city coordinates for the map
city_coords = {
    'Alberta': (53.9333, -116.5765),
    'Manitoba': (49.8951, -97.1384),
    'Ontario': (51.2538, -85.3232),
    'Quebec': (52.9399, -73.5491),
    'Vancouver': (49.2827, -123.1207)
}

# Initialize the Dash app
app = Dash(__name__)

# Define the layout of the app
app.layout = html.Div([
    html.H1("Restaurant Data Analysis"),
    
    # Dropdown for selecting city
    dcc.Dropdown(
        id='city-dropdown',
        options=[
            {'label': 'All Cities', 'value': 'All'},
            {'label': 'Alberta', 'value': 'Alberta'},
            {'label': 'Manitoba', 'value': 'Manitoba'},
            {'label': 'Ontario', 'value': 'Ontario'},
            {'label': 'Quebec', 'value': 'Quebec'},
            {'label': 'Vancouver', 'value': 'Vancouver'}
        ],
        value='All',
        clearable=False
    ),
    
    # Filter sliders
    dcc.Slider(id='rating-slider', min=0, max=5, step=0.1, value=0, marks={i: str(i) for i in range(6)}, tooltip={"placement": "bottom", "always_visible": True}),
    dcc.Slider(id='reviews-slider', min=0, max=500, step=10, value=0, marks={i: str(i) for i in range(0, 501, 50)}, tooltip={"placement": "bottom", "always_visible": True}),
    
    # Dropdown for selecting a restaurant from the top 10
    html.Label("Select a Restaurant"),
    dcc.Dropdown(id='restaurant-dropdown', clearable=False),
    
    # Placeholder for graphs (initially empty)
    html.Div(id='graphs-container'),
    
    # Placeholder for selected restaurant details
    html.Div(id='restaurant-details-container')
])

# Define the callback to update the graphs and top 10 restaurant dropdown
@app.callback(
    [Output('graphs-container', 'children'),
     Output('restaurant-dropdown', 'options')],
    [Input('city-dropdown', 'value'),
     Input('rating-slider', 'value'),
     Input('reviews-slider', 'value')]
)
def update_graphs(selected_city, min_rating, min_reviews):
    # Filter data based on selected city
    filtered_df = df[df['city'] == selected_city] if selected_city != 'All' else df
    
    # Apply additional filters
    filtered_df = filtered_df[(filtered_df['rating'] >= min_rating) & (filtered_df['number_of_reviews'] >= min_reviews)]
    
    # Get top 10 results based on rating
    top_10_df = filtered_df.nlargest(10, 'rating')
    
    # Create the figures as before
    fig_rating = px.histogram(filtered_df, x='rating', nbins=10, title='Rating Distribution')
    fig_service = px.histogram(filtered_df, x='service', nbins=10, title='Service Distribution')
    fig_food = px.histogram(filtered_df, x='food', nbins=10, title='Food Distribution')
    fig_ambience = px.histogram(filtered_df, x='ambience', nbins=10, title='Ambience Distribution')
    fig_value = px.histogram(filtered_df, x='value', nbins=10, title='Value Distribution')
    
    # Cuisine type distribution
    cuisine_counts = filtered_df['food_type'].value_counts().reset_index()
    cuisine_counts.columns = ['Cuisine', 'Count']
    fig_cuisine = px.bar(cuisine_counts, x='Cuisine', y='Count', title='Cuisine Types')

    # Map for selected city
    lat, lon = city_coords.get(selected_city, (None, None))
    map_fig = go.Figure()
    if lat and lon:
        map_fig.add_trace(go.Scattergeo(lat=[lat], lon=[lon], text=selected_city, marker=dict(size=12, color='red')))
    map_fig.update_layout(title='Location of Selected City', geo=dict(scope='north america', showland=True))

    # Output the graphs and the top 10 restaurant options
    restaurant_options = [{'label': name, 'value': name} for name in top_10_df['rest_name']]
    
    return [
        [
            dcc.Graph(figure=map_fig),
            dcc.Graph(figure=fig_rating),
            dcc.Graph(figure=fig_service),
            dcc.Graph(figure=fig_food),
            dcc.Graph(figure=fig_ambience),
            dcc.Graph(figure=fig_value),
            dcc.Graph(figure=fig_cuisine),
            html.H3("Top 10 Restaurants by Rating"),
            dcc.Graph(figure=px.bar(top_10_df, x='rest_name', y='rating', title="Top 10 Restaurants by Rating"))
        ],
        restaurant_options
    ]

# Define the callback to show details of the selected restaurant
@app.callback(
    Output('restaurant-details-container', 'children'),
    [Input('restaurant-dropdown', 'value'),
     Input('city-dropdown', 'value')]
)
def display_restaurant_details(selected_restaurant, selected_city):
    if not selected_restaurant:
        return []
    
    # Filter data to get the specific restaurant's details
    restaurant_data = df[(df['city'] == selected_city) & (df['rest_name'] == selected_restaurant)].iloc[0]
    
    # Extract specific fields
    image_url = restaurant_data['image_url']
    about_rest = restaurant_data['about_rest']
    ambience = restaurant_data['ambience']
    food = restaurant_data['food']
    service = restaurant_data['service']
    value = restaurant_data['value']
    
    # Display the restaurant's image, about section, and ratings
    return [
        html.Img(src=image_url, style={'width': '100%', 'height': 'auto'}),
        html.H3("About the Restaurant"),
        html.P(about_rest),
        html.H3("Ratings"),
        html.P(f"Ambience: {ambience}/5"),
        html.P(f"Food: {food}/5"),
        html.P(f"Service: {service}/5"),
        html.P(f"Value: {value}/5")
    ]

if __name__ == '__main__':
    app.run_server(debug=True, port=8061)


# In[ ]:




