import plotly.graph_objects as go

fig = go.Figure(data=go.Bar(y=[2, 1, 3]))
fig.write_image("test.png")
print("Image export succeeded")
