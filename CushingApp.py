# -*- coding: utf-8 -*-
"""
Created on Wed Dec 27 13:34:00 2023

@author: bukhtiar.zafar
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load CSV file into a DataFrame
csv_file_path = r'C:\Users\bukhtiar.zafar\Downloads\Cushing.csv'
df = pd.read_csv(csv_file_path)

# Create a Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Cushing'),

    # Dash DataTable component
    dash_table.DataTable(
        id='editable-table',
        columns=[{'name': col, 'id': col, 'editable': True} for col in df.columns],
        data=df.to_dict('records'),
        editable=True,  # Make the table editable
        row_selectable='single',
        selected_rows=[],
    ),

    # Graph component for displaying the line chart
    dcc.Graph(id='line-chart')
])

# Callback function to update the line chart based on selected row and edited table values
@app.callback(
    Output('line-chart', 'figure'),
    [Input('editable-table', 'selected_rows'),
     Input('editable-table', 'data_previous'),
     Input('editable-table', 'data')]
)
def update_line_chart(selected_rows, previous_data, current_data):
    if not selected_rows:
        # No row selected, return an empty figure
        return {}

    selected_row_index = selected_rows[0]

    if previous_data is None or current_data is None:
        # Return line chart for the initially selected row
        selected_row_data = df.iloc[selected_row_index]
    else:
        # Return line chart for the currently selected row after editing
        selected_row_data = pd.DataFrame(current_data).iloc[selected_row_index]

    # Create a line chart using the selected row data
    first_column_value = selected_row_data.iloc[0]
    fig = px.line(x=selected_row_data.index, y=selected_row_data.values,
                  labels={'x': 'Column', 'y': 'Value'},
                  title=f'Line Chart for {first_column_value}')

    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)



