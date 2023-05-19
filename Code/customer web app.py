import streamlit as st
import pandas as pd
import os
import plotly.express as pe
import altair as alt
import plotly.graph_objects as go
import seaborn as sns



st.set_page_config(page_title='Customer Shopping Data', layout='wide')
st.title('Customer Shopping Visualization')
st.subheader('Data')
st.write("<hr>", unsafe_allow_html=True)
csv_file_path = os.path.join(os.getcwd(), 'customer_shopping_data.csv')

# read csv file with desired columns
df = pd.read_csv(csv_file_path, usecols=['gender','age','category','quantity','price','payment_method','invoice_date','shopping_mall'])
st.dataframe(df)






# ---- Age Distribution (Histogram) ----
#st.subheader('Age Distribution')
st.write("<hr>", unsafe_allow_html=True)
hist = alt.Chart(df, width=400, height=350).mark_bar().encode(x=alt.X('age',
                                               bin = alt.BinParams(maxbins = 20)),
                                       y = 'count()').properties(title=alt.TitleParams(text='Age Distribution', fontSize=20))
st.altair_chart(hist, use_container_width=True)




# ---- Category Distribution (Plotly Pie) ----
pie_chart = pe.pie(df,
                   title='Percentage of Category',
                   values='quantity', names='category', color='category', color_discrete_map={'Clothing':'cyan',
                                                                            'Cosmetics':'blue',
                                                                            'Food & Beverage':'royalblue',
                                                                            'Toys':'darkblue',
                                                                            'Shoes':'gold',
                                                                            'Technology':'darkorange',
                                                                            'Books':'lightgreen',
                                                                            'Souvenir':'mediumturquoise'})
pie_chart.update_layout(title={'font':{'size':20}}, font={'size':15}, autosize=False, width=600, height=550)
st.plotly_chart(pie_chart)




# ---- Price Distribution (altair Bar) ----
hist = alt.Chart(df, width=800, height=400).mark_bar().encode(x=alt.X('price', bin=alt.BinParams(maxbins=15)), 
                                                              y='count()').properties(title=alt.TitleParams(text='Price Distribution', fontSize=20))
st.altair_chart(hist)




# ---- Payment Method (Plotly pie) ----
pie_chart2 = pe.pie(df, values='quantity', names='payment_method', color='payment_method',
             color_discrete_map={'Cash':'#ffb865','Credit Card':'#dba39a','Debit Card':'#e3b6aa'},
             title='Payment Method Distribution')

pie_chart2.update_layout(title={'font':{'size':20}}, font={'size':15}, autosize=False, width=700, height=450)
st.plotly_chart(pie_chart2)







#left, right = st.columns(2)
#left.plotly_chart(pie_chart)
#right.plotly_chart(pie_chart2)













# ---- Heatmap (Plotly Heatmap) ----
pivot = pd.pivot_table(df, values='quantity', index='shopping_mall', columns='category',aggfunc='sum')
heatmap = go.Figure(go.Heatmap(
    z=pivot.values.tolist(),
    x=pivot.columns.tolist(),
    y=pivot.index.tolist(),
    colorscale='Viridis'))

heatmap.update_layout(xaxis_title='Category',
                      yaxis_title='Shopping Mall',
                      title={'text':'Quantity by Shopping Mall and Category',
                      'font':{'size':20}})

st.plotly_chart(heatmap)





''''''
# ---- Heatmap (altair) ----
heatmap_cols = ['gender', 'age', 'category', 'quantity', 'price', 'payment_method', 'shopping_mall']
heatmap = alt.Chart(df[heatmap_cols]).mark_rect().encode(x=alt.X('gender:N'),
                                                           y=alt.Y('category:N'),
                                                           color=alt.Color('mean(price):Q', title='Mean Price'),
                                                           tooltip=[alt.Tooltip('gender'),alt.Tooltip('category'),
                                                                    alt.Tooltip('mean(price)', title='Mean Price')]).properties(
                                                                        width=600,height=400,title=alt.TitleParams(text='Mean Price by Gender and Category',
                                                                                                                   fontSize=20))

st.altair_chart(heatmap)
''''''



# ----- Freequency table of each gender of every mall -----
contigency_table = pd.crosstab(df['gender'], df['shopping_mall'])
st.write(contigency_table.style.background_gradient(cmap=sns.light_palette('#7FFFD4', as_cmap=True)))







# ---- Grouped Bar Chart (Plotly) ----
grouped = df.groupby(['gender', 'shopping_mall']).size().reset_index(name='count')

# Create a pivot table with gender as rows and shopping_mall as columns
pivoted = pd.pivot_table(grouped, values='count', index='shopping_mall', columns='gender')

# Create the Plotly figure
fig = pe.bar(pivoted, x=pivoted.index, y=['Female', 'Male'], barmode='group', width=800)

# Set the chart title and axis labels
fig.update_layout(title="Number of visitors to each shopping mall by gender",
                  xaxis_title="Shopping Mall",
                  yaxis_title="Count")

# Show the chart
st.plotly_chart(fig, use_container_width=True)






