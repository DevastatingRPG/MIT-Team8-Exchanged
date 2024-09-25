from dash import Dash
from layout import create_layout
from callbacks import register_callbacks

app = Dash()

app.layout = create_layout()

register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True)